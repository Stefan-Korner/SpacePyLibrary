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
# CCSDS Stack - Unit Tests                                                    *
#******************************************************************************
import CCSDS.FRAME, testData

#############
# functions #
#############
def test_FRAME_DUoperations():
  """function to test the transfer frame data units"""
  tmFrame = CCSDS.FRAME.TMframe()
  print "tmFrame =", tmFrame
  print ""
  tcFrame1 = CCSDS.FRAME.TCframe(testData.TC_FRAME_01)
  if tcFrame1.versionNumber != testData.TC_FRAME_01_versionNumber:
    print "tcFrame1 versionNumber wrong:", tcFrame1.versionNumber, "- should be", testData.TC_FRAME_01_versionNumber
    return False
  if tcFrame1.reservedFieldB != testData.TC_FRAME_01_reservedFieldB:
    print "tcFrame1 reservedFieldB wrong:", tcFrame1.reservedFieldB, "- should be", testData.TC_FRAME_01_reservedFieldB
    return False
  if tcFrame1.virtualChannelId != testData.TC_FRAME_01_virtualChannelId:
    print "tcFrame1 virtualChannelId wrong:", tcFrame1.virtualChannelId, "- should be", testData.TC_FRAME_01_virtualChannelId
    return False
  if tcFrame1.controlCommandFlag != testData.TC_FRAME_01_controlCommandFlag:
    print "tcFrame1 controlCommandFlag wrong:", tcFrame1.controlCommandFlag, "- should be", testData.TC_FRAME_01_controlCommandFlag
    return False
  if tcFrame1.reservedFieldA != testData.TC_FRAME_01_reservedFieldA:
    print "tcFrame1 reservedFieldA wrong:", tcFrame1.reservedFieldA, "- should be", testData.TC_FRAME_01_reservedFieldA
    return False
  if tcFrame1.frameLength != testData.TC_FRAME_01_frameLength:
    print "tcFrame1 frameLength wrong:", tcFrame1.frameLength, "- should be", testData.TC_FRAME_01_frameLength
    return False
  if tcFrame1.sequenceNumber != testData.TC_FRAME_01_sequenceNumber:
    print "tcFrame1 sequenceNumber wrong:", tcFrame1.sequenceNumber, "- should be", testData.TC_FRAME_01_sequenceNumber
    return False
  if tcFrame1.spacecraftId != testData.TC_FRAME_01_spacecraftId:
    print "tcFrame1 spacecraftId wrong:", tcFrame1.spacecraftId, "- should be", testData.TC_FRAME_01_spacecraftId
    return False
  if tcFrame1.bypassFlag != testData.TC_FRAME_01_bypassFlag:
    print "tcFrame1 bypassFlag wrong:", tcFrame1.bypassFlag, "- should be", testData.TC_FRAME_01_bypassFlag
    return False
  tcFrame2 = CCSDS.FRAME.TCframe(testData.TC_FRAME_02)
  if tcFrame2.versionNumber != testData.TC_FRAME_02_versionNumber:
    print "tcFrame2 versionNumber wrong:", tcFrame2.versionNumber, "- should be", testData.TC_FRAME_02_versionNumber
    return False
  if tcFrame2.reservedFieldB != testData.TC_FRAME_02_reservedFieldB:
    print "tcFrame2 reservedFieldB wrong:", tcFrame2.reservedFieldB, "- should be", testData.TC_FRAME_02_reservedFieldB
    return False
  if tcFrame2.virtualChannelId != testData.TC_FRAME_02_virtualChannelId:
    print "tcFrame2 virtualChannelId wrong:", tcFrame2.virtualChannelId, "- should be", testData.TC_FRAME_02_virtualChannelId
    return False
  if tcFrame2.controlCommandFlag != testData.TC_FRAME_02_controlCommandFlag:
    print "tcFrame2 controlCommandFlag wrong:", tcFrame2.controlCommandFlag, "- should be", testData.TC_FRAME_02_controlCommandFlag
    return False
  if tcFrame2.reservedFieldA != testData.TC_FRAME_02_reservedFieldA:
    print "tcFrame2 reservedFieldA wrong:", tcFrame2.reservedFieldA, "- should be", testData.TC_FRAME_02_reservedFieldA
    return False
  if tcFrame2.frameLength != testData.TC_FRAME_02_frameLength:
    print "tcFrame2 frameLength wrong:", tcFrame2.frameLength, "- should be", testData.TC_FRAME_02_frameLength
    return False
  if tcFrame2.sequenceNumber != testData.TC_FRAME_02_sequenceNumber:
    print "tcFrame2 sequenceNumber wrong:", tcFrame2.sequenceNumber, "- should be", testData.TC_FRAME_02_sequenceNumber
    return False
  if tcFrame2.spacecraftId != testData.TC_FRAME_02_spacecraftId:
    print "tcFrame2 spacecraftId wrong:", tcFrame2.spacecraftId, "- should be", testData.TC_FRAME_02_spacecraftId
    return False
  if tcFrame2.bypassFlag != testData.TC_FRAME_02_bypassFlag:
    print "tcFrame2 bypassFlag wrong:", tcFrame2.bypassFlag, "- should be", testData.TC_FRAME_02_bypassFlag
    return False
  clcw = CCSDS.FRAME.CLCW()
  print "clcw =", clcw
  return True

########
# main #
########
if __name__ == "__main__":
  print "***** test_FRAME_DUoperations() start"
  retVal = test_FRAME_DUoperations()
  print "***** test_FRAME_DUoperations() done:", retVal

