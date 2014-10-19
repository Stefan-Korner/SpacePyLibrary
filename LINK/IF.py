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

# =============================================================================
class CLCWdefaults(object):
  """Default values for CLCW"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """default constructor"""
    self.type = 0
    self.version = 0
    self.statusField = 0
    self.copInEffect = 1
    self.virtualChannelId = 0
    self.spareField = 0
    self.noRfAvailable = 0
    self.noBitLock = 0
    self.lockout = 0
    self.wait = 0
    self.retransmit = 0
    self.farmBcounter = 0
    self.reportType = 0
    self.reportValue = 0

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
class PacketLink(object):
  """Interface to the packet link"""
  # ---------------------------------------------------------------------------
  def pushTMpacket(self, tmPacketDu):
    """consumes a telemetry packet"""
    pass

# =============================================================================
class TMframeGenerator(object):
  """Interface of the generator for telemetry packets"""
  # ---------------------------------------------------------------------------
  def initCLCW(self, clcwDefaults=CLCWdefaults()):
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
# packet link is a singleton
s_packetLink = None
# telemetry frame generator is a singleton
s_tmFrameGenerator = None
