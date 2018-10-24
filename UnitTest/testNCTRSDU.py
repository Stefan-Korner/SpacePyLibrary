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
# Generic Data Processor - Unit Tests                                         *
#******************************************************************************
import GRND.NCTRSDU, testData

#############
# functions #
#############
def test_NCTRS_DUoperations():
  """function to test the NCTRS data units"""
  tmDu1a = GRND.NCTRSDU.TMdataUnit(testData.NCTRS_TM_FRAME_01)
  if tmDu1a.packetSize != testData.NCTRS_TM_FRAME_01_packetSize:
    print "tmDu1a packetSize wrong:", tmDu1a.packetSize, "- should be", testData.NCTRS_TM_FRAME_01_packetSize
    return False
  if tmDu1a.spacecraftId != testData.NCTRS_TM_FRAME_01_spacecraftId:
    print "tmDu1a spacecraftId wrong:", tmDu1a.spacecraftId, "- should be", testData.NCTRS_TM_FRAME_01_spacecraftId
    return False
  if tmDu1a.dataStreamType != testData.NCTRS_TM_FRAME_01_dataStreamType:
    print "tmDu1a dataStreamType wrong:", tmDu1a.dataStreamType, "- should be", testData.NCTRS_TM_FRAME_01_dataStreamType
    return False
  if tmDu1a.virtualChannelId != testData.NCTRS_TM_FRAME_01_virtualChannelId:
    print "tmDu1a virtualChannelId wrong:", tmDu1a.virtualChannelId, "- should be", testData.NCTRS_TM_FRAME_01_virtualChannelId
    return False
  if tmDu1a.routeId != testData.NCTRS_TM_FRAME_01_routeId:
    print "tmDu1a routeId wrong:", tmDu1a.routeId, "- should be", testData.NCTRS_TM_FRAME_01_routeId
    return False
  if tmDu1a.earthReceptionTime != testData.NCTRS_TM_FRAME_01_earthReceptionTime:
    print "tmDu1a earthReceptionTime wrong:", tmDu1a.earthReceptionTime, "- should be", testData.NCTRS_TM_FRAME_01_earthReceptionTime
    return False
  if tmDu1a.sequenceFlag != testData.NCTRS_TM_FRAME_01_sequenceFlag:
    print "tmDu1a sequenceFlag wrong:", tmDu1a.sequenceFlag, "- should be", testData.NCTRS_TM_FRAME_01_sequenceFlag
    return False
  if tmDu1a.qualityFlag != testData.NCTRS_TM_FRAME_01_qualityFlag:
    print "tmDu1a qualityFlag wrong:", tmDu1a.qualityFlag, "- should be", testData.NCTRS_TM_FRAME_01_qualityFlag
    return False
  tmDu1b = GRND.NCTRSDU.TMdataUnit()
  tmDu1b.setFrame(testData.TM_FRAME_01)
  tmDu1b.spacecraftId = testData.NCTRS_TM_FRAME_01_spacecraftId
  tmDu1b.dataStreamType = testData.NCTRS_TM_FRAME_01_dataStreamType
  tmDu1b.virtualChannelId = testData.NCTRS_TM_FRAME_01_virtualChannelId
  tmDu1b.routeId = testData.NCTRS_TM_FRAME_01_routeId
  tmDu1b.earthReceptionTime = testData.NCTRS_TM_FRAME_01_earthReceptionTime
  tmDu1b.sequenceFlag = testData.NCTRS_TM_FRAME_01_sequenceFlag
  tmDu1b.qualityFlag = testData.NCTRS_TM_FRAME_01_qualityFlag
  if tmDu1a != tmDu1b:
    print "tmDu1a and tmDu1b differ."
    print "tmDu1a =", tmDu1a
    print "tmDu1b =", tmDu1b
    return False
  tcDu = GRND.NCTRSDU.TCdataUnit()
  print "tcDu =", tcDu
  tcPktDu = GRND.NCTRSDU.TCpacketDataUnit()
  print "tcPktDu =", tcPktDu
  tcCltuDu1a = GRND.NCTRSDU.TCcltuDataUnit(testData.NCTRS_CLTU_01)
  if tcCltuDu1a.packetSize != testData.NCTRS_CLTU_01_packetSize:
    print "tcCltuDu1a packetSize wrong:", tcCltuDu1a.packetSize, "- should be", testData.NCTRS_CLTU_01_packetSize
    return False
  if tcCltuDu1a.spacecraftId != testData.NCTRS_CLTU_01_spacecraftId:
    print "tcCltuDu1a spacecraftId wrong:", tcCltuDu1a.spacecraftId, "- should be", testData.NCTRS_CLTU_01_spacecraftId
    return False
  if tcCltuDu1a.dataUnitType != testData.NCTRS_CLTU_01_dataUnitType:
    print "tcCltuDu1a dataUnitType wrong:", tcCltuDu1a.dataUnitType, "- should be", testData.NCTRS_CLTU_01_dataUnitType
    return False
  if tcCltuDu1a.delay != testData.NCTRS_CLTU_01_delay:
    print "tcCltuDu1a delay wrong:", tcCltuDu1a.delay, "- should be", testData.NCTRS_CLTU_01_delay
    return False
  if tcCltuDu1a.latestProdTime != testData.NCTRS_CLTU_01_latestProdTime:
    print "tcCltuDu1a latestProdTime wrong:", tcCltuDu1a.latestProdTime, "- should be", testData.NCTRS_CLTU_01_latestProdTime
    return False
  if tcCltuDu1a.serviceType != testData.NCTRS_CLTU_01_serviceType:
    print "tcCltuDu1a serviceType wrong:", tcCltuDu1a.serviceType, "- should be", testData.NCTRS_CLTU_01_serviceType
    return False
  if tcCltuDu1a.earliestProdTime != testData.NCTRS_CLTU_01_earliestProdTime:
    print "tcCltuDu1a earliestProdTime wrong:", tcCltuDu1a.earliestProdTime, "- should be", testData.NCTRS_CLTU_01_earliestProdTime
    return False
  if tcCltuDu1a.virtualChannelId != testData.NCTRS_CLTU_01_virtualChannelId:
    print "tcCltuDu1a virtualChannelId wrong:", tcCltuDu1a.virtualChannelId, "- should be", testData.NCTRS_CLTU_01_virtualChannelId
    return False
  if tcCltuDu1a.mapId != testData.NCTRS_CLTU_01_mapId:
    print "tcCltuDu1a mapId wrong:", tcCltuDu1a.mapId, "- should be", testData.NCTRS_CLTU_01_mapId
    return False
  if tcCltuDu1a.aggregationFlag != testData.NCTRS_CLTU_01_aggregationFlag:
    print "tcCltuDu1a aggregationFlag wrong:", tcCltuDu1a.aggregationFlag, "- should be", testData.NCTRS_CLTU_01_aggregationFlag
    return False
  if tcCltuDu1a.tcId != testData.NCTRS_CLTU_01_tcId:
    print "tcCltuDu1a tcId wrong:", tcCltuDu1a.tcId, "- should be", testData.NCTRS_CLTU_01_tcId
    return False
  if tcCltuDu1a.earliestProdTimeFlag != testData.NCTRS_CLTU_01_earliestProdTimeFlag:
    print "tcCltuDu1a earliestProdTimeFlag wrong:", tcCltuDu1a.earliestProdTimeFlag, "- should be", testData.NCTRS_CLTU_01_earliestProdTimeFlag
    return False
  if tcCltuDu1a.latestProdTimeFlag != testData.NCTRS_CLTU_01_latestProdTimeFlag:
    print "tcCltuDu1a latestProdTimeFlag wrong:", tcCltuDu1a.latestProdTimeFlag, "- should be", testData.NCTRS_CLTU_01_latestProdTimeFlag
    return False
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
  if tcCltuDu1a != tcCltuDu1b:
    print "tcCltuDu1a and tcCltuDu1b differ."
    print "tcCltuDu1a =", tcCltuDu1a
    print "tcCltuDu1b =", tcCltuDu1b
    return False
  tcCltuDu2a = GRND.NCTRSDU.TCcltuDataUnit(testData.NCTRS_CLTU_02)
  if tcCltuDu2a.packetSize != testData.NCTRS_CLTU_02_packetSize:
    print "tcCltuDu2a packetSize wrong:", tcCltuDu2a.packetSize, "- should be", testData.NCTRS_CLTU_02_packetSize
    return False
  if tcCltuDu2a.spacecraftId != testData.NCTRS_CLTU_02_spacecraftId:
    print "tcCltuDu2a spacecraftId wrong:", tcCltuDu2a.spacecraftId, "- should be", testData.NCTRS_CLTU_02_spacecraftId
    return False
  if tcCltuDu2a.dataUnitType != testData.NCTRS_CLTU_02_dataUnitType:
    print "tcCltuDu2a dataUnitType wrong:", tcCltuDu2a.dataUnitType, "- should be", testData.NCTRS_CLTU_02_dataUnitType
    return False
  if tcCltuDu2a.delay != testData.NCTRS_CLTU_02_delay:
    print "tcCltuDu2a delay wrong:", tcCltuDu2a.delay, "- should be", testData.NCTRS_CLTU_02_delay
    return False
  if tcCltuDu2a.latestProdTime != testData.NCTRS_CLTU_02_latestProdTime:
    print "tcCltuDu2a latestProdTime wrong:", tcCltuDu2a.latestProdTime, "- should be", testData.NCTRS_CLTU_02_latestProdTime
    return False
  if tcCltuDu2a.serviceType != testData.NCTRS_CLTU_02_serviceType:
    print "tcCltuDu2a serviceType wrong:", tcCltuDu2a.serviceType, "- should be", testData.NCTRS_CLTU_02_serviceType
    return False
  if tcCltuDu2a.earliestProdTime != testData.NCTRS_CLTU_02_earliestProdTime:
    print "tcCltuDu2a earliestProdTime wrong:", tcCltuDu2a.earliestProdTime, "- should be", testData.NCTRS_CLTU_02_earliestProdTime
    return False
  if tcCltuDu2a.virtualChannelId != testData.NCTRS_CLTU_02_virtualChannelId:
    print "tcCltuDu2a virtualChannelId wrong:", tcCltuDu2a.virtualChannelId, "- should be", testData.NCTRS_CLTU_02_virtualChannelId
    return False
  if tcCltuDu2a.mapId != testData.NCTRS_CLTU_02_mapId:
    print "tcCltuDu2a mapId wrong:", tcCltuDu2a.mapId, "- should be", testData.NCTRS_CLTU_02_mapId
    return False
  if tcCltuDu2a.aggregationFlag != testData.NCTRS_CLTU_02_aggregationFlag:
    print "tcCltuDu2a aggregationFlag wrong:", tcCltuDu2a.aggregationFlag, "- should be", testData.NCTRS_CLTU_02_aggregationFlag
    return False
  if tcCltuDu2a.tcId != testData.NCTRS_CLTU_02_tcId:
    print "tcCltuDu2a tcId wrong:", tcCltuDu2a.tcId, "- should be", testData.NCTRS_CLTU_02_tcId
    return False
  if tcCltuDu2a.earliestProdTimeFlag != testData.NCTRS_CLTU_02_earliestProdTimeFlag:
    print "tcCltuDu2a earliestProdTimeFlag wrong:", tcCltuDu2a.earliestProdTimeFlag, "- should be", testData.NCTRS_CLTU_02_earliestProdTimeFlag
    return False
  if tcCltuDu2a.latestProdTimeFlag != testData.NCTRS_CLTU_02_latestProdTimeFlag:
    print "tcCltuDu2a latestProdTimeFlag wrong:", tcCltuDu2a.latestProdTimeFlag, "- should be", testData.NCTRS_CLTU_02_latestProdTimeFlag
    return False
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
  if tcCltuDu2a != tcCltuDu2b:
    print "tcCltuDu2a and tcCltu2Du1b differ."
    print "tcCltuDu2a =", tcCltuDu2a
    print "tcCltuDu2b =", tcCltuDu2b
    return False
  tcDirDu = GRND.NCTRSDU.TCdirectivesDataUnit()
  print "tcDirDu =", tcDirDu
  return True

########
# main #
########
if __name__ == "__main__":
  print "***** test_NCTRS_DUoperations() start"
  retVal = test_NCTRS_DUoperations()
  print "***** test_NCTRS_DUoperations() done:", retVal
