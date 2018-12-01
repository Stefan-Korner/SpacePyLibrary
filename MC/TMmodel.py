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
# Monitoring and Control (M&C) - Telemetry Model                              *
#******************************************************************************
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import MC.IF

###########
# classes #
###########
# =============================================================================
class TMmodel(MC.IF.TMmodel):
  """Implementation of the telemetry model"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """Initialise attributes only"""
  # ---------------------------------------------------------------------------
  def pushTMpacket(self, tmPacketDu, ertUTC):
    """
    consumes a telemetry packet:
    implementation of MC.IF.TMmodel.pushTMpacket
    """
    LOG_INFO("pushTMpacket", "TM")

#############
# functions #
#############
def init():
  # initialise singleton(s)
  MC.IF.s_tmModel = TMmodel()
