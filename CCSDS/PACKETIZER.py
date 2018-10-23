#******************************************************************************
# (C) 2018, Stefan Korner, Austria                                            *
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
  def __init__(self):
    """default constructor"""
    self.pendingPacketFragment = None
    self.expectedPacketSize = 0
  # ---------------------------------------------------------------------------
  def reset(self):
    """resets pending packet fragment"""
    self.pendingPacketFragment = None
    self.expectedPacketSize = 0
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
    except:
      LOG_ERROR("error in TM packet extraction from TM frame")
      self.reset()
    # --- leading fragment ---
    if leadingFragment:
      # there must be a pending packet fragment from the previous frame
      if self.pendingPacketFragment:
        newPacketSize = len(self.pendingPacketFragment) + len(leadingFragment)
        if newPacketSize < self.expectedPacketSize:
          self.pendingPacketFragment += leadingFragment
          # consistency check
          if len(packets) > 0 or trailingFragment:
            LOG_ERROR("TM packet fragment not fully assembled")
            self.reset()
          else:
            # other fragment(s) should follow in next frame
            return
        elif newPacketSize == self.expectedPacketSize:
          # spillover packet complete assembled
          packet = self.pendingPacketFragment + leadingFragment
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
      expectedPacketSize = CCSDS.PACKET.getPacketSize(trailingFragment)
      # consistency check
      if len(trailingFragment) >= 0 or expectedPacketSize:
        LOG_ERROR("invalid TM packet fragment size at TM frame end")
        self.reset()
      else:
        self.expectedPacketSize = expectedPacketSize
        self.pendingPacketFragment = trailingFragment
  # ---------------------------------------------------------------------------
  def notifyTMpacketCallback(self, binPacket):
    """notifies when the next TM packet is assembled"""
    # shall be overloaded in derived class, default implementaion logs packet
    LOG("Packetizer.notifyTMpacketCallback" + UTIL.DU.array2str(binPacket))

