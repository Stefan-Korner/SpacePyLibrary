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
import CCSDS.SEGMENT, testData

#############
# functions #
#############
def test_SEGMENT_DUoperations():
  """function to test the transfer segment data units"""
  tcSegment1 = CCSDS.SEGMENT.TCsegment(testData.TC_SEGMENT_01)
  if tcSegment1.sequenceFlags != testData.TC_SEGMENT_01_sequenceFlags:
    print("tcSegment1 sequenceFlags wrong:", tcSegment1.sequenceFlags, "- should be", testData.TC_SEGMENT_01_sequenceFlags)
    return False
  if tcSegment1.mapId != testData.TC_SEGMENT_01_mapId:
    print("tcSegment1 mapId wrong:", tcSegment1.mapId, "- should be", testData.TC_SEGMENT_01_mapId)
    return False
  tcSegment2 = CCSDS.SEGMENT.TCsegment(testData.TC_SEGMENT_02)
  if tcSegment2.sequenceFlags != testData.TC_SEGMENT_02_sequenceFlags:
    print("tcSegment2 sequenceFlags wrong:", tcSegment2.sequenceFlags, "- should be", testData.TC_SEGMENT_02_sequenceFlags)
    return False
  if tcSegment2.mapId != testData.TC_SEGMENT_02_mapId:
    print("tcSegment2 mapId wrong:", tcSegment2.mapId, "- should be", testData.TC_SEGMENT_02_mapId)
    return False
  return True

########
# main #
########
if __name__ == "__main__":
  print("***** test_SEGMENT_DUoperations() start")
  retVal = test_SEGMENT_DUoperations()
  print("***** test_SEGMENT_DUoperations() done:", retVal)
