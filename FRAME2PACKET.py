#!/usr/bin/env python
#******************************************************************************
# (C) 2018, Stefan Korner, Austria                                            *
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
# Converts CCSDS TM transfer frame dumps to CCSDS TM packet dumps,            *
# which are compatible with the SPACE.TMRPLY format.                          *
#                                                                             *
# The following frame formats are supported:                                  *
# - NCTRS binary format defined by GRND.NCTRSDU                               *
# - CRYOSAT binary format defined by GRND.CRYOSATDU                           *
#                                                                             *
# The frame format is defined by a configutation option:                      *
# - Read NCTRS frames: TM_READ_FORMAT = NCTRS                                 *
# - Read CRYOSAT format: TM_READ_FORMAT = CRYOSAT                             *
#                                                                             *
# Frames dumps can be generated (e.g. for testing) via SIM                    *
# with the recordFrames function:                                             *
# - Generate NCTRS frames: TM_FRAME_FORMAT = NCTRS                            *
# - Generate CRYOSAT format: TM_FRAME_FORMAT = CRYOSAT                        *
#******************************************************************************
# Command line: FRAME2PACKET.py <frame dump file name> <packet file name>     *                                                                            *
#******************************************************************************
import sys
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import GRND.CRYOSATDU, GRND.NCTRSDU
import UTIL.SYS

#############
# constants #
#############
SYS_CONFIGURATION = [
  ["TM_FRAME_FORMAT", "NCTRS"],
  ["TM_TRANSFER_FRAME_SIZE", "1115"],
  ["SYS_COLOR_LOG", "1"]]

####################
# global variables #
####################
s_spilloverPacket = ""

#############
# functions #
#############
# -----------------------------------------------------------------------------
def generatePackets(frameDumpFileName, packetFileName):
  """Extracts CCSDS TM packets from CCSDS TM transfer frames"""
  # open the frame dump file for binary reading
  try:
    frameDumpFile = open(frameDumpFileName, "rb")
  except:
    LOG_ERROR("cannot read " + frameDumpFileName)
    sys.exit(-1)
  # open the packet file for ASCII writing
  try:
    packetFile = open(packetFileName, "w")
  except:
    LOG_ERROR("cannot open " + packetFileName)
    sys.exit(-1)
  # iterate over annotated frames
  frameSize = int(UTIL.SYS.s_configuration.TM_TRANSFER_FRAME_SIZE)
  frameDumpFormat = UTIL.SYS.s_configuration.TM_FRAME_FORMAT
  if frameDumpFormat == "NCTRS":
    generatePacketsFromNCTRSframes(frameDumpFile, frameSize, packetFile)
  elif frameDumpFormat == "CRYOSAT":
    generatePacketsFromCRYOSATframes(frameDumpFile, frameSize, packetFile)
  else:
    LOG_ERROR("invalid frame dump format in config option TM_FRAME_FORMAT: " + frameDumpFormat)
    sys.exit(-1)
  # close files
  packetFile.close()
  frameDumpFile.close()
# -----------------------------------------------------------------------------
def generatePacketsFromNCTRSframes(frameDumpFile, frameSize, packetFile):
  """Extracts CCSDS TM packets from NCTRS TM transfer frames"""
  frameNumber = 1
  while True:
    nctrsHeader = frameDumpFile.read(GRND.NCTRSDU.TM_DU_HEADER_BYTE_SIZE)
    if len(nctrsHeader) == 0:
      # end of file reached
      return
    elif len(nctrsHeader) != GRND.NCTRSDU.TM_DU_HEADER_BYTE_SIZE:
      LOG_ERROR("frameDumpFile has incomplete NCTRS frame " + str(frameNumber))
      sys.exit(-1)
    # nctrsHeader completely read --> read CCSDS frame
    ccsdsFrame = frameDumpFile.read(frameSize)
    if len(ccsdsFrame) != frameSize:
      LOG_ERROR("frameDumpFile has incomplete CCSDS frame " + str(frameNumber))
      sys.exit(-1)
    generatePacketsFromCCSDSframe(ccsdsFrame, frameNumber, packetFile)
    # prepare read of next frame
    frameNumber += 1
# -----------------------------------------------------------------------------
def generatePacketsFromCRYOSATframes(frameDumpFile, frameSize, packetFile):
  """Extracts CCSDS TM packets from CRYOSAT TM transfer frames"""
  frameNumber = 1
  while True:
    cryosatHeader = frameDumpFile.read(GRND.CRYOSATDU.TM_FRAME_DU_HEADER_BYTE_SIZE)
    if len(cryosatHeader) == 0:
      # end of file reached
      return
    elif len(cryosatHeader) != GRND.CRYOSATDU.TM_FRAME_DU_HEADER_BYTE_SIZE:
      LOG_ERROR("frameDumpFile has incomplete CRYOSAT frame " + str(frameNumber))
      sys.exit(-1)
    # cryosatHeader completely read --> read CCSDS frame
    ccsdsFrame = frameDumpFile.read(frameSize)
    if len(ccsdsFrame) != frameSize:
      LOG_ERROR("frameDumpFile has incomplete CCSDS frame " + str(frameNumber))
      sys.exit(-1)
    generatePacketsFromCCSDSframe(ccsdsFrame, frameNumber, packetFile)
    # prepare read of next frame
    frameNumber += 1
# -----------------------------------------------------------------------------
def generatePacketsFromCCSDSframe(ccsdsFrame, frameNumber, packetFile):
  LOG_INFO("frame " + str(frameNumber))
  packetFile.write("frame " + str(frameNumber) + "\n")
# -----------------------------------------------------------------------------
def printUsage(launchScriptName):
  """Prints the commandline options"""
  print ""
  print "usage:"
  print "------"
  print ""
  print launchScriptName + " <frame dump file name> <packet file name>"
  print ""

########
# main #
########
# process command line
if len(sys.argv) != 3:
  print "error: invalid command line!"
  launchScriptName = sys.argv[0]
  printUsage(launchScriptName)
  sys.exit(-1)
frameDumpFileName = sys.argv[1]
packetFileName = sys.argv[2]
# initialise the system configuration
UTIL.SYS.s_configuration.setDefaults(SYS_CONFIGURATION)
LOG("frameDumpFileName = " + frameDumpFileName)
LOG("launchScriptName = " + packetFileName)
generatePackets(frameDumpFileName, packetFileName)
