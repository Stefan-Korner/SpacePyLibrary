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
import CCSDS.TIME
import UTIL.TCO, UTIL.TIME
import testData

#############
# functions #
#############
# -----------------------------------------------------------------------------
def correlateOBTcucPFC17(byteArray):
  """convenience function for backward compatibility"""
  timeDU = CCSDS.TIME.createCUC(byteArray)
  pyTime = CCSDS.TIME.convertFromCUC(timeDU)
  return UTIL.TCO.correlateFromOBTmissionEpoch(pyTime)
# -----------------------------------------------------------------------------
def test_ERTandCDS2(missionEpochString, missionEpochDelta):
  """tests ERT correlation and CDS2 data unit"""
  UTIL.TCO.setERTmissionEpochStr(missionEpochString)
  zeroERTtime = missionEpochDelta
  zeroERTtimeCorr = UTIL.TCO.correlateToERTmissionEpoch(zeroERTtime)
  zeroCDStimeDU = CCSDS.TIME.convertToCDS(zeroERTtimeCorr,
                                          CCSDS.TIME.TIME_FORMAT_CDS2)
  if zeroCDStimeDU.days != 0:
    print("Invalid zero CCSDS time days:", zeroCDStimeDU.days)
    return False
  if zeroCDStimeDU.mils != 0:
    print("Invalid zero CCSDS time milliseconds:", zeroCDStimeDU.mils)
    return False
  if zeroCDStimeDU.mics != 0:
    print("Invalid zero CCSDS time microsedonds:", zeroCDStimeDU.mics)
    return False
  days1ERTtime = zeroERTtime + (24 * 60 * 60)
  days1ERTtimeCorr = UTIL.TCO.correlateToERTmissionEpoch(days1ERTtime)
  days1CDStimeDU = CCSDS.TIME.convertToCDS(days1ERTtimeCorr,
                                           CCSDS.TIME.TIME_FORMAT_CDS2)
  if days1CDStimeDU.days != 1:
    print("Invalid days1 CCSDS time days:", days1CDStimeDU.days)
    return False
  if days1CDStimeDU.mils != 0:
    print("Invalid days1 CCSDS time milliseconds:", days1CDStimeDU.mils)
    return False
  if days1CDStimeDU.mics != 0:
    print("Invalid days1 CCSDS time microseconds:", days1CDStimeDU.mics)
    return False
  mils1ERTtime = zeroERTtime + 0.001
  mils1ERTtimeCorr = UTIL.TCO.correlateToERTmissionEpoch(mils1ERTtime)
  mils1CDStimeDU = CCSDS.TIME.convertToCDS(mils1ERTtimeCorr,
                                           CCSDS.TIME.TIME_FORMAT_CDS2)
  if mils1CDStimeDU.days != 0:
    print("Invalid mils1 CCSDS time days:", mils1CDStimeDU.days)
    return False
  if mils1CDStimeDU.mils != 1:
    print("Invalid mils1 CCSDS time milliseconds:", mils1CDStimeDU.mils)
    return False
  if mils1CDStimeDU.mics != 0:
    print("Invalid mils1 CCSDS time microseconds:", mils1CDStimeDU.mics)
    return False
  mics1ERTtime = zeroERTtime + 0.000001
  mics1ERTtimeCorr = UTIL.TCO.correlateToERTmissionEpoch(mics1ERTtime)
  mics1CDStimeDU = CCSDS.TIME.convertToCDS(mics1ERTtimeCorr,
                                           CCSDS.TIME.TIME_FORMAT_CDS2)
  if mics1CDStimeDU.days != 0:
    print("Invalid mics1 CCSDS time days:", mics1CDStimeDU.days)
    return False
  if mics1CDStimeDU.mils != 0:
    print("Invalid mics1 CCSDS time milliseconds:", mics1CDStimeDU.mils)
    return False
  if mics1CDStimeDU.mics != 1:
    print("Invalid mics1 CCSDS time microseconds:", mics1CDStimeDU.mics)
    return False
  return True
