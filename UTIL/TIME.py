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
# Utilities - Basic Time Conversions                                          *
#******************************************************************************
import time

#############
# constants #
#############
SECONDS_OF_DAY = (24 * 60 * 60)

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
