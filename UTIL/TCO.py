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
# Utilities - Time Correlation to the mission epoch for                       *
#             Onboard Time (OBT) and Earth Reception Time (ERT)               *
#******************************************************************************
import UTIL.TIME

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
def setOBTmissionEpochStr(missionEpochStr):
  """sets the OBT mission epoch string"""
  global s_optMissionEpochStr, s_obtMissionEpoch
  global s_obtLeapSeconds, s_obtMissionEpochWithLeapSeconds
  s_obtMissionEpochStr = missionEpochStr
  s_obtMissionEpoch = UTIL.TIME.getTimeFromASDstr(s_obtMissionEpochStr)
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
  s_ertMissionEpoch = UTIL.TIME.getTimeFromASDstr(s_ertMissionEpochStr)
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
