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
# CCSDS Stack - Unit Tests                                                    *
#******************************************************************************
import array
import CCSDS.CLTU, testData

#############
# functions #
#############
def test_CLTUoperations():
  """function to test the BCH encoding operations"""
  frame1a = array.array("B", testData.TC_FRAME_01)
  cltu1 = CCSDS.CLTU.encodeCltu(frame1a)
  okState, msg = CCSDS.CLTU.checkCltu(cltu1)
  if not okState:
    print("CLTU 1 check failed:", msg)
    return False
  if cltu1 != array.array("B", testData.CLTU_01):
    print("CLTU 1 does not match the expected one")
    return False
  frame1b = CCSDS.CLTU.decodeCltu(cltu1)
  if frame1b == None:
    print("CLTU 1 decoding failed")
    return False
  # ignore the fill bytes
  if frame1a != frame1b[:len(frame1a)]:
    print("CLTU 1 encoding and decoding not symmetrical")
    return False
  frame2a = array.array("B", testData.TC_FRAME_02)
  cltu2 = CCSDS.CLTU.encodeCltu(frame2a)
  okState, msg = CCSDS.CLTU.checkCltu(cltu2)
  if not okState:
    print("CLTU 2 check failed:", msg)
    return False
  if cltu2 != array.array("B", testData.CLTU_02):
    print("CLTU 2 does not match the expected one")
    return False
  frame2b = CCSDS.CLTU.decodeCltu(cltu2)
  if frame2b == None:
    print("CLTU 2 decoding failed")
    return False
  # ignore the fill bytes
  if frame2a != frame2b[:len(frame2a)]:
    print("CLTU 2 encoding and decoding not symmetrical")
    return False
  return True

########
# main #
########
if __name__ == "__main__":
  print("***** test_CLTUoperations() start")
  retVal = test_CLTUoperations()
  print("***** test_CLTUoperations() done:", retVal)
