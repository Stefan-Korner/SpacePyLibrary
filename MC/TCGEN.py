#******************************************************************************
# (C) 2018, Stefan Korner, Austria                                            *
#                                                                             *
# The Space Python Library is free software; you can redistribute it and/or   *
# modify it under under the terms of the MIT License as published by the      *
# Massachusetts Institute of Technology.                                      *
#                                                                             *
# The Space Python Library is distributed in the hope that it will be useful, *
# but WITHOUT ANY WARRANTY; without even the implied warranty of              *
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the MIT License    *
# for more details.                                                           *
#******************************************************************************
# Monitoring and Control (M&C) - Telecommand Packet Generator                 *
#******************************************************************************
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import CCSDS.DU, CCSDS.PACKET, CCSDS.TIME
import MC.IF
import PUS.PACKET, PUS.SERVICES, PUS.VP
import SUPP.IF
import UTIL.SYS, UTIL.TCO, UTIL.TIME

###########
# classes #
###########
# =============================================================================
class TCpacketDefaults(object):
  """Default values for TC packet creation"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """default constructor"""
    # PUS packets already have these defaults
    self.ccsdsPacketVersionNumber = 0
    self.ccsdsPacketSegmentationFlags = CCSDS.PACKET.UNSEGMENTED

# =============================================================================
class TCpacketGeneratorImpl(MC.IF.TCpacketGenerator):
  """Implementation of the generator for telecommand packets"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """default constructor"""
    self.packetCache = {}
    self.sequenceCounters = {}
    self.packetDefaults = TCpacketDefaults()
  # ---------------------------------------------------------------------------
  def getTCpacket(self,
                  pktName,
                  tcStruct,
                  reuse=True):
    """
    creates a CCSDS TC packet with optional parameter values:
    implementation of MC.IF.TCpacketGenerator.getTCpacket
    """
    # fetch the packet definition
    tcPktDef = SUPP.IF.s_definitions.getTCpktDefByName(pktName)
    if tcPktDef == None:
      raise Error("invalid packet name for packet creation: " + pktName)
    binarySize = tcPktDef.pktSPsize
    applicationProcessId = tcPktDef.pktAPID
    if reuse and pktName in self.packetCache:
      # reuse a packet with the same definition from the cache
      packet = self.packetCache[pktName]
      packet.setLen(binarySize)
      packet.setPacketLength()
    else:
      # create the TC packet
      if tcPktDef.pktHasDFhdr:
        # PUS packet
        serviceType = tcPktDef.pktType
        serviceSubType = tcPktDef.pktSType
        packet = self.getTCpacketHelper(binarySize,
                                        applicationProcessId,
                                        serviceType,
                                        serviceSubType)
      else:
        # CCSDS packet
        packet = self.getTCpacketHelper(binarySize,
                                        applicationProcessId)
      self.packetCache[pktName] = packet
    # apply the segmentationFlags
    packet.segmentationFlags = CCSDS.PACKET.UNSEGMENTED
    ### apply the encoded tcStruct ###
    if not tcStruct:
      # create an empty tcStruct with the correct structure
      tcStructDef = tcPktDef.tcStructDef
      if tcStructDef == None:
        raise Error("invalid packet structure for packet creation: " + pktName)
      tcStruct = PUS.VP.Struct(tcStructDef)
    #-- find the correct position for the data
    structBytePos = CCSDS.PACKET.PRIMARY_HEADER_BYTE_SIZE
    if tcPktDef.pktHasDFhdr:
      # PUS packet
      structBytePos += tcPktDef.pktDFHsize
    structBitPos = structBytePos << 3
    structEndBitPos = structBitPos + tcStruct.getBitWidth()
    structEndBytePos = (structEndBitPos + 7) >> 3
    #-- re-size the packet to exactly fit
    tcPacketSize = structEndBytePos
    if tcPktDef.pktCheck:
      tcPacketSize += CCSDS.DU.CRC_BYTE_SIZE
    packet.setLen(tcPacketSize)
    packet.setPacketLength()
    #-- encode the struct
    tcStruct.encode(packet, structBitPos)
    # re-calculate the sequence counter (maintained per APID)
    if applicationProcessId in self.sequenceCounters:
      sequenceCounter = (self.sequenceCounters[applicationProcessId] + 1) % 16384
    else:
      sequenceCounter = 0
    packet.sequenceControlCount = sequenceCounter
    self.sequenceCounters[applicationProcessId] = sequenceCounter
    # re-calculate the CRC
    if tcPktDef.pktCheck:
      packet.setChecksum()
    return packet
  # ---------------------------------------------------------------------------
  def getTCpacketHelper(self,
                        binarySize,
                        applicationProcessId,
                        serviceType=None,
                        serviceSubType=None):
    """helper for creating TC packets"""
    if serviceType == None or serviceSubType == None:
      # CCSDS packet
      minimumSize = CCSDS.PACKET.PRIMARY_HEADER_BYTE_SIZE
      if binarySize < minimumSize:
        raise ValueError("binary size too small, must be >= " + str(minimumSize))
      binaryString = "\0" * binarySize
      packet = CCSDS.PACKET.TCpacket(binaryString)
      packet.packetType = CCSDS.PACKET.TC_PACKET_TYPE
      packet.setPacketLength()
      packet.versionNumber = self.packetDefaults.ccsdsPacketVersionNumber
      packet.dataFieldHeaderFlag = 0
      packet.segmentationFlags = self.packetDefaults.ccsdsPacketSegmentationFlags
    else:
      # PUS packet
      minimumSize = CCSDS.PACKET.PRIMARY_HEADER_BYTE_SIZE + \
                    PUS.PACKET.TC_PACKET_DATAFIELD_HEADER_BYTE_SIZE
      if binarySize < minimumSize:
        raise ValueError("binary size too small, must be >= " + str(minimumSize))
      binaryString = "\0" * binarySize
      packet = PUS.PACKET.TCpacket(binaryString)
      packet.packetType = CCSDS.PACKET.TC_PACKET_TYPE
      packet.setPacketLength()
      packet.dataFieldHeaderFlag = 1
      packet.pusVersionNumber = PUS.PACKET.PUS_VERSION_NUMBER
      packet.serviceType = serviceType
      packet.serviceSubType = serviceSubType
    packet.applicationProcessId = applicationProcessId
    return packet

#############
# functions #
#############
def init():
  """initialise singleton(s)"""
  MC.IF.s_tcPacketGenerator = TCpacketGeneratorImpl()
