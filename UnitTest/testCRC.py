#!/usr/bin/env python
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
from __future__ import print_function
import UTIL.CRC, testData

#############
# functions #
#############
def test_CRCoperation():
  """function to test the CRC calculation"""
  crc = UTIL.CRC.calculate(testData.TM_PACKET_02[:-2])
  expectedCrc = (0x0100 * testData.TM_PACKET_02[-2]) + testData.TM_PACKET_02[-1]
  if crc != expectedCrc:
    print("CRC", ("%04X" % crc), "does not match the expected one: ", ("%04X" % expectedCrc))
    return False
  print("CRC =", ("%04X" % crc), " ---> OK")

  crc = UTIL.CRC.calculate(testData.TM_PACKET_03[:-2])
  expectedCrc = (0x0100 * testData.TM_PACKET_03[-2]) + testData.TM_PACKET_03[-1]
  if crc != expectedCrc:
    print("CRC", ("%04X" % crc), "does not match the expected one: ", ("%04X" % expectedCrc))
    return False
  print("CRC =", ("%04X" % crc), " ---> OK")

  crc = UTIL.CRC.calculate(testData.TM_PACKET_04[:-2])
  expectedCrc = (0x0100 * testData.TM_PACKET_04[-2]) + testData.TM_PACKET_04[-1]
  if crc != expectedCrc:
    print("CRC", ("%04X" % crc), "does not match the expected one: ", ("%04X" % expectedCrc))
    return False
  print("CRC =", ("%04X" % crc), " ---> OK")

  crc = UTIL.CRC.calculate(testData.TC_PACKET_01[:-2])
  expectedCrc = (0x0100 * testData.TC_PACKET_01[-2]) + testData.TC_PACKET_01[-1]
  if crc != expectedCrc:
    print("CRC", ("%04X" % crc), "does not match the expected one: ", ("%04X" % expectedCrc))
    return False
  print("CRC =", ("%04X" % crc), " ---> OK")




  crc = UTIL.CRC.calculate(testData.TC_FRAME_01[:-2])
  expectedCrc = (0x0100 * testData.TC_FRAME_01[-2]) + testData.TC_FRAME_01[-1]
  if crc != expectedCrc:
    print("CRC", ("%04X" % crc), "does not match the expected one: ", ("%04X" % expectedCrc))
    return False
  print("CRC =", ("%04X" % crc), " ---> OK")
  crc = UTIL.CRC.calculate(testData.TC_FRAME_02[:-2])
  expectedCrc = (0x0100 * testData.TC_FRAME_02[-2]) + testData.TC_FRAME_02[-1]
  if crc != expectedCrc:
    print("CRC", ("%04X" % crc), "does not match the expected one: ", ("%04X" % expectedCrc))
    return False
  print("CRC =", ("%04X" % crc), " ---> OK")
  return True

########
# main #
########
if __name__ == "__main__":
  print("***** test_CRCoperation() start")
  retVal = test_CRCoperation()
  print("***** test_CRCoperation() done:", retVal)
