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
# Ground Simulation - Ground Interface                                        *
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
class ClientConfiguration(object):
  """NCTRS Client Configuration"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """Initialise the connection relevant informations"""
    self.nctrsHost = UTIL.SYS.s_configuration.NCTRS_HOST
    self.nctrsTMconn = False
    self.nctrsTMport = UTIL.SYS.s_configuration.NCTRS_TM_SERVER_PORT
    self.nctrsTCconn = False
    self.nctrsTCport = UTIL.SYS.s_configuration.NCTRS_TC_SERVER_PORT
    self.nctrsAdminConn = False
    self.nctrsAdminPort = UTIL.SYS.s_configuration.NCTRS_ADMIN_SERVER_PORT
  # ---------------------------------------------------------------------------
  def dump(self):
    """Dumps the status of the configuration attributes"""
    LOG_INFO("Ground segment configuration", "NCTRS")
    LOG("NCTRS host = " + str(self.nctrsHost), "NCTRS")
    LOG("NCTRS TM conn = " + str(self.nctrsTMconn), "NCTRS")
    LOG("NCTRS TM port = " + str(self.nctrsTMport), "NCTRS")
    LOG("NCTRS TC conn = " + str(self.nctrsTCconn), "NCTRS")
    LOG("NCTRS TC port = " + str(self.nctrsTCport), "NCTRS")
    LOG("NCTRS admin message conn = " + str(self.nctrsAdminConn), "NCTRS")
    LOG("NCTRS admin message port = " + str(self.nctrsAdminPort), "NCTRS")

# =============================================================================
class Configuration(object):
  """Server Configuration"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """Initialise the connection relevant informations"""
    self.nctrsTMconn = False
    self.nctrsTMport = UTIL.SYS.s_configuration.NCTRS_TM_SERVER_PORT
    self.nctrsTCconn = False
    self.nctrsTCport = UTIL.SYS.s_configuration.NCTRS_TC_SERVER_PORT
    self.nctrsAdminConn = False
    self.nctrsAdminPort = UTIL.SYS.s_configuration.NCTRS_ADMIN_SERVER_PORT
    self.grndAck1 = ENABLE_ACK
    self.grndAck2 = ENABLE_ACK
    self.frameRecordFile = None
    self.frameRecordFormat = UTIL.SYS.s_configuration.TM_RECORD_FORMAT
  # ---------------------------------------------------------------------------
  def dump(self):
    """Dumps the status of the configuration attributes"""
    LOG_INFO("Ground segment configuration", "GRND")
    LOG("NCTRS TM conn = " + str(self.nctrsTMconn), "GRND")
    LOG("NCTRS TM port = " + str(self.nctrsTMport), "GRND")
    LOG("NCTRS TC conn = " + str(self.nctrsTCconn), "GRND")
    LOG("NCTRS TC port = " + str(self.nctrsTCport), "GRND")
    LOG("NCTRS admin message conn = " + str(self.nctrsAdminConn), "GRND")
    LOG("NCTRS admin message port = " + str(self.nctrsAdminPort), "GRND")
    LOG("TC Ack 1 = " + ACK_STRS[self.grndAck1], "GRND")
    LOG("TC Ack 2 = " + ACK_STRS[self.grndAck2], "GRND")
    LOG("Frame Record File = " + str(self.frameRecordFile), "GRND")
    LOG("Frame Record Format = " + str(self.frameRecordFormat), "GRND")

##############
# interfaces #
##############
# =============================================================================
class TMmcsLink(object):
  """Telemetry interface to the mission control system"""
  # ---------------------------------------------------------------------------
  def pushTMframe(self, tmFrameDu, ertUTC):
    """consumes a telemetry frame"""
    pass
  # ---------------------------------------------------------------------------
  def recordFrames(self, recordFileName):
    """starts TM frame recording"""
    pass
  # ---------------------------------------------------------------------------
  def stopFrameRecorder(self):
    """stops TM frame recording"""
    pass

####################
# global variables #
####################
# client configuration is a singleton
s_clientConfiguration = None
# configuration is a singleton
s_configuration = None
# telemetry link is a singleton
s_tmMcsLink = None