# -----------------------------------------------------------------------------
def test_TIMEoperations():
  """function to test the TIME operations"""
  actualTime1 = UTIL.TIME.getActualTime()
  actualTime1Str = "%.6f" % actualTime1
  actualTimeStr = UTIL.TIME.getASDtimeStr(actualTime1)
  actualTime2 = UTIL.TIME.getTimeFromASDstr(actualTimeStr)
  actualTime2Str = "%6f" % actualTime1
  print("actual time =", actualTimeStr)
  if actualTime1Str != actualTime2Str:
    print("Time conversions not symmetrical:", actualTime1Str, actualTime2Str)
    return False
  zeroTime = 0.0
  zeroTimeStr1 = UTIL.TIME.getASDtimeStr(zeroTime)
  if zeroTimeStr1 != "1970.001.00.00.00.000":
    print("Invalid ASD zero time 1:", zeroTimeStr1)
    return False
  zeroTimeStr2 = UTIL.TIME.getASDtimeStr(zeroTime, withMicros=True)
  if zeroTimeStr2 != "1970.001.00.00.00.000000":
    print("Invalid ASD zero time 2:", zeroTimeStr2)
    return False
  if not test_ERTandCDS2(UTIL.TCO.GPS_MISSION_EPOCH_STR,
                         UTIL.TCO.GPS_MISSION_EPOCH_DELTA):
    return False
  if not test_ERTandCDS2(UTIL.TCO.TAI_MISSION_EPOCH_STR,
                         UTIL.TCO.TAI_MISSION_EPOCH_DELTA):
    print("!!! Warning: negative time values are not supported on this platform !!!")
  zeroEpochTime1 = UTIL.TCO.correlateFromOBTmissionEpoch(zeroTime)
  if zeroEpochTime1 != 0:
    zeroEpochTime1Str = UTIL.TIME.getASDtimeStr(zeroEpochTime1)
    print("Invalid zero epoch time:", zeroEpochTime1Str)
    return False
  zeroEpochTime2 = correlateOBTcucPFC17(testData.ZERO_CUC2_TIME_FIELD)
  if zeroEpochTime2 != 0:
    zeroEpochTime2Str = UTIL.TIME.getASDtimeStr(zeroEpochTime2)
    print("Invalid zero epoch time:", zeroEpochTime2Str)
    return False
  UTIL.TCO.setOBTmissionEpochStr(UTIL.TCO.GPS_MISSION_EPOCH_STR)
  UTIL.TCO.setOBTleapSeconds(UTIL.TCO.GPS_LEAP_SECONDS_2009)
  cucTime1 = correlateOBTcucPFC17(testData.CUC2_TIME1_FIELD)
  cucTime1Str = UTIL.TIME.getASDtimeStr(cucTime1, withMicros=True)
  if cucTime1Str != testData.CUC2_TIME1_STR:
    print("Invalid CUC time 1:", cucTime1Str)
    return False
  cucTime2 = correlateOBTcucPFC17(testData.CUC2_TIME2_FIELD)
  cucTime2Str = UTIL.TIME.getASDtimeStr(cucTime2, withMicros=True)
  if cucTime2Str != testData.CUC2_TIME2_STR:
    print("Invalid CUC time 2:", cucTime2Str)
    return False
  cucTime3 = correlateOBTcucPFC17(testData.CUC2_TIME3_FIELD)
  cucTime3Str = UTIL.TIME.getASDtimeStr(cucTime3, withMicros=True)
  if cucTime3Str != testData.CUC2_TIME3_STR:
    print("Invalid CUC time 3:", cucTime3Str)
    return False
  cucTime4 = correlateOBTcucPFC17(testData.CUC2_TIME4_FIELD)
  cucTime4Str = UTIL.TIME.getASDtimeStr(cucTime4, withMicros=True)
  if cucTime4Str != testData.CUC2_TIME4_STR:
    print("Invalid CUC time 4:", cucTime4Str)
    return False
  cucTime5 = correlateOBTcucPFC17(testData.CUC2_TIME5_FIELD)
  cucTime5Str = UTIL.TIME.getASDtimeStr(cucTime5, withMicros=True)
  if cucTime5Str != testData.CUC2_TIME5_STR:
    print("Invalid CUC time 5:", cucTime5Str)
    return False
  cucTime6 = correlateOBTcucPFC17(testData.CUC2_TIME6_FIELD)
  cucTime6Str = UTIL.TIME.getASDtimeStr(cucTime6, withMicros=True)
  if cucTime6Str != testData.CUC2_TIME6_STR:
    print("Invalid CUC time 6:", cucTime6Str)
    return False
  return True

########
# main #
########
if __name__ == "__main__":
  print("***** test_TIMEoperations() start")
  retVal = test_TIMEoperations()
  print("***** test_TIMEoperations() done:", retVal)
