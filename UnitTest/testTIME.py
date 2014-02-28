#!/usr/bin/env python
#******************************************************************************
# (C) 2014, Stefan Korner, Austria                                            *
#                                                                             *
# The Space Python Library is free software; you can redistribute it and/or   *
# modify it under the terms of the GNU Lesser General Public License as       *
# published by the Free Software Foundation; either version 2.1 of the        *
# License, or (at your option) any later version.                             *
#                                                                             *
# The Space C++ Library is distributed in the hope that it will be useful,    *
# but WITHOUT ANY WARRANTY; without even the implied warranty of              *
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser     *
# General Public License for more details.                                    *
#******************************************************************************
# Unit Tests                                                                  *
#******************************************************************************
import GDP.TIME
import testData

#############
# functions #
#############
def test_TIMEoperations():
  """function to test the TIME operations"""
  actualTime1 = GDP.TIME.getActualTime()
  actualTime1Str = "%.6f" % actualTime1
  actualTimeStr = GDP.TIME.getASDtimeStr(actualTime1)
  actualTime2 = GDP.TIME.getTimeFromASDstr(actualTimeStr)
  actualTime2Str = "%6f" % actualTime1
  print "actual time =", actualTimeStr
  if actualTime1Str != actualTime2Str:
    print "Time conversions not symmetrical:", actualTime1Str, actualTime2Str
    return False
  zeroTime = 0.0
  zeroTimeStr1 = GDP.TIME.getASDtimeStr(zeroTime)
  if zeroTimeStr1 != "1970.001.00.00.00.000":
    print "Invalid ASD zero time 1:", zeroTimeStr1
    return False
  zeroTimeStr2 = GDP.TIME.getASDtimeStr(zeroTime, withMicros=True)
  if zeroTimeStr2 != "1970.001.00.00.00.000000":
    print "Invalid ASD zero time 2:", zeroTimeStr2
    return False
  zeroCCSDStime = GDP.TIME.EPOCH_1958_SEC_DELTA
  zeroCCSDStimeDU = GDP.TIME.getCCSDStimeDU(zeroCCSDStime)
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
  days1CCSDStimeDU = GDP.TIME.getCCSDStimeDU(days1CCSDStime)
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
  mils1CCSDStimeDU = GDP.TIME.getCCSDStimeDU(mils1CCSDStime)
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
  mics1CCSDStimeDU = GDP.TIME.getCCSDStimeDU(mics1CCSDStime)
  if mics1CCSDStimeDU.days != 0:
    print "Invalid mics1 CCSDS time days:", mils1CCSDStimeDU.days
    return False
  if mics1CCSDStimeDU.mils != 0:
    print "Invalid mics1 CCSDS time milliseconds:", mics1CCSDStimeDU.mils
    return False
  if mics1CCSDStimeDU.mics != 1:
    print "Invalid mics1 CCSDS time microseconds:", mics1CCSDStimeDU.mics
    return False
  zeroEpochTime1 = GDP.TIME.correlateFromMissionEpoch(zeroTime)
  if zeroEpochTime1 != GDP.TIME.TCO_MISSION_EPOCH:
    zeroEpochTime1Str = GDP.TIME.getASDtimeStr(zeroEpochTime1)
    print "Invalid zero epoch time:", zeroEpochTime1Str
    return False
  zeroEpochTime2 = GDP.TIME.correlateCucPFC17(testData.ZERO_CUC_TIME_FIELD)
  if zeroEpochTime2 != GDP.TIME.TCO_MISSION_EPOCH:
    zeroEpochTime2Str = GDP.TIME.getASDtimeStr(zeroEpochTime2)
    print "Invalid zero epoch time:", zeroEpochTime2Str
    return False
  cucTime1 = GDP.TIME.correlateCucPFC17(testData.CUC_TIME1_FIELD)
  cucTime1Str = GDP.TIME.getASDtimeStr(cucTime1, withMicros=True)
  if cucTime1Str != testData.CUC_TIME1_STR:
    print "Invalid CUC time 1:", cucTime1Str
    return False
  cucTime2 = GDP.TIME.correlateCucPFC17(testData.CUC_TIME2_FIELD)
  cucTime2Str = GDP.TIME.getASDtimeStr(cucTime2, withMicros=True)
  if cucTime2Str != testData.CUC_TIME2_STR:
    print "Invalid CUC time 2:", cucTime2Str
    return False
  cucTime3 = GDP.TIME.correlateCucPFC17(testData.CUC_TIME3_FIELD)
  cucTime3Str = GDP.TIME.getASDtimeStr(cucTime3, withMicros=True)
  if cucTime3Str != testData.CUC_TIME3_STR:
    print "Invalid CUC time 3:", cucTime3Str
    return False
  cucTime4 = GDP.TIME.correlateCucPFC17(testData.CUC_TIME4_FIELD)
  cucTime4Str = GDP.TIME.getASDtimeStr(cucTime4, withMicros=True)
  if cucTime4Str != testData.CUC_TIME4_STR:
    print "Invalid CUC time 4:", cucTime4Str
    return False
  cucTime5 = GDP.TIME.correlateCucPFC17(testData.CUC_TIME5_FIELD)
  cucTime5Str = GDP.TIME.getASDtimeStr(cucTime5, withMicros=True)
  if cucTime5Str != testData.CUC_TIME5_STR:
    print "Invalid CUC time 5:", cucTime5Str
    return False
  cucTime6 = GDP.TIME.correlateCucPFC17(testData.CUC_TIME6_FIELD)
  cucTime6Str = GDP.TIME.getASDtimeStr(cucTime6, withMicros=True)
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
