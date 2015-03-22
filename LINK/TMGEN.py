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
# Link Simulation - Telemetry Frame Generator                                 *
#******************************************************************************
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import CCSDS.FRAME
import LINK.IF
import PUS.PACKET
import SCOS.ENV
import SPACE.IF

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
    self.transferFrameSize = SCOS.ENV.s_environment.getTransferFrameSize()
    self.versionNumber = 0
    self.spacecraftId = SCOS.ENV.s_environment.getSpacecraftID()
    self.virtualChannelId = SCOS.ENV.s_environment.getVirtualChannelID()
    self.operationalControlField = 1
    if SCOS.ENV.s_environment.transferFrameHasSecondaryHeader():
      self.secondaryHeaderFlag = 1
      self.secondaryHeaderSize = \
        SCOS.ENV.TRANSFER_FRAME_SECONDARY_HEADER_SIZE - 1
    else:
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
class TMframeGeneratorImpl(LINK.IF.TMframeGenerator):
  """Generator for telemetry frames"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """default constructor"""
    self.masterChannelFrameCount = 0
    self.virtualChannelFrameCount = 0
    self.frameDefaults = TMframeDefaults()
    self.initCLCW()
  # ---------------------------------------------------------------------------
  def initCLCW(self, clcwDefaults=LINK.IF.CLCWdefaults()):
    """
    initialise CLCW:
    implementation of LINK.IF.TMframeGenerator.getCLCW
    """
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
    """
    returns the CLCW for the next TM frame:
    implementation of LINK.IF.TMframeGenerator.getCLCW
    """
    return self.clcw
  # ---------------------------------------------------------------------------
  def setCLCWcount(self, value):
    """
    sets the counter in the CLCW for the next TM frame
    implementation of LINK.IF.TMframeGenerator.createTMframe
    """
    self.clcw.reportValue = value
  # ---------------------------------------------------------------------------
  def getTMframe(self, tmDataPacket):
    """
    creates a Transfer TM frame with embedded TM packet
    implementation of LINK.IF.TMframeGenerator.getTMframe
    """
    # create the idle packet
    reservedFrameDataSize = CCSDS.FRAME.TM_FRAME_PRIMARY_HEADER_BYTE_SIZE + \
                            len(tmDataPacket) + \
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
      # ---> an exception must be raisedas long as
      #      TM packet segmentation is not implemeted
      raise Error("TM packet with SPID " + str(spid) + " does not fit into transfer frame")
    createIdlePacket = (remainingFrameDataSize != 0)
    if createIdlePacket:
      tmIdlePacket = \
        SPACE.IF.s_tmPacketGenerator.getIdlePacket(remainingFrameDataSize)
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
    tmFrame.append(tmDataPacket.getBufferString())
    if createIdlePacket:
      tmFrame.append(tmIdlePacket.getBufferString())
    tmFrame.append(self.clcw.getBufferString())
    if CCSDS.FRAME.CRC_CHECK:
      tmFrame.append("\0" * CCSDS.FRAME.CRC_BYTE_SIZE)
      tmFrame.setChecksum()
    return tmFrame

#############
# functions #
#############
def init():
  # initialise singleton(s)
  LINK.IF.s_tmFrameGenerator = TMframeGeneratorImpl()
