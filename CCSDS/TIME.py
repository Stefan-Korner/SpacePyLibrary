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
# CCSDS Stack - Implements the CDS and CUC time formats                       *
#               according to CCSDS 301.0-B-4                                  *
#                                                                             *
# Note: Time format CUC4 (4 bytes coarse time and 4 bytes fine time) can only *
#       be represented in a CCSDS time p-field when the p-field extension is  *
#       used. This is only relevant when the p-field is transmitted.          *
#******************************************************************************
import time
from UTIL.DU import BITS, BYTES, UNSIGNED, STRING, TIME, BinaryUnit
import UTIL.TIME

#############
# constants #
#############
# the value of the time format maps to the CCSDS p-field
# with agency defined epoch
TIME_FORMAT_CDS1 = 0x48
TIME_FORMAT_CDS2 = 0x49
TIME_FORMAT_CUC0 = 0x2C
TIME_FORMAT_CUC1 = 0x2D
TIME_FORMAT_CUC2 = 0x2E
TIME_FORMAT_CUC3 = 0x2F
TIME_FORMAT_CUC4 = 0xFF   # non-standard p-field value
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

#############
# functions #
#############
# -----------------------------------------------------------------------------
def isCDStimeFormat(timeFormat):
  """returns True if CDS1 or CDS2"""
  return (timeFormat == TIME_FORMAT_CDS1 or timeFormat == TIME_FORMAT_CDS2)
# -----------------------------------------------------------------------------
def isCUCtimeFormat(timeFormat):
  """returns True if CUC0 or CUC1 or CUC2 or CUC3 or CUC4 """
  return (timeFormat == TIME_FORMAT_CUC0 or timeFormat == TIME_FORMAT_CUC1 or
          timeFormat == TIME_FORMAT_CUC2 or timeFormat == TIME_FORMAT_CUC3 or
          timeFormat == TIME_FORMAT_CUC4)
# -----------------------------------------------------------------------------
def timeFormat(timeFormatString):
  """returns the time format from string"""
  if timeFormatString == "CDS1":
    return TIME_FORMAT_CDS1
  if timeFormatString == "CDS2":
    return TIME_FORMAT_CDS2
  if timeFormatString == "CUC0":
    return TIME_FORMAT_CUC0
  if timeFormatString == "CUC1":
    return TIME_FORMAT_CUC1
  if timeFormatString == "CUC2":
    return TIME_FORMAT_CUC2
  if timeFormatString == "CUC3":
    return TIME_FORMAT_CUC3
  if timeFormatString == "CUC4":
    return TIME_FORMAT_CUC4
  return None
# -----------------------------------------------------------------------------
def byteArraySize(timeFormat):
  """returns the size of a byte array that can hold the raw representation"""
  if timeFormat == TIME_FORMAT_CDS1:
    return CDS1_TIME_BYTE_SIZE
  if timeFormat == TIME_FORMAT_CDS2:
    return CDS2_TIME_BYTE_SIZE
  if timeFormat == TIME_FORMAT_CUC0:
    return CUC0_TIME_BYTE_SIZE
  if timeFormat == TIME_FORMAT_CUC1:
    return CUC1_TIME_BYTE_SIZE
  if timeFormat == TIME_FORMAT_CUC2:
    return CUC2_TIME_BYTE_SIZE
  if timeFormat == TIME_FORMAT_CUC3:
    return CUC3_TIME_BYTE_SIZE
  if timeFormat == TIME_FORMAT_CUC4:
    return CUC4_TIME_BYTE_SIZE
  return None
# -----------------------------------------------------------------------------
def createCDS(byteArray):
  """returns a CDS binary data unit representation of time"""
  # note: this function determines the timeFormat from the byteArray length,
  #       createCCSDS is more secure
  if len(byteArray) == CDS1_TIME_BYTE_SIZE:
    return BinaryUnit(byteArray, CDS1_TIME_BYTE_SIZE, CDS1_TIME_ATTRIBUTES)
  elif len(byteArray) == CDS2_TIME_BYTE_SIZE:
    return BinaryUnit(byteArray, CDS2_TIME_BYTE_SIZE, CDS2_TIME_ATTRIBUTES)
  return None
# -----------------------------------------------------------------------------
def convertToCDS(pyTime, timeFormat):
  """returns a CDS binary data unit representation of time"""
  # split seconds and micros
  secs = int(pyTime)
  mics = int(round((pyTime - secs) * 1000000))
  # convert into CDS components
  days = secs / UTIL.TIME.SECONDS_OF_DAY
  secs %= UTIL.TIME.SECONDS_OF_DAY
  mils = (secs * 1000) + (mics / 1000)
  if timeFormat == TIME_FORMAT_CDS1:
    timeDU = BinaryUnit("\0" * CDS1_TIME_BYTE_SIZE,
                        CDS1_TIME_BYTE_SIZE,
                        CDS1_TIME_ATTRIBUTES)
  elif timeFormat == TIME_FORMAT_CDS2:
    mics %= 1000
    timeDU = BinaryUnit("\0" * CDS2_TIME_BYTE_SIZE,
                        CDS2_TIME_BYTE_SIZE,
                        CDS2_TIME_ATTRIBUTES)
    timeDU.mics = mics
  else:
    return None
  timeDU.days = days
  timeDU.mils = mils
  return timeDU
# -----------------------------------------------------------------------------
def convertFromCDS(timeDU):
  """returns python time representation from CDS binary data unit"""
  secs = timeDU.days * UTIL.TIME.SECONDS_OF_DAY
  mils = timeDU.mils
  secs += (mils / 1000)
  mics = 0
  if len(timeDU) == CDS2_TIME_BYTE_SIZE:
    mics = timeDU.mics
    mics += (mils % 1000) * 1000
  elif len(timeDU) != CDS1_TIME_BYTE_SIZE:
    return None
  pyTime = mics / 1000000.0
  pyTime += secs
  return pyTime
