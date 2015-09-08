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
CUC_MISSION_EPOCH_STR = "1958.001.00.00.00.000"
UNIX_MISSION_EPOCH_STR = "1970.001.00.00.00.000"
GPS_LEAP_SECONDS_1980 = 0
GPS_LEAP_SECONDS_2009 = 15
GPS_LEAP_SECONDS_2012 = 16
GPS_LEAP_SECONDS_2015 = 17
TIME_BYTE_SIZE = 8
TIME_ATTRIBUTES = {
  "days": (0, 2, UNSIGNED),
  "mils": (2, 4, UNSIGNED),
  "mics": (6, 2, UNSIGNED)}
CUC_TIME_PFC17_BYTE_SIZE = 6

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
def getERTccsdsTimeDU(pyTime):
  """returns an 8 byte binary data unit representation of time"""
  pyTime = correlateToERTmissionEpoch(pyTime)
  # split seconds and micros
  secs = int(pyTime)
  mics = int(round((pyTime - secs) * 1000000))
  # convert into CCSDS components
  days = secs / (24 * 60 * 60)
  secs %= (24 * 60 * 60)
  mils = secs * 1000 + mics / 1000
  mics %= 1000
  # create the binary data
  timeDU = BinaryUnit("\0" * TIME_BYTE_SIZE, TIME_BYTE_SIZE, TIME_ATTRIBUTES)
  timeDU.days = days
  timeDU.mils = mils
  timeDU.mics = mics
  return timeDU
# -----------------------------------------------------------------------------
def correlateOBTcucPFC17(byteArray):
  """correlate the mission epoch time to the local time"""
  if len(byteArray) != CUC_TIME_PFC17_BYTE_SIZE:
    # invalid format
    return 0.0
  pyEpochTime = (byteArray[0] * 0x1000000) + \
                (byteArray[1] * 0x0010000) + \
                (byteArray[2] * 0x0000100) + \
                (byteArray[3] * 0x0000001) + \
                (byteArray[4] / 256.0) + \
                (byteArray[5] / 65535.0)
  return correlateFromOBTmissionEpoch(pyEpochTime)
