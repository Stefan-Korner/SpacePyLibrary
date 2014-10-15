#******************************************************************************
# (C) 2014, Stefan Korner, Austria                                            *
#                                                                             *
# The Space Python Library is free software; you can redistribute it and/or   *
# modify it under the terms of the GNU Lesser General Public License as       *
# published by the Free Software Foundation; either version 2.1 of the        *
# License, or (at your option) any later version.                             *
#                                                                             *
# The Space C++ Library is distributed in the hope that it will be useful,    *
# but WITHOUT ANY WARRANTY; without even the implied warranty of              *
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser     *
# General Public License for more details.                                    *
#******************************************************************************
# EGSE interfaces - EDEN protocol Data Units Module                           *
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
PDU_HEADER_BYTE_SIZE = 42
PDU_ATTRIBUTES = {
  "pduType":         ( 0,  4, BYTES),
  "subType":         ( 4, 10, BYTES),
  "field1":          (14, 16, BYTES),
  "field2":          (30,  4, BYTES),
  "field3":          (34,  4, BYTES),
  "dataFieldLength": (38, 4, BYTES)}

# =============================================================================
# constant values of attributes:
# -----------------------------------------------------------------------------
# possible values for
# - PDU.pduType
PDU_TYPE_TC =   "TC  "
PDU_TYPE_TC_E = "TC-E"
PDU_TYPE_TC_A = "TC-A"
PDU_TYPE_TM =   "TM  "
PDU_TYPE_TM_D = "TM-D"
PDU_TYPE_TC_D = "TC-D"
PDU_TYPE_USER = "USER"
PDU_TYPE_SEQ =  "SEQ "
PDU_TYPE_ERR =  "ERR "
PDU_TYPE_CMD =  "CMD "
PDU_TYPE_DUMP = "DUMP"
PDU_TYPE_PAR =  "PAR "
# -----------------------------------------------------------------------------
# possible values for
# - PDU.subType
SUB_TYPE_ANSW =       "ANSW      "
SUB_TYPE_CLTU =       "CLTU      "
SUB_TYPE_ENVELOPE =   "ENVELOPE  "
SUB_TYPE_ERR =        "ERR       "
SUB_TYPE_EXEC =       "EXEC      "
SUB_TYPE_FRAME =      "FRAME     "
SUB_TYPE_LOG =        "LOG       "
SUB_TYPE_PHYSICAL =   "PHYSICAL  "
SUB_TYPE_PROTOCOL =   "PROTOCOL  "
SUB_TYPE_SEGMENT =    "SEGMENT   "
SUB_TYPE_SCOE =       "SCOE      "
SUB_TYPE_SPACE =      "SPACE     "
SUB_TYPE_SPECIF_OND = "SPECIF_OND"
SUB_TYPE_STATUS =     "STATUS    "
SUB_TYPE_STOP =       "STOP      "
SUB_TYPE_TIMEOUT =    "TIMEOUT   "
SUB_TYPE_UNKNOWN =    "UNKNOWN   "

###########
# classes #
###########
# =============================================================================
class PDU(BinaryUnit):
  """Generic EDEN protocol data unit"""
  # ---------------------------------------------------------------------------
  def __init__(self, binaryString=None):
    """default constructor: initialise with header size"""
    # note: correct packetSize is not forced!
    emptyData = (binaryString == None)
    if emptyData:
      binaryString = "\0" * PDU_HEADER_BYTE_SIZE
    BinaryUnit.__init__(self,
                        binaryString,
                        PDU_HEADER_BYTE_SIZE,
                        PDU_HEADER_ATTRIBUTES)
  # ---------------------------------------------------------------------------
  def getDataField(self):
    """returns the dataField"""
    # the dataFieldSize must contain the correct size
    headerByteSize = PDU_HEADER_BYTE_SIZE
    return self.getBytes(headerByteSize, self.dataFieldSize)
  # ---------------------------------------------------------------------------
  def setDataField(self, dataField):
    """set the dataField and the dataFieldSize"""
    self.setLen(PDU_HEADER_BYTE_SIZE)
    self.append(dataField)
    self.dataFieldSize = len(dataField)
