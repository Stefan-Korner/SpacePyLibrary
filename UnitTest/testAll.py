#!/usr/bin/env python3
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
import testDU, testNCTRSDU, testBCH, testCLTU, testCRC, testFRAME, testSEGMENT
import testPACKET, testSPACE, testTIME

#############
# functions #
#############
# -----------------------------------------------------------------------------
def testOne(testFkt):
  """invocation of a single unit test"""
  print("-----", str(testFkt), "start")
  retVal = testFkt()
  print("-----", str(testFkt), "done:", retVal)
  return retVal
# -----------------------------------------------------------------------------
def testAll():
  """aggregation of unit tests"""
  if not testOne(testDU.test_DUoperations):
    return False
  if not testOne(testNCTRSDU.test_NCTRS_DUoperations):
    return False
  if not testOne(testBCH.test_BCHoperations):
    return False
  if not testOne(testCLTU.test_CLTUoperations):
    return False
  if not testOne(testCRC.test_CRCoperation):
    return False
  if not testOne(testFRAME.test_FRAME_DUoperations):
    return False
  if not testOne(testSEGMENT.test_SEGMENT_DUoperations):
    return False
  if not testOne(testPACKET.test_PACKET_DUoperations):
    return False
  if not testOne(testSPACE.test_DEFoperations):
    return False
  if not testOne(testSPACE.test_TMGENoperations):
    return False
  if not testOne(testTIME.test_TIMEoperations):
    return False
  return True

########
# main #
########
if __name__ == "__main__":
  print("***** testAll() start")
  retVal = testAll()
  print("***** testAll() done:", retVal)
