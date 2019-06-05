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
import CCSDS.FRAME, testData

#############
# test case #
#############
class TestFRAME(unittest.TestCase):
  def test(self):
    """test the transfer frame data units"""
    tmFrame0 = CCSDS.FRAME.TMframe()
    self.assertEqual(tmFrame0.versionNumber, 0)
    self.assertEqual(tmFrame0.spacecraftId, 0)
    self.assertEqual(tmFrame0.virtualChannelId, 0)
    self.assertEqual(tmFrame0.operationalControlField, 0)
    self.assertEqual(tmFrame0.masterChannelFrameCount, 0)
    self.assertEqual(tmFrame0.virtualChannelFCountLow, 0)
    self.assertEqual(tmFrame0.secondaryHeaderFlag, 0)
    self.assertEqual(tmFrame0.synchronisationFlag, 0)
    self.assertEqual(tmFrame0.packetOrderFlag, 0)
    self.assertEqual(tmFrame0.segmentLengthId, 0)
    self.assertEqual(tmFrame0.firstHeaderPointer, 0)
    tmFrame1 = CCSDS.FRAME.TMframe(testData.TM_FRAME_01)
    self.assertEqual(tmFrame1.versionNumber,
                     testData.TM_FRAME_01_versionNumber)
    self.assertEqual(tmFrame1.spacecraftId,
                     testData.TM_FRAME_01_spacecraftId)
    self.assertEqual(tmFrame1.virtualChannelId,
                     testData.TM_FRAME_01_virtualChannelId)
    self.assertEqual(tmFrame1.operationalControlField,
                     testData.TM_FRAME_01_operationalControlField)
    self.assertEqual(tmFrame1.masterChannelFrameCount,
                     testData.TM_FRAME_01_masterChannelFrameCount)
    self.assertEqual(tmFrame1.virtualChannelFCountLow,
                     testData.TM_FRAME_01_virtualChannelFCountLow)
    self.assertEqual(tmFrame1.secondaryHeaderFlag,
                     testData.TM_FRAME_01_secondaryHeaderFlag)
    self.assertEqual(tmFrame1.synchronisationFlag,
                     testData.TM_FRAME_01_synchronisationFlag)
    self.assertEqual(tmFrame1.packetOrderFlag,
                     testData.TM_FRAME_01_packetOrderFlag)
    self.assertEqual(tmFrame1.segmentLengthId,
                     testData.TM_FRAME_01_segmentLengthId)
    self.assertEqual(tmFrame1.firstHeaderPointer,
                     testData.TM_FRAME_01_firstHeaderPointer)
    # extract packets and check it
    leadingFragment, packets, trailingFragment = tmFrame1.getPackets()
    self.assertEqual(leadingFragment,
                     testData.TM_FRAME_01_leadingFragment)
    self.assertEqual(len(packets), testData.TM_FRAME_01_nrPackets)
    self.assertEqual(trailingFragment,
                     testData.TM_FRAME_01_trailingFragment)
    tcFrame1 = CCSDS.FRAME.TCframe(testData.TC_FRAME_01)
    self.assertEqual(tcFrame1.versionNumber,
                     testData.TC_FRAME_01_versionNumber)
    self.assertEqual(tcFrame1.reservedFieldB,
                     testData.TC_FRAME_01_reservedFieldB)
    self.assertEqual(tcFrame1.virtualChannelId,
                     testData.TC_FRAME_01_virtualChannelId)
    self.assertEqual(tcFrame1.controlCommandFlag,
                     testData.TC_FRAME_01_controlCommandFlag)
    self.assertEqual(tcFrame1.reservedFieldA,
                     testData.TC_FRAME_01_reservedFieldA)
    self.assertEqual(tcFrame1.frameLength,
                     testData.TC_FRAME_01_frameLength)
    self.assertEqual(tcFrame1.sequenceNumber,
                     testData.TC_FRAME_01_sequenceNumber)
    self.assertEqual(tcFrame1.spacecraftId,
                     testData.TC_FRAME_01_spacecraftId)
    self.assertEqual(tcFrame1.bypassFlag,
                     testData.TC_FRAME_01_bypassFlag)
    tcFrame2 = CCSDS.FRAME.TCframe(testData.TC_FRAME_02)
    self.assertEqual(tcFrame2.versionNumber,
                     testData.TC_FRAME_02_versionNumber)
    self.assertEqual(tcFrame2.reservedFieldB,
                     testData.TC_FRAME_02_reservedFieldB)
    self.assertEqual(tcFrame2.virtualChannelId,
                     testData.TC_FRAME_02_virtualChannelId)
    self.assertEqual(tcFrame2.controlCommandFlag,
                     testData.TC_FRAME_02_controlCommandFlag)
    self.assertEqual(tcFrame2.reservedFieldA,
                     testData.TC_FRAME_02_reservedFieldA)
    self.assertEqual(tcFrame2.frameLength,
                     testData.TC_FRAME_02_frameLength)
    self.assertEqual(tcFrame2.sequenceNumber,
                     testData.TC_FRAME_02_sequenceNumber)
    self.assertEqual(tcFrame2.spacecraftId,
                     testData.TC_FRAME_02_spacecraftId)
    self.assertEqual(tcFrame2.bypassFlag,
                     testData.TC_FRAME_02_bypassFlag)
    clcw = CCSDS.FRAME.CLCW()
    self.assertEqual(clcw.type, 0)
    self.assertEqual(clcw.version, 0)
    self.assertEqual(clcw.statusField, 0)
    self.assertEqual(clcw.copInEffect, 0)
    self.assertEqual(clcw.virtualChannelId, 0)
    self.assertEqual(clcw.spareField, 0)
    self.assertEqual(clcw.noRfAvailable, 0)
    self.assertEqual(clcw.noBitLock, 0)
    self.assertEqual(clcw.lockout, 0)
    self.assertEqual(clcw.wait, 0)
    self.assertEqual(clcw.retransmit, 0)
    self.assertEqual(clcw.farmBcounter, 0)
    self.assertEqual(clcw.reportType, 0)
    self.assertEqual(clcw.reportValue, 0)

########
# main #
########
if __name__ == "__main__":
  unittest.main()
