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
# CCSDS Stack - Transfer Frame Module                                         *
#******************************************************************************
from UTIL.DU import BITS, BYTES, UNSIGNED, STRING, TIME, BinaryUnit
import CCSDS.DU

#############
# constants #
#############
CRC_CHECK = True

# =============================================================================
# the attribute dictionaries contain for each transfer frame attribute:
# - key: attribute name
# - value: fieldOffset, fieldLength, fieldType
# -----------------------------------------------------------------------------
TM_FRAME_PRIMARY_HEADER_BYTE_SIZE = 6
TM_FRAME_PRIMARY_HEADER_ATTRIBUTES = {
  "versionNumber":            ( 0,  2, BITS),
  "spacecraftId":             ( 2, 10, BITS),
  "virtualChannelId":         (12,  3, BITS),
  "operationalControlField":  (15,  1, BITS),
  "masterChannelFrameCount":  ( 2,  1, UNSIGNED),
  "virtualChannelFCountLow":  ( 3,  1, UNSIGNED),
  # byte 4
  "secondaryHeaderFlag":      (32,  1, BITS),
  "synchronisationFlag":      (33,  1, BITS),
  "packetOrderFlag":          (34,  1, BITS),
  "segmentLengthId":          (35,  2, BITS),
  "firstHeaderPointer":       (37, 11, BITS)}
# -----------------------------------------------------------------------------
TM_FRAME_SECONDARY_HEADER_BYTE_SIZE = 4
TM_FRAME_SECONDARY_HEADER_ATTRIBUTES = {
  "secondaryHeaderVersionNr": ( 0,  2, BITS),
  "secondaryHeaderSize":      ( 2,  6, BITS),
  "virtualChannelFCountHigh": ( 1,  3, UNSIGNED)}
# -----------------------------------------------------------------------------
CLCW_BYTE_SIZE = 4
CLCW_ATTRIBUTES = {
  "type":                     ( 0,  1, BITS),
  "version":                  ( 1,  2, BITS),
  "statusField":              ( 3,  3, BITS),
  "copInEffect":              ( 6,  2, BITS),
  # byte 1
  "virtualChannelId":         ( 8,  6, BITS),
  "spareField":               (14,  2, BITS),
  # byte 2
  "noRfAvailable":            (16,  1, BITS),
  "noBitLock":                (17,  1, BITS),
  "lockout":                  (18,  1, BITS),
  "wait":                     (19,  1, BITS),
  "retransmit":               (20,  1, BITS),
  "farmBcounter":             (21,  2, BITS),
  "reportType":               (23,  1, BITS),
  "reportValue":              ( 3,  1, UNSIGNED)}
# -----------------------------------------------------------------------------
TC_FRAME_HEADER_BYTE_SIZE = 5
TC_FRAME_HEADER_ATTRIBUTES = {
  "versionNumber":           ( 0,  2, BITS),
  "bypassFlag":              ( 2,  1, BITS),
  "controlCommandFlag":      ( 3,  1, BITS),
  "reservedFieldA":          ( 4,  2, BITS),
  "spacecraftId":            ( 6, 10, BITS),
  # byte 2
  "virtualChannelId":        (16,  6, BITS),
  "reservedFieldB":          (22,  2, BITS),
  "frameLength":             ( 3,  1, UNSIGNED),
  "sequenceNumber":          ( 4,  1, UNSIGNED)}

###########
# classes #
###########
# =============================================================================
class TMframe(CCSDS.DU.DataUnit):
  """telemetry transfer frame"""
  # ---------------------------------------------------------------------------
  def __init__(self, binaryString=None, enableSecondaryHeader=False):
    # default constructor: initialise with primary header size
    if enableSecondaryHeader:
      CCSDS.DU.DataUnit.__init__(self,
                                 binaryString,
                                 TM_FRAME_PRIMARY_HEADER_BYTE_SIZE,
                                 TM_FRAME_PRIMARY_HEADER_ATTRIBUTES,
                                 TM_FRAME_SECONDARY_HEADER_BYTE_SIZE,
                                 TM_FRAME_SECONDARY_HEADER_ATTRIBUTES)
    else:
      CCSDS.DU.DataUnit.__init__(self,
                                 binaryString,
                                 TM_FRAME_PRIMARY_HEADER_BYTE_SIZE,
                                 TM_FRAME_PRIMARY_HEADER_ATTRIBUTES)
  # ---------------------------------------------------------------------------
  def initAttributes(self):
    """hook for initializing attributes, delegates to parent class"""
    CCSDS.DU.DataUnit.initAttributes(self)
    if self.attributeMap2 == None:
      self.secondaryHeaderFlag = 0
    else:
      self.secondaryHeaderFlag = 1

# =============================================================================
class CLCW(BinaryUnit):
  """Command link control word"""
  # ---------------------------------------------------------------------------
  def __init__(self, binaryString=None):
    """default constructor"""
    BinaryUnit.__init__(self,
                        binaryString,
                        CLCW_BYTE_SIZE,
                        CLCW_ATTRIBUTES)

# =============================================================================
class TCframe(CCSDS.DU.DataUnit):
  """telecommand transfer frame"""
  # ---------------------------------------------------------------------------
  def __init__(self, binaryString=None):
    """default constructor"""
    CCSDS.DU.DataUnit.__init__(self,
                               binaryString,
                               TC_FRAME_HEADER_BYTE_SIZE,
                               TC_FRAME_HEADER_ATTRIBUTES)
  # ---------------------------------------------------------------------------
  def initAttributes(self):
    """hook for initializing attributes, delegates to parent class"""
    CCSDS.DU.DataUnit.initAttributes(self)
    self.clipToFrameLength()
  # ---------------------------------------------------------------------------
  def clipToFrameLength(self):
    """clip the buffer size to the size of (frameLength + 1)"""
    # the frame DU must be correctly initialised
    if self.frameLength != 0:
      self.setLen(self.frameLength + 1)
  # ---------------------------------------------------------------------------
  def getSegment(self):
    """returns the segment"""
    if self.controlCommandFlag != 0:
      raise AttributeError("getSegment() only possible when controlCommandFlag is 0")
    # the frameLength must contain the correct size
    segmentByteSize = self.frameLength + 1 - TC_FRAME_HEADER_BYTE_SIZE
    if CRC_CHECK:
      segmentByteSize -= 2
    return self.getBytes(TC_FRAME_HEADER_BYTE_SIZE, segmentByteSize)
  # ---------------------------------------------------------------------------
  def setSegment(self, segment):
    """set the CLTU and the packetSize"""
    if self.controlCommandFlag != 0:
      raise AttributeError("setSegment() only possible when controlCommandFlag is 0")
    self.setLen(TC_FRAME_HEADER_BYTE_SIZE)
    self.append(segment)
    if CRC_CHECK:
      self.append("\0" * 2)
    self.frameLength = len(self) - 1
