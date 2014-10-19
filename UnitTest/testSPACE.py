#!/usr/bin/env python
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
# Space Segment - Unit Tests                                                  *
#******************************************************************************
import testData
import SCOS.ENV
import SPACE.DEF, SPACE.TMGEN

#############
# functions #
#############
# -----------------------------------------------------------------------------
def test_DEFoperations():
  """function to test the DEF definition module"""
  SPACE.DEF.init()
  print "----- TM packet definitions -----"
  tmPktDefs = SPACE.IF.s_definitions.getTMpktDefs()
  for tmPktDef in tmPktDefs:
    print tmPktDef.pktSPID,
  print ""
  print "----- TM parameter definitions -----"
  tmParamDefs = SPACE.IF.s_definitions.getTMparamDefs()
  for tmParamDef in tmParamDefs:
    print tmParamDef.paramName,
  print ""
  # force a re-creation of the persistent definitions
  # (for the next test run)
  SPACE.IF.s_definitions.createDefinitions()
  return True
# -----------------------------------------------------------------------------
def test_TMGENoperations():
  """function to test the TMGEN telemetry generator"""
  SPACE.TMGEN.init()
  # TM_PACKET_02 has a checksum
  tmPacket = SPACE.IF.s_tmPacketGenerator.getTMpacket(SCOS.ENV.TPKT_PKT_IDLE_FRAME_SPID)
  if tmPacket.versionNumber != testData.TM_PACKET_02_versionNumber:
    print "tmPacket versionNumber wrong:", tmPacket.versionNumber, "- should be", testData.TM_PACKET_02_versionNumber
    return False
  if tmPacket.packetType != testData.TM_PACKET_02_packetType:
    print "tmPacket packetType wrong:", tmPacket.packetType, "- should be", testData.TM_PACKET_02_packetType
    return False
  if tmPacket.dataFieldHeaderFlag != testData.TM_PACKET_02_dataFieldHeaderFlag:
    print "tmPacket dataFieldHeaderFlag wrong:", tmPacket.dataFieldHeaderFlag, "- should be", testData.TM_PACKET_02_dataFieldHeaderFlag
    return False
  if tmPacket.applicationProcessId != testData.TM_PACKET_02_applicationProcessId:
    print "tmPacket applicationProcessId wrong:", tmPacket.applicationProcessId, "- should be", testData.TM_PACKET_02_applicationProcessId
    return False
  if tmPacket.segmentationFlags != testData.TM_PACKET_02_segmentationFlags:
    print "tmPacket segmentationFlags wrong:", tmPacket.segmentationFlags, "- should be", testData.TM_PACKET_02_segmentationFlags
    return False
  if tmPacket.sequenceControlCount != testData.TM_PACKET_02_sequenceControlCount:
    print "tmPacket sequenceControlCount wrong:", tmPacket.sequenceControlCount, "- should be", testData.TM_PACKET_02_sequenceControlCount
    return False
  if tmPacket.packetLength != testData.TM_PACKET_02_packetLength:
    print "tmPacket packetLength wrong:", tmPacket.packetLength, "- should be", testData.TM_PACKET_02_packetLength
    return False
  if tmPacket.pusVersionNumber != testData.TM_PACKET_02_pusVersionNumber:
    print "tmPacket pusVersionNumber wrong:", tmPacket.pusVersionNumber, "- should be", testData.TM_PACKET_02_pusVersionNumber
    return False
  if tmPacket.serviceType != testData.TM_PACKET_02_serviceType:
    print "tmPacket serviceType wrong:", tmPacket.serviceType, "- should be", testData.TM_PACKET_02_serviceType
    return False
  if tmPacket.serviceSubType != testData.TM_PACKET_02_serviceSubType:
    print "tmPacket serviceSubType wrong:", tmPacket.serviceSubType, "- should be", testData.TM_PACKET_02_serviceSubType
    return False
  if not tmPacket.checkPacketLength():
    print "tmPacket has inconsistent packetLength"
    return False
  if not tmPacket.checkChecksum():
    print "tmPacket has invalid checksum"
    return False
  return True

########
# main #
########
if __name__ == "__main__":
  print "***** test_DEFoperations() start"
  retVal = test_DEFoperations()
  print "***** test_DEFoperations() done:", retVal
  print "***** test_TMGENoperations() start"
  retVal = test_TMGENoperations()
  print "***** test_TMGENoperations() done:", retVal
