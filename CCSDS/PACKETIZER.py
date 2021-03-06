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
# CCSDS Stack - Packetizer that converts TM frames to TM packets              *
# Must be overloaded to handle the packet callback.                           *
# Restriction: Supports only one virtual channel                              *
#******************************************************************************
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import CCSDS.FRAME, CCSDS.PACKET
import UTIL.DU

###########
# classes #
###########
# =============================================================================
class Packetizer():
  """Converter from TM frames to TM packets"""
  # ---------------------------------------------------------------------------
  def __init__(self, expectedVCID):
    """default constructor"""
    self.pendingPacketFragment = None
    self.expectedVCID = expectedVCID
  # ---------------------------------------------------------------------------
  def reset(self):
    """resets pending packet fragment"""
    self.pendingPacketFragment = None
  # ---------------------------------------------------------------------------
  def isPacketPending(self):
    """checks if there is a pending packet (waiting for next fragment)"""
    return (self.pendingPacketFragment != None)
  # ---------------------------------------------------------------------------
  def pushTMframe(self, binFrame):
    """consumes a telemetry frame"""
    # extract packets incl. fragments from frame
    try:
      frameDU = CCSDS.FRAME.TMframe(binFrame)
      leadingFragment, packets, trailingFragment = frameDU.getPackets()
    except Exception as ex:
      LOG_ERROR("error in TM packet extraction from TM frame: " + str(ex))
      self.reset()
      return
    # consistency check
    if frameDU.virtualChannelId != self.expectedVCID:
      LOG_WARNING("frame has unexpected virtual channel ID: " + str(frameDU.virtualChannelId))
      return
    # --- leading fragment ---
    if leadingFragment:
      # there must be a pending packet fragment from the previous frame
      if self.pendingPacketFragment:
        packet = self.pendingPacketFragment + leadingFragment
        newPacketSize = len(packet)
        expectedPacketSize = CCSDS.PACKET.getPacketSize(packet)
        if newPacketSize < expectedPacketSize:
          # consistency check
          if len(packets) > 0 or trailingFragment:
            LOG_ERROR("TM packet fragment not fully assembled")
            self.reset()
          else:
            # other fragment(s) should follow in next frame
            self.pendingPacketFragment = packet
            return
        elif newPacketSize == expectedPacketSize:
          # spillover packet complete assembled
          self.notifyTMpacketCallback(packet)
          self.reset()
        else:
          # assembled packet does not match the expected size (too large)
          LOG_ERROR("invalid TM packet fragment size in TM frame")
          self.reset()
      else:
        LOG_ERROR("unexpected TM packet fragment in TM frame")
        # ignore the packet fragment, regular packets should follow
    # --- complete packets ---
    if len(packets) > 0:
      for packet in packets:
        self.notifyTMpacketCallback(packet)
    # --- trailing fragment ---
    if trailingFragment:
      self.pendingPacketFragment = trailingFragment
  # ---------------------------------------------------------------------------
  def notifyTMpacketCallback(self, binPacket):
    """notifies when the next TM packet is assembled"""
    # shall be overloaded in derived class, default implementaion logs packet
    LOG("Packetizer.notifyTMpacketCallback" + UTIL.DU.array2str(binPacket))
