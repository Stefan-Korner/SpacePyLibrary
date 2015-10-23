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
# Utilities - Time Conversions                                                *
#******************************************************************************
import time
from UTIL.DU import BITS, BYTES, UNSIGNED, BinaryUnit

#############
# constants #
#############
TAI_MISSION_EPOCH_DELTA = -378691200
TAI_MISSION_EPOCH_STR = "1958.001.00.00.00.000"
UNIX_MISSION_EPOCH_STR = "1970.001.00.00.00.000"
GPS_MISSION_EPOCH_DELTA = 315964800
GPS_MISSION_EPOCH_STR = "1980.006.00.00.00.000"
GPS_LEAP_SECONDS_1980 = 0
GPS_LEAP_SECONDS_2009 = 15
GPS_LEAP_SECONDS_2012 = 16
GPS_LEAP_SECONDS_2015 = 17
SECONDS_OF_DAY = (24 * 60 * 60)
TIME_FORMAT_CDS1 = 1
TIME_FORMAT_CDS2 = 2
TIME_FORMAT_CUC = 3
# constants for CDS time
CDS1_TIME_BYTE_SIZE = 6
CDS1_TIME_ATTRIBUTES = {
  "days": (0, 2, UNSIGNED),
  "mils": (2, 4, UNSIGNED)}
CDS2_TIME_BYTE_SIZE = 8
CDS2_TIME_ATTRIBUTES = {
  "days": (0, 2, UNSIGNED),
  "mils": (2, 4, UNSIGNED),
  "mics": (6, 2, UNSIGNED)}
# constants for CUC time
CUC0_TIME_BYTE_SIZE = 4
CUC0_TIME_ATTRIBUTES = {
  "coarse": (0, 4, UNSIGNED)}
CUC1_TIME_BYTE_SIZE = 5
CUC1_TIME_ATTRIBUTES = {
  "coarse": (0, 4, UNSIGNED),
  "fine":   (4, 1, UNSIGNED)}
CUC2_TIME_BYTE_SIZE = 6
CUC2_TIME_ATTRIBUTES = {
  "coarse": (0, 4, UNSIGNED),
  "fine":   (4, 2, UNSIGNED)}
CUC3_TIME_BYTE_SIZE = 7
CUC3_TIME_ATTRIBUTES = {
  "coarse": (0, 4, UNSIGNED),
  "fine":   (4, 3, UNSIGNED)}
CUC4_TIME_BYTE_SIZE = 8
CUC4_TIME_ATTRIBUTES = {
  "coarse": (0, 4, UNSIGNED),
  "fine":   (4, 4, UNSIGNED)}

####################
# global variables #
####################
# shall be initialised via setOBTmissionEpochStr()
s_obtMissionEpochStr = ""
s_obtMissionEpoch = 0
s_obtMissionEpochWithLeapSeconds = 0
# shall be initialised via setOBTleapSeconds()
s_obtLeapSeconds = 0
# shall be initialised via setERTmissionEpochStr()
s_ertMissionEpochStr = ""
s_ertMissionEpoch = 0
s_ertMissionEpochWithLeapSeconds = 0
# shall be initialised via setERTleapSeconds()
s_ertLeapSeconds = 0

#############
# functions #
#############
# -----------------------------------------------------------------------------
def getActualTime():
  """returns the actual time"""
  pyTime = time.time()
  return pyTime
# -----------------------------------------------------------------------------
def getASDtimeStr(pyTime, withMicros=False):
  """returns the ASD format YYYY.DDD.hh.mm.ss.MMM or YYYY.DDD.hh.mm.ss.MMMMMM"""
  # calculate the seconds part
  secs = int(pyTime)
  tm = time.gmtime(secs)
  tmStr = time.strftime("%Y.%j.%H.%M.%S", tm)
  if withMicros:
    mics = min(int(round((pyTime - secs) * 1000000)), 999999)
    return tmStr + (".%06d" % mics)
  # with milliseconds only
  mils = min(int(round((pyTime - secs) * 1000)), 999)
  return tmStr + (".%03d" % mils)
# -----------------------------------------------------------------------------
def getTimeFromASDstr(tmStr):
  """
  returns the absolute time from ASD format strings
  YYYY.DDD.hh.mm.ss.MMM or YYYY.DDD.hh.mm.ss.MMMMMM
  """
  timePieces = tmStr.split(".")
  if len(timePieces) != 6:
    # invalid format
    return 0.0
  secondsStr = timePieces[0] + "." + timePieces[1] + "." + \
               timePieces[2] + "." + timePieces[3] + "." + \
               timePieces[4]
  microMilliStr = timePieces[5]
  if len(microMilliStr) == 3:
    # milliseconds
    seconds = float(microMilliStr) / 1000
  elif len(microMilliStr) == 6:
    # microseconds
    seconds = float(microMilliStr) / 1000000
  else:
    # invalid format
    return 0.0
  try:
    # force the tm_isdst to 0
    tm = time.strptime(secondsStr, "%Y.%j.%H.%M.%S")[:-1] + (0,)
    seconds += int(time.mktime(tm)) - time.timezone
    return seconds
  except:
    # invalid format
    return 0.0
