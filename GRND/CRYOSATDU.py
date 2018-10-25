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
# Ground Simulation - CRYOSAT Data Units Module                               *
#******************************************************************************
from UTIL.DU import BITS, BYTES, UNSIGNED, STRING, TIME, BinaryUnit

#############
# constants #
#############
# =============================================================================
# the attribute dictionaries contain for each data unit attribute:
# - key: attribute name
# - value: fieldOffset, fieldLength, fieldType
# -----------------------------------------------------------------------------
TM_FRAME_DU_HEADER_BYTE_SIZE = 16
TM_FRAME_DU_ATTRIBUTES = {
  "downlinkTimeSec":      ( 0, 4, UNSIGNED),
  "downlinkTimeMicro":    ( 4, 4, UNSIGNED),
  "numberCorrSymbols":    ( 8, 4, UNSIGNED),
  "rsErorFlag":           (12, 1, UNSIGNED),
  "spare":                (13, 1, UNSIGNED),
  "padding":              (14, 2, UNSIGNED)}

###########
# classes #
###########
# =============================================================================
class TMframeDataUnit(BinaryUnit):
  """CRYOSAT telemetry frame data unit"""
  # ---------------------------------------------------------------------------
  def __init__(self, binaryString=None):
    """default constructor: initialise with header size"""
    BinaryUnit.__init__(self,
                        binaryString,
                        TM_FRAME_DU_HEADER_BYTE_SIZE,
                        TM_FRAME_DU_ATTRIBUTES)
  # ---------------------------------------------------------------------------
  def getFrame(self):
    """returns the tranfer frame"""
    headerByteSize = TM_FRAME_DU_HEADER_BYTE_SIZE
    return self.getBytes(headerByteSize, len(self) - headerByteSize)
  # ---------------------------------------------------------------------------
  def setFrame(self, frame):
    """set the transfer frame"""
    self.setLen(TM_FRAME_DU_HEADER_BYTE_SIZE)
    self.append(frame)
