#!/usr/bin/env python
#******************************************************************************
# (C) 2019, Stefan Korner, Austria                                            *
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
import SCOS.ENV, SCOS.MIB

#############
# test case #
#############
class TestMIB(unittest.TestCase):
  def test(self):
    """load MIB tables"""
    mibDir = SCOS.ENV.s_environment.mibDir()
    expectedMibDir = "../TESTENV/data/ASCII"
    self.assertEqual(mibDir, expectedMibDir)
    pidMap, picMap, tpcfMap, pcfMap, plfMap, vpdMap, ccfMap, cpcMap, cdfMap = SCOS.MIB.readAllTables()
    self.assertNotEqual(len(pidMap), 0)
    self.assertNotEqual(len(picMap), 0)
    self.assertNotEqual(len(tpcfMap), 0)
    self.assertNotEqual(len(pcfMap), 0)
    self.assertNotEqual(len(plfMap), 0)
    self.assertNotEqual(len(vpdMap), 0)
    self.assertNotEqual(len(ccfMap), 0)
    self.assertNotEqual(len(cpcMap), 0)
    self.assertNotEqual(len(cdfMap), 0)

########
# main #
########
if __name__ == "__main__":
  unittest.main()
