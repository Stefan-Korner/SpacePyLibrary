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
from __future__ import print_function
import testData
import CCSDS.PACKET
import PUS.PACKET

#############
# functions #
#############
def test_PACKET_DUoperations():
  """function to test the PUS packets"""
  # default TM packet
  tmPacket = CCSDS.PACKET.TMpacket()
  print("tmPacket =", tmPacket)
  print("")
  # TM_PACKET_01 has no checksum
  tmPusPacket1 = PUS.PACKET.TMpacket(testData.TM_PACKET_01)
  if tmPusPacket1.versionNumber != testData.TM_PACKET_01_versionNumber:
    print("tmPusPacket1 versionNumber wrong:", tmPusPacket1.versionNumber, "- should be", testData.TM_PACKET_01_versionNumber)
    return False
  if tmPusPacket1.packetType != testData.TM_PACKET_01_packetType:
    print("tmPusPacket1 packetType wrong:", tmPusPacket1.packetType, "- should be", testData.TM_PACKET_01_packetType)
    return False
  if tmPusPacket1.dataFieldHeaderFlag != testData.TM_PACKET_01_dataFieldHeaderFlag:
    print("tmPusPacket1 dataFieldHeaderFlag wrong:", tmPusPacket1.dataFieldHeaderFlag, "- should be", testData.TM_PACKET_01_dataFieldHeaderFlag)
    return False
  if tmPusPacket1.applicationProcessId != testData.TM_PACKET_01_applicationProcessId:
    print("tmPusPacket1 applicationProcessId wrong:", tmPusPacket1.applicationProcessId, "- should be", testData.TM_PACKET_01_applicationProcessId)
    return False
  if tmPusPacket1.segmentationFlags != testData.TM_PACKET_01_segmentationFlags:
    print("tmPusPacket1 segmentationFlags wrong:", tmPusPacket1.segmentationFlags, "- should be", testData.TM_PACKET_01_segmentationFlags)
    return False
  if tmPusPacket1.sequenceControlCount != testData.TM_PACKET_01_sequenceControlCount:
    print("tmPusPacket1 sequenceControlCount wrong:", tmPusPacket1.sequenceControlCount, "- should be", testData.TM_PACKET_01_sequenceControlCount)
    return False
  if tmPusPacket1.packetLength != testData.TM_PACKET_01_packetLength:
    print("tmPusPacket1 packetLength wrong:", tmPusPacket1.packetLength, "- should be", testData.TM_PACKET_01_packetLength)
    return False
  if tmPusPacket1.pusVersionNumber != testData.TM_PACKET_01_pusVersionNumber:
    print("tmPusPacket1 pusVersionNumber wrong:", tmPusPacket1.pusVersionNumber, "- should be", testData.TM_PACKET_01_pusVersionNumber)
    return False
  if tmPusPacket1.serviceType != testData.TM_PACKET_01_serviceType:
    print("tmPusPacket1 serviceType wrong:", tmPusPacket1.serviceType, "- should be", testData.TM_PACKET_01_serviceType)
    return False
  if tmPusPacket1.serviceSubType != testData.TM_PACKET_01_serviceSubType:
    print("tmPusPacket1 serviceSubType wrong:", tmPusPacket1.serviceSubType, "- should be", testData.TM_PACKET_01_serviceSubType)
    return False
  if not tmPusPacket1.checkPacketLength():
    print("tmPusPacket1 has inconsistent packetLength")
    return False
  # TM_PACKET_02 has a checksum
  tmPusPacket2 = PUS.PACKET.TMpacket(testData.TM_PACKET_02)
  if tmPusPacket2.versionNumber != testData.TM_PACKET_02_versionNumber:
    print("tmPusPacket2 versionNumber wrong:", tmPusPacket2.versionNumber, "- should be", testData.TM_PACKET_02_versionNumber)
    return False
  if tmPusPacket2.packetType != testData.TM_PACKET_02_packetType:
    print("tmPusPacket2 packetType wrong:", tmPusPacket2.packetType, "- should be", testData.TM_PACKET_02_packetType)
    return False
  if tmPusPacket2.dataFieldHeaderFlag != testData.TM_PACKET_02_dataFieldHeaderFlag:
    print("tmPusPacket2 dataFieldHeaderFlag wrong:", tmPusPacket2.dataFieldHeaderFlag, "- should be", testData.TM_PACKET_02_dataFieldHeaderFlag)
    return False
  if tmPusPacket2.applicationProcessId != testData.TM_PACKET_02_applicationProcessId:
    print("tmPusPacket2 applicationProcessId wrong:", tmPusPacket2.applicationProcessId, "- should be", testData.TM_PACKET_02_applicationProcessId)
    return False
  if tmPusPacket2.segmentationFlags != testData.TM_PACKET_02_segmentationFlags:
    print("tmPusPacket2 segmentationFlags wrong:", tmPusPacket2.segmentationFlags, "- should be", testData.TM_PACKET_02_segmentationFlags)
    return False
  if tmPusPacket2.sequenceControlCount != testData.TM_PACKET_02_sequenceControlCount:
    print("tmPusPacket2 sequenceControlCount wrong:", tmPusPacket2.sequenceControlCount, "- should be", testData.TM_PACKET_02_sequenceControlCount)
    return False
  if tmPusPacket2.packetLength != testData.TM_PACKET_02_packetLength:
    print("tmPusPacket2 packetLength wrong:", tmPusPacket2.packetLength, "- should be", testData.TM_PACKET_02_packetLength)
    return False
  if tmPusPacket2.pusVersionNumber != testData.TM_PACKET_02_pusVersionNumber:
    print("tmPusPacket2 pusVersionNumber wrong:", tmPusPacket2.pusVersionNumber, "- should be", testData.TM_PACKET_02_pusVersionNumber)
    return False
  if tmPusPacket2.serviceType != testData.TM_PACKET_02_serviceType:
    print("tmPusPacket2 serviceType wrong:", tmPusPacket2.serviceType, "- should be", testData.TM_PACKET_02_serviceType)
    return False
  if tmPusPacket2.serviceSubType != testData.TM_PACKET_02_serviceSubType:
    print("tmPusPacket2 serviceSubType wrong:", tmPusPacket2.serviceSubType, "- should be", testData.TM_PACKET_02_serviceSubType)
    return False
  if not tmPusPacket2.checkPacketLength():
    print("tmPusPacket2 has inconsistent packetLength")
    return False
  if not tmPusPacket2.checkChecksum():
    print("tmPusPacket2 has invalid checksum")
    return False
  # TM_PACKET_03 has a checksum
  tmPusPacket3 = PUS.PACKET.TMpacket(testData.TM_PACKET_03)
  if tmPusPacket3.versionNumber != testData.TM_PACKET_03_versionNumber:
    print("tmPusPacket3 versionNumber wrong:", tmPusPacket3.versionNumber, "- should be", testData.TM_PACKET_03_versionNumber)
    return False
  if tmPusPacket3.packetType != testData.TM_PACKET_03_packetType:
    print("tmPusPacket3 packetType wrong:", tmPusPacket3.packetType, "- should be", testData.TM_PACKET_03_packetType)
    return False
  if tmPusPacket3.dataFieldHeaderFlag != testData.TM_PACKET_03_dataFieldHeaderFlag:
    print("tmPusPacket3 dataFieldHeaderFlag wrong:", tmPusPacket3.dataFieldHeaderFlag, "- should be", testData.TM_PACKET_03_dataFieldHeaderFlag)
    return False
  if tmPusPacket3.applicationProcessId != testData.TM_PACKET_03_applicationProcessId:
    print("tmPusPacket3 applicationProcessId wrong:", tmPusPacket3.applicationProcessId, "- should be", testData.TM_PACKET_03_applicationProcessId)
    return False
  if tmPusPacket3.segmentationFlags != testData.TM_PACKET_03_segmentationFlags:
    print("tmPusPacket3 segmentationFlags wrong:", tmPusPacket3.segmentationFlags, "- should be", testData.TM_PACKET_03_segmentationFlags)
    return False
  if tmPusPacket3.sequenceControlCount != testData.TM_PACKET_03_sequenceControlCount:
    print("tmPusPacket3 sequenceControlCount wrong:", tmPusPacket3.sequenceControlCount, "- should be", testData.TM_PACKET_03_sequenceControlCount)
    return False
  if tmPusPacket3.packetLength != testData.TM_PACKET_03_packetLength:
    print("tmPusPacket3 packetLength wrong:", tmPusPacket3.packetLength, "- should be", testData.TM_PACKET_03_packetLength)
    return False
  if tmPusPacket3.pusVersionNumber != testData.TM_PACKET_03_pusVersionNumber:
    print("tmPusPacket3 pusVersionNumber wrong:", tmPusPacket3.pusVersionNumber, "- should be", testData.TM_PACKET_03_pusVersionNumber)
    return False
  if tmPusPacket3.serviceType != testData.TM_PACKET_03_serviceType:
    print("tmPusPacket3 serviceType wrong:", tmPusPacket3.serviceType, "- should be", testData.TM_PACKET_03_serviceType)
    return False
  if tmPusPacket3.serviceSubType != testData.TM_PACKET_03_serviceSubType:
    print("tmPusPacket3 serviceSubType wrong:", tmPusPacket3.serviceSubType, "- should be", testData.TM_PACKET_03_serviceSubType)
    return False
  if not tmPusPacket3.checkPacketLength():
    print("tmPusPacket3 has inconsistent packetLength")
    return False
  if not tmPusPacket3.checkChecksum():
    print("tmPusPacket3 has invalid checksum")
    return False
  # TM_PACKET_04 has a checksum
  tmPusPacket4 = PUS.PACKET.TMpacket(testData.TM_PACKET_04)
  if tmPusPacket4.versionNumber != testData.TM_PACKET_04_versionNumber:
    print("tmPusPacket4 versionNumber wrong:", tmPusPacket4.versionNumber, "- should be", testData.TM_PACKET_04_versionNumber)
    return False
  if tmPusPacket4.packetType != testData.TM_PACKET_04_packetType:
    print("tmPusPacket4 packetType wrong:", tmPusPacket4.packetType, "- should be", testData.TM_PACKET_04_packetType)
    return False
  if tmPusPacket4.dataFieldHeaderFlag != testData.TM_PACKET_04_dataFieldHeaderFlag:
    print("tmPusPacket4 dataFieldHeaderFlag wrong:", tmPusPacket4.dataFieldHeaderFlag, "- should be", testData.TM_PACKET_04_dataFieldHeaderFlag)
    return False
  if tmPusPacket4.applicationProcessId != testData.TM_PACKET_04_applicationProcessId:
    print("tmPusPacket4 applicationProcessId wrong:", tmPusPacket4.applicationProcessId, "- should be", testData.TM_PACKET_04_applicationProcessId)
    return False
  if tmPusPacket4.segmentationFlags != testData.TM_PACKET_04_segmentationFlags:
    print("tmPusPacket4 segmentationFlags wrong:", tmPusPacket4.segmentationFlags, "- should be", testData.TM_PACKET_04_segmentationFlags)
    return False
  if tmPusPacket4.sequenceControlCount != testData.TM_PACKET_04_sequenceControlCount:
    print("tmPusPacket4 sequenceControlCount wrong:", tmPusPacket4.sequenceControlCount, "- should be", testData.TM_PACKET_04_sequenceControlCount)
    return False
  if tmPusPacket4.packetLength != testData.TM_PACKET_04_packetLength:
    print("tmPusPacket4 packetLength wrong:", tmPusPacket4.packetLength, "- should be", testData.TM_PACKET_04_packetLength)
    return False
  if tmPusPacket4.pusVersionNumber != testData.TM_PACKET_04_pusVersionNumber:
    print("tmPusPacket4 pusVersionNumber wrong:", tmPusPacket4.pusVersionNumber, "- should be", testData.TM_PACKET_04_pusVersionNumber)
    return False
  if tmPusPacket4.serviceType != testData.TM_PACKET_04_serviceType:
    print("tmPusPacket4 serviceType wrong:", tmPusPacket4.serviceType, "- should be", testData.TM_PACKET_04_serviceType)
    return False
  if tmPusPacket4.serviceSubType != testData.TM_PACKET_04_serviceSubType:
    print("tmPusPacket4 serviceSubType wrong:", tmPusPacket4.serviceSubType, "- should be", testData.TM_PACKET_04_serviceSubType)
    return False
  if not tmPusPacket4.checkPacketLength():
    print("tmPusPacket4 has inconsistent packetLength")
    return False
  if not tmPusPacket4.checkChecksum():
    print("tmPusPacket4 has invalid checksum")
    return False
  # default TC packet
  tcPacket = CCSDS.PACKET.TCpacket()
  print("tcPacket =", tcPacket)
  print("")
  # TC_PACKET_01 has a checksum
  tcPusPacket = PUS.PACKET.TCpacket(testData.TC_PACKET_01)
  if tcPusPacket.versionNumber != testData.TC_PACKET_01_versionNumber:
    print("tcPusPacket versionNumber wrong:", tcPusPacket.versionNumber, "- should be", testData.TC_PACKET_01_versionNumber)
    return False
  if tcPusPacket.packetType != testData.TC_PACKET_01_packetType:
    print("tcPusPacket packetType wrong:", tcPusPacket.packetType, "- should be", testData.TC_PACKET_01_packetType)
    return False
  if tcPusPacket.dataFieldHeaderFlag != testData.TC_PACKET_01_dataFieldHeaderFlag:
    print("tcPusPacket dataFieldHeaderFlag wrong:", tcPusPacket.dataFieldHeaderFlag, "- should be", testData.TC_PACKET_01_dataFieldHeaderFlag)
    return False
  if tcPusPacket.applicationProcessId != testData.TC_PACKET_01_applicationProcessId:
    print("tcPusPacket applicationProcessId wrong:", tcPusPacket.applicationProcessId, "- should be", testData.TC_PACKET_01_applicationProcessId)
    return False
  if tcPusPacket.segmentationFlags != testData.TC_PACKET_01_segmentationFlags:
    print("tcPusPacket segmentationFlags wrong:", tcPusPacket.segmentationFlags, "- should be", testData.TC_PACKET_01_segmentationFlags)
    return False
  if tcPusPacket.sequenceControlCount != testData.TC_PACKET_01_sequenceControlCount:
    print("tcPusPacket sequenceControlCount wrong:", tcPusPacket.sequenceControlCount, "- should be", testData.TC_PACKET_01_sequenceControlCount)
    return False
  if tcPusPacket.packetLength != testData.TC_PACKET_01_packetLength:
    print("tcPusPacket packetLength wrong:", tcPusPacket.packetLength, "- should be", testData.TC_PACKET_01_packetLength)
    return False
  if tcPusPacket.pusVersionNumber != testData.TC_PACKET_01_pusVersionNumber:
    print("tcPusPacket pusVersionNumber wrong:", tcPusPacket.pusVersionNumber, "- should be", testData.TC_PACKET_01_pusVersionNumber)
    return False
  if tcPusPacket.ack != testData.TC_PACKET_01_ack:
    print("tcPusPacket ack wrong:", tcPusPacket.ack, "- should be", testData.TC_PACKET_01_ack)
    return False
  if tcPusPacket.serviceType != testData.TC_PACKET_01_serviceType:
    print("tcPusPacket serviceType wrong:", tcPusPacket.serviceType, "- should be", testData.TC_PACKET_01_serviceType)
    return False
  if tcPusPacket.serviceSubType != testData.TC_PACKET_01_serviceSubType:
    print("tcPusPacket serviceSubType wrong:", tcPusPacket.serviceSubType, "- should be", testData.TC_PACKET_01_serviceSubType)
    return False
  if not tcPusPacket.checkPacketLength():
    print("tcPusPacket has inconsistent packetLength")
    return False
  if not tcPusPacket.checkChecksum():
    print("tcPusPacket has invalid checksum")
    return False
  return True

########
# main #
########
if __name__ == "__main__":
  print("***** test_PACKET_DUoperations() start")
  retVal = test_PACKET_DUoperations()
  print("***** test_PACKET_DUoperations() done:", retVal)
