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
import array
import UTIL.DU

#############
# functions #
#############
def test_DUoperations():
  """function to test the data unit operations"""
  b = UTIL.DU.BinaryUnit()
  print "b =", b
  print "len(b) =", len(b)
  b = UTIL.DU.BinaryUnit("1234")
  print "b =", b
  print "len(b) =", len(b)
  b.setLen(10)
  print "b =", b
  print "len(b) =", len(b)
  b.append("Hello, world!")
  print "b =", b
  print "len(b) =", len(b)
  b.setLen(255)
  print "b =", b
  print "len(b) =", len(b)
  b.setLen(256)
  print "b =", b
  print "len(b) =", len(b)
  b.setLen(257)
  print "b =", b
  print "len(b) =", len(b)
  b = UTIL.DU.BinaryUnit("1234")
  print "b =", b
  print "b.getBits( 0,  8) =", ("%08X" % b.getBits( 0,  8))
  print "b.getBits( 8,  8) =", ("%08X" % b.getBits( 8,  8))
  print "b.getBits( 8, 16) =", ("%08X" % b.getBits( 8, 16))
  print "b.getBits(12, 16) =", ("%08X" % b.getBits(12, 16))
  print "b.getBits( 2,  1) =", ("%08X" % b.getBits( 2,  1))
  print "b.getBits( 2,  2) =", ("%08X" % b.getBits( 2,  2))
  b.setBits( 0,  8, 0x00000087)
  print "b.setBits( 0,  8, 0x00000087) =", b
  b.setBits( 8,  4, 0x00000006)
  print "b.setBits( 8,  4, 0x00000006) =", b
  b.setBits(12, 16, 0x00005432)
  print "b.setBits(12, 16, 0x00005432) =", b
  b.setBits(28,  4, 0x00000001)
  print "b.setBits(28,  4, 0x00000001) =", b
  print "b.getBytes(1, 2) =", b.getBytes(1, 2)
  b.setBytes(1, 2, array.array('B', 'AB'))
  print "b.setBytes(1, 2, array.array('B', 'AB')) =", b
  print "b.getUnsigned(1, 2) =", ("%08X" % b.getUnsigned(1, 2))
  b.setUnsigned(0, 2, 0x00001234)
  print "b.setUnsigned(0, 2, 0x00001234) =", b
  print UTIL.DU.str2array("00 01 FF FE 64 12")
  return True

########
# main #
########
if __name__ == "__main__":
  print "***** test_DUoperations() start"
  retVal = test_DUoperations()
  print "***** test_DUoperations() done:", retVal
