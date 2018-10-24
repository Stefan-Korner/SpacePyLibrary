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
import array
import CCSDS.DU, CCSDS.TIME
import UTIL.DU, UTIL.TCO, UTIL.TIME
import testData

#############
# functions #
#############
# -----------------------------------------------------------------------------
def test_DUtimeOperations():
  """function to test time operations"""
  UTIL.TCO.setOBTmissionEpochStr(UTIL.TCO.UNIX_MISSION_EPOCH_STR)
  UTIL.TCO.setOBTleapSeconds(0)
  b = CCSDS.DU.DataUnit(testData.ZERO_CUC2_TIME_FIELD,
                        testData.CUC2_TIME_DU_BYTE_SIZE,
                        testData.CUC2_TIME_DU_ATTRIBUTES)
  zeroTime = b.time
  zeroEpochTime = UTIL.TCO.correlateFromOBTmissionEpoch(zeroTime)
  if zeroEpochTime != 0:
    zeroEpochTimeStr = UTIL.TIME.getASDtimeStr(zeroEpochTime)
    print("Invalid zero epoch time:", zeroEpochTimeStr)
    return False
  UTIL.TCO.setOBTmissionEpochStr(UTIL.TCO.GPS_MISSION_EPOCH_STR)
  UTIL.TCO.setOBTleapSeconds(UTIL.TCO.GPS_LEAP_SECONDS_2009)
  b = CCSDS.DU.DataUnit(testData.CUC2_TIME1_FIELD,
                        testData.CUC2_TIME_DU_BYTE_SIZE,
                        testData.CUC2_TIME_DU_ATTRIBUTES)
  timeCorr = UTIL.TCO.correlateFromOBTmissionEpoch(b.time)
  timeStr = UTIL.TIME.getASDtimeStr(timeCorr, withMicros=True)
  if timeStr != testData.CUC2_TIME1_STR:
    print("Invalid CUC time 1:", timeStr)
    return False
  b = CCSDS.DU.DataUnit(testData.CUC2_TIME2_FIELD,
                        testData.CUC2_TIME_DU_BYTE_SIZE,
                        testData.CUC2_TIME_DU_ATTRIBUTES)
  timeCorr = UTIL.TCO.correlateFromOBTmissionEpoch(b.time)
  timeStr = UTIL.TIME.getASDtimeStr(timeCorr, withMicros=True)
  if timeStr != testData.CUC2_TIME2_STR:
    print("Invalid CUC time 2:", timeStr)
    return False
  b = CCSDS.DU.DataUnit(testData.CUC2_TIME3_FIELD,
                        testData.CUC2_TIME_DU_BYTE_SIZE,
                        testData.CUC2_TIME_DU_ATTRIBUTES)
  timeCorr = UTIL.TCO.correlateFromOBTmissionEpoch(b.time)
  timeStr = UTIL.TIME.getASDtimeStr(timeCorr, withMicros=True)
  if timeStr != testData.CUC2_TIME3_STR:
    print("Invalid CUC time 3:", timeStr)
    return False
  b = CCSDS.DU.DataUnit(testData.CUC2_TIME4_FIELD,
                        testData.CUC2_TIME_DU_BYTE_SIZE,
                        testData.CUC2_TIME_DU_ATTRIBUTES)
  timeCorr = UTIL.TCO.correlateFromOBTmissionEpoch(b.time)
  timeStr = UTIL.TIME.getASDtimeStr(timeCorr, withMicros=True)
  if timeStr != testData.CUC2_TIME4_STR:
    print("Invalid CUC time 4:", timeStr)
    return False
  b = CCSDS.DU.DataUnit(testData.CUC2_TIME5_FIELD,
                        testData.CUC2_TIME_DU_BYTE_SIZE,
                        testData.CUC2_TIME_DU_ATTRIBUTES)
  timeCorr = UTIL.TCO.correlateFromOBTmissionEpoch(b.time)
  timeStr = UTIL.TIME.getASDtimeStr(timeCorr, withMicros=True)
  if timeStr != testData.CUC2_TIME5_STR:
    print("Invalid CUC time 5:", timeStr)
    return False
  b = CCSDS.DU.DataUnit(testData.CUC2_TIME6_FIELD,
                        testData.CUC2_TIME_DU_BYTE_SIZE,
                        testData.CUC2_TIME_DU_ATTRIBUTES)
  timeCorr = UTIL.TCO.correlateFromOBTmissionEpoch(b.time)
  timeStr = UTIL.TIME.getASDtimeStr(timeCorr, withMicros=True)
  if timeStr != testData.CUC2_TIME6_STR:
    print("Invalid CUC time 6:", timeStr)
    return False
  return True
