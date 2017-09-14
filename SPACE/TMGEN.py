#******************************************************************************
# (C) 2014, Stefan Korner, Austria                                            *
#                                                                             *
# The Space Python Library is free software; you can redistribute it and/or   *
# modify it under the terms of the GNU Lesser General Public License as       *
# published by the Free Software Foundation; either version 2.1 of the        *
# License, or (at your option) any later version.                             *
#                                                                             *
# The Space Python Library is distributed in the hope that it will be useful, *
# but WITHOUT ANY WARRANTY; without even the implied warranty of              *
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser     *
# General Public License for more details.                                    *
#******************************************************************************
# Space Simulation - Telemetry Packet Generator                               *
#******************************************************************************
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import CCSDS.PACKET, CCSDS.TIME
import PUS.PACKET
import SCOS.ENV
import SPACE.IF
import UTIL.SYS, UTIL.TCO, UTIL.TIME

###########
# classes #
###########
# =============================================================================
class TMpacketDefaults(object):
  """Default values for TM packet creation"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """default constructor"""
    self.versionNumber = 0
    self.segmentationFlags = CCSDS.PACKET.UNSEGMENTED
    self.pusVersionNumber = 1
    self.idlePacketAPID = SCOS.ENV.TPKT_PKT_IDLE_APID

# =============================================================================
class TMpacketGeneratorImpl(SPACE.IF.TMpacketGenerator):
  """Implementation of the generator for telemetry packets"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """default constructor"""
    self.packetCache = {}
    self.sequenceCounters = {}
    self.packetDefaults = TMpacketDefaults()
    self.tcAckAPIDparamByteOffset = int(UTIL.SYS.s_configuration.TC_ACK_APID_PARAM_BYTE_OFFSET)
    self.tcAckSSCparamByteOffset = int(UTIL.SYS.s_configuration.TC_ACK_SSC_PARAM_BYTE_OFFSET)
    self.tmTTtimeFormat = CCSDS.TIME.timeFormat(UTIL.SYS.s_configuration.TM_TT_TIME_FORMAT)
    self.tmTTtimeByteOffset = int(UTIL.SYS.s_configuration.TM_TT_TIME_BYTE_OFFSET)
  # ---------------------------------------------------------------------------
  def getIdlePacket(self, packetSize):
    """
    creates an idle packet for filling space in a parent container
    (e.g. a CCSDS TM frame):
    implementation of SPACE.IF.TMpacketGenerator.getIdlePacket
    """
    # the idle packet is a TM packet without a secondary header (CCSDS)
    # but with a CRC (if an application expects a CRC)
    if packetSize < (CCSDS.PACKET.PRIMARY_HEADER_BYTE_SIZE + CCSDS.PACKET.CRC_BYTE_SIZE):
      raise Error("no sufficient space for idle packet")
    applicationProcessId = self.packetDefaults.idlePacketAPID
    idlePacket = self.getTMpacketHelper(packetSize, applicationProcessId)
    # re-calculate the sequence counter (maintained per APID)
    if applicationProcessId in self.sequenceCounters:
      sequenceCounter = (self.sequenceCounters[applicationProcessId] + 1) % 16384
    else:
      sequenceCounter = 0
    idlePacket.sequenceControlCount = sequenceCounter
    self.sequenceCounters[applicationProcessId] = sequenceCounter
    # re-calculate the CRC
    idlePacket.setChecksum()
    return idlePacket
  # ---------------------------------------------------------------------------
  def getTMpacket(self,
                  spid,
                  parameterValues=[],
                  dataField=None,
                  segmentationFlags=CCSDS.PACKET.UNSEGMENTED,
                  obtUTC=None,
                  reuse=True):
    """
    creates a CCSDS TM packet with optional parameter values:
    implementation of SPACE.IF.TMpacketGenerator.getTMpacket
    """
    # fetch the packet definition
    tmPktDef = SPACE.IF.s_definitions.getTMpktDefBySPID(spid)
    if tmPktDef == None:
      raise Error("invalid SPID for packet creation: " + str(spid))
    binarySize = tmPktDef.pktSPsize
    applicationProcessId = tmPktDef.pktAPID
    if reuse and spid in self.packetCache:
      # reuse a packet with the same definition from the cache
      packet = self.packetCache[spid]
      packet.setLen(binarySize)
      packet.setPacketLength()
    else:
      # create the TM packet
      if tmPktDef.pktHasDFhdr:
        # PUS packet
        serviceType = tmPktDef.pktType
        serviceSubType = tmPktDef.pktSType
        packet = self.getTMpacketHelper(binarySize,
                                        applicationProcessId,
                                        serviceType,
                                        serviceSubType)
        # initialise PI1 and PI2 if configured
        if tmPktDef.pktPI1val != None:
          pi1BitPos = tmPktDef.pktPI1off * 8
          pi1BitWidth = tmPktDef.pktPI1wid
          pi1Value = tmPktDef.pktPI1val
          packet.setBits(pi1BitPos, pi1BitWidth, pi1Value)
        if tmPktDef.pktPI2val != None:
          pi2BitPos = tmPktDef.pktPI2off * 8
          pi2BitWidth = tmPktDef.pktPI2wid
          pi2Value = tmPktDef.pktPI2val
          packet.setBits(pi2BitPos, pi2BitWidth, pi2Value)
      else:
        # CCSDS packet
        packet = self.getTMpacketHelper(binarySize,
                                        applicationProcessId)
      self.packetCache[spid] = packet
    # apply the segmentationFlags
    packet.segmentationFlags = segmentationFlags
    # apply the datafield
    if dataField:
      dataFieldOffset, dataFieldData = dataField
      minExpectedPacketSize = dataFieldOffset + len(dataFieldData)
      if tmPktDef.pktCheck:
        minExpectedPacketSize += 2
      # re-size the packet if needed
      if len(packet) < minExpectedPacketSize:
        packet.setLen(minExpectedPacketSize)
        packet.setPacketLength()
      packet.setBytes(dataFieldOffset, len(dataFieldData), dataFieldData)
    # apply the parameters
    for paramNameValue in parameterValues:
      paramName, paramValue = paramNameValue
      # special handling for PUS service 1 parameters for TC acknowledgement
      if paramName == "PUS_TYPE1_APID":
        bytePos = self.tcAckAPIDparamByteOffset
        byteLength = 2
        value = int(paramValue) | 0x1800
        packet.setUnsigned(bytePos, byteLength, value)
        continue
      if paramName == "PUS_TYPE1_SSC":
        bytePos = self.tcAckSSCparamByteOffset
        byteLength = 2
        value = int(paramValue) | 0xC000
        packet.setUnsigned(bytePos, byteLength, value)
        continue
      # search the definition of the parameter (TMparamExtraction)
      paramExtraction = tmPktDef.getParamExtraction(paramName)
      if paramExtraction == None:
        LOG_WARNING("packet with SPID " + str(spid) + " does not have a parameter " + paramName, "SPACE")
      else:
        # apply the parameter value
        bitPos = paramExtraction.bitPos
        bitLength = paramExtraction.bitWidth
        isInteger = paramExtraction.isInteger
        if isInteger:
          packet.setBits(bitPos, bitLength, paramValue)
        else:
          bytePos = bitPos / 8
          byteLength = bitLength / 8
          packet.setString(bytePos, byteLength, paramValue)
    # re-calculate the time stamp
    if tmPktDef.pktHasDFhdr and self.tmTTtimeByteOffset > 0:
      if obtUTC == None:
        obtUTC = UTIL.TIME.getActualTime()
      obtTime = UTIL.TCO.correlateToOBTmissionEpoch(obtUTC)
      timeDU = CCSDS.TIME.convertToCCSDS(obtTime, self.tmTTtimeFormat)
      packet.setBytes(self.tmTTtimeByteOffset,
                      len(timeDU),
                      timeDU.getBufferString())
    # re-calculate the sequence counter (maintained per APID)
    if applicationProcessId in self.sequenceCounters:
      sequenceCounter = (self.sequenceCounters[applicationProcessId] + 1) % 16384
    else:
      sequenceCounter = 0
    packet.sequenceControlCount = sequenceCounter
    self.sequenceCounters[applicationProcessId] = sequenceCounter
    # re-calculate the CRC
    if tmPktDef.pktCheck:
      packet.setChecksum()
    return packet
  # ---------------------------------------------------------------------------
  def getTMpacketHelper(self,
                        binarySize,
                        applicationProcessId,
                        serviceType=None,
                        serviceSubType=None):
    """helper for creating TM packets"""
    if serviceType == None or serviceSubType == None:
      # CCSDS packet
      minimumSize = CCSDS.PACKET.PRIMARY_HEADER_BYTE_SIZE
      if binarySize < minimumSize:
        raise ValueError("binary size too small, must be >= " + str(minimumSize))
      binaryString = "\0" * binarySize
      packet = CCSDS.PACKET.TMpacket(binaryString)
      packet.setPacketLength()
      packet.packetType = CCSDS.PACKET.TM_PACKET_TYPE
      packet.dataFieldHeaderFlag = 0
    else:
      # PUS packet
      minimumSize = CCSDS.PACKET.PRIMARY_HEADER_BYTE_SIZE + \
                    PUS.PACKET.TM_PACKET_DATAFIELD_HEADER_BYTE_SIZE
      if binarySize < minimumSize:
        raise ValueError("binary size too small, must be >= " + str(minimumSize))
      binaryString = "\0" * binarySize
      packet = PUS.PACKET.TMpacket(binaryString)
      packet.setPacketLength()
      packet.packetType = CCSDS.PACKET.TM_PACKET_TYPE
      packet.dataFieldHeaderFlag = 1
      packet.pusVersionNumber = self.packetDefaults.pusVersionNumber
      packet.serviceType = serviceType
      packet.serviceSubType = serviceSubType
    packet.versionNumber = self.packetDefaults.versionNumber
    packet.segmentationFlags = self.packetDefaults.segmentationFlags
    packet.applicationProcessId = applicationProcessId
    return packet

#############
# functions #
#############
def init():
  # initialise singleton(s)
  SPACE.IF.s_tmPacketGenerator = TMpacketGeneratorImpl()
