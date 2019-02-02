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
# CCSDS Stack - Unit Tests                                                    *
#******************************************************************************
from __future__ import print_function
import testData
import CCSDS.ASSEMBLER, CCSDS.FRAME, CCSDS.PACKET, CCSDS.PACKETIZER
import UTIL.SYS

####################
# global variables #
####################
# Assembler and Packetizer are singletons
s_assembler = None
s_packetizer = None
# the last passed TM packet and TM frame
s_tmBinFrame = None
s_tmBinPacket = None
s_tmIdleBinPacket = None

###########
# classes #
###########
# =============================================================================
class Assembler(CCSDS.ASSEMBLER.Assembler):
  """Subclass of CCSDS.ASSEMBLER.Assembler"""
  def __init__(self):
    """Initialise attributes only"""
    CCSDS.ASSEMBLER.Assembler.__init__(self)
  # ---------------------------------------------------------------------------
  def notifyTMframeCallback(self, binFrame):
    """notifies when the next TM frame is assembled"""
    # overloaded from CCSDS.ASSEMBLER.Assembler
    global s_packetizer, s_tmBinFrame
    s_tmBinFrame = binFrame
    s_packetizer.pushTMframe(binFrame)

# =============================================================================
class Packetizer(CCSDS.PACKETIZER.Packetizer):
  """Subclass of CCSDS.PACKETIZER.Packetizer"""
  def __init__(self):
    """Initialise attributes only"""
    CCSDS.PACKETIZER.Packetizer.__init__(self)
  # ---------------------------------------------------------------------------
  def notifyTMpacketCallback(self, binPacket):
    """notifies when the next TM packet is assembled"""
    # overloaded from CSDS.PACKETIZER.Packetizer
    global s_tmBinPacket, s_tmIdleBinPacket
    tmPacket = CCSDS.PACKET.TMpacket(binPacket)
    if tmPacket.applicationProcessId == CCSDS.PACKET.IDLE_PKT_APID:
      s_tmIdleBinPacket = binPacket
    else:
      s_tmBinPacket = binPacket

#############
# functions #
#############
# -----------------------------------------------------------------------------
def initConfiguration():
  """initialise the system configuration"""
  UTIL.SYS.s_configuration.setDefaults([
  ["SPACECRAFT_ID", "758"],
  ["TM_VIRTUAL_CHANNEL_ID", "0"],
  ["TM_TRANSFER_FRAME_SIZE", "1115"],
  ["TM_TRANSFER_FRAME_HAS_SEC_HDR", "0"]])
# -----------------------------------------------------------------------------
def test_setup():
  """setup the environment"""
  global s_assembler, s_packetizer
  # initialise the system configuration
  initConfiguration()
  s_assembler = Assembler()
  s_packetizer = Packetizer()
  return True
# -----------------------------------------------------------------------------
def test_idleFrame():
  """pass an idle frame through Assembler and Packetizer"""
  global s_assembler, s_packetizer, s_tmBinFrame, s_tmBinPacket, s_tmIdleBinPacket
  s_tmBinFrame = None
  s_tmBinPacket = None
  s_tmIdleBinPacket = None
  s_assembler.flushTMframeOrIdleFrame()
  if s_tmBinFrame == None:
    print("expected idle frame missing")
    return False
  tmFrame = CCSDS.FRAME.TMframe(s_tmBinFrame)
  firstHeaderPointer = tmFrame.firstHeaderPointer
  if firstHeaderPointer != CCSDS.FRAME.IDLE_FRAME_PATTERN:
    print("unexpected frame is no idle frame")
    return False
  if s_tmBinPacket != None:
    print("unexpected packet passed via idle frame")
    return False
  if s_tmIdleBinPacket != None:
    print("unexpected idle packet passed via idle frame")
    return False
  return True
# -----------------------------------------------------------------------------
def test_singlePacket():
  """pass a single packet through Assembler and Packetizer"""
  global s_assembler, s_packetizer, s_tmBinFrame, s_tmBinPacket, s_tmIdleBinPacket
  s_tmBinFrame = None
  s_tmBinPacket = None
  s_tmIdleBinPacket = None
  tmPacket = CCSDS.PACKET.TMpacket(testData.TM_PACKET_01)
  s_assembler.pushTMpacket(tmPacket.getBuffer())
  if s_tmBinFrame != None:
    print("unexpected frame passed")
    return False
  if s_tmBinPacket != None:
    print("unexpected packet passed")
    return False
  if s_tmIdleBinPacket != None:
    print("unexpected idle packet passed")
    return False
  s_assembler.flushTMframe()
  if s_tmBinFrame == None:
    print("expected frame missing")
    return False
  if s_tmBinPacket == None:
    print("expected packet missing")
    return False
  if s_tmIdleBinPacket == None:
    print("expected idle packet missing")
    return False
  receivedTmPacket = CCSDS.PACKET.TMpacket(s_tmBinPacket)
  if receivedTmPacket != tmPacket:
    print("packet corrupted during frame assembling and packetizing")
    return False
  receivedTmPacket = CCSDS.PACKET.TMpacket(s_tmIdleBinPacket)
  if receivedTmPacket.applicationProcessId != CCSDS.PACKET.IDLE_PKT_APID:
    print("idle packet corrupted during frame assembling and packetizing")
    return False
  return True

########
# main #
########
if __name__ == "__main__":
  print("***** test_setup() start")
  retVal = test_setup()
  print("***** test_setup() done:", retVal)
  print("***** test_idleFrame() start")
  retVal = test_idleFrame()
  print("***** test_idleFrame() done:", retVal)
  print("***** test_singlePacket() start")
  retVal = test_singlePacket()
  print("***** test_singlePacket() done:", retVal)