# -----------------------------------------------------------------------------
def test_DUoperations():
  """function to test the data unit operations"""
  b = UTIL.DU.BinaryUnit()
  print("b =", b)
  print("len(b) =", len(b))
  b = UTIL.DU.BinaryUnit("1234")
  print("b =", b)
  print("len(b) =", len(b))
  b.setLen(10)
  print("b =", b)
  print("len(b) =", len(b))
  b.append("Hello, world!")
  print("b =", b)
  print("len(b) =", len(b))
  b.setLen(255)
  print("b =", b)
  print("len(b) =", len(b))
  b.setLen(256)
  print("b =", b)
  print("len(b) =", len(b))
  b.setLen(257)
  print("b =", b)
  print("len(b) =", len(b))
  b = UTIL.DU.BinaryUnit("1234")
  print("b =", b)
  print("b.getBits( 0,  8) =", ("%08X" % b.getBits( 0,  8)))
  print("b.getBits( 8,  8) =", ("%08X" % b.getBits( 8,  8)))
  print("b.getBits( 8, 16) =", ("%08X" % b.getBits( 8, 16)))
  print("b.getBits(12, 16) =", ("%08X" % b.getBits(12, 16)))
  print("b.getBits( 2,  1) =", ("%08X" % b.getBits( 2,  1)))
  print("b.getBits( 2,  2) =", ("%08X" % b.getBits( 2,  2)))
  b.setBits( 0,  8, 0x00000087)
  print("b.setBits( 0,  8, 0x00000087) =", b)
  b.setBits( 8,  4, 0x00000006)
  print("b.setBits( 8,  4, 0x00000006) =", b)
  b.setBits(12, 16, 0x00005432)
  print("b.setBits(12, 16, 0x00005432) =", b)
  b.setBits(28,  4, 0x00000001)
  print("b.setBits(28,  4, 0x00000001) =", b)
  print("b.getBytes(1, 2) =", b.getBytes(1, 2))
  b.setBytes(1, 2, array.array('B', 'AB'))
  print("b.setBytes(1, 2, array.array('B', 'AB')) =", b)
  print("b.getUnsigned(1, 2) =", ("%08X" % b.getUnsigned(1, 2)))
  b.setUnsigned(0, 2, 0x00001234)
  print("b.setUnsigned(0, 2, 0x00001234) =", b)
  b = UTIL.DU.BinaryUnit(16 * 'w')
  print("b =", b)
  value = 10.0
  b.setFloat(0, 4, value)
  print("b =", b)
  if str(b) != "\n0000 41 20 00 00 77 77 77 77 77 77 77 77 77 77 77 77 A ..wwwwwwwwwwww":
    print("unexpected float encoding")
    return False
  b.setFloat(6, 8, value)
  print("b =", b)
  if str(b) != "\n0000 41 20 00 00 77 77 40 24 00 00 00 00 00 00 77 77 A ..ww@$......ww":
    print("unexpected float encoding")
    return False
  value1 = b.getFloat(0, 4)
  print("value1 =", value1)
  if value1 != value:
    print("unexpected float32 decoding")
    return False
  value2 = b.getFloat(6, 8)
  print("value2 =", value2)
  if value2 != value:
    print("unexpected float64 decoding")
    return False
  a = UTIL.DU.str2array("00 01 FF FE 64 12")
  print('str2array("00 01 FF FE 64 12") =', a)
  a = UTIL.DU.str2array("0001FFFE6412", True)
  print('str2array("0001FFFE6412", True) =', a)
  h = UTIL.DU.array2str(a)
  print("array2str([0, 1, 255, 254, 100, 18]) =", h)
  return test_DUtimeOperations()

########
# main #
########
if __name__ == "__main__":
  print("***** test_DUoperations() start")
  retVal = test_DUoperations()
  print("***** test_DUoperations() done:", retVal)
