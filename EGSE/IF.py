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
# EGSE Interface                                                              *
#******************************************************************************
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import UTIL.SYS

#############
# constants #
#############
#TBD

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
  # ---------------------------------------------------------------------------
  def dump(self):
    """Dumps the status of the configuration attributes"""
    LOG_INFO("EGSE interface configuration", "EGSE")
    LOG("CCS connected = " + str(self.connected), "EGSE")
    LOG("CCS interface port = " + str(self.ccsPort), "EGSE")
    LOG("CCS connected 2 = " + str(self.connected2), "EGSE")
    LOG("CCS interface port 2 = " + str(self.ccsPort2), "EGSE")

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
