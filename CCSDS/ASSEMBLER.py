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
import UTIL.DU

###########
# classes #
###########
# =============================================================================
class Assembler():
  """Converter from TM packets to TM frames"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """default constructor"""
    self.pendingFrame = None
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
    pass
  # ---------------------------------------------------------------------------
  def flushTMframe(self):
    """finalize a telemetry frame with an idle packet"""
    pass
  # ---------------------------------------------------------------------------
  def notifyTMframeCallback(self, binFrame):
    """notifies when the next TM frame is assembled"""
    # shall be overloaded in derived class, default implementaion logs frame
    LOG("Assembler.notifyTMframeCallback" + UTIL.DU.array2str(binFrame))
