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
# Generic Data Processor - Unit Tests                                         *
#******************************************************************************
import unittest
import GRND.NCTRSDU, testData

#############
# test case #
#############
class TestNCTRSDU(unittest.TestCase):
  def test(self):
    """test the NCTRS data units"""
    tmDu1a = GRND.NCTRSDU.TMdataUnitV0(testData.NCTRS_TM_FRAME_01)
    self.assertEqual(tmDu1a.packetSize,
                     testData.NCTRS_TM_FRAME_01_packetSize)
    self.assertEqual(tmDu1a.spacecraftId,
                     testData.NCTRS_TM_FRAME_01_spacecraftId)
    self.assertEqual(tmDu1a.dataStreamType,
                     testData.NCTRS_TM_FRAME_01_dataStreamType)
    self.assertEqual(tmDu1a.virtualChannelId,
                     testData.NCTRS_TM_FRAME_01_virtualChannelId)
    self.assertEqual(tmDu1a.routeId,
                     testData.NCTRS_TM_FRAME_01_routeId)
    self.assertEqual(tmDu1a.earthReceptionTime,
                     testData.NCTRS_TM_FRAME_01_earthReceptionTime)
    self.assertEqual(tmDu1a.sequenceFlag,
                     testData.NCTRS_TM_FRAME_01_sequenceFlag)
    self.assertEqual(tmDu1a.qualityFlag,
                     testData.NCTRS_TM_FRAME_01_qualityFlag)
    tmDu1b = GRND.NCTRSDU.TMdataUnitV0()
    tmDu1b.setFrame(testData.TM_FRAME_01)
    tmDu1b.spacecraftId = testData.NCTRS_TM_FRAME_01_spacecraftId
    tmDu1b.dataStreamType = testData.NCTRS_TM_FRAME_01_dataStreamType
    tmDu1b.virtualChannelId = testData.NCTRS_TM_FRAME_01_virtualChannelId
    tmDu1b.routeId = testData.NCTRS_TM_FRAME_01_routeId
    tmDu1b.earthReceptionTime = testData.NCTRS_TM_FRAME_01_earthReceptionTime
    tmDu1b.sequenceFlag = testData.NCTRS_TM_FRAME_01_sequenceFlag
    tmDu1b.qualityFlag = testData.NCTRS_TM_FRAME_01_qualityFlag
    self.assertEqual(tmDu1a, tmDu1b)
    tcDu = GRND.NCTRSDU.TCdataUnit()
    self.assertEqual(tcDu.packetSize,
                     GRND.NCTRSDU.TC_DU_HEADER_BYTE_SIZE)
    self.assertEqual(tcDu.dataUnitType, 0)
    self.assertEqual(tcDu.spacecraftId, 0)
    tcPktDu = GRND.NCTRSDU.TCpacketDataUnit()
    self.assertEqual(tcPktDu.packetSize,
                     GRND.NCTRSDU.TC_DU_HEADER_BYTE_SIZE +
                     GRND.NCTRSDU.TC_PACKET_HEADER_BYTE_SIZE)
    self.assertEqual(tcPktDu.dataUnitType,
                     GRND.NCTRSDU.TC_PACKET_HEADER_DU_TYPE)
    self.assertEqual(tcPktDu.spacecraftId, 0)
    self.assertEqual(tcPktDu.serviceType, 0)
    self.assertEqual(tcPktDu.tcId, 0)
    self.assertEqual(tcPktDu.virtualChannelId, 0)
    self.assertEqual(tcPktDu.mapId, 0)
    tcCltuDu1a = GRND.NCTRSDU.TCcltuDataUnit(testData.NCTRS_CLTU_01)
    self.assertEqual(tcCltuDu1a.packetSize,
                     testData.NCTRS_CLTU_01_packetSize)
    self.assertEqual(tcCltuDu1a.spacecraftId,
                     testData.NCTRS_CLTU_01_spacecraftId)
    self.assertEqual(tcCltuDu1a.dataUnitType,
                     testData.NCTRS_CLTU_01_dataUnitType)
    self.assertEqual(tcCltuDu1a.delay,
                     testData.NCTRS_CLTU_01_delay)
    self.assertEqual(tcCltuDu1a.latestProdTime,
                     testData.NCTRS_CLTU_01_latestProdTime)
    self.assertEqual(tcCltuDu1a.serviceType,
                     testData.NCTRS_CLTU_01_serviceType)
    self.assertEqual(tcCltuDu1a.earliestProdTime,
                     testData.NCTRS_CLTU_01_earliestProdTime)
    self.assertEqual(tcCltuDu1a.virtualChannelId,
                     testData.NCTRS_CLTU_01_virtualChannelId)
    self.assertEqual(tcCltuDu1a.mapId,
                     testData.NCTRS_CLTU_01_mapId)
    self.assertEqual(tcCltuDu1a.aggregationFlag,
                     testData.NCTRS_CLTU_01_aggregationFlag)
    self.assertEqual(tcCltuDu1a.tcId,
                     testData.NCTRS_CLTU_01_tcId)
    self.assertEqual(tcCltuDu1a.earliestProdTimeFlag,
                     testData.NCTRS_CLTU_01_earliestProdTimeFlag)
    self.assertEqual(tcCltuDu1a.latestProdTimeFlag,
                     testData.NCTRS_CLTU_01_latestProdTimeFlag)
    tcCltuDu1b = GRND.NCTRSDU.TCcltuDataUnit()
    tcCltuDu1b.setCltu(testData.CLTU_01)
    tcCltuDu1b.spacecraftId = testData.NCTRS_CLTU_01_spacecraftId
    tcCltuDu1b.delay = testData.NCTRS_CLTU_01_delay
    tcCltuDu1b.latestProdTime = testData.NCTRS_CLTU_01_latestProdTime
    tcCltuDu1b.serviceType = testData.NCTRS_CLTU_01_serviceType
    tcCltuDu1b.earliestProdTime = testData.NCTRS_CLTU_01_earliestProdTime
    tcCltuDu1b.virtualChannelId = testData.NCTRS_CLTU_01_virtualChannelId
    tcCltuDu1b.mapId = testData.NCTRS_CLTU_01_mapId
    tcCltuDu1b.aggregationFlag = testData.NCTRS_CLTU_01_aggregationFlag
    tcCltuDu1b.tcId = testData.NCTRS_CLTU_01_tcId
    tcCltuDu1b.earliestProdTimeFlag = testData.NCTRS_CLTU_01_earliestProdTimeFlag
    tcCltuDu1b.latestProdTimeFlag = testData.NCTRS_CLTU_01_latestProdTimeFlag
    self.assertEqual(tcCltuDu1a, tcCltuDu1b)
    tcCltuDu2a = GRND.NCTRSDU.TCcltuDataUnit(testData.NCTRS_CLTU_02)
    self.assertEqual(tcCltuDu2a.packetSize,
                     testData.NCTRS_CLTU_02_packetSize)
    self.assertEqual(tcCltuDu2a.spacecraftId,
                     testData.NCTRS_CLTU_02_spacecraftId)
    self.assertEqual(tcCltuDu2a.dataUnitType,
                     testData.NCTRS_CLTU_02_dataUnitType)
    self.assertEqual(tcCltuDu2a.delay,
                     testData.NCTRS_CLTU_02_delay)
    self.assertEqual(tcCltuDu2a.latestProdTime,
                     testData.NCTRS_CLTU_02_latestProdTime)
    self.assertEqual(tcCltuDu2a.serviceType,
                     testData.NCTRS_CLTU_02_serviceType)
    self.assertEqual(tcCltuDu2a.earliestProdTime,
                     testData.NCTRS_CLTU_02_earliestProdTime)
    self.assertEqual(tcCltuDu2a.virtualChannelId,
                     testData.NCTRS_CLTU_02_virtualChannelId)
    self.assertEqual(tcCltuDu2a.mapId,
                     testData.NCTRS_CLTU_02_mapId)
    self.assertEqual(tcCltuDu2a.aggregationFlag,
                     testData.NCTRS_CLTU_02_aggregationFlag)
    self.assertEqual(tcCltuDu2a.tcId,
                     testData.NCTRS_CLTU_02_tcId)
    self.assertEqual(tcCltuDu2a.earliestProdTimeFlag,
                     testData.NCTRS_CLTU_02_earliestProdTimeFlag)
    self.assertEqual(tcCltuDu2a.latestProdTimeFlag,
                     testData.NCTRS_CLTU_02_latestProdTimeFlag)
    tcCltuDu2b = GRND.NCTRSDU.TCcltuDataUnit()
    tcCltuDu2b.setCltu(testData.CLTU_02)
    tcCltuDu2b.spacecraftId = testData.NCTRS_CLTU_02_spacecraftId
    tcCltuDu2b.delay = testData.NCTRS_CLTU_02_delay
    tcCltuDu2b.latestProdTime = testData.NCTRS_CLTU_02_latestProdTime
    tcCltuDu2b.serviceType = testData.NCTRS_CLTU_02_serviceType
    tcCltuDu2b.earliestProdTime = testData.NCTRS_CLTU_02_earliestProdTime
    tcCltuDu2b.virtualChannelId = testData.NCTRS_CLTU_02_virtualChannelId
    tcCltuDu2b.mapId = testData.NCTRS_CLTU_02_mapId
    tcCltuDu2b.aggregationFlag = testData.NCTRS_CLTU_02_aggregationFlag
    tcCltuDu2b.tcId = testData.NCTRS_CLTU_02_tcId
    tcCltuDu2b.earliestProdTimeFlag = testData.NCTRS_CLTU_02_earliestProdTimeFlag
    tcCltuDu2b.latestProdTimeFlag = testData.NCTRS_CLTU_02_latestProdTimeFlag
    self.assertEqual(tcCltuDu2a, tcCltuDu2b)
    tcDirDu = GRND.NCTRSDU.TCdirectivesDataUnit()
    self.assertEqual(tcDirDu.packetSize,
                     GRND.NCTRSDU.TC_DU_HEADER_BYTE_SIZE +
                     GRND.NCTRSDU.TC_DIRECTIVES_BYTE_SIZE)
    self.assertEqual(tcDirDu.dataUnitType,
                     GRND.NCTRSDU.TC_DIRECTIVES_DU_TYPE)
    self.assertEqual(tcDirDu.spacecraftId, 0)
    self.assertEqual(tcDirDu.directiveType, 0)
    self.assertEqual(tcDirDu.directiveId, 0)
    self.assertEqual(tcDirDu.virtualChannelId, 0)
    self.assertEqual(tcDirDu.parameter, 0)
    return True

########
# main #
########
if __name__ == "__main__":
  unittest.main()
