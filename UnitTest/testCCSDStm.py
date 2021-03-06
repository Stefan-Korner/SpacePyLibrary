#!/usr/bin/env python3
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
import unittest
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
s_tmBinFrames = []
s_tmBinPackets = []

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
  def notifyTMframeCallback(self, tmFrameDu):
    """notifies when the next TM frame is assembled"""
    # overloaded from CCSDS.ASSEMBLER.Assembler
    global s_packetizer, s_tmBinFrames
    binFrame = tmFrameDu.getBuffer()
    s_tmBinFrames.append(binFrame)
    s_packetizer.pushTMframe(binFrame)

# =============================================================================
class Packetizer(CCSDS.PACKETIZER.Packetizer):
  """Subclass of CCSDS.PACKETIZER.Packetizer"""
  def __init__(self):
    """Initialise attributes only"""
    frameVCID = int(UTIL.SYS.s_configuration.TM_TRANSFER_FRAME_VCID)
    CCSDS.PACKETIZER.Packetizer.__init__(self, frameVCID)
  # ---------------------------------------------------------------------------
  def notifyTMpacketCallback(self, binPacket):
    """notifies when the next TM packet is assembled"""
    # overloaded from CSDS.PACKETIZER.Packetizer
    global s_tmBinPackets
    s_tmBinPackets.append(binPacket)

#############
# functions #
#############
def initConfiguration():
  """initialise the system configuration"""
  UTIL.SYS.s_configuration.setDefaults([
  ["SPACECRAFT_ID", "758"],
  ["TM_VIRTUAL_CHANNEL_ID", "0"],
  ["TM_TRANSFER_FRAME_SIZE", "1115"],
  ["TM_TRANSFER_FRAME_VCID", "0"],
  ["TM_TRANSFER_FRAME_HAS_SEC_HDR", "0"],
  ["TM_TRANSFER_FRAME_HAS_N_PKTS", "0"]])

