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
# Link Simulation - Ground to Space Interface                                 *
#******************************************************************************
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR

###########
# classes #
###########
# =============================================================================
class Configuration(object):
  """Configuration"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """Initialise the connection relevant informations"""
    self.enableCLCW = True
  # ---------------------------------------------------------------------------
  def dump(self):
    """Dumps the status of the configuration attributes"""
    LOG_INFO("Space link configuration", "LINK")
    LOG("Enable CLCW = " + str(self.enableCLCW), "LINK")

##############
# interfaces #
##############
# =============================================================================
class SpaceLink(object):
  """Interface to the spacecraft"""
  # ---------------------------------------------------------------------------
  def getUplinkQueue(self):
    """returns the uplink queue"""
    pass
  # ---------------------------------------------------------------------------
  def getDownlinkQueue(self):
    """returns the downlink queue"""
    pass
  # ---------------------------------------------------------------------------
  def pushTCcltu(self, cltu):
    """consumes a command link transfer unit"""
    pass

# =============================================================================
class GroundLink(object):
  """Interface to the ground"""
  # ---------------------------------------------------------------------------
  def pushTMpacketAndERT(self, tmPacketDu, ertUTC):
    """consumes a telemetry packet with ERT"""
    pass
  # ---------------------------------------------------------------------------
  def initCLCW(self, clcwDefaults):
    """initialise CLCW"""
  # ---------------------------------------------------------------------------
  def getCLCW(self):
    """returns the CLCW for the next TM frame"""
    pass
  # ---------------------------------------------------------------------------
  def setCLCWcount(self, value):
    """sets the counter in the CLCW for the next TM frame"""
    pass
  # ---------------------------------------------------------------------------
  def getTMframe(self, tmPacketDu):
    """creates a Transfer TM frame with embedded TM packet"""
    pass

####################
# global variables #
####################
# configuration is a singleton
s_configuration = None
# space link is a singleton
s_spaceLink = None
# ground link is a singleton
s_groundLink = None
