#******************************************************************************
# (C) 2019, Stefan Korner, Austria                                            *
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
# CCSDS Stack - Assembler that assembles TM frames from TM packets            *
# Must be overloaded to handle the frame callback.                            *
# Restriction: Supports only one virtual channel                              *
#******************************************************************************
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import CCSDS.FRAME, CCSDS.PACKET
import UTIL.DU, UTIL.SYS

#############
# constants #
#############
# default value from the CCSDS standard
TRANSFER_FRAME_SECONDARY_HEADER_SIZE = 4

###########
# classes #
###########
# =============================================================================
class TMframeDefaults(object):
  """Default values for TM transfer frame creation"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """default constructor"""
    # primary header defaults
    self.transferFrameSize = int(UTIL.SYS.s_configuration.TM_TRANSFER_FRAME_SIZE)
    self.versionNumber = 0
    self.spacecraftId = int(UTIL.SYS.s_configuration.SPACECRAFT_ID)
    self.virtualChannelId = int(UTIL.SYS.s_configuration.TM_VIRTUAL_CHANNEL_ID)
    self.operationalControlField = 1
    if UTIL.SYS.s_configuration.TM_TRANSFER_FRAME_HAS_SEC_HDR == "1":
      # transfer frame has secondary header
      self.secondaryHeaderFlag = 1
      self.secondaryHeaderSize = \
        TRANSFER_FRAME_SECONDARY_HEADER_SIZE - 1
    else:
      # transfer frame has no secondary header
      self.secondaryHeaderFlag = 0
      self.secondaryHeaderSize = 0
    self.synchronisationFlag = 0
    self.packetOrderFlag = 0
    self.segmentLengthId = 3
    self.firstHeaderPointer = 0
    # secondary header defaults
    self.secondaryHeaderVersionNr = 0
    self.virtualChannelFCountHigh = 0

# =============================================================================
class CLCWdefaults(object):
  """Default values for CLCW"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """default constructor"""
    self.type = 0
    self.version = 0
    self.statusField = 0
    self.copInEffect = 1
    self.virtualChannelId = 0
    self.spareField = 0
    self.noRfAvailable = 0
    self.noBitLock = 0
    self.lockout = 0
    self.wait = 0
    self.retransmit = 0
    self.farmBcounter = 0
    self.reportType = 0
    self.reportValue = 0

# =============================================================================
class IdlePacketDefaults(object):
  """Default values for IDLE packet creation"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """default constructor"""
    # PUS packets already have these defaults
    self.ccsdsPacketVersionNumber = 0

# =============================================================================
class Assembler():
  """Converter from TM packets to TM frames"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """default constructor"""
    #self.pendingFrame = None
    self.pendingBinPacket = None
    self.idlePacketSequenceCounter = 0
    self.masterChannelFrameCount = 0
    self.virtualChannelFrameCount = 0
    self.frameDefaults = TMframeDefaults()
    self.idlePacketDefaults = IdlePacketDefaults()
    self.initCLCW()
  # ---------------------------------------------------------------------------
  def initCLCW(self):
    """initialise CLCW"""
    clcwDefaults = CLCWdefaults()
    self.clcw = CCSDS.FRAME.CLCW()
    self.clcw.type = clcwDefaults.type
    self.clcw.version = clcwDefaults.version
    self.clcw.statusField = clcwDefaults.statusField
    self.clcw.copInEffect = clcwDefaults.copInEffect
    self.clcw.virtualChannelId = clcwDefaults.virtualChannelId
    self.clcw.spareField = clcwDefaults.spareField
    self.clcw.noRfAvailable = clcwDefaults.noRfAvailable
    self.clcw.noBitLock = clcwDefaults.noBitLock
    self.clcw.lockout = clcwDefaults.lockout
    self.clcw.wait = clcwDefaults.wait
    self.clcw.retransmit = clcwDefaults.retransmit
    self.clcw.farmBcounter = clcwDefaults.farmBcounter
    self.clcw.reportType = clcwDefaults.reportType
    self.clcw.reportValue = clcwDefaults.reportValue
  # ---------------------------------------------------------------------------
  def getCLCW(self):
    """returns the CLCW for the next TM frame"""
    return self.clcw
  # ---------------------------------------------------------------------------
  def setCLCWcount(self, value):
    """sets the counter in the CLCW for the next TM frame"""
    self.clcw.reportValue = value
  # ---------------------------------------------------------------------------
  def reset(self):
    """resets pending frame"""
    self.pendingFrame = None
  # ---------------------------------------------------------------------------
  def isFramePending(self):
    """checks if there is a pending frame (waiting for next packet)"""
    return (self.pendingFrame != None)
  # ---------------------------------------------------------------------------
  def pushTMpacket(self, binPacket):
    """consumes a telemetry packet"""
    # TODO: replace the code with the correct spillover packet implementation
    self.pendingBinPacket = binPacket
  # ---------------------------------------------------------------------------
  def flushTMframe(self):
    """finalize a telemetry frame with an idle packet"""
    # TODO: replace the code with the correct spillover packet implementation
    if self.pendingBinPacket == None:
      return
    # create the idle packet
    reservedFrameDataSize = CCSDS.FRAME.TM_FRAME_PRIMARY_HEADER_BYTE_SIZE + \
                            len(self.pendingBinPacket) + \
                            CCSDS.FRAME.CLCW_BYTE_SIZE
    enableSecondaryHeader = (self.frameDefaults.secondaryHeaderFlag == 1)
    if enableSecondaryHeader:
      reservedFrameDataSize += CCSDS.FRAME.TM_FRAME_SECONDARY_HEADER_BYTE_SIZE
    if CCSDS.FRAME.CRC_CHECK:
      reservedFrameDataSize += 2
    remainingFrameDataSize = self.frameDefaults.transferFrameSize - \
                             reservedFrameDataSize
    if remainingFrameDataSize < 0:
      # TM packet does not fit into the frame
      # ---> an exception must be raised as long as
      #      TM packet segmentation is not implemeted
      raise Error("TM packet does not fit into transfer frame")
    # create the transfer frame
    tmFrame = CCSDS.FRAME.TMframe(enableSecondaryHeader=enableSecondaryHeader)
    tmFrame.versionNumber = self.frameDefaults.versionNumber
    tmFrame.spacecraftId = self.frameDefaults.spacecraftId
    tmFrame.virtualChannelId = self.frameDefaults.virtualChannelId
    tmFrame.operationalControlField = self.frameDefaults.operationalControlField
    tmFrame.masterChannelFrameCount = self.masterChannelFrameCount
    self.masterChannelFrameCount += 1
    self.masterChannelFrameCount %= 256
    tmFrame.virtualChannelFCountLow = self.virtualChannelFrameCount
    self.virtualChannelFrameCount += 1
    self.virtualChannelFrameCount %= 256
    tmFrame.secondaryHeaderFlag = self.frameDefaults.secondaryHeaderFlag
    tmFrame.synchronisationFlag = self.frameDefaults.synchronisationFlag
    tmFrame.packetOrderFlag = self.frameDefaults.packetOrderFlag
    tmFrame.segmentLengthId = self.frameDefaults.segmentLengthId
    tmFrame.firstHeaderPointer = self.frameDefaults.firstHeaderPointer
    if enableSecondaryHeader:
      tmFrame.secondaryHeaderVersionNr = self.frameDefaults.secondaryHeaderVersionNr
      tmFrame.secondaryHeaderSize = self.frameDefaults.secondaryHeaderSize
      tmFrame.virtualChannelFCountHigh = self.frameDefaults.virtualChannelFCountHigh
    tmFrame.append(self.pendingBinPacket)
    if remainingFrameDataSize != 0:
      # create idle packet
      tmIdlePacket = self.getIdlePacket(remainingFrameDataSize)
      tmFrame.append(tmIdlePacket.getBufferString())
    tmFrame.append(self.clcw.getBufferString())
    if CCSDS.FRAME.CRC_CHECK:
      tmFrame.append("\0" * CCSDS.DU.CRC_BYTE_SIZE)
      tmFrame.setChecksum()
    self.notifyTMframeCallback(tmFrame.getBuffer())
    self.tmFrame = None
  # ---------------------------------------------------------------------------
  def getIdlePacket(self, packetSize):
    """creates an idle packet for filling space in the frame"""
    # TODO: move this method into a separate class
    # note: there is a similar code in SPACE.TMGEN
    # the idle packet is a TM packet without a secondary header (CCSDS)
    # but with a CRC (if an application expects a CRC)
    if packetSize < (CCSDS.PACKET.PRIMARY_HEADER_BYTE_SIZE + CCSDS.DU.CRC_BYTE_SIZE):
      raise Error("no sufficient space for idle packet")
    minimumSize = CCSDS.PACKET.PRIMARY_HEADER_BYTE_SIZE
    if packetSize < minimumSize:
      raise ValueError("binary size too small, must be >= " + str(minimumSize))
    binaryString = "\0" * packetSize
    idlePacket = CCSDS.PACKET.TMpacket(binaryString)
    idlePacket.packetType = CCSDS.PACKET.TM_PACKET_TYPE
    idlePacket.setPacketLength()
    idlePacket.versionNumber = self.idlePacketDefaults.ccsdsPacketVersionNumber
    idlePacket.dataFieldHeaderFlag = 0
    idlePacket.segmentationFlags = CCSDS.PACKET.UNSEGMENTED
    idlePacket.applicationProcessId = CCSDS.PACKET.IDLE_PKT_APID
    # re-calculate the sequence counter
    self.idlePacketSequenceCounter = (self.idlePacketSequenceCounter + 1) % 16384
    idlePacket.sequenceControlCount = self.idlePacketSequenceCounter
    # re-calculate the CRC
    idlePacket.setChecksum()
    return idlePacket
  # ---------------------------------------------------------------------------
  def flushTMframeOrIdleFrame(self):
    """finalize a telemetry frame with an idle packet or create an idle frame"""
    # TODO: replace the dummy code with the correct code
    idleFrame = CCSDS.FRAME.TMframe()
    idleFrame.firstHeaderPointer = CCSDS.FRAME.IDLE_FRAME_PATTERN
    self.notifyTMframeCallback(idleFrame.getBuffer())
  # ---------------------------------------------------------------------------
  def notifyTMframeCallback(self, binFrame):
    """notifies when the next TM frame is assembled"""
    # shall be overloaded in derived class, default implementaion logs frame
    LOG("Assembler.notifyTMframeCallback" + UTIL.DU.array2str(binFrame))
