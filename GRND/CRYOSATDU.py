#******************************************************************************
# (C) 2015, Stefan Korner, Austria                                            *
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
# Ground Simulation - CRYOSAT Data Units Module                               *
#******************************************************************************
from UTIL.DU import BITS, BYTES, UNSIGNED, BinaryUnit

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
  "padding":              (12, 2, UNSIGNED)}

###########
# classes #
###########
# =============================================================================
class TMframeDataUnit(BinaryUnit):
  """CRYOSAT telemetry frame data unit"""
  # ---------------------------------------------------------------------------
  def __init__(self, binaryString=None):
    """default constructor: initialise with header size"""
    # note: correct packetSize is not forced!
    emptyData = (binaryString == None)
    if emptyData:
      binaryString = "\0" * TM_FRAME_DU_HEADER_BYTE_SIZE
    BinaryUnit.__init__(self,
                        binaryString,
                        TM_FRAME_DU_HEADER_BYTE_SIZE,
                        TM_FRAME_DU_ATTRIBUTES)
  # ---------------------------------------------------------------------------
  def getFrame(self):
    """returns the tranfer frame"""
    # the packetSize must contain the correct size
    headerByteSize = TM_FRAME_DU_HEADER_BYTE_SIZE
    return self.getBytes(headerByteSize, self.packetSize - headerByteSize)
  # ---------------------------------------------------------------------------
  def setFrame(self, frame):
    """set the transfer frame"""
    self.setLen(TM_FRAME_DU_HEADER_BYTE_SIZE)
    self.append(frame)
