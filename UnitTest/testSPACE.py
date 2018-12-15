#!/usr/bin/env python3
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
# Space Segment - Unit Tests                                                  *
#******************************************************************************
import testData
import CCSDS.PACKET
import SPACE.DEF, SPACE.TMGEN
import UTIL.SYS

#############
# constants #
#############
SYS_CONFIGURATION = [
  ["HOST", "127.0.0.1"],
  ["NCTRS_ADMIN_SERVER_PORT", "13006"],
  ["NCTRS_TC_SERVER_PORT", "13007"],
  ["NCTRS_TM_SERVER_PORT", "2502"],
  ["SPACECRAFT_ID", "758"],
  ["DEF_GROUND_STATION_ID", "10"],
  ["GROUND_STATION_NAME", "ESA G/S "],
  ["TC_ACK_ACCEPT_SUCC_MNEMO", "ACK1"],
  ["TC_ACK_ACCEPT_FAIL_MNEMO", "NAK1"],
  ["TC_ACK_EXESTA_SUCC_MNEMO", "ACK2"],
  ["TC_ACK_EXESTA_FAIL_MNEMO", "NAK2"],
  ["TC_ACK_EXEPRO_SUCC_MNEMO", "ACK3"],
  ["TC_ACK_EXEPRO_FAIL_MNEMO", "NAK3"],
  ["TC_ACK_EXECUT_SUCC_MNEMO", "ACK4"],
  ["TC_ACK_EXECUT_FAIL_MNEMO", "NAK4"],
  ["TC_ACK_APID_PARAM_BYTE_OFFSET", "18"],
  ["TC_ACK_SSC_PARAM_BYTE_OFFSET", "20"],
  ["TC_TT_TIME_FORMAT", "CUC4"],
  ["TC_TT_TIME_BYTE_OFFSET", "11"],
  ["TC_TT_PKT_BYTE_OFFSET", "17"],
  ["TM_CYCLIC_MNEMO", "TM_PKT1"],
  ["TM_CYCLIC_PERIOD_MS", "5000"],
  ["TM_TT_TIME_FORMAT", "CUC4"],
  ["TM_TT_TIME_BYTE_OFFSET", "10"],
  ["TM_RECORD_FORMAT", "NCTRS"],
  ["TM_REPLAY_KEY", "SPID"],
  ["OBT_MISSION_EPOCH_STR", UTIL.TCO.UNIX_MISSION_EPOCH_STR],
  ["OBT_LEAP_SECONDS", "0"],
  ["ERT_MISSION_EPOCH_STR", UTIL.TCO.UNIX_MISSION_EPOCH_STR],
  ["ERT_LEAP_SECONDS", "0"],
  ["SYS_COLOR_LOG", "1"],
  ["SYS_APP_MNEMO", "SIM"],
  ["SYS_APP_NAME", "Simulator"],
  ["SYS_APP_VERSION", "1.0"]]

#############
# functions #
#############
# -----------------------------------------------------------------------------
def test_DEFoperations():
  """function to test the DEF definition module"""
  SPACE.DEF.init()
  print("----- TM packet definitions -----")
  tmPktDefs = SPACE.IF.s_definitions.getTMpktDefs()
  for tmPktDef in tmPktDefs:
    print(tmPktDef.pktSPID, end=' ')
  print("")
  print("----- TM parameter definitions -----")
  tmParamDefs = SPACE.IF.s_definitions.getTMparamDefs()
  for tmParamDef in tmParamDefs:
    print(tmParamDef.paramName, end=' ')
  print("")
  # force a re-creation of the persistent definitions
  # (for the next test run)
  SPACE.IF.s_definitions.createDefinitions()
  return True
