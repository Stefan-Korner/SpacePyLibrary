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
# Unit Tests                                                                  *
#******************************************************************************
import UTIL.TIME
import testData

#############
# functions #
#############
# -----------------------------------------------------------------------------
def correlateOBTcucPFC17(byteArray):
  """convenience function for backward compatibility"""
  timeDU = UTIL.TIME.createCUC(byteArray)
  pyTime = UTIL.TIME.convertFromCUC(timeDU)
  return UTIL.TIME.correlateFromOBTmissionEpoch(pyTime)
# -----------------------------------------------------------------------------
def test_TIMEoperations():
  """function to test the TIME operations"""
  actualTime1 = UTIL.TIME.getActualTime()
  actualTime1Str = "%.6f" % actualTime1
  actualTimeStr = UTIL.TIME.getASDtimeStr(actualTime1)
  actualTime2 = UTIL.TIME.getTimeFromASDstr(actualTimeStr)
  actualTime2Str = "%6f" % actualTime1
  print "actual time =", actualTimeStr
  if actualTime1Str != actualTime2Str:
    print "Time conversions not symmetrical:", actualTime1Str, actualTime2Str
    return False
  zeroTime = 0.0
  zeroTimeStr1 = UTIL.TIME.getASDtimeStr(zeroTime)
  if zeroTimeStr1 != "1970.001.00.00.00.000":
    print "Invalid ASD zero time 1:", zeroTimeStr1
    return False
  zeroTimeStr2 = UTIL.TIME.getASDtimeStr(zeroTime, withMicros=True)
  if zeroTimeStr2 != "1970.001.00.00.00.000000":
    print "Invalid ASD zero time 2:", zeroTimeStr2
    return False
  UTIL.TIME.setERTmissionEpochStr(UTIL.TIME.TAI_MISSION_EPOCH_STR)
  zeroCCSDStime = UTIL.TIME.TAI_MISSION_EPOCH_DELTA
  zeroCCSDStimeDU = UTIL.TIME.getERTccsdsTimeDU(zeroCCSDStime)
  if zeroCCSDStimeDU.days != 0:
    print "Invalid zero CCSDS time days:", zeroCCSDStimeDU.days
    return False
  if zeroCCSDStimeDU.mils != 0:
    print "Invalid zero CCSDS time milliseconds:", zeroCCSDStimeDU.mils
    return False
  if zeroCCSDStimeDU.mics != 0:
    print "Invalid zero CCSDS time microsedonds:", zeroCCSDStimeDU.mics
    return False
  days1CCSDStime = zeroCCSDStime + (24 * 60 * 60)
  days1CCSDStimeDU = UTIL.TIME.getERTccsdsTimeDU(days1CCSDStime)
  if days1CCSDStimeDU.days != 1:
    print "Invalid days1 CCSDS time days:", days1CCSDStimeDU.days
    return False
  if days1CCSDStimeDU.mils != 0:
    print "Invalid days1 CCSDS time milliseconds:", days1CCSDStimeDU.mils
    return False
  if days1CCSDStimeDU.mics != 0:
    print "Invalid days1 CCSDS time microseconds:", days1CCSDStimeDU.mics
    return False
  mils1CCSDStime = zeroCCSDStime + 0.001
  mils1CCSDStimeDU = UTIL.TIME.getERTccsdsTimeDU(mils1CCSDStime)
  if mils1CCSDStimeDU.days != 0:
    print "Invalid mils1 CCSDS time days:", mils1CCSDStimeDU.days
    return False
  if mils1CCSDStimeDU.mils != 1:
    print "Invalid mils1 CCSDS time milliseconds:", mils1CCSDStimeDU.mils
    return False
  if mils1CCSDStimeDU.mics != 0:
    print "Invalid mils1 CCSDS time microseconds:", mils1CCSDStimeDU.mics
    return False
  mics1CCSDStime = zeroCCSDStime + 0.000001
  mics1CCSDStimeDU = UTIL.TIME.getERTccsdsTimeDU(mics1CCSDStime)
  if mics1CCSDStimeDU.days != 0:
    print "Invalid mics1 CCSDS time days:", mils1CCSDStimeDU.days
    return False
  if mics1CCSDStimeDU.mils != 0:
    print "Invalid mics1 CCSDS time milliseconds:", mics1CCSDStimeDU.mils
    return False
  if mics1CCSDStimeDU.mics != 1:
    print "Invalid mics1 CCSDS time microseconds:", mics1CCSDStimeDU.mics
    return False
  zeroEpochTime1 = UTIL.TIME.correlateFromOBTmissionEpoch(zeroTime)
  if zeroEpochTime1 != 0:
    zeroEpochTime1Str = UTIL.TIME.getASDtimeStr(zeroEpochTime1)
    print "Invalid zero epoch time:", zeroEpochTime1Str
    return False
  zeroEpochTime2 = correlateOBTcucPFC17(testData.ZERO_CUC_TIME_FIELD)
  if zeroEpochTime2 != 0:
    zeroEpochTime2Str = UTIL.TIME.getASDtimeStr(zeroEpochTime2)
    print "Invalid zero epoch time:", zeroEpochTime2Str
    return False
  UTIL.TIME.setOBTmissionEpochStr(UTIL.TIME.GPS_MISSION_EPOCH_STR)
  UTIL.TIME.setOBTleapSeconds(UTIL.TIME.GPS_LEAP_SECONDS_2009)
  cucTime1 = correlateOBTcucPFC17(testData.CUC_TIME1_FIELD)
  cucTime1Str = UTIL.TIME.getASDtimeStr(cucTime1, withMicros=True)
  if cucTime1Str != testData.CUC_TIME1_STR:
    print "Invalid CUC time 1:", cucTime1Str
    return False
  cucTime2 = correlateOBTcucPFC17(testData.CUC_TIME2_FIELD)
  cucTime2Str = UTIL.TIME.getASDtimeStr(cucTime2, withMicros=True)
  if cucTime2Str != testData.CUC_TIME2_STR:
    print "Invalid CUC time 2:", cucTime2Str
    return False
  cucTime3 = correlateOBTcucPFC17(testData.CUC_TIME3_FIELD)
  cucTime3Str = UTIL.TIME.getASDtimeStr(cucTime3, withMicros=True)
  if cucTime3Str != testData.CUC_TIME3_STR:
    print "Invalid CUC time 3:", cucTime3Str
    return False
  cucTime4 = correlateOBTcucPFC17(testData.CUC_TIME4_FIELD)
  cucTime4Str = UTIL.TIME.getASDtimeStr(cucTime4, withMicros=True)
  if cucTime4Str != testData.CUC_TIME4_STR:
    print "Invalid CUC time 4:", cucTime4Str
    return False
  cucTime5 = correlateOBTcucPFC17(testData.CUC_TIME5_FIELD)
  cucTime5Str = UTIL.TIME.getASDtimeStr(cucTime5, withMicros=True)
  if cucTime5Str != testData.CUC_TIME5_STR:
    print "Invalid CUC time 5:", cucTime5Str
    return False
  cucTime6 = correlateOBTcucPFC17(testData.CUC_TIME6_FIELD)
  cucTime6Str = UTIL.TIME.getASDtimeStr(cucTime6, withMicros=True)
  if cucTime6Str != testData.CUC_TIME6_STR:
    print "Invalid CUC time 6:", cucTime6Str
    return False
  return True

########
# main #
########
if __name__ == "__main__":
  print "***** test_TIMEoperations() start"
  retVal = test_TIMEoperations()
  print "***** test_TIMEoperations() done:", retVal
