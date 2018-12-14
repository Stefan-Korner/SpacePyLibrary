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
# FRAME layer model                                                           *
#******************************************************************************
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import GRND.IF, GRND.NCTRS
import UTIL.TASK

#############
# constants #
#############
SEND_AS_PACKET = 0
SEND_AS_FRAME = 1
SEND_AS_CLTU = 1

###########
# classes #
###########
# =============================================================================
class FrameModel():
  """Implementation of the CS side frame processing"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """Initialise attributes only"""
    pass
  # ---------------------------------------------------------------------------
  def sendTCpacket(self, tcPacketDu, sendFormat):
    """sends a TM packet"""
    if sendFormat == SEND_AS_PACKET:
      LOG_INFO("TC packet ready for sending", "FRAME")
      return True
    return self.sendTCframe("", sendFormat)
  # ---------------------------------------------------------------------------
  def sendTCframe(self, tcFrameDu, sendFormat):
    """sends a TC frame"""
    if sendFormat == SEND_AS_FRAME:
      LOG_INFO("TC frame ready for sending", "FRAME")
      return True
    return self.sendTCcltu("", sendFormat)
  # ---------------------------------------------------------------------------
  def sendTCcltu(self, cltu, sendFormat):
    """sends a command link transfer unit"""
    if sendFormat == SEND_AS_CLTU:
      LOG_INFO("CLTU ready for sending", "FRAME")
      return True
    LOG_ERROR("invalid send format passed: " + str(sendFormat), "FRAME")
    return FALSE
  # ---------------------------------------------------------------------------
  def receiveTMframe(self, tmFrameDu):
    """TM frame received"""
    LOG_INFO("TM frame received", "FRAME")
    self.receiveTMpacket("")
  # ---------------------------------------------------------------------------
  def receiveTMpacket(self, tmPacketDu):
    """TM packet received"""
    LOG_INFO("TM packet extracted", "FRAME")

####################
# global variables #
####################
# frame model singletons
s_frameModel = None

#############
# functions #
#############
# functions to encapsulate access to s_frameModel
# -----------------------------------------------------------------------------
def init():
  """initialise singleton(s)"""
  global s_frameModel
  s_frameModel = FrameModel()