# -----------------------------------------------------------------------------
def createCUC(byteArray):
  """returns a CUC binary data unit representation of time"""
  # note: this function determines the timeFormat from the byteArray length,
  #       createCCSDS is more secure
  if len(byteArray) == CUC0_TIME_BYTE_SIZE:
    return BinaryUnit(byteArray, CUC0_TIME_BYTE_SIZE, CUC0_TIME_ATTRIBUTES)
  elif len(byteArray) == CUC1_TIME_BYTE_SIZE:
    return BinaryUnit(byteArray, CUC1_TIME_BYTE_SIZE, CUC1_TIME_ATTRIBUTES)
  elif len(byteArray) == CUC2_TIME_BYTE_SIZE:
    return BinaryUnit(byteArray, CUC2_TIME_BYTE_SIZE, CUC2_TIME_ATTRIBUTES)
  elif len(byteArray) == CUC3_TIME_BYTE_SIZE:
    return BinaryUnit(byteArray, CUC3_TIME_BYTE_SIZE, CUC3_TIME_ATTRIBUTES)
  elif len(byteArray) == CUC4_TIME_BYTE_SIZE:
    return BinaryUnit(byteArray, CUC4_TIME_BYTE_SIZE, CUC4_TIME_ATTRIBUTES)
  return None
# -----------------------------------------------------------------------------
def convertToCUC(pyTime, timeFormat):
  """returns a CUC binary data unit representation of time"""
  coarseTime = int(pyTime)
  if timeFormat == TIME_FORMAT_CUC0:
    timeDU = BinaryUnit("\0" * CUC0_TIME_BYTE_SIZE,
                        CUC0_TIME_BYTE_SIZE,
                        CUC0_TIME_ATTRIBUTES)
  elif timeFormat == TIME_FORMAT_CUC1:
    fineTime = pyTime - coarseTime
    timeDU = BinaryUnit("\0" * CUC1_TIME_BYTE_SIZE,
                        CUC1_TIME_BYTE_SIZE,
                        CUC1_TIME_ATTRIBUTES)
    timeDU.fine = int(fineTime * 0x100)
  elif timeFormat == TIME_FORMAT_CUC2:
    fineTime = pyTime - coarseTime
    timeDU = BinaryUnit("\0" * CUC2_TIME_BYTE_SIZE,
                        CUC2_TIME_BYTE_SIZE,
                        CUC2_TIME_ATTRIBUTES)
    timeDU.fine = int(fineTime * 0x10000)
  elif timeFormat == TIME_FORMAT_CUC3:
    fineTime = pyTime - coarseTime
    timeDU = BinaryUnit("\0" * CUC3_TIME_BYTE_SIZE,
                        CUC3_TIME_BYTE_SIZE,
                        CUC3_TIME_ATTRIBUTES)
    timeDU.fine = int(fineTime * 0x1000000)
  elif timeFormat == TIME_FORMAT_CUC4:
    fineTime = pyTime - coarseTime
    timeDU = BinaryUnit("\0" * CUC4_TIME_BYTE_SIZE,
                        CUC4_TIME_BYTE_SIZE,
                        CUC4_TIME_ATTRIBUTES)
    timeDU.fine = int(fineTime * 0x100000000)
  else:
    return None
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
  else:
    return None
  return (timeDU.coarse + fineTime)
# -----------------------------------------------------------------------------
def createCCSDS(byteArray, timeFormat):
  """returns a CDS or CUC binary data unit representation of time"""
  if timeFormat == TIME_FORMAT_CDS1:
    return BinaryUnit(byteArray, CDS1_TIME_BYTE_SIZE, CDS1_TIME_ATTRIBUTES)
  if timeFormat == TIME_FORMAT_CDS2:
    return BinaryUnit(byteArray, CDS2_TIME_BYTE_SIZE, CDS2_TIME_ATTRIBUTES)
  if timeFormat == TIME_FORMAT_CUC0:
    return BinaryUnit(byteArray, CUC0_TIME_BYTE_SIZE, CUC0_TIME_ATTRIBUTES)
  if timeFormat == TIME_FORMAT_CUC1:
    return BinaryUnit(byteArray, CUC1_TIME_BYTE_SIZE, CUC1_TIME_ATTRIBUTES)
  if timeFormat == TIME_FORMAT_CUC2:
    return BinaryUnit(byteArray, CUC2_TIME_BYTE_SIZE, CUC2_TIME_ATTRIBUTES)
  if timeFormat == TIME_FORMAT_CUC3:
    return BinaryUnit(byteArray, CUC3_TIME_BYTE_SIZE, CUC3_TIME_ATTRIBUTES)
  if timeFormat == TIME_FORMAT_CUC4:
    return BinaryUnit(byteArray, CUC4_TIME_BYTE_SIZE, CUC4_TIME_ATTRIBUTES)
  return None
# -----------------------------------------------------------------------------
def convertToCCSDS(pyTime, timeFormat):
  """returns a CDS or CUC binary data unit representation of time"""
  if isCDStimeFormat(timeFormat):
    return convertToCDS(pyTime, timeFormat)
  if isCUCtimeFormat(timeFormat):
    return convertToCUC(pyTime, timeFormat)
  return None
# -----------------------------------------------------------------------------
def convertFromCCSDS(timeDU, timeFormat):
  """returns python time representation from CDS or CUC binary data unit"""
  if isCDStimeFormat(timeFormat):
    return convertFromCDS(timeDU)
  if isCUCtimeFormat(timeFormat):
    return convertFromCUC(timeDU)
  return None