# -----------------------------------------------------------------------------
def setOBTmissionEpochStr(missionEpochStr):
  """sets the OBT mission epoch string"""
  global s_optMissionEpochStr, s_obtMissionEpoch
  global s_obtLeapSeconds, s_obtMissionEpochWithLeapSeconds
  s_obtMissionEpochStr = missionEpochStr
  s_obtMissionEpoch = getTimeFromASDstr(s_obtMissionEpochStr)
  s_obtMissionEpochWithLeapSeconds = s_obtMissionEpoch - s_obtLeapSeconds
# -----------------------------------------------------------------------------
def setOBTleapSeconds(leapSeconds):
  """sets the OBT leap seconds"""
  global s_obtMissionEpoch
  global s_obtLeapSeconds, s_obtMissionEpochWithLeapSeconds
  s_obtLeapSeconds = leapSeconds
  s_obtMissionEpochWithLeapSeconds = s_obtMissionEpoch - s_obtLeapSeconds
# -----------------------------------------------------------------------------
def correlateFromOBTmissionEpoch(pyEpochTime):
  """correlate the OBT mission epoch time to the local time"""
  return pyEpochTime + s_obtMissionEpochWithLeapSeconds
# -----------------------------------------------------------------------------
def correlateToOBTmissionEpoch(pyUTCtime):
  """correlate the local time to OBT mission epoch time"""
  return pyUTCtime - s_obtMissionEpochWithLeapSeconds
# -----------------------------------------------------------------------------
def setERTmissionEpochStr(missionEpochStr):
  """sets the ERT mission epoch string"""
  global s_ertMissionEpochStr, s_ertMissionEpoch
  global s_ertLeapSeconds, s_ertMissionEpochWithLeapSeconds
  s_ertMissionEpochStr = missionEpochStr
  s_ertMissionEpoch = getTimeFromASDstr(s_ertMissionEpochStr)
  s_ertMissionEpochWithLeapSeconds = s_ertMissionEpoch - s_ertLeapSeconds
# -----------------------------------------------------------------------------
def setERTleapSeconds(leapSeconds):
  """sets the ERT leap seconds"""
  global s_ertMissionEpoch
  global s_ertLeapSeconds, s_ertMissionEpochWithLeapSeconds
  s_ertLeapSeconds = leapSeconds
  s_ertMissionEpochWithLeapSeconds = s_ertMissionEpoch - s_ertLeapSeconds
# -----------------------------------------------------------------------------
def correlateFromERTmissionEpoch(pyEpochTime):
  """correlate the ERT mission epoch time to the local time"""
  return pyEpochTime + s_ertMissionEpochWithLeapSeconds
# -----------------------------------------------------------------------------
def correlateToERTmissionEpoch(pyUTCtime):
  """correlate the local time to ERT mission epoch time"""
  return pyUTCtime - s_ertMissionEpochWithLeapSeconds
# -----------------------------------------------------------------------------
def timeFormat(timeFormatString):
  """returns the time format from 'CUC', 'CDS1', 'CDS2'"""
  if timeFormatString == "CDS1":
    return TIME_FORMAT_CDS1
  elif timeFormatString == "CDS2":
    return TIME_FORMAT_CDS2
  return TIME_FORMAT_CUC
# -----------------------------------------------------------------------------
def createCDS(byteArray):
  """returns a CDS binary data unit representation of time"""
  if len(byteArray) == CDS1_TIME_BYTE_SIZE:
    return BinaryUnit(byteArray, CDS1_TIME_BYTE_SIZE, CDS2_TIME_ATTRIBUTES)
  return BinaryUnit(byteArray, CDS2_TIME_BYTE_SIZE, CDS2_TIME_ATTRIBUTES)
# -----------------------------------------------------------------------------
def convertToCDS(pyTime, hasMicro):
  """returns a CDS binary data unit representation of time"""
  # split seconds and micros
  secs = int(pyTime)
  mics = int(round((pyTime - secs) * 1000000))
  # convert into CDS components
  days = secs / SECONDS_OF_DAY
  secs %= SECONDS_OF_DAY
  mils = (secs * 1000) + (mics / 1000)
  if hasMicro:
    mics %= 1000
    timeDU = BinaryUnit("\0" * CDS2_TIME_BYTE_SIZE,
                        CDS2_TIME_BYTE_SIZE,
                        CDS2_TIME_ATTRIBUTES)
    timeDU.mics = mics
  else:
    timeDU = BinaryUnit("\0" * CDS1_TIME_BYTE_SIZE,
                        CDS1_TIME_BYTE_SIZE,
                        CDS1_TIME_ATTRIBUTES)
  timeDU.days = days
  timeDU.mils = mils
  return timeDU
