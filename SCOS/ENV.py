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
# SCOS-2000 Functionality - Environment                                       *
#******************************************************************************
import os, sys
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR

#############
# constants #
#############
# size values in byte
SCOS_PACKET_HEADER_SIZE = 64
# reserved data space for packets when no size is defined in the MIB
TM_PKT_DEFAULT_DATAFIELD_DATA_SPACE = 16
# default value from the CCSDS standard
TPKT_PKT_IDLE_APID = 2047
TRANSFER_FRAME_DEFAULT_SIZE = 1115
TRANSFER_FRAME_SECONDARY_HEADER_SIZE = 4

###########
# classes #
###########
# =============================================================================
class Environment(object):
  """Manager for environment data"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """initialise from TPKTconnTable.dat and TPKTconfigTable.dat"""
    self.hostName = os.getenv("HOST")
    self.runtimeRoot = os.getenv("TESTENV")
    if self.runtimeRoot == None:
      LOG_ERROR("TESTENV not initialised")
      sys.exit(-1)
    # read essential information from TPKTconfigTable.dat
    tpktConfigTableFileName = self.mibDir() + "/TPKTconfigTable.dat"
    try:
      tpktConfigTableFile = open(tpktConfigTableFileName);
    except:
      LOG_ERROR("cannot read " + tpktConfigTableFileName)
      sys.exit(-1)
    fileContents = tpktConfigTableFile.readlines()
    tpktConfigTableFile.close()
    # parse the file and take the first data entry
    self.spacecraftID = None
    self.virtualChannelID = None
    self.transferFrameSize = None
    self.transferFrameHasSecondaryHdr = None
    for line in fileContents:
      tokens = line.split()
      if len(tokens) >= 8 and tokens[0] != "#":
        # line found
        self.spacecraftID = int(tokens[0])
        self.virtualChannelID = int(tokens[1])
        self.transferFrameSize = int(tokens[6])
        if self.transferFrameSize == -1:
          self.transferFrameSize = TRANSFER_FRAME_DEFAULT_SIZE
        self.transferFrameHasSecondaryHdr = \
          (tokens[7] == "y" or tokens[7] == "Y")
        break
    if self.spacecraftID == None:
      LOG_ERROR("no valid entry found in " + tpktConfigTableFileName)
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
    return self.spacecraftID
  # ---------------------------------------------------------------------------
  def getVirtualChannelID(self):
    """Returns the Virtual Channel ID"""
    return self.virtualChannelID
  # ---------------------------------------------------------------------------
  def getTransferFrameSize(self):
    """Returns the transfer frame size"""
    return self.transferFrameSize
  # ---------------------------------------------------------------------------
  def transferFrameHasSecondaryHeader(self):
    """Returns if the transfer frame has a secondary header"""
    return self.transferFrameHasSecondaryHdr

####################
# global variables #
####################
# environment is a singleton
s_environment = Environment()
