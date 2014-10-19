#!/usr/bin/env python
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
# Unit Tests                                                                  *
#******************************************************************************
import UTIL.CRC, testData

#############
# functions #
#############
def test_CRCoperation():
  """function to test the CRC calculation"""
  crc = UTIL.CRC.calculate(testData.TC_PACKET_01[:-2])
  expectedCrc = (0x0100 * testData.TC_PACKET_01[-2]) + testData.TC_PACKET_01[-1]
  if crc != expectedCrc:
    print "CRC", ("%04X" % crc), "does not match the expected one: ", ("%04X" % expectedCrc)
    return False
  print "CRC =", ("%04X" % crc), " ---> OK"
  crc = UTIL.CRC.calculate(testData.TC_FRAME_01[:-2])
  expectedCrc = (0x0100 * testData.TC_FRAME_01[-2]) + testData.TC_FRAME_01[-1]
  if crc != expectedCrc:
    print "CRC", ("%04X" % crc), "does not match the expected one: ", ("%04X" % expectedCrc)
    return False
  print "CRC =", ("%04X" % crc), " ---> OK"
  crc = UTIL.CRC.calculate(testData.TC_FRAME_02[:-2])
  expectedCrc = (0x0100 * testData.TC_FRAME_02[-2]) + testData.TC_FRAME_02[-1]
  if crc != expectedCrc:
    print "CRC", ("%04X" % crc), "does not match the expected one: ", ("%04X" % expectedCrc)
    return False
  print "CRC =", ("%04X" % crc), " ---> OK"
  return True

########
# main #
########
if __name__ == "__main__":
  print "***** test_CRCoperation() start"
  retVal = test_CRCoperation()
  print "***** test_CRCoperation() done:", retVal
