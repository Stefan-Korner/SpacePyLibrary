#!/usr/bin/env python
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
# CCSDS Stack - Unit Tests                                                    *
#******************************************************************************
import unittest
import testData
import CCSDS.PACKET
import PUS.PACKET

#############
# test case #
#############
class TestPACKET(unittest.TestCase):
  def test(self):
    """test PUS packets"""
    # default TM packet
    tmPacket = CCSDS.PACKET.TMpacket()
    self.assertEqual(tmPacket.versionNumber, 0)
    self.assertEqual(tmPacket.packetType, CCSDS.PACKET.TM_PACKET_TYPE)
    self.assertEqual(tmPacket.dataFieldHeaderFlag, 0)
    self.assertEqual(tmPacket.applicationProcessId, 0)
    self.assertEqual(tmPacket.segmentationFlags, 0)
    self.assertEqual(tmPacket.sequenceControlCount, 0)
    self.assertEqual(tmPacket.packetLength, 65535)
    # TM_PACKET_01 has no checksum
    tmPusPacket1 = PUS.PACKET.TMpacket(testData.TM_PACKET_01)
    self.assertEqual(tmPusPacket1.versionNumber,
                     testData.TM_PACKET_01_versionNumber)
    self.assertEqual(tmPusPacket1.packetType,
                     testData.TM_PACKET_01_packetType)
    self.assertEqual(tmPusPacket1.dataFieldHeaderFlag,
                     testData.TM_PACKET_01_dataFieldHeaderFlag)
    self.assertEqual(tmPusPacket1.applicationProcessId,
                     testData.TM_PACKET_01_applicationProcessId)
    self.assertEqual(tmPusPacket1.segmentationFlags,
                     testData.TM_PACKET_01_segmentationFlags)
    self.assertEqual(tmPusPacket1.sequenceControlCount,
                     testData.TM_PACKET_01_sequenceControlCount)
    self.assertEqual(tmPusPacket1.packetLength,
                     testData.TM_PACKET_01_packetLength)
    self.assertEqual(tmPusPacket1.pusVersionNumber,
                     testData.TM_PACKET_01_pusVersionNumber)
    self.assertEqual(tmPusPacket1.serviceType,
                     testData.TM_PACKET_01_serviceType)
    self.assertEqual(tmPusPacket1.serviceSubType,
                     testData.TM_PACKET_01_serviceSubType)
    self.assertTrue(tmPusPacket1.checkPacketLength())
    # TM_PACKET_02 has a checksum
    tmPusPacket2 = PUS.PACKET.TMpacket(testData.TM_PACKET_02)
    self.assertEqual(tmPusPacket2.versionNumber,
                     testData.TM_PACKET_02_versionNumber)
    self.assertEqual(tmPusPacket2.packetType,
                     testData.TM_PACKET_02_packetType)
    self.assertEqual(tmPusPacket2.dataFieldHeaderFlag,
                     testData.TM_PACKET_02_dataFieldHeaderFlag)
    self.assertEqual(tmPusPacket2.applicationProcessId,
                     testData.TM_PACKET_02_applicationProcessId)
    self.assertEqual(tmPusPacket2.segmentationFlags,
                     testData.TM_PACKET_02_segmentationFlags)
    self.assertEqual(tmPusPacket2.sequenceControlCount,
                     testData.TM_PACKET_02_sequenceControlCount)
    self.assertEqual(tmPusPacket2.packetLength,
                     testData.TM_PACKET_02_packetLength)
    self.assertEqual(tmPusPacket2.pusVersionNumber,
                     testData.TM_PACKET_02_pusVersionNumber)
    self.assertEqual(tmPusPacket2.serviceType,
                     testData.TM_PACKET_02_serviceType)
    self.assertEqual(tmPusPacket2.serviceSubType,
                     testData.TM_PACKET_02_serviceSubType)
    self.assertTrue(tmPusPacket2.checkPacketLength())
    self.assertTrue(tmPusPacket2.checkChecksum())
    # TM_PACKET_03 has a checksum
    tmPusPacket3 = PUS.PACKET.TMpacket(testData.TM_PACKET_03)
    self.assertEqual(tmPusPacket3.versionNumber,
                     testData.TM_PACKET_03_versionNumber)
    self.assertEqual(tmPusPacket3.packetType,
                     testData.TM_PACKET_03_packetType)
    self.assertEqual(tmPusPacket3.dataFieldHeaderFlag,
                     testData.TM_PACKET_03_dataFieldHeaderFlag)
    self.assertEqual(tmPusPacket3.applicationProcessId,
                     testData.TM_PACKET_03_applicationProcessId)
    self.assertEqual(tmPusPacket3.segmentationFlags,
                     testData.TM_PACKET_03_segmentationFlags)
    self.assertEqual(tmPusPacket3.sequenceControlCount,
                     testData.TM_PACKET_03_sequenceControlCount)
    self.assertEqual(tmPusPacket3.packetLength,
                     testData.TM_PACKET_03_packetLength)
    self.assertEqual(tmPusPacket3.pusVersionNumber,
                     testData.TM_PACKET_03_pusVersionNumber)
    self.assertEqual(tmPusPacket3.serviceType,
                     testData.TM_PACKET_03_serviceType)
    self.assertEqual(tmPusPacket3.serviceSubType,
                     testData.TM_PACKET_03_serviceSubType)
    self.assertTrue(tmPusPacket3.checkPacketLength())
    self.assertTrue(tmPusPacket3.checkChecksum())
    # TM_PACKET_04 has a checksum
    tmPusPacket4 = PUS.PACKET.TMpacket(testData.TM_PACKET_04)
    self.assertEqual(tmPusPacket4.versionNumber,
                     testData.TM_PACKET_04_versionNumber)
    self.assertEqual(tmPusPacket4.packetType,
                     testData.TM_PACKET_04_packetType)
    self.assertEqual(tmPusPacket4.dataFieldHeaderFlag,
                     testData.TM_PACKET_04_dataFieldHeaderFlag)
    self.assertEqual(tmPusPacket4.applicationProcessId,
                     testData.TM_PACKET_04_applicationProcessId)
    self.assertEqual(tmPusPacket4.segmentationFlags,
                     testData.TM_PACKET_04_segmentationFlags)
    self.assertEqual(tmPusPacket4.sequenceControlCount,
                     testData.TM_PACKET_04_sequenceControlCount)
    self.assertEqual(tmPusPacket4.packetLength,
                     testData.TM_PACKET_04_packetLength)
    self.assertEqual(tmPusPacket4.pusVersionNumber,
                     testData.TM_PACKET_04_pusVersionNumber)
    self.assertEqual(tmPusPacket4.serviceType,
                     testData.TM_PACKET_04_serviceType)
    self.assertEqual(tmPusPacket4.serviceSubType,
                     testData.TM_PACKET_04_serviceSubType)
    self.assertTrue(tmPusPacket4.checkPacketLength())
    self.assertTrue(tmPusPacket4.checkChecksum())
    # default TC packet
    tcPacket = CCSDS.PACKET.TCpacket()
    self.assertEqual(tcPacket.versionNumber, 0)
    self.assertEqual(tcPacket.packetType, CCSDS.PACKET.TC_PACKET_TYPE)
    self.assertEqual(tcPacket.dataFieldHeaderFlag, 0)
    self.assertEqual(tcPacket.applicationProcessId, 0)
    self.assertEqual(tcPacket.segmentationFlags, 0)
    self.assertEqual(tcPacket.sequenceControlCount, 0)
    self.assertEqual(tcPacket.packetLength, 65535)
    # TC_PACKET_01 has a checksum
    tcPusPacket = PUS.PACKET.TCpacket(testData.TC_PACKET_01)
    self.assertEqual(tcPusPacket.versionNumber,
                     testData.TC_PACKET_01_versionNumber)
    self.assertEqual(tcPusPacket.packetType,
                     testData.TC_PACKET_01_packetType)
    self.assertEqual(tcPusPacket.dataFieldHeaderFlag,
                     testData.TC_PACKET_01_dataFieldHeaderFlag)
    self.assertEqual(tcPusPacket.applicationProcessId,
                     testData.TC_PACKET_01_applicationProcessId)
    self.assertEqual(tcPusPacket.segmentationFlags,
                     testData.TC_PACKET_01_segmentationFlags)
    self.assertEqual(tcPusPacket.sequenceControlCount,
                     testData.TC_PACKET_01_sequenceControlCount)
    self.assertEqual(tcPusPacket.packetLength,
                     testData.TC_PACKET_01_packetLength)
    self.assertEqual(tcPusPacket.pusVersionNumber,
                     testData.TC_PACKET_01_pusVersionNumber)
    self.assertEqual(tcPusPacket.ack,
                     testData.TC_PACKET_01_ack)
    self.assertEqual(tcPusPacket.serviceType,
                     testData.TC_PACKET_01_serviceType)
    self.assertEqual(tcPusPacket.serviceSubType,
                     testData.TC_PACKET_01_serviceSubType)
    self.assertTrue(tcPusPacket.checkPacketLength())
    self.assertTrue(tcPusPacket.checkChecksum())

########
# main #
########
if __name__ == "__main__":
  unittest.main()
