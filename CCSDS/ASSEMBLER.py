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
import CCSDS.DU, CCSDS.FRAME, CCSDS.PACKET
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
class Assembler(object):
  """Converter from TM packets to TM frames"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """default constructor"""
    if UTIL.SYS.s_configuration.TM_TRANSFER_FRAME_HAS_N_PKTS == "1":
      self.multiPacketMode = True
    else:
      self.multiPacketMode = False
    self.pendingFrame = None
    self.masterChannelFrameCount = 0
    self.virtualChannelFrameCount = 0
    self.frameDefaults = TMframeDefaults()
    self.initCLCW(CLCWdefaults())
  # ---------------------------------------------------------------------------
  def initCLCW(self, clcwDefaults):
    """initialise CLCW"""
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
    if not self.multiPacketMode:
      # simplified processing for single packet mode
      if self.pendingFrame != None:
        LOG_ERROR("unexpected pending frame")
      self.createPendingFrame()
      binPacketLen = len(binPacket)
      if self.pendingFrameFreeSpace() < binPacketLen:
        LOG_ERROR("packet too big for insert into frame")
        return
      self.pendingFrame.append(binPacket)
      self.flushTMframe()
      return
    # multi packet mode
    if self.pendingFrame == None:
      self.createPendingFrame()
    binPacketLen = len(binPacket)
    # add as much as possible from the TM packet to the frame
    freeSpace = self.pendingFrameFreeSpace()
    if freeSpace >= binPacketLen:
      # the complete TM packet can be added TM packet directly
      self.pendingFrame.append(binPacket)
      if freeSpace == binPacketLen:
        self.flushTMframe()
      return
    # the TM packet must be split into fragments:
    # add the first fragment and flush the frame
    firstFragment = binPacket[:freeSpace]
    self.pendingFrame.append(firstFragment)
    self.flushTMframe()
    # create frames with the remaining fragments
    remainingFragments = binPacket[freeSpace:]
    emptyFrameFreeSpace = self.emptyFrameFreeSpace()
    while len(remainingFragments) >= emptyFrameFreeSpace:
      # the next fragment fully fits into the next frame
      nextFragment = remainingFragments[:emptyFrameFreeSpace]
      self.createPendingFrame()
      self.pendingFrame.append(nextFragment)
      self.pendingFrame.firstHeaderPointer = CCSDS.FRAME.NO_FIRST_PACKET_PATTERN
      self.flushTMframe()
      remainingFragments = remainingFragments[emptyFrameFreeSpace:]
    # handle last fragment (if there is one) that partially fills a frame
    lastFragment = remainingFragments
    lastFragmentLen = len(lastFragment)
    if lastFragmentLen > 0:
      self.createPendingFrame()
      self.pendingFrame.append(lastFragment)
      self.pendingFrame.firstHeaderPointer = lastFragmentLen
      # the frame of the last fragment is not automatically flushed,
      # because it can be filled with further TM packet(s)
  # ---------------------------------------------------------------------------
  def createPendingFrame(self):
    """
    creates the TM frames only with the headers -->
    packet or packet fragments are appended later
    """
    enableSecondaryHeader = (self.frameDefaults.secondaryHeaderFlag == 1)
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
    self.pendingFrame = tmFrame
  # ---------------------------------------------------------------------------
  def emptyFrameFreeSpace(self):
    """free space of an empty frame, considers a CRC"""
    usedSpace = CCSDS.FRAME.TM_FRAME_PRIMARY_HEADER_BYTE_SIZE + CCSDS.FRAME.CLCW_BYTE_SIZE
    if self.frameDefaults.secondaryHeaderFlag == 1:
      usedSpace += CCSDS.FRAME.TM_FRAME_SECONDARY_HEADER_BYTE_SIZE
    if CCSDS.FRAME.CRC_CHECK:
      usedSpace += CCSDS.DU.CRC_BYTE_SIZE
    return self.frameDefaults.transferFrameSize - usedSpace
  # ---------------------------------------------------------------------------
  def pendingFrameFreeSpace(self):
    """checks free space of the pending frame, considers a CRC"""
    usedSpace = len(self.pendingFrame) + CCSDS.FRAME.CLCW_BYTE_SIZE
    if CCSDS.FRAME.CRC_CHECK:
      usedSpace += CCSDS.DU.CRC_BYTE_SIZE
    return self.frameDefaults.transferFrameSize - usedSpace
  # ---------------------------------------------------------------------------
  def flushTMframe(self):
    """finalize a telemetry frame with an idle packet"""
    if self.pendingFrame == None:
      return
    # append idle packet
    idlePacketSize = self.pendingFrameFreeSpace()
    if idlePacketSize > 0:
      # ensure that the idle packet has a consistent packet header
      # note: this might cause a spillover if the idle packet
      idlePacketSize = max(idlePacketSize, CCSDS.PACKET.PACKET_MIN_BYTE_SIZE)
      tmIdlePacket = CCSDS.PACKET.createIdlePacket(idlePacketSize)
      self.pendingFrame.append(tmIdlePacket.getBufferString())
    # append CLCW
    self.pendingFrame.append(self.clcw.getBufferString())
    # append CRC
    if CCSDS.FRAME.CRC_CHECK:
      self.pendingFrame.append("\0" * CCSDS.DU.CRC_BYTE_SIZE)
      self.pendingFrame.setChecksum()
    # frame complete
    self.notifyTMframeCallback(self.pendingFrame)
    self.pendingFrame = None
  # ---------------------------------------------------------------------------
  def flushTMframeOrIdleFrame(self):
    """finalize a telemetry frame with an idle packet or create an idle frame"""
    if self.pendingFrame != None:
      self.flushTMframe()
      return
    self.createPendingFrame()
    self.pendingFrame.firstHeaderPointer = CCSDS.FRAME.IDLE_FRAME_PATTERN
    self.flushTMframe()
  # ---------------------------------------------------------------------------
  def notifyTMframeCallback(self, tmFrameDu):
    """notifies when the next TM frame is assembled"""
    # shall be overloaded in derived class, default implementaion logs frame
    LOG("Assembler.notifyTMframeCallback" + UTIL.DU.array2str(tmFrameDu.getBuffer()))