# -----------------------------------------------------------------------------
def convertFromCDS(timeDU):
  """returns python time representation from CDS binary data unit"""
  secs = timeDU.days * SECONDS_OF_DAY
  mils = timeDU.mils
  secs += (mils / 1000)
  mics = 0
  if len(timeDU) == CDS2_TIME_BYTE_SIZE:
    mics = timeDU.mics
    mics += (mils % 1000) * 1000
  pyTime = mics / 1000000.0
  pyTime += secs
  return pyTime
# -----------------------------------------------------------------------------
def createCUC(byteArray):
  """returns a CUC binary data unit representation of time"""
  if len(byteArray) == CUC0_TIME_BYTE_SIZE:
    return BinaryUnit(byteArray, CUC0_TIME_BYTE_SIZE, CUC0_TIME_ATTRIBUTES)
  elif len(byteArray) == CUC1_TIME_BYTE_SIZE:
    return BinaryUnit(byteArray, CUC1_TIME_BYTE_SIZE, CUC1_TIME_ATTRIBUTES)
  elif len(byteArray) == CUC2_TIME_BYTE_SIZE:
    return BinaryUnit(byteArray, CUC2_TIME_BYTE_SIZE, CUC2_TIME_ATTRIBUTES)
  elif len(byteArray) == CUC2_TIME_BYTE_SIZE:
    return BinaryUnit(byteArray, CUC3_TIME_BYTE_SIZE, CUC3_TIME_ATTRIBUTES)
  return BinaryUnit(byteArray, CUC4_TIME_BYTE_SIZE, CUC4_TIME_ATTRIBUTES)
# -----------------------------------------------------------------------------
def convertToCUC(pyTime, fineTimeSize):
  """returns a CUC binary data unit representation of time"""
  coarseTime = int(pyTime)
  if fineTimeSize == 0:
    timeDU = BinaryUnit("\0" * CUC0_TIME_BYTE_SIZE,
                        CUC0_TIME_BYTE_SIZE,
                        CUC0_TIME_ATTRIBUTES)
  elif fineTimeSize == 1:
    fineTime = pyTime - coarseTime
    timeDU = BinaryUnit("\0" * CUC1_TIME_BYTE_SIZE,
                        CUC1_TIME_BYTE_SIZE,
                        CUC1_TIME_ATTRIBUTES)
    timeDU.fine = int(fineTime * 0x100)
  elif fineTimeSize == 2:
    fineTime = pyTime - coarseTime
    timeDU = BinaryUnit("\0" * CUC2_TIME_BYTE_SIZE,
                        CUC2_TIME_BYTE_SIZE,
                        CUC2_TIME_ATTRIBUTES)
    timeDU.fine = int(fineTime * 0x10000)
  elif fineTimeSize == 3:
    fineTime = pyTime - coarseTime
    timeDU = BinaryUnit("\0" * CUC3_TIME_BYTE_SIZE,
                        CUC3_TIME_BYTE_SIZE,
                        CUC3_TIME_ATTRIBUTES)
    timeDU.fine = int(fineTime * 0x1000000)
  else:
    # fineTimeSize == 4:
    fineTime = pyTime - coarseTime
    timeDU = BinaryUnit("\0" * CUC4_TIME_BYTE_SIZE,
                        CUC4_TIME_BYTE_SIZE,
                        CUC4_TIME_ATTRIBUTES)
    timeDU.fine = int(fineTime * 0x100000000)
  timeDU.coarse = coarseTime
  return timeDU
# -----------------------------------------------------------------------------
def convertFromCUC(timeDU):
  """returns python time representation from CUC binary data unit"""
  fineTime = 0.0
  duSize = len(timeDU)
  if duSize == CUC1_TIME_BYTE_SIZE:
    fineTime += timeDU.fine
    fineTime /= 0x100
  elif duSize == CUC2_TIME_BYTE_SIZE:
    fineTime += timeDU.fine
    fineTime /= 0x10000
  elif duSize == CUC3_TIME_BYTE_SIZE:
    fineTime += timeDU.fine
    fineTime /= 0x1000000
  elif duSize == CUC4_TIME_BYTE_SIZE:
    fineTime += timeDU.fine
    fineTime /= 0x100000000
  return (timeDU.coarse + fineTime)
# -----------------------------------------------------------------------------
def getERTccsdsTimeDU(pyTime):
  """convenience function for backward compatibility"""
  pyTime = correlateToERTmissionEpoch(pyTime)
  return convertToCDS(pyTime, True)
