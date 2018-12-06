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
# Monitoring and Control (M&C) - Telecommand Model                            *
#******************************************************************************
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import MC.IF
import UTIL.DU

###########
# classes #
###########
# =============================================================================
class TCmodel(MC.IF.TCmodel):
  """Implementation of the telecommand model"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """Initialise attributes only"""
  # ---------------------------------------------------------------------------
  def pushTCpacket(self, tcPacketDu):
    """
    consumes a telecommand packet:
    implementation of MC.IF.TCmodel.pushTCpacket
    """
    LOG_INFO("pushTCpacket", "TC")
    LOG("PUS Packet:" + UTIL.DU.array2str(tcPacketDu.getBufferString()[0:min(16,len(tcPacketDu))]), "TC")

#############
# functions #
#############
def init():
  # initialise singleton(s)
  MC.IF.s_tcModel = TCmodel()
