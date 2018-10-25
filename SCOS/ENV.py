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
# SCOS-2000 Functionality - Environment                                       *
#******************************************************************************
import os, sys
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import UTIL.SYS

#############
# constants #
#############
# size values in byte
SCOS_PACKET_HEADER_SIZE = 64
# reserved data space for packets when no size is defined in the MIB
TM_PKT_DEFAULT_DATAFIELD_DATA_SPACE = 16
# default value from the CCSDS standard
TRANSFER_FRAME_SECONDARY_HEADER_SIZE = 4

###########
# classes #
###########
# =============================================================================
class Environment(object):
  """Manager for environment data"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """initialise from environment variables"""
    self.hostName = os.getenv("HOST")
    self.runtimeRoot = os.getenv("TESTENV")
    if self.runtimeRoot == None:
      LOG_ERROR("TESTENV not initialised")
      sys.exit(-1)
  # ---------------------------------------------------------------------------
  def mibDir(self):
    """Get the MIB directory"""
    return self.runtimeRoot + "/data/ASCII"
  # ---------------------------------------------------------------------------
  def tmFilesDir(self):
    """Get the TM replay files directory"""
    return self.runtimeRoot + "/data/tmFiles"
  # ---------------------------------------------------------------------------
  def definitionFileName(self):
    """Get the testdata.sim file name"""
    return self.runtimeRoot + "/testbin/testdata.sim"
  # ---------------------------------------------------------------------------
  def getSpacecraftID(self):
    """Returns the spacecraft ID"""
    return int(UTIL.SYS.s_configuration.SPACECRAFT_ID)
  # ---------------------------------------------------------------------------
  def getVirtualChannelID(self):
    """Returns the Virtual Channel ID"""
    return int(UTIL.SYS.s_configuration.TM_VIRTUAL_CHANNEL_ID)
  # ---------------------------------------------------------------------------
  def getTransferFrameSize(self):
    """Returns the transfer frame size"""
    return int(UTIL.SYS.s_configuration.TM_TRANSFER_FRAME_SIZE)
  # ---------------------------------------------------------------------------
  def transferFrameHasSecondaryHeader(self):
    """Returns if the transfer frame has a secondary header"""
    return (UTIL.SYS.s_configuration.TM_TRANSFER_FRAME_HAS_SEC_HDR == "1")

####################
# global variables #
####################
# environment is a singleton
s_environment = Environment()
