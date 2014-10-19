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
EPOCH_1958_SEC_DELTA = -378691200
TIME_BYTE_SIZE = 8
TIME_ATTRIBUTES = {
  "days": (0, 2, UNSIGNED),
  "mils": (2, 4, UNSIGNED),
  "mics": (6, 2, UNSIGNED)}
CMD_GPS_LEAP_SECONDS = 15
CUC_TIME_PFC17_BYTE_SIZE = 6

####################
# global variables #
####################
# shall be initialised via setMissionEpochStr()
s_tcoMissionEpochStr = ""
s_tcoMissionEpoch = 0

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
def getCCSDStimeDU(pyTime):
  """returns an 8 byte binary data unit representation of time"""
  # align it to the CCSDS epoch 1958
  pyTime -= EPOCH_1958_SEC_DELTA
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
def setMissionEpochStr(missionEpochStr):
  """sets the mission epoch string"""
  global s_tcoMissionEpochStr, s_tcoMissionEpoch
  s_tcoMissionEpochStr = missionEpochStr
  s_tcoMissionEpoch = getTimeFromASDstr(s_tcoMissionEpochStr) - CMD_GPS_LEAP_SECONDS
# -----------------------------------------------------------------------------
def correlateFromMissionEpoch(pyEpochTime):
  """correlate the mission epoch time to the local time"""
  return pyEpochTime + s_tcoMissionEpoch
# -----------------------------------------------------------------------------
def correlateCucPFC17(byteArray):
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
  return correlateFromMissionEpoch(pyEpochTime)
