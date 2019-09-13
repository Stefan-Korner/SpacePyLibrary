#!/usr/bin/env python
#******************************************************************************
# (C) 2019, Stefan Korner, Austria                                            *
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
# Tutorial - Example_7                                                        *
#******************************************************************************
import sys
from UTIL.SYS import LOG, LOG_ERROR
import CCSDS.FRAME
import UTIL.DU

#############
# constants #
#############
FRAME_FILE_NAME = "Example_7.hex"

########
# main #
########
# open the frame dump file for binary reading
try:
  frameFile = open(FRAME_FILE_NAME, "r")
except:
  LOG_ERROR("cannot read " + self.frameDumpFileName)
  sys.exit(-1)
# read hex frames from file and display related packets
for h, hexFrame in enumerate(frameFile.readlines()):
  LOG("--- tmFrame_" + str(h) + " ---")
  binFrame = UTIL.DU.str2array(hexFrame)
  # create a CCSDS TM Frame object that wraps the binary data
  tmFrame = CCSDS.FRAME.TMframe(binFrame)
  # extract the TM Packets
  leadingFragment, tmPackets, trailingFragment = tmFrame.getPackets()
  LOG("leadingFragment = " + str(leadingFragment))
  for i, tmPacket in enumerate(tmPackets):
    LOG("tmPacket_" + str(i) + " = " + UTIL.DU.array2str(tmPacket))
  LOG("trailingFragment = " + str(trailingFragment))
# close file
frameFile.close()
