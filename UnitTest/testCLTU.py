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
# CCSDS Stack - Unit Tests                                                    *
#******************************************************************************
import array, unittest
import CCSDS.CLTU, testData

#############
# test case #
#############
class TestCLTU(unittest.TestCase):
  def test(self):
    """test the BCH encoding operations"""
    frame1a = array.array("B", testData.TC_FRAME_01)
    cltu1 = CCSDS.CLTU.encodeCltu(frame1a)
    okState, msg = CCSDS.CLTU.checkCltu(cltu1)
    self.assertTrue(okState)
    self.assertEqual(cltu1, array.array("B", testData.CLTU_01))
    frame1b = CCSDS.CLTU.decodeCltu(cltu1)
    self.assertIsNotNone(frame1b)
    # ignore the fill bytes
    self.assertEqual(frame1a, frame1b[:len(frame1a)])
    frame2a = array.array("B", testData.TC_FRAME_02)
    cltu2 = CCSDS.CLTU.encodeCltu(frame2a)
    okState, msg = CCSDS.CLTU.checkCltu(cltu2)
    self.assertTrue(okState)
    self.assertEqual(cltu2, array.array("B", testData.CLTU_02))
    frame2b = CCSDS.CLTU.decodeCltu(cltu2)
    self.assertIsNotNone(frame2b)
    # ignore the fill bytes
    self.assertEqual(frame2a, frame2b[:len(frame2a)])

########
# main #
########
if __name__ == "__main__":
  unittest.main()
