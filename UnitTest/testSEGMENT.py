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
import unittest
import CCSDS.SEGMENT, testData

#############
# test case #
#############
class TestSEGMENT_DUoperations(unittest.TestCase):
  def test(self):
    """test the transfer segment data units"""
    tcSegment1 = CCSDS.SEGMENT.TCsegment(testData.TC_SEGMENT_01)
    self.assertEqual(tcSegment1.sequenceFlags, testData.TC_SEGMENT_01_sequenceFlags)
    self.assertEqual(tcSegment1.mapId, testData.TC_SEGMENT_01_mapId)
    tcSegment2 = CCSDS.SEGMENT.TCsegment(testData.TC_SEGMENT_02)
    self.assertEqual(tcSegment2.sequenceFlags, testData.TC_SEGMENT_02_sequenceFlags)
    self.assertEqual(tcSegment2.mapId, testData.TC_SEGMENT_02_mapId)

########
# main #
########
if __name__ == "__main__":
  unittest.main()
