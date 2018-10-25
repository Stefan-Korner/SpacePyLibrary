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
import CCSDS.FRAME, testData

#############
# functions #
#############
def test_FRAME_DUoperations():
  """function to test the transfer frame data units"""
  tmFrame0 = CCSDS.FRAME.TMframe()
  print "tmFrame0 =", tmFrame0
  print ""
  tmFrame1 = CCSDS.FRAME.TMframe(testData.TM_FRAME_01)
  print "tmFrame1 =", tmFrame1
  if tmFrame1.versionNumber != testData.TM_FRAME_01_versionNumber:
    print "tmFrame1 versionNumber wrong:", tmFrame1.versionNumber, "- should be", testData.TM_FRAME_01_versionNumber
    return False
  if tmFrame1.spacecraftId != testData.TM_FRAME_01_spacecraftId:
    print "tmFrame1 spacecraftId wrong:", tmFrame1.spacecraftId, "- should be", testData.TM_FRAME_01_spacecraftId
    return False
  if tmFrame1.virtualChannelId != testData.TM_FRAME_01_virtualChannelId:
    print "tmFrame1 virtualChannelId wrong:", tmFrame1.virtualChannelId, "- should be", testData.TM_FRAME_01_virtualChannelId
    return False
  if tmFrame1.operationalControlField != testData.TM_FRAME_01_operationalControlField:
    print "tmFrame1 operationalControlField wrong:", tmFrame1.operationalControlField, "- should be", testData.TM_FRAME_01_operationalControlField
    return False
  if tmFrame1.masterChannelFrameCount != testData.TM_FRAME_01_masterChannelFrameCount:
    print "tmFrame1 masterChannelFrameCount wrong:", tmFrame1.masterChannelFrameCount, "- should be", testData.TM_FRAME_01_masterChannelFrameCount
    return False
  if tmFrame1.virtualChannelFCountLow != testData.TM_FRAME_01_virtualChannelFCountLow:
    print "tmFrame1 virtualChannelFCountLow wrong:", tmFrame1.virtualChannelFCountLow, "- should be", testData.TM_FRAME_01_virtualChannelFCountLow
    return False
  if tmFrame1.secondaryHeaderFlag != testData.TM_FRAME_01_secondaryHeaderFlag:
    print "tmFrame1 secondaryHeaderFlag wrong:", tmFrame1.secondaryHeaderFlag, "- should be", testData.TM_FRAME_01_secondaryHeaderFlag
    return False
  if tmFrame1.synchronisationFlag != testData.TM_FRAME_01_synchronisationFlag:
    print "tmFrame1 synchronisationFlag wrong:", tmFrame1.synchronisationFlag, "- should be", testData.TM_FRAME_01_synchronisationFlag
    return False
  if tmFrame1.packetOrderFlag != testData.TM_FRAME_01_packetOrderFlag:
    print "tmFrame1 packetOrderFlag wrong:", tmFrame1.packetOrderFlag, "- should be", testData.TM_FRAME_01_packetOrderFlag
    return False
  if tmFrame1.segmentLengthId != testData.TM_FRAME_01_segmentLengthId:
    print "tmFrame1 segmentLengthId wrong:", tmFrame1.segmentLengthId, "- should be", testData.TM_FRAME_01_segmentLengthId
    return False
  if tmFrame1.firstHeaderPointer != testData.TM_FRAME_01_firstHeaderPointer:
    print "tmFrame1 firstHeaderPointer wrong:", tmFrame1.firstHeaderPointer, "- should be", testData.TM_FRAME_01_firstHeaderPointer
    return False
  # extract packets and check it
  leadingFragment, packets, trailingFragment = tmFrame1.getPackets()
  if leadingFragment != testData.TM_FRAME_01_leadingFragment:
    print "tmFrame1 leadingFragment wrong:", leadingFragment, "- should be", testData.TM_FRAME_01_leadingFragment
    return False
  if len(packets) != testData.TM_FRAME_01_nrPackets:
    print "tmFrame1 nr. of packets wrong:", len(packets), "- should be", testData.TM_FRAME_01_nrPackets
    return False
  if trailingFragment != testData.TM_FRAME_01_trailingFragment:
    print "tmFrame1 trailingFragment wrong:", trailingFragment, "- should be", testData.TM_FRAME_01_trailingFragment
    return False
  print ""
  tcFrame1 = CCSDS.FRAME.TCframe(testData.TC_FRAME_01)
  print "tcFrame1 =", tcFrame1
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