# -----------------------------------------------------------------------------
def test_TMGENoperations():
  """function to test the TMGEN telemetry generator"""
  SPACE.TMGEN.init()
  # create TM packet without TM parameters
  tmPacket = SPACE.IF.s_tmPacketGenerator.getTMpacket(
    spid=testData.TM_PACKET_03_SPID,
    parameterValues=[],
    dataField=None,
    segmentationFlags=CCSDS.PACKET.UNSEGMENTED,
    obtUTC=0.0,
    reuse=True)
  print("tmPacket =", tmPacket)
  if tmPacket.getDumpString() != "\n" + \
    "0000 0C D2 C0 00 00 26 10 03 19 00 00 00 00 00 00 00 .....&..........\n" + \
    "0010 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................\n" + \
    "0020 00 00 00 00 00 00 00 00 00 00 00 A9 07          .............":
    print("unexpected TM packet encoding")
    return False
  if tmPacket.versionNumber != testData.TM_PACKET_03_versionNumber:
    print("tmPacket versionNumber wrong:", tmPacket.versionNumber, "- should be", testData.TM_PACKET_03_versionNumber)
    return False
  if tmPacket.packetType != testData.TM_PACKET_03_packetType:
    print("tmPacket packetType wrong:", tmPacket.packetType, "- should be", testData.TM_PACKET_03_packetType)
    return False
  if tmPacket.dataFieldHeaderFlag != testData.TM_PACKET_03_dataFieldHeaderFlag:
    print("tmPacket dataFieldHeaderFlag wrong:", tmPacket.dataFieldHeaderFlag, "- should be", testData.TM_PACKET_03_dataFieldHeaderFlag)
    return False
  if tmPacket.applicationProcessId != testData.TM_PACKET_03_applicationProcessId:
    print("tmPacket applicationProcessId wrong:", tmPacket.applicationProcessId, "- should be", testData.TM_PACKET_03_applicationProcessId)
    return False
  if tmPacket.segmentationFlags != testData.TM_PACKET_03_segmentationFlags:
    print("tmPacket segmentationFlags wrong:", tmPacket.segmentationFlags, "- should be", testData.TM_PACKET_03_segmentationFlags)
    return False
  if tmPacket.sequenceControlCount != testData.TM_PACKET_03_sequenceControlCount:
    print("tmPacket sequenceControlCount wrong:", tmPacket.sequenceControlCount, "- should be", testData.TM_PACKET_03_sequenceControlCount)
    return False
  if tmPacket.packetLength != testData.TM_PACKET_03_packetLength:
    print("tmPacket packetLength wrong:", tmPacket.packetLength, "- should be", testData.TM_PACKET_03_packetLength)
    return False
  if tmPacket.pusVersionNumber != testData.TM_PACKET_03_pusVersionNumber:
    print("tmPacket pusVersionNumber wrong:", tmPacket.pusVersionNumber, "- should be", testData.TM_PACKET_03_pusVersionNumber)
    return False
  if tmPacket.serviceType != testData.TM_PACKET_03_serviceType:
    print("tmPacket serviceType wrong:", tmPacket.serviceType, "- should be", testData.TM_PACKET_03_serviceType)
    return False
  if tmPacket.serviceSubType != testData.TM_PACKET_03_serviceSubType:
    print("tmPacket serviceSubType wrong:", tmPacket.serviceSubType, "- should be", testData.TM_PACKET_03_serviceSubType)
    return False
  if not tmPacket.checkPacketLength():
    print("tmPacket has inconsistent packetLength")
    return False
  if not tmPacket.checkChecksum():
    print("tmPacket has invalid checksum")
    return False
  # create TM packet with initialized TM parameters
  parameterValuesList = []
  parameterValuesList.append(["PAR1", 1])
  parameterValuesList.append(["PAR3", 1])
  parameterValuesList.append(["PAR5", 1])
  parameterValuesList.append(["PAR7", 1])
  parameterValuesList.append(["PAR9", 0x12345678])
  parameterValuesList.append(["PAR11", 10.0])
  parameterValuesList.append(["PAR12", 10.0])
  tmPacket = SPACE.IF.s_tmPacketGenerator.getTMpacket(
    spid=testData.TM_PACKET_03_SPID,
    parameterValues=parameterValuesList,
    dataField=None,
    segmentationFlags=CCSDS.PACKET.UNSEGMENTED,
    obtUTC=0.0,
    reuse=True)
  print("tmPacket =", tmPacket)
  if tmPacket.getDumpString() != "\n" + \
    "0000 0C D2 C0 01 00 26 10 03 19 00 00 00 00 00 00 00 .....&..........\n" + \
    "0010 00 00 AA 12 34 56 78 00 00 00 00 00 00 00 00 41 ....4Vx........A\n" + \
    "0020 20 00 00 40 24 00 00 00 00 00 00 BC 77           ..@$.......w":
    print("unexpected TM packet encoding")
    return False
  return True

########
# main #
########
if __name__ == "__main__":
  # initialise the system configuration
  UTIL.SYS.s_configuration.setDefaults(SYS_CONFIGURATION)
  print("***** test_DEFoperations() start")
  retVal = test_DEFoperations()
  print("***** test_DEFoperations() done:", retVal)
  print("***** test_TMGENoperations() start")
  retVal = test_TMGENoperations()
  print("***** test_TMGENoperations() done:", retVal)
