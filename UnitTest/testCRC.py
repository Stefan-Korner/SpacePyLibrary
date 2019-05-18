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
import unittest
import UTIL.CRC, testData

#############
# test case #
#############
class TestCRC(unittest.TestCase):
  def test(self):
    """test the CRC from different CCSDS packets and CCSDS frames"""
    crc = UTIL.CRC.calculate(testData.TM_PACKET_02[:-2])
    expectedCrc = (0x0100 * testData.TM_PACKET_02[-2]) + testData.TM_PACKET_02[-1]
    self.assertEqual(crc, expectedCrc)
    crc = UTIL.CRC.calculate(testData.TM_PACKET_03[:-2])
    expectedCrc = (0x0100 * testData.TM_PACKET_03[-2]) + testData.TM_PACKET_03[-1]
    self.assertEqual(crc, expectedCrc)
    crc = UTIL.CRC.calculate(testData.TM_PACKET_04[:-2])
    expectedCrc = (0x0100 * testData.TM_PACKET_04[-2]) + testData.TM_PACKET_04[-1]
    self.assertEqual(crc, expectedCrc)
    crc = UTIL.CRC.calculate(testData.TM_FRAME_01[:-2])
    expectedCrc = (0x0100 * testData.TM_FRAME_01[-2]) + testData.TM_FRAME_01[-1]
    self.assertEqual(crc, expectedCrc)
    crc = UTIL.CRC.calculate(testData.TC_PACKET_01[:-2])
    expectedCrc = (0x0100 * testData.TC_PACKET_01[-2]) + testData.TC_PACKET_01[-1]
    self.assertEqual(crc, expectedCrc)
    crc = UTIL.CRC.calculate(testData.TC_FRAME_01[:-2])
    expectedCrc = (0x0100 * testData.TC_FRAME_01[-2]) + testData.TC_FRAME_01[-1]
    self.assertEqual(crc, expectedCrc)
    crc = UTIL.CRC.calculate(testData.TC_FRAME_02[:-2])
    expectedCrc = (0x0100 * testData.TC_FRAME_02[-2]) + testData.TC_FRAME_02[-1]
    self.assertEqual(crc, expectedCrc)

########
# main #
########
if __name__ == "__main__":
  unittest.main()
