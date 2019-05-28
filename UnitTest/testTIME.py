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
# Unit Tests                                                                  *
#******************************************************************************
import unittest
import CCSDS.TIME
import UTIL.TCO, UTIL.TIME
import testData

###################
# helper function #
###################
def correlateOBTcucPFC17(byteArray):
  """convenience function for backward compatibility"""
  timeDU = CCSDS.TIME.createCUC(byteArray)
  pyTime = CCSDS.TIME.convertFromCUC(timeDU)
  return UTIL.TCO.correlateFromOBTmissionEpoch(pyTime)

#############
# test case #
#############
class TestTIME(unittest.TestCase):
  def test_TIMEoperations(self):
    """function to test the TIME operations"""
    # test CCSDS.TIME.isCDStimeFormat()
    self.assertTrue(CCSDS.TIME.isCDStimeFormat(CCSDS.TIME.TIME_FORMAT_CDS1))
    self.assertTrue(CCSDS.TIME.isCDStimeFormat(CCSDS.TIME.TIME_FORMAT_CDS2))
    self.assertTrue(CCSDS.TIME.isCDStimeFormat(CCSDS.TIME.TIME_FORMAT_CDS3))
    self.assertFalse(CCSDS.TIME.isCDStimeFormat(CCSDS.TIME.TIME_FORMAT_CUC0))
    self.assertFalse(CCSDS.TIME.isCDStimeFormat(CCSDS.TIME.TIME_FORMAT_CUC1))
    self.assertFalse(CCSDS.TIME.isCDStimeFormat(CCSDS.TIME.TIME_FORMAT_CUC2))
    self.assertFalse(CCSDS.TIME.isCDStimeFormat(CCSDS.TIME.TIME_FORMAT_CUC3))
    self.assertFalse(CCSDS.TIME.isCDStimeFormat(CCSDS.TIME.TIME_FORMAT_CUC4))
    self.assertFalse(CCSDS.TIME.isCDStimeFormat(99))
    # test CCSDS.TIME.isCUCtimeFormat()
    self.assertFalse(CCSDS.TIME.isCUCtimeFormat(CCSDS.TIME.TIME_FORMAT_CDS1))
    self.assertFalse(CCSDS.TIME.isCUCtimeFormat(CCSDS.TIME.TIME_FORMAT_CDS2))
    self.assertFalse(CCSDS.TIME.isCUCtimeFormat(CCSDS.TIME.TIME_FORMAT_CDS3))
    self.assertTrue(CCSDS.TIME.isCUCtimeFormat(CCSDS.TIME.TIME_FORMAT_CUC0))
    self.assertTrue(CCSDS.TIME.isCUCtimeFormat(CCSDS.TIME.TIME_FORMAT_CUC1))
    self.assertTrue(CCSDS.TIME.isCUCtimeFormat(CCSDS.TIME.TIME_FORMAT_CUC2))
    self.assertTrue(CCSDS.TIME.isCUCtimeFormat(CCSDS.TIME.TIME_FORMAT_CUC3))
    self.assertTrue(CCSDS.TIME.isCUCtimeFormat(CCSDS.TIME.TIME_FORMAT_CUC4))
    self.assertFalse(CCSDS.TIME.isCUCtimeFormat(99))
    # test CCSDS.TIME.timeFormat()
    self.assertEqual(CCSDS.TIME.timeFormat("CDS1"), CCSDS.TIME.TIME_FORMAT_CDS1)
    self.assertEqual(CCSDS.TIME.timeFormat("CDS2"), CCSDS.TIME.TIME_FORMAT_CDS2)
    self.assertEqual(CCSDS.TIME.timeFormat("CDS3"), CCSDS.TIME.TIME_FORMAT_CDS3)
    self.assertEqual(CCSDS.TIME.timeFormat("CUC0"), CCSDS.TIME.TIME_FORMAT_CUC0)
    self.assertEqual(CCSDS.TIME.timeFormat("CUC1"), CCSDS.TIME.TIME_FORMAT_CUC1)
    self.assertEqual(CCSDS.TIME.timeFormat("CUC2"), CCSDS.TIME.TIME_FORMAT_CUC2)
    self.assertEqual(CCSDS.TIME.timeFormat("CUC3"), CCSDS.TIME.TIME_FORMAT_CUC3)
    self.assertEqual(CCSDS.TIME.timeFormat("CUC4"), CCSDS.TIME.TIME_FORMAT_CUC4)
    self.assertIsNone(CCSDS.TIME.timeFormat("???"))
    # test CCSDS.TIME.timeFormatStr()
    self.assertEqual(CCSDS.TIME.timeFormatStr(CCSDS.TIME.TIME_FORMAT_CDS1), "CDS1")
    self.assertEqual(CCSDS.TIME.timeFormatStr(CCSDS.TIME.TIME_FORMAT_CDS2), "CDS2")
    self.assertEqual(CCSDS.TIME.timeFormatStr(CCSDS.TIME.TIME_FORMAT_CDS3), "CDS3")
    self.assertEqual(CCSDS.TIME.timeFormatStr(CCSDS.TIME.TIME_FORMAT_CUC0), "CUC0")
    self.assertEqual(CCSDS.TIME.timeFormatStr(CCSDS.TIME.TIME_FORMAT_CUC1), "CUC1")
    self.assertEqual(CCSDS.TIME.timeFormatStr(CCSDS.TIME.TIME_FORMAT_CUC2), "CUC2")
    self.assertEqual(CCSDS.TIME.timeFormatStr(CCSDS.TIME.TIME_FORMAT_CUC3), "CUC3")
    self.assertEqual(CCSDS.TIME.timeFormatStr(CCSDS.TIME.TIME_FORMAT_CUC4), "CUC4")
    self.assertEqual(CCSDS.TIME.timeFormatStr(99), "???")
    # other tests
    actualTime1 = UTIL.TIME.getActualTime()
    actualTime1Str = "%.6f" % actualTime1
    actualTimeStr = UTIL.TIME.getASDtimeStr(actualTime1)
    actualTime2 = UTIL.TIME.getTimeFromASDstr(actualTimeStr)
    actualTime2Str = "%6f" % actualTime1
    self.assertEqual(actualTime1Str, actualTime2Str)
    zeroTime = 0.0
    zeroTimeStr1 = UTIL.TIME.getASDtimeStr(zeroTime)
    self.assertEqual(zeroTimeStr1, "1970.001.00.00.00.000")
    zeroTimeStr2 = UTIL.TIME.getASDtimeStr(zeroTime, withMicros=True)
    self.assertEqual(zeroTimeStr2, "1970.001.00.00.00.000000")
    self.validateERTandCDS1(UTIL.TCO.GPS_MISSION_EPOCH_STR,
                            UTIL.TCO.GPS_MISSION_EPOCH_DELTA)
    self.validateERTandCDS1(UTIL.TCO.TAI_MISSION_EPOCH_STR,
                            UTIL.TCO.TAI_MISSION_EPOCH_DELTA)
    self.validateERTandCDS2(UTIL.TCO.GPS_MISSION_EPOCH_STR,
                            UTIL.TCO.GPS_MISSION_EPOCH_DELTA)
    self.validateERTandCDS2(UTIL.TCO.TAI_MISSION_EPOCH_STR,
                            UTIL.TCO.TAI_MISSION_EPOCH_DELTA)
    self.validateERTandCDS3(UTIL.TCO.GPS_MISSION_EPOCH_STR,
                            UTIL.TCO.GPS_MISSION_EPOCH_DELTA)
    self.validateERTandCDS3(UTIL.TCO.TAI_MISSION_EPOCH_STR,
                            UTIL.TCO.TAI_MISSION_EPOCH_DELTA)
    zeroEpochTime1 = UTIL.TCO.correlateFromOBTmissionEpoch(zeroTime)
    self.assertEqual(zeroEpochTime1, 0)
    zeroEpochTime2 = correlateOBTcucPFC17(testData.ZERO_CUC2_TIME_FIELD)
    self.assertEqual(zeroEpochTime2, 0)
    UTIL.TCO.setOBTmissionEpochStr(UTIL.TCO.GPS_MISSION_EPOCH_STR)
    UTIL.TCO.setOBTleapSeconds(UTIL.TCO.GPS_LEAP_SECONDS_2009)
    cucTime1 = correlateOBTcucPFC17(testData.CUC2_TIME1_FIELD)
    cucTime1Str = UTIL.TIME.getASDtimeStr(cucTime1, withMicros=True)
    self.assertEqual(cucTime1Str, testData.CUC2_TIME1_STR)
    cucTime2 = correlateOBTcucPFC17(testData.CUC2_TIME2_FIELD)
    cucTime2Str = UTIL.TIME.getASDtimeStr(cucTime2, withMicros=True)
    self.assertEqual(cucTime2Str, testData.CUC2_TIME2_STR)
    cucTime3 = correlateOBTcucPFC17(testData.CUC2_TIME3_FIELD)
    cucTime3Str = UTIL.TIME.getASDtimeStr(cucTime3, withMicros=True)
    self.assertEqual(cucTime3Str, testData.CUC2_TIME3_STR)
    cucTime4 = correlateOBTcucPFC17(testData.CUC2_TIME4_FIELD)
    cucTime4Str = UTIL.TIME.getASDtimeStr(cucTime4, withMicros=True)
    self.assertEqual(cucTime4Str, testData.CUC2_TIME4_STR)
    cucTime5 = correlateOBTcucPFC17(testData.CUC2_TIME5_FIELD)
    cucTime5Str = UTIL.TIME.getASDtimeStr(cucTime5, withMicros=True)
    self.assertEqual(cucTime5Str, testData.CUC2_TIME5_STR)
    cucTime6 = correlateOBTcucPFC17(testData.CUC2_TIME6_FIELD)
    cucTime6Str = UTIL.TIME.getASDtimeStr(cucTime6, withMicros=True)
    self.assertEqual(cucTime6Str, testData.CUC2_TIME6_STR)
  def validateERTandCDS1(self, missionEpochString, missionEpochDelta):
    """tests ERT correlation and CDS1 data unit"""
    UTIL.TCO.setERTmissionEpochStr(missionEpochString)
    zeroERTtime = missionEpochDelta
    zeroERTtimeCorr = UTIL.TCO.correlateToERTmissionEpoch(zeroERTtime)
    zeroCDStimeDU = CCSDS.TIME.convertToCDS(zeroERTtimeCorr,
                                            CCSDS.TIME.TIME_FORMAT_CDS1)
    self.assertEqual(zeroCDStimeDU.days, 0)
    self.assertEqual(zeroCDStimeDU.mils, 0)
    days1ERTtime = zeroERTtime + (24 * 60 * 60)
    days1ERTtimeCorr = UTIL.TCO.correlateToERTmissionEpoch(days1ERTtime)
    days1CDStimeDU = CCSDS.TIME.convertToCDS(days1ERTtimeCorr,
                                             CCSDS.TIME.TIME_FORMAT_CDS1)
    self.assertEqual(days1CDStimeDU.days, 1)
    self.assertEqual(days1CDStimeDU.mils, 0)
    mils1ERTtime = zeroERTtime + 0.001
    mils1ERTtimeCorr = UTIL.TCO.correlateToERTmissionEpoch(mils1ERTtime)
    mils1CDStimeDU = CCSDS.TIME.convertToCDS(mils1ERTtimeCorr,
                                             CCSDS.TIME.TIME_FORMAT_CDS1)
    self.assertEqual(mils1CDStimeDU.days, 0)
    self.assertEqual(mils1CDStimeDU.mils, 1)
  def validateERTandCDS2(self, missionEpochString, missionEpochDelta):
    """tests ERT correlation and CDS2 data unit"""
    UTIL.TCO.setERTmissionEpochStr(missionEpochString)
    zeroERTtime = missionEpochDelta
    zeroERTtimeCorr = UTIL.TCO.correlateToERTmissionEpoch(zeroERTtime)
    zeroCDStimeDU = CCSDS.TIME.convertToCDS(zeroERTtimeCorr,
                                            CCSDS.TIME.TIME_FORMAT_CDS2)
    self.assertEqual(zeroCDStimeDU.days, 0)
    self.assertEqual(zeroCDStimeDU.mils, 0)
    self.assertEqual(zeroCDStimeDU.mics, 0)
    days1ERTtime = zeroERTtime + (24 * 60 * 60)
    days1ERTtimeCorr = UTIL.TCO.correlateToERTmissionEpoch(days1ERTtime)
    days1CDStimeDU = CCSDS.TIME.convertToCDS(days1ERTtimeCorr,
                                             CCSDS.TIME.TIME_FORMAT_CDS2)
    self.assertEqual(days1CDStimeDU.days, 1)
    self.assertEqual(days1CDStimeDU.mils, 0)
    self.assertEqual(days1CDStimeDU.mics, 0)
    mils1ERTtime = zeroERTtime + 0.001
    mils1ERTtimeCorr = UTIL.TCO.correlateToERTmissionEpoch(mils1ERTtime)
    mils1CDStimeDU = CCSDS.TIME.convertToCDS(mils1ERTtimeCorr,
                                             CCSDS.TIME.TIME_FORMAT_CDS2)
    self.assertEqual(mils1CDStimeDU.days, 0)
    self.assertEqual(mils1CDStimeDU.mils, 1)
    self.assertEqual(mils1CDStimeDU.mics, 0)
    mics1ERTtime = zeroERTtime + 0.000001
    mics1ERTtimeCorr = UTIL.TCO.correlateToERTmissionEpoch(mics1ERTtime)
    mics1CDStimeDU = CCSDS.TIME.convertToCDS(mics1ERTtimeCorr,
                                             CCSDS.TIME.TIME_FORMAT_CDS2)
    self.assertEqual(mics1CDStimeDU.days, 0)
    self.assertEqual(mics1CDStimeDU.mils, 0)
    self.assertEqual(mics1CDStimeDU.mics, 1)
  def validateERTandCDS3(self, missionEpochString, missionEpochDelta):
    """tests ERT correlation and CDS3 data unit"""
    UTIL.TCO.setERTmissionEpochStr(missionEpochString)
    zeroERTtime = missionEpochDelta
    zeroERTtimeCorr = UTIL.TCO.correlateToERTmissionEpoch(zeroERTtime)
    zeroCDStimeDU = CCSDS.TIME.convertToCDS(zeroERTtimeCorr,
                                            CCSDS.TIME.TIME_FORMAT_CDS3)
    self.assertEqual(zeroCDStimeDU.days, 0)
    self.assertEqual(zeroCDStimeDU.mils, 0)
    self.assertEqual(zeroCDStimeDU.pics, 0)
    days1ERTtime = zeroERTtime + (24 * 60 * 60)
    days1ERTtimeCorr = UTIL.TCO.correlateToERTmissionEpoch(days1ERTtime)
    days1CDStimeDU = CCSDS.TIME.convertToCDS(days1ERTtimeCorr,
                                             CCSDS.TIME.TIME_FORMAT_CDS3)
    self.assertEqual(days1CDStimeDU.days, 1)
    self.assertEqual(days1CDStimeDU.mils, 0)
    self.assertEqual(days1CDStimeDU.pics, 0)
    mils1ERTtime = zeroERTtime + 0.001
    mils1ERTtimeCorr = UTIL.TCO.correlateToERTmissionEpoch(mils1ERTtime)
    mils1CDStimeDU = CCSDS.TIME.convertToCDS(mils1ERTtimeCorr,
                                             CCSDS.TIME.TIME_FORMAT_CDS3)
    self.assertEqual(mils1CDStimeDU.days, 0)
    # special verification due to rounding
    try:
      self.assertEqual(mils1CDStimeDU.mils, 1)
      self.assertEqual(mils1CDStimeDU.pics, 0)
    except:
      self.assertEqual(mils1CDStimeDU.mils, 0)
      self.assertEqual(mils1CDStimeDU.pics, 999987125)
    pics1ERTtime = zeroERTtime + 0.000000000001
    pics1ERTtimeCorr = UTIL.TCO.correlateToERTmissionEpoch(pics1ERTtime)
    pics1CDStimeDU = CCSDS.TIME.convertToCDS(pics1ERTtimeCorr,
                                             CCSDS.TIME.TIME_FORMAT_CDS3)
    self.assertEqual(pics1CDStimeDU.days, 0)
    self.assertEqual(pics1CDStimeDU.mils, 0)
    # special verification due to rounding
    try:
      self.assertEqual(pics1CDStimeDU.pics, 1)
    except:
      self.assertEqual(pics1CDStimeDU.pics, 0)

########
# main #
########
if __name__ == "__main__":
  unittest.main()
