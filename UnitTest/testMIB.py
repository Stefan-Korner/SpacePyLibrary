#!/usr/bin/env python3
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
import SCOS.ENV, SCOS.MIB

#############
# functions #
#############
# -----------------------------------------------------------------------------
def test_MIB():
  """load MIB tables"""
  mibDir = SCOS.ENV.s_environment.mibDir()
  expectedMibDir = "../TESTENV/data/ASCII"
  if mibDir != expectedMibDir:
    print("mibDir", mibDir, "does not match the expected one: ", expectedMibDir)
    return False
  pidMap, picMap, tpcfMap, pcfMap, plfMap, ccfMap, cpcMap, cdfMap = SCOS.MIB.readAllTables()
  if len(pidMap) == 0:
    print("pidMap does not contain entries")
    return False
  if len(picMap) == 0:
    print("picMap does not contain entries")
    return False
  if len(tpcfMap) == 0:
    print("tpcfMap does not contain entries")
    return False
  if len(pcfMap) == 0:
    print("pcfMap does not contain entries")
    return False
  if len(plfMap) == 0:
    print("plfMap does not contain entries")
    return False
  if len(ccfMap) == 0:
    print("ccfMap does not contain entries")
    return False
  if len(cpcMap) == 0:
    print("cpcMap does not contain entries")
    return False
  if len(cdfMap) == 0:
    print("cdfMap does not contain entries")
    return False
  return True

########
# main #
########
if __name__ == "__main__":
  print("***** test_MIB() start")
  retVal = test_MIB()
  print("***** test_MIB() done:", retVal)
