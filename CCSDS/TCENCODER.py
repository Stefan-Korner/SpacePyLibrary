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
# CCSDS Stack - TC Encoder that converts TC packets into TC frames or CLTUs   *
# Must be overloaded to handle the CLTU callback.                             *
# Restriction: Maps one packet to one frame / one CLTU                        *
# Restriction: Supports only one virtual channel                              *
#******************************************************************************
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import CCSDS.CLTU, CCSDS.FRAME, CCSDS.SEGMENT
import UTIL.DU

###########
# classes #
###########
# =============================================================================
class TCencoder():
  """Converter from TC packets to TC frames or CLTUs"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """default constructor"""
    self.segmentMapId = 0
    self.frameVersionNumber = 0
    self.frameBypassFlag = 1
    self.frameControlCommandFlag = 0
    self.frameSpacecraftId = 758
    self.frameVirtualChannelId = 0
    self.frameSequenceNumber = 0
  # ---------------------------------------------------------------------------
  def pushTCpacket(self, binPacket, convertToCLTU):
    """consumes a telecommand packet"""
    # create the segment from the packet
    segmentDU = CCSDS.SEGMENT.TCsegment()
    segmentDU.setTCpacketData(binPacket)
    segmentDU.sequenceFlags = CCSDS.SEGMENT.UNSEGMENTED
    segmentDU.mapId = self.segmentMapId
    # create the frame from the segment
    frameDU = CCSDS.FRAME.TCframe()
    frameDU.setSegment(segmentDU.buffer)
    frameDU.versionNumber = self.frameVersionNumber
    frameDU.bypassFlag = self.frameBypassFlag
    frameDU.controlCommandFlag = self.frameControlCommandFlag
    frameDU.spacecraftId = self.frameSpacecraftId
    frameDU.virtualChannelId = self.frameVirtualChannelId
    frameDU.sequenceNumber = self.frameSequenceNumber
    if CCSDS.FRAME.CRC_CHECK:
      frameDU.setChecksum()
    self.frameSequenceNumber = (self.frameSequenceNumber + 1) % 256
    if convertToCLTU:
      # create the CLTU from the frame
      cltu = CCSDS.CLTU.encodeCltu(frameDU.buffer)
      self.notifyCLTUcallback(cltu)
    else:
      self.notifyTCframeCallback(frameDU)
  # ---------------------------------------------------------------------------
  def notifyTCframeCallback(self, frameDU):
    """notifies when the next TC frame is assembled"""
    # shall be overloaded in derived class, default implementaion logs frame
    LOG("TCencoder.notifyTCframeCallback" + UTIL.DU.array2str(frameDU.getBufferString()))
  # ---------------------------------------------------------------------------
  def notifyCLTUcallback(self, cltu):
    """notifies when the next CLTU is assembled"""
    # shall be overloaded in derived class, default implementaion logs CLTU
    LOG("TCencoder.notifyCLTUcallback" + UTIL.DU.array2str(cltu))

