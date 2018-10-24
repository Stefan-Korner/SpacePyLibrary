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
# CCSDS Stack - Telecommand Segmentation Module                               *
#******************************************************************************
from UTIL.DU import BITS, BYTES, UNSIGNED, STRING, TIME, BinaryUnit

#############
# constants #
#############
# =============================================================================
# the attribute dictionaries contain for each TC segment attribute:
# - key: attribute name
# - value: fieldOffset, fieldLength, fieldType
# -----------------------------------------------------------------------------
TC_SEGMENT_HEADER_BYTE_SIZE = 1
TC_SEGMENT_HEADER_ATTRIBUTES = {
  "sequenceFlags":            (0, 2, BITS),
  "mapId":                    (2, 6, BITS)}
FIRST_SEGMENT = 1
CONTINUATION_SEGMENT = 0
LAST_SEGMENT = 2
UNSEGMENTED = 3

# =============================================================================
# constant values of attributes:
# -----------------------------------------------------------------------------
# possible values for
# - TCsegment.sequenceFlags
FIRST_PORTION = 1
MIDDLE_PORTION = 0
LAST_PORTION = 2
UNSEGMENTED = 3

###########
# classes #
###########
# =============================================================================
class TCsegment(BinaryUnit):
  """Telecommand segment"""
  # ---------------------------------------------------------------------------
  def __init__(self, binaryString=None):
    """default constructor"""
    BinaryUnit.__init__(self,
                        binaryString,
                        TC_SEGMENT_HEADER_BYTE_SIZE,
                        TC_SEGMENT_HEADER_ATTRIBUTES)
  # ---------------------------------------------------------------------------
  def getTCpacketData(self):
    """returns the TC packet data"""
    packetDataLength = len(self) - TC_SEGMENT_HEADER_BYTE_SIZE
    return self.getBytes(TC_SEGMENT_HEADER_BYTE_SIZE, packetDataLength)
  # ---------------------------------------------------------------------------
  def setTCpacketData(self, tcPacketData):
    """set the TC packet data"""
    self.setLen(TC_SEGMENT_HEADER_BYTE_SIZE)
    self.append(tcPacketData)
