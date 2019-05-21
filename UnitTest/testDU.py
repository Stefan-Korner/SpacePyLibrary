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
import array, unittest
import CCSDS.DU, CCSDS.TIME
import UTIL.DU, UTIL.TCO, UTIL.TIME
import testData

#############
# test case #
#############
class TestDU(unittest.TestCase):
  def test_DUtime(self):
    """function to test time operations"""
    UTIL.TCO.setOBTmissionEpochStr(UTIL.TCO.UNIX_MISSION_EPOCH_STR)
    UTIL.TCO.setOBTleapSeconds(0)
    b = CCSDS.DU.DataUnit(testData.ZERO_CUC2_TIME_FIELD,
                          testData.CUC2_TIME_DU_BYTE_SIZE,
                          testData.CUC2_TIME_DU_ATTRIBUTES)
    zeroTime = b.time
    zeroEpochTime = UTIL.TCO.correlateFromOBTmissionEpoch(zeroTime)
    self.assertEqual(zeroEpochTime, 0)
    UTIL.TCO.setOBTmissionEpochStr(UTIL.TCO.GPS_MISSION_EPOCH_STR)
    UTIL.TCO.setOBTleapSeconds(UTIL.TCO.GPS_LEAP_SECONDS_2009)
    b = CCSDS.DU.DataUnit(testData.CUC2_TIME1_FIELD,
                          testData.CUC2_TIME_DU_BYTE_SIZE,
                          testData.CUC2_TIME_DU_ATTRIBUTES)
    timeCorr = UTIL.TCO.correlateFromOBTmissionEpoch(b.time)
    timeStr = UTIL.TIME.getASDtimeStr(timeCorr, withMicros=True)
    self.assertEqual(timeStr, testData.CUC2_TIME1_STR)
    b = CCSDS.DU.DataUnit(testData.CUC2_TIME2_FIELD,
                          testData.CUC2_TIME_DU_BYTE_SIZE,
                          testData.CUC2_TIME_DU_ATTRIBUTES)
    timeCorr = UTIL.TCO.correlateFromOBTmissionEpoch(b.time)
    timeStr = UTIL.TIME.getASDtimeStr(timeCorr, withMicros=True)
    self.assertEqual(timeStr, testData.CUC2_TIME2_STR)
    b = CCSDS.DU.DataUnit(testData.CUC2_TIME3_FIELD,
                          testData.CUC2_TIME_DU_BYTE_SIZE,
                          testData.CUC2_TIME_DU_ATTRIBUTES)
    timeCorr = UTIL.TCO.correlateFromOBTmissionEpoch(b.time)
    timeStr = UTIL.TIME.getASDtimeStr(timeCorr, withMicros=True)
    self.assertEqual(timeStr, testData.CUC2_TIME3_STR)
    b = CCSDS.DU.DataUnit(testData.CUC2_TIME4_FIELD,
                          testData.CUC2_TIME_DU_BYTE_SIZE,
                          testData.CUC2_TIME_DU_ATTRIBUTES)
    timeCorr = UTIL.TCO.correlateFromOBTmissionEpoch(b.time)
    timeStr = UTIL.TIME.getASDtimeStr(timeCorr, withMicros=True)
    self.assertEqual(timeStr, testData.CUC2_TIME4_STR)
    b = CCSDS.DU.DataUnit(testData.CUC2_TIME5_FIELD,
                          testData.CUC2_TIME_DU_BYTE_SIZE,
                          testData.CUC2_TIME_DU_ATTRIBUTES)
    timeCorr = UTIL.TCO.correlateFromOBTmissionEpoch(b.time)
    timeStr = UTIL.TIME.getASDtimeStr(timeCorr, withMicros=True)
    self.assertEqual(timeStr, testData.CUC2_TIME5_STR)
    b = CCSDS.DU.DataUnit(testData.CUC2_TIME6_FIELD,
                          testData.CUC2_TIME_DU_BYTE_SIZE,
                          testData.CUC2_TIME_DU_ATTRIBUTES)
    timeCorr = UTIL.TCO.correlateFromOBTmissionEpoch(b.time)
    timeStr = UTIL.TIME.getASDtimeStr(timeCorr, withMicros=True)
    self.assertEqual(timeStr, testData.CUC2_TIME6_STR)
  def test_DU(self):
    """function to test the data unit operations"""
    # test UTIL.DU.fieldTypeStr()
    self.assertEqual(UTIL.DU.fieldTypeStr(UTIL.DU.BITS), "BITS")
    self.assertEqual(UTIL.DU.fieldTypeStr(UTIL.DU.SBITS), "SBITS")
    self.assertEqual(UTIL.DU.fieldTypeStr(UTIL.DU.BYTES), "BYTES")
    self.assertEqual(UTIL.DU.fieldTypeStr(UTIL.DU.UNSIGNED), "UNSIGNED")
    self.assertEqual(UTIL.DU.fieldTypeStr(UTIL.DU.SIGNED), "SIGNED")
    self.assertEqual(UTIL.DU.fieldTypeStr(UTIL.DU.FLOAT), "FLOAT")
    self.assertEqual(UTIL.DU.fieldTypeStr(UTIL.DU.TIME), "TIME")
    self.assertEqual(UTIL.DU.fieldTypeStr(UTIL.DU.STRING), "STRING")
    self.assertEqual(UTIL.DU.fieldTypeStr(99), "???")
    # other tests
    b = UTIL.DU.BinaryUnit()
    self.assertEqual(str(b), "EMPTY")
    self.assertEqual(len(b), 0)
    b = UTIL.DU.BinaryUnit("1234")
    self.assertEqual(str(b), "\n"
"0000 31 32 33 34                                     1234")
    self.assertEqual(len(b), 4)
    b.setLen(10)
    self.assertEqual(str(b), "\n"
"0000 31 32 33 34 00 00 00 00 00 00                   1234......")
    self.assertEqual(len(b), 10)
    b.append("Hello, world!")
    self.assertEqual(str(b), "\n"
"0000 31 32 33 34 00 00 00 00 00 00 48 65 6C 6C 6F 2C 1234......Hello,\n"
"0010 20 77 6F 72 6C 64 21                             world!")
    self.assertEqual(len(b), 23)
    b.setLen(255)
    self.assertEqual(str(b), "\n"
"0000 31 32 33 34 00 00 00 00 00 00 48 65 6C 6C 6F 2C 1234......Hello,\n"
"0010 20 77 6F 72 6C 64 21 00 00 00 00 00 00 00 00 00  world!.........\n"
"0020 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................\n"
"0030 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................\n"
"0040 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................\n"
"0050 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................\n"
"0060 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................\n"
"0070 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................\n"
"0080 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................\n"
"0090 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................\n"
"00A0 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................\n"
"00B0 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................\n"
"00C0 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................\n"
"00D0 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................\n"
"00E0 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................\n"
"00F0 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00    ...............")
    self.assertEqual(len(b), 255)
    b.setLen(256)
    self.assertEqual(str(b), "\n"
"0000 31 32 33 34 00 00 00 00 00 00 48 65 6C 6C 6F 2C 1234......Hello,\n"
"0010 20 77 6F 72 6C 64 21 00 00 00 00 00 00 00 00 00  world!.........\n"
"0020 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................\n"
"0030 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................\n"
"0040 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................\n"
"0050 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................\n"
"0060 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................\n"
"0070 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................\n"
"0080 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................\n"
"0090 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................\n"
"00A0 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................\n"
"00B0 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................\n"
"00C0 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................\n"
"00D0 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................\n"
"00E0 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................\n"
"00F0 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................")
    self.assertEqual(len(b), 256)
    b.setLen(257)
    self.assertEqual(str(b), "\n"
"0000 31 32 33 34 00 00 00 00 00 00 48 65 6C 6C 6F 2C 1234......Hello,\n"
"0010 20 77 6F 72 6C 64 21 00 00 00 00 00 00 00 00 00  world!.........\n"
"0020 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................\n"
"0030 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................\n"
"0040 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................\n"
"0050 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................\n"
"0060 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................\n"
"0070 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................\n"
"0080 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................\n"
"0090 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................\n"
"00A0 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................\n"
"00B0 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................\n"
"00C0 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................\n"
"00D0 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................\n"
"00E0 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................\n"
"00F0 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 ................\n"
"0100 00                                              .")
    self.assertEqual(len(b), 257)
    b = UTIL.DU.BinaryUnit("1234")
    self.assertEqual(str(b), "\n"
"0000 31 32 33 34                                     1234")
    self.assertEqual("%08X" % b.getBits( 0,  8), "00000031")
    self.assertEqual("%08X" % b.getBits( 8,  8), "00000032")
    self.assertEqual("%08X" % b.getBits( 8, 16), "00003233")
    self.assertEqual("%08X" % b.getBits(12, 16), "00002333")
    self.assertEqual("%08X" % b.getBits( 2,  1), "00000001")
    value = b.getBits(2, 2)
    self.assertEqual(value, 0x0000003)
    value = b.getSBits(2, 2)
    self.assertEqual(value, -1)
    b.setSBits(1, 7, -16)
    self.assertEqual(str(b), "\n"
"0000 70 32 33 34                                     p234")
    value = b.getBits(1, 7)
    self.assertEqual(value, 0x0000070)
    value = b.getSBits(1, 7)
    self.assertEqual(value, -16)
    b.setBits( 0,  8, 0x00000087)
    self.assertEqual(str(b), "\n"
"0000 87 32 33 34                                     .234")
    b.setBits( 8,  4, 0x00000006)
    self.assertEqual(str(b), "\n"
"0000 87 62 33 34                                     .b34")
    b.setBits(12, 16, 0x00005432)
    self.assertEqual(str(b), "\n"
"0000 87 65 43 24                                     .eC$")
    b.setBits(28,  4, 0x00000001)
    self.assertEqual(str(b), "\n"
"0000 87 65 43 21                                     .eC!")
    self.assertEqual(str(b.getBytes(1, 2)), "array('B', [101, 67])")
    b.setBytes(1, 2, array.array('B', 'AB'.encode()))
    self.assertEqual(str(b), "\n"
"0000 87 41 42 21                                     .AB!")
    value = b.getUnsigned(1, 2)
    self.assertEqual(value, 0x00004142)
    value = b.getSigned(1, 2)
    self.assertEqual(value, 0x00004142)
    b.setUnsigned(0, 2, 0x0000F234)
    self.assertEqual(str(b), "\n"
"0000 F2 34 42 21                                     .4B!")
    value = b.getUnsigned(0, 2)
    self.assertEqual(value, 0x0000F234)
    value = b.getSigned(0, 2)
    self.assertEqual(value, -3532)
    b.setSigned(0, 2, -1)
    self.assertEqual(str(b), "\n"
"0000 FF FF 42 21                                     ..B!")
    value = b.getUnsigned(0, 2)
    self.assertEqual(value, 0x0000FFFF)
    value = b.getSigned(0, 2)
    self.assertEqual(value, -1)
    b = UTIL.DU.BinaryUnit(16 * 'w')
    self.assertEqual(str(b), "\n"
"0000 77 77 77 77 77 77 77 77 77 77 77 77 77 77 77 77 wwwwwwwwwwwwwwww")
    value = 10.0
    b.setFloat(0, 4, value)
    self.assertEqual(str(b), "\n"
"0000 41 20 00 00 77 77 77 77 77 77 77 77 77 77 77 77 A ..wwwwwwwwwwww")
    b.setFloat(6, 8, value)
    self.assertEqual(str(b), "\n"
"0000 41 20 00 00 77 77 40 24 00 00 00 00 00 00 77 77 A ..ww@$......ww")
    value1 = b.getFloat(0, 4)
    self.assertEqual(str(value1), "10.0")
    self.assertEqual(value1, value)
    value2 = b.getFloat(6, 8)
    self.assertEqual(str(value2), "10.0")
    self.assertEqual(value2, value)
    a = UTIL.DU.str2array("00 01 FF FE 64 12")
    self.assertEqual(str(a), "array('B', [0, 1, 255, 254, 100, 18])")
    a = UTIL.DU.str2array("0001FFFE6412", True)
    self.assertEqual(str(a), "array('B', [0, 1, 255, 254, 100, 18])")
    h = UTIL.DU.array2str(a)
    self.assertEqual(str(h), "\n"
"0000 00 01 FF FE 64 12                               ....d.")

########
# main #
########
if __name__ == "__main__":
  unittest.main()
