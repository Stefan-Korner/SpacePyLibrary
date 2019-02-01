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

####################
# global variables #
####################
# Assembler and Packetizer are singletons
s_assembler = None
s_packetizer = None
# the last passed TM packet and TM frame
s_tmFrame = None
s_tmPacket = None

###########
# classes #
###########
# =============================================================================
class Assembler(CCSDS.ASSEMBLER.Assembler):
  """Subclass of CCSDS.ASSEMBLER.Assembler"""
  def __init__(self):
    """Initialise attributes only"""
    CCSDS.ASSEMBLER.Assembler.__init__(self)
# =============================================================================
class Packetizer(CCSDS.PACKETIZER.Packetizer):
  """Subclass of CCSDS.PACKETIZER.Packetizer"""
  def __init__(self):
    """Initialise attributes only"""
    CCSDS.PACKETIZER.Packetizer.__init__(self)

#############
# functions #
#############
def test_AssemblerPacketizer():
  """function to test TM frame assembling and packetizing"""
  global s_assembler, s_packetizer, s_tmFrame, s_tmPacket
  s_assembler = Assembler()
  s_packetizer = Packetizer()
  # test 1: pass a single packet through Assembler and Packetizer
  tmPacket = CCSDS.PACKET.TMpacket(testData.TM_PACKET_01)
  s_tmFrame = None
  s_tmPacket = None
  s_assembler.pushTMpacket(tmPacket.getBuffer())
  if s_tmFrame != None:
    print("unexpected frame passed")
    return False
  if s_tmPacket != None:
    print("unexpected packet passed")
    return False
  s_assembler.flushTMframe()
  if s_tmFrame == None:
    print("expected frame missing")
    return False
  if s_tmPacket == None:
    print("expected packet missing")
    return False
  return True

########
# main #
########
if __name__ == "__main__":
  print("***** test_AssemblerPacketizer() start")
  retVal = test_AssemblerPacketizer()
  print("***** test_AssemblerPacketizer() done:", retVal)
