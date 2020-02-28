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
# Space Segment - Unit Tests                                                  *
#******************************************************************************
import unittest
import testData
import CCSDS.PACKET
import SPACE.IF, SPACE.TMGEN
import SUPP.DEF, SUPP.IF
import UTIL.SYS

#############
# functions #
#############
def initConfiguration():
  """initialise the system configuration"""
  UTIL.SYS.s_configuration.setDefaults([
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
  ["TC_PARAM_LENGTH_BYTES", "2"],
  ["TC_TT_TIME_FORMAT", "CUC4"],
  ["TC_TT_TIME_BYTE_OFFSET", "11"],
  ["TC_TT_PKT_BYTE_OFFSET", "17"],
  ["TM_CYCLIC_MNEMO", "TM_PKT1"],
  ["TM_CYCLIC_PERIOD_MS", "5000"],
  ["TM_PARAM_LENGTH_BYTES", "2"],
  ["TM_PKT_SIZE_ADD", "0"],
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
  ["SYS_APP_VERSION", "1.0"]])

#############
# test case #
#############
class TestSPACE(unittest.TestCase):
  # ---------------------------------------------------------------------------
  @classmethod
  def setUpClass(cls):
    """setup the environment"""
    global s_assembler, s_packetizer
    # initialise the system configuration
    initConfiguration()
    SUPP.DEF.init()
    SUPP.IF.s_definitions.createDefinitions()
    SPACE.TMGEN.init()
  # ---------------------------------------------------------------------------
  def test_DEFoperations(self):
    """function to test the DEF definition module"""
    tmPktDefs = SUPP.IF.s_definitions.getTMpktDefs()
    self.assertEqual(tmPktDefs[0].pktSPID, 10001)
    self.assertEqual(tmPktDefs[1].pktSPID, 10002)
    self.assertEqual(tmPktDefs[2].pktSPID, 10003)
    self.assertEqual(tmPktDefs[3].pktSPID, 10004)
    self.assertEqual(tmPktDefs[4].pktSPID, 10005)
    self.assertEqual(tmPktDefs[5].pktSPID, 10006)
    self.assertEqual(tmPktDefs[6].pktSPID, 10007)
    self.assertEqual(tmPktDefs[7].pktSPID, 10008)
    self.assertEqual(tmPktDefs[8].pktSPID, 12343)
    self.assertEqual(tmPktDefs[9].pktSPID, 12345)
    tmParamDefs = SUPP.IF.s_definitions.getTMparamDefs()
    self.assertEqual(tmParamDefs[0].paramName, "PAR1")
    self.assertEqual(tmParamDefs[1].paramName, "PAR10")
    self.assertEqual(tmParamDefs[2].paramName, "PAR11")
    self.assertEqual(tmParamDefs[3].paramName, "PAR12")
    self.assertEqual(tmParamDefs[4].paramName, "PAR13")
    self.assertEqual(tmParamDefs[5].paramName, "PAR14")
    self.assertEqual(tmParamDefs[6].paramName, "PAR15")
    self.assertEqual(tmParamDefs[7].paramName, "PAR2")
    self.assertEqual(tmParamDefs[8].paramName, "PAR3")
    self.assertEqual(tmParamDefs[9].paramName, "PAR4")
    self.assertEqual(tmParamDefs[10].paramName, "PAR5")
    self.assertEqual(tmParamDefs[11].paramName, "PAR6")
    self.assertEqual(tmParamDefs[12].paramName, "PAR7")
    self.assertEqual(tmParamDefs[13].paramName, "PAR8")
    self.assertEqual(tmParamDefs[14].paramName, "PAR9")
    self.assertEqual(tmParamDefs[15].paramName, "TC_ID")
    self.assertEqual(tmParamDefs[16].paramName, "TC_SSC")
  # ---------------------------------------------------------------------------
  def test_TMGENoperations(self):
    """function to test the TMGEN telemetry generator"""
    # create TM packet without TM parameters
    tmPacket = SPACE.IF.s_tmPacketGenerator.getTMpacket(
      spid=testData.TM_PACKET_03_SPID,
      parameterValues=[],
      tmStruct=None,
      dataField=None,
      segmentationFlags=CCSDS.PACKET.UNSEGMENTED,
      obtUTC=0.0,
      reuse=True)
    self.assertEqual(tmPacket.getDumpString(), "\n" + \
      "0000 0C D2 C0 00 00 26 10 03 19 00 00 00 00 00 00 00 .....&..........\n" + \
      "0010 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................\n" + \
      "0020 00 00 00 00 00 00 00 00 00 00 00 A9 07          .............")
    self.assertEqual(tmPacket.versionNumber,
                     testData.TM_PACKET_03_versionNumber)
    self.assertEqual(tmPacket.packetType,
                     testData.TM_PACKET_03_packetType)
    self.assertEqual(tmPacket.dataFieldHeaderFlag,
                     testData.TM_PACKET_03_dataFieldHeaderFlag)
    self.assertEqual(tmPacket.applicationProcessId,
                     testData.TM_PACKET_03_applicationProcessId)
    self.assertEqual(tmPacket.segmentationFlags,
                     testData.TM_PACKET_03_segmentationFlags)
    self.assertEqual(tmPacket.sequenceControlCount,
                     testData.TM_PACKET_03_sequenceControlCount)
    self.assertEqual(tmPacket.packetLength,
                     testData.TM_PACKET_03_packetLength)
    self.assertEqual(tmPacket.pusVersionNumber,
                     testData.TM_PACKET_03_pusVersionNumber)
    self.assertEqual(tmPacket.serviceType,
                     testData.TM_PACKET_03_serviceType)
    self.assertEqual(tmPacket.serviceSubType,
                     testData.TM_PACKET_03_serviceSubType)
    self.assertTrue(tmPacket.checkPacketLength())
    self.assertTrue(tmPacket.checkChecksum())
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
      tmStruct=None,
      dataField=None,
      segmentationFlags=CCSDS.PACKET.UNSEGMENTED,
      obtUTC=0.0,
      reuse=True)
    self.assertEqual(tmPacket.getDumpString(), "\n" + \
      "0000 0C D2 C0 01 00 26 10 03 19 00 00 00 00 00 00 00 .....&..........\n" + \
      "0010 00 00 AA 12 34 56 78 00 00 00 00 00 00 00 00 41 ....4Vx........A\n" + \
      "0020 20 00 00 40 24 00 00 00 00 00 00 BC 77           ..@$.......w")

########
# main #
########
if __name__ == "__main__":
  unittest.main()
