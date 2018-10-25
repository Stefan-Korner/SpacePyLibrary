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
# EGSE Interface                                                              *
#******************************************************************************
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import UTIL.SYS

#############
# constants #
#############
ENABLE_ACK = 0
ENABLE_NAK = 1
DISABLE_ACK = 2
ACK_STRS = ["ENABLE_ACK", "ENABLE_NAK", "DISABLE_ACK"]

###########
# classes #
###########
# =============================================================================
class Configuration(object):
  """Configuration"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """Initialise the connection relevant informations"""
    self.egseProtocol = UTIL.SYS.s_configuration.EGSE_PROTOCOL
    self.connected = False
    self.ccsPort = UTIL.SYS.s_configuration.CCS_SERVER_PORT
    self.connected2 = False
    self.ccsPort2 = UTIL.SYS.s_configuration.CCS_SERVER_PORT2
    self.egseAck1 = ENABLE_ACK
    self.egseAck2 = ENABLE_ACK
  # ---------------------------------------------------------------------------
  def dump(self):
    """Dumps the status of the configuration attributes"""
    LOG_INFO("EGSE interface configuration", "EGSE")
    LOG("CCS connected = " + str(self.connected), "EGSE")
    LOG("CCS interface port = " + str(self.ccsPort), "EGSE")
    LOG("CCS connected 2 = " + str(self.connected2), "EGSE")
    LOG("CCS interface port 2 = " + str(self.ccsPort2), "EGSE")
    LOG("TC Ack 1 = " + ACK_STRS[self.egseAck1], "EGSE")
    LOG("TC Ack 2 = " + ACK_STRS[self.egseAck2], "EGSE")

##############
# interfaces #
##############
# =============================================================================
class CCSlink(object):
  """Interface to the central checkout system"""
  # ---------------------------------------------------------------------------
  def pushTMpacket(self, tmPacketDu):
    """consumes a telemetry packet"""
    pass

####################
# global variables #
####################
# configuration is a singleton
s_configuration = None
# CCS link is a singleton
s_ccsLink = None
