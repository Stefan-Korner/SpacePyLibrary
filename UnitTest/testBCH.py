#!/usr/bin/env python
#******************************************************************************
# (C) 2014, Stefan Korner, Austria                                            *
#                                                                             *
# The Space Python Library is free software; you can redistribute it and/or   *
# modify it under the terms of the GNU Lesser General Public License as       *
# published by the Free Software Foundation; either version 2.1 of the        *
# License, or (at your option) any later version.                             *
#                                                                             *
# The Space C++ Library is distributed in the hope that it will be useful,    *
# but WITHOUT ANY WARRANTY; without even the implied warranty of              *
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser     *
# General Public License for more details.                                    *
#******************************************************************************
# Unit Tests                                                                  *
#******************************************************************************
import GDP.BCH, testData

#############
# functions #
#############
def test_BCHoperations():
  """function to test the BCH encoding operations"""
  sreg = GDP.BCH.encodeStart()
  sreg = GDP.BCH.encodeStep(sreg, testData.BCH_BLOCK_01[0])
  sreg = GDP.BCH.encodeStep(sreg, testData.BCH_BLOCK_01[1])
  sreg = GDP.BCH.encodeStep(sreg, testData.BCH_BLOCK_01[2])
  sreg = GDP.BCH.encodeStep(sreg, testData.BCH_BLOCK_01[3])
  sreg = GDP.BCH.encodeStep(sreg, testData.BCH_BLOCK_01[4])
  sreg = GDP.BCH.encodeStep(sreg, testData.BCH_BLOCK_01[5])
  sreg = GDP.BCH.encodeStep(sreg, testData.BCH_BLOCK_01[6])
  code = GDP.BCH.encodeStop(sreg)
  if code != testData.BCH_BLOCK_01[7]:
    print "BCH code wrong:", ("%02X" % code), "- should be", ("%02X" % testData.BCH_BLOCK_01[7])
    return False
  sreg = GDP.BCH.encodeStart()
  sreg = GDP.BCH.encodeStep(sreg, testData.BCH_BLOCK_02[0])
  sreg = GDP.BCH.encodeStep(sreg, testData.BCH_BLOCK_02[1])
  sreg = GDP.BCH.encodeStep(sreg, testData.BCH_BLOCK_02[2])
  sreg = GDP.BCH.encodeStep(sreg, testData.BCH_BLOCK_02[3])
  sreg = GDP.BCH.encodeStep(sreg, testData.BCH_BLOCK_02[4])
  sreg = GDP.BCH.encodeStep(sreg, testData.BCH_BLOCK_02[5])
  sreg = GDP.BCH.encodeStep(sreg, testData.BCH_BLOCK_02[6])
  code = GDP.BCH.encodeStop(sreg)
  if code != testData.BCH_BLOCK_02[7]:
    print "BCH code wrong:", ("%02X" % code), "- should be", ("%02X" % testData.BCH_BLOCK_02[7])
    return False
  return True

########
# main #
########
if __name__ == "__main__":
  print "***** test_BCHoperations() start"
  retVal = test_BCHoperations()
  print "***** test_BCHoperations() done:", retVal