#############
# test case #
#############
class TestCCSDStm(unittest.TestCase):
  # ---------------------------------------------------------------------------
  @classmethod
  def setUpClass(cls):
    """setup the environment"""
    global s_assembler, s_packetizer
    # initialise the system configuration
    initConfiguration()
    s_assembler = Assembler()
    s_packetizer = Packetizer()
  # ---------------------------------------------------------------------------
  def test_idleFrame(self):
    """pass an idle frame through Assembler and Packetizer"""
    global s_assembler, s_packetizer, s_tmBinFrames, s_tmBinPackets
    s_assembler.multiPacketMode = False
    s_assembler.reset()
    s_packetizer.reset()
    s_tmBinFrames = []
    s_tmBinPackets = []
    s_assembler.flushTMframeOrIdleFrame()
    self.assertEqual(len(s_tmBinFrames), 1)
    binFrame = s_tmBinFrames[0]
    self.assertEqual(len(binFrame), s_assembler.frameDefaults.transferFrameSize)
    tmFrame = CCSDS.FRAME.TMframe(binFrame)
    firstHeaderPointer = tmFrame.firstHeaderPointer
    self.assertEqual(firstHeaderPointer, CCSDS.FRAME.IDLE_FRAME_PATTERN)
    self.assertEqual(len(s_tmBinPackets), 0)
  # ---------------------------------------------------------------------------
  def test_singlePacket_1(self):
    """pass a single packet through Assembler and Packetizer"""
    global s_assembler, s_packetizer, s_tmBinFrames, s_tmBinPackets
    s_assembler.multiPacketMode = False
    s_assembler.reset()
    s_packetizer.reset()
    s_tmBinFrames = []
    s_tmBinPackets = []
    tmPacket = CCSDS.PACKET.TMpacket(testData.TM_PACKET_01)
    s_assembler.pushTMpacket(tmPacket.getBuffer())
    self.assertEqual(len(s_tmBinFrames), 1)
    self.assertEqual(len(s_tmBinPackets), 2)
    s_assembler.flushTMframe()
    self.assertEqual(len(s_tmBinFrames), 1)
    self.assertEqual(len(s_tmBinPackets), 2)
    binFrame = s_tmBinFrames[0]
    self.assertEqual(len(binFrame), s_assembler.frameDefaults.transferFrameSize)
    receivedTmPacket = CCSDS.PACKET.TMpacket(s_tmBinPackets[0])
    self.assertEqual(receivedTmPacket, tmPacket)
    receivedTmPacket = CCSDS.PACKET.TMpacket(s_tmBinPackets[1])
    self.assertEqual(receivedTmPacket.applicationProcessId, CCSDS.PACKET.IDLE_PKT_APID)
  # ---------------------------------------------------------------------------
  def test_doublePacket_1(self):
    """pass 2 packets through Assembler and Packetizer"""
    global s_assembler, s_packetizer, s_tmBinFrames, s_tmBinPackets
    s_assembler.multiPacketMode = False
    s_assembler.reset()
    s_packetizer.reset()
    s_tmBinFrames = []
    s_tmBinPackets = []
    tm1Packet = CCSDS.PACKET.TMpacket(testData.TM_PACKET_01)
    s_assembler.pushTMpacket(tm1Packet.getBuffer())
    tm2Packet = CCSDS.PACKET.TMpacket(testData.TM_PACKET_02)
    s_assembler.pushTMpacket(tm2Packet.getBuffer())
    self.assertEqual(len(s_tmBinFrames), 2)
    self.assertEqual(len(s_tmBinPackets), 4)
    s_assembler.flushTMframe()
    self.assertEqual(len(s_tmBinFrames), 2)
    self.assertEqual(len(s_tmBinPackets), 4)
    binFrame = s_tmBinFrames[0]
    self.assertEqual(len(binFrame), s_assembler.frameDefaults.transferFrameSize)
    binFrame = s_tmBinFrames[1]
    self.assertEqual(len(binFrame), s_assembler.frameDefaults.transferFrameSize)
    receivedTmPacket = CCSDS.PACKET.TMpacket(s_tmBinPackets[0])
    self.assertEqual(receivedTmPacket, tm1Packet)
    receivedTmPacket = CCSDS.PACKET.TMpacket(s_tmBinPackets[1])
    self.assertEqual(receivedTmPacket.applicationProcessId, CCSDS.PACKET.IDLE_PKT_APID)
    receivedTmPacket = CCSDS.PACKET.TMpacket(s_tmBinPackets[2])
    self.assertEqual(receivedTmPacket, tm2Packet)
    receivedTmPacket = CCSDS.PACKET.TMpacket(s_tmBinPackets[3])
    self.assertEqual(receivedTmPacket.applicationProcessId, CCSDS.PACKET.IDLE_PKT_APID)
  # ---------------------------------------------------------------------------
  def test_singlePacket_n(self):
    """pass a single packet through Assembler and Packetizer"""
    global s_assembler, s_packetizer, s_tmBinFrames, s_tmBinPackets
    s_assembler.multiPacketMode = True
    s_assembler.reset()
    s_packetizer.reset()
    s_tmBinFrames = []
    s_tmBinPackets = []
    tmPacket = CCSDS.PACKET.TMpacket(testData.TM_PACKET_01)
    s_assembler.pushTMpacket(tmPacket.getBuffer())
    self.assertEqual(len(s_tmBinFrames), 0)
    self.assertEqual(len(s_tmBinPackets), 0)
    s_assembler.flushTMframe()
    self.assertEqual(len(s_tmBinFrames), 1)
    self.assertEqual(len(s_tmBinPackets), 2)
    binFrame = s_tmBinFrames[0]
    self.assertEqual(len(binFrame), s_assembler.frameDefaults.transferFrameSize)
    receivedTmPacket = CCSDS.PACKET.TMpacket(s_tmBinPackets[0])
    self.assertEqual(receivedTmPacket, tmPacket)
    receivedTmPacket = CCSDS.PACKET.TMpacket(s_tmBinPackets[1])
    self.assertEqual(receivedTmPacket.applicationProcessId, CCSDS.PACKET.IDLE_PKT_APID)
  # ---------------------------------------------------------------------------
  def test_doublePacket_n(self):
    """pass 2 packets through Assembler and Packetizer"""
    global s_assembler, s_packetizer, s_tmBinFrames, s_tmBinPackets
    s_assembler.multiPacketMode = True
    s_assembler.reset()
    s_packetizer.reset()
    s_tmBinFrames = []
    s_tmBinPackets = []
    tm1Packet = CCSDS.PACKET.TMpacket(testData.TM_PACKET_01)
    s_assembler.pushTMpacket(tm1Packet.getBuffer())
    tm2Packet = CCSDS.PACKET.TMpacket(testData.TM_PACKET_02)
    s_assembler.pushTMpacket(tm2Packet.getBuffer())
    self.assertEqual(len(s_tmBinFrames), 0)
    self.assertEqual(len(s_tmBinPackets), 0)
    s_assembler.flushTMframe()
    self.assertEqual(len(s_tmBinFrames), 1)
    self.assertEqual(len(s_tmBinPackets), 3)
    binFrame = s_tmBinFrames[0]
    self.assertEqual(len(binFrame), s_assembler.frameDefaults.transferFrameSize)
    receivedTmPacket = CCSDS.PACKET.TMpacket(s_tmBinPackets[0])
    self.assertEqual(receivedTmPacket, tm1Packet)
    receivedTmPacket = CCSDS.PACKET.TMpacket(s_tmBinPackets[1])
    self.assertEqual(receivedTmPacket, tm2Packet)
    receivedTmPacket = CCSDS.PACKET.TMpacket(s_tmBinPackets[2])
    self.assertEqual(receivedTmPacket.applicationProcessId, CCSDS.PACKET.IDLE_PKT_APID)
  # ---------------------------------------------------------------------------
  def test_spilloverPacket(self):
    """pass 5 packets to force a spillover packet"""
    global s_assembler, s_packetizer, s_tmBinFrames, s_tmBinPackets
    s_assembler.multiPacketMode = True
    s_assembler.reset()
    s_packetizer.reset()
    s_tmBinFrames = []
    s_tmBinPackets = []
    tm1Packet = CCSDS.PACKET.TMpacket(testData.TM_PACKET_01)
    s_assembler.pushTMpacket(tm1Packet.getBuffer())
    tm2Packet = CCSDS.PACKET.TMpacket(testData.TM_PACKET_02)
    s_assembler.pushTMpacket(tm2Packet.getBuffer())
    tm3Packet = CCSDS.PACKET.TMpacket(testData.TM_PACKET_03)
    s_assembler.pushTMpacket(tm3Packet.getBuffer())
    tm4Packet = CCSDS.PACKET.TMpacket(testData.TM_PACKET_02)
    s_assembler.pushTMpacket(tm4Packet.getBuffer())
    tm5Packet = CCSDS.PACKET.TMpacket(testData.TM_PACKET_01)
    s_assembler.pushTMpacket(tm5Packet.getBuffer())
    self.assertEqual(len(s_tmBinFrames), 0)
    self.assertEqual(len(s_tmBinPackets), 0)
    tm6Packet = CCSDS.PACKET.TMpacket(testData.TM_PACKET_02)
    s_assembler.pushTMpacket(tm6Packet.getBuffer())
    self.assertEqual(len(s_tmBinFrames), 1)
    self.assertEqual(len(s_tmBinPackets), 5)
    s_assembler.flushTMframe()
    self.assertEqual(len(s_tmBinFrames), 2)
    self.assertEqual(len(s_tmBinPackets), 7)
    binFrame = s_tmBinFrames[0]
    self.assertEqual(len(binFrame), s_assembler.frameDefaults.transferFrameSize)
    binFrame = s_tmBinFrames[1]
    self.assertEqual(len(binFrame), s_assembler.frameDefaults.transferFrameSize)
    receivedTmPacket = CCSDS.PACKET.TMpacket(s_tmBinPackets[0])
    self.assertEqual(receivedTmPacket, tm1Packet)
    receivedTmPacket = CCSDS.PACKET.TMpacket(s_tmBinPackets[1])
    self.assertEqual(receivedTmPacket, tm2Packet)
    receivedTmPacket = CCSDS.PACKET.TMpacket(s_tmBinPackets[2])
    self.assertEqual(receivedTmPacket, tm3Packet)
    receivedTmPacket = CCSDS.PACKET.TMpacket(s_tmBinPackets[3])
    self.assertEqual(receivedTmPacket, tm4Packet)
    receivedTmPacket = CCSDS.PACKET.TMpacket(s_tmBinPackets[4])
    self.assertEqual(receivedTmPacket, tm5Packet)
    receivedTmPacket = CCSDS.PACKET.TMpacket(s_tmBinPackets[5])
    self.assertEqual(receivedTmPacket, tm6Packet)
    receivedTmPacket = CCSDS.PACKET.TMpacket(s_tmBinPackets[6])
    self.assertEqual(receivedTmPacket.applicationProcessId, CCSDS.PACKET.IDLE_PKT_APID)
  # ---------------------------------------------------------------------------
  def test_spillover2Frames(self):
    """pass 5 packets to force a spillover packet"""
    global s_assembler, s_packetizer, s_tmBinFrames, s_tmBinPackets
    s_assembler.multiPacketMode = True
    s_assembler.reset()
    s_packetizer.reset()
    s_tmBinFrames = []
    s_tmBinPackets = []
    tm1Packet = CCSDS.PACKET.TMpacket(testData.TM_PACKET_02)
    s_assembler.pushTMpacket(tm1Packet.getBuffer())
    self.assertEqual(len(s_tmBinFrames), 0)
    self.assertEqual(len(s_tmBinPackets), 0)
    tm2Packet = CCSDS.PACKET.TMpacket(testData.TM_PACKET_04)
    s_assembler.pushTMpacket(tm2Packet.getBuffer())
    self.assertEqual(len(s_tmBinFrames), 2)
    self.assertEqual(len(s_tmBinPackets), 1)
    s_assembler.flushTMframe()
    self.assertEqual(len(s_tmBinFrames), 3)
    self.assertEqual(len(s_tmBinPackets), 3)
    binFrame = s_tmBinFrames[0]
    self.assertEqual(len(binFrame), s_assembler.frameDefaults.transferFrameSize)
    binFrame = s_tmBinFrames[1]
    self.assertEqual(len(binFrame), s_assembler.frameDefaults.transferFrameSize)
    binFrame = s_tmBinFrames[2]
    self.assertEqual(len(binFrame), s_assembler.frameDefaults.transferFrameSize)
    receivedTmPacket = CCSDS.PACKET.TMpacket(s_tmBinPackets[0])
    self.assertEqual(receivedTmPacket, tm1Packet)
    receivedTmPacket = CCSDS.PACKET.TMpacket(s_tmBinPackets[1])
    self.assertEqual(receivedTmPacket, tm2Packet)
    receivedTmPacket = CCSDS.PACKET.TMpacket(s_tmBinPackets[2])
    self.assertEqual(receivedTmPacket.applicationProcessId, CCSDS.PACKET.IDLE_PKT_APID)

########
# main #
########
if __name__ == "__main__":
  unittest.main()
