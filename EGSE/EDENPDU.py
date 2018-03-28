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
# EGSE interfaces - EDEN protocol Data Units Module                           *
# implements Core_EGSE_AD03_GAL_REQ_ALS_SA_R_0002_EGSE_IRD_issue2.pdf         *
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
PDU_HEADER_BYTE_SIZE = 42
PDU_HEADER_ATTRIBUTES = {
  "pduType":         ( 0,  4, STRING),
  "subType":         ( 4, 10, STRING),
  "field1":          (14, 16, STRING),
  "field2":          (30,  4, UNSIGNED),
  "field3":          (34,  4, UNSIGNED),
  "dataFieldLength": (38,  4, UNSIGNED)}
# -----------------------------------------------------------------------------
CCSDS_PDU_SEC_HEADER_BYTE_SIZE = 36
# -----------------------------------------------------------------------------
TC_SPACE_SEC_HEADER_BYTE_SIZE = CCSDS_PDU_SEC_HEADER_BYTE_SIZE
TC_SPACE_SEC_HEADER_ATTRIBUTES = {
  "structureType":         ( 0,  1, UNSIGNED),
  "channel":               ( 1,  1, UNSIGNED),
  "spare":                 ( 2,  1, BYTES),
  "telecommandType":       ( 3,  1, UNSIGNED),
  "tcIdentificationWord":  ( 4,  4, UNSIGNED),
  "telecommandOrigin":     ( 8,  1, UNSIGNED),
  "telecommandProtMode":   ( 9,  1, UNSIGNED),
  "time":                  (10, 22, BYTES),
  "mapId":                 (32,  1, UNSIGNED),
  "ancillaryInformation":  (33,  1, UNSIGNED),
  "telecommandEchoStatus": (34,  1, UNSIGNED),
  "sequenceFlags":         (35,  1, UNSIGNED)}
# -----------------------------------------------------------------------------
TC_SCOE_SEC_HEADER_BYTE_SIZE = CCSDS_PDU_SEC_HEADER_BYTE_SIZE
TC_SCOE_SEC_HEADER_ATTRIBUTES = {
  "structureType":         ( 0,  1, UNSIGNED),
  "spare1":                ( 1,  3, BYTES),
  "tcIdentificationWord":  ( 4,  4, UNSIGNED),
  "telecommandOrigin":     ( 8,  1, UNSIGNED),
  "spare2":                ( 9,  1, UNSIGNED),
  "time":                  (10, 22, BYTES),
  "spare3":                (32,  2, BYTES),
  "telecommandEchoStatus": (34,  1, UNSIGNED),
  "spare4":                (35,  1, BYTES)}
# -----------------------------------------------------------------------------
TM_SPACE_SEC_HEADER_BYTE_SIZE = CCSDS_PDU_SEC_HEADER_BYTE_SIZE
TM_SPACE_SEC_HEADER_ATTRIBUTES = {
  "structureType":            ( 0,  1, UNSIGNED),
  "channel":                  ( 1,  1, UNSIGNED),
  "dataQuality":              ( 2,  1, UNSIGNED),
  "spare1":                   ( 3,  1, BYTES),
  "clcw":                     ( 4,  4, UNSIGNED),
  "spare2":                   ( 8,  2, BYTES),
  "time":                     (10, 22, BYTES),
  "masterChannelFrameCount":  (32,  1, UNSIGNED),
  "virtualChannelFrameCount": (33,  1, UNSIGNED),
  "spare3":                   (34,  2, BYTES)}
# -----------------------------------------------------------------------------
TM_SCOE_SEC_HEADER_BYTE_SIZE = CCSDS_PDU_SEC_HEADER_BYTE_SIZE
TM_SCOE_SEC_HEADER_ATTRIBUTES = {
  "structureType":            ( 0,  1, UNSIGNED),
  "spare1":                   ( 1,  9, BYTES),
  "time":                     (10, 22, BYTES),
  "spare2":                   (32,  4, BYTES)}

# =============================================================================
# constant values of attributes:
# -----------------------------------------------------------------------------
# possible values for
# - PDU.pduType
PDU_TYPE_NULL = "????"
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
SUB_TYPE_NULL =       "??????????"
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
# -----------------------------------------------------------------------------
# possible values for
# - PDU.field1
FIELD1_NULL = "????????????????"
# -----------------------------------------------------------------------------
# possible values for TC_SPACE_SEC_HEADER / TC_SCOE_SEC_HEADER
# - TC_SPACE_SEC_HEADER.structureType
TC_SPACE_STRUCTURE_TYPE = 0
# - TC_SCOE_SEC_HEADER.structureType
TC_SCOE_STRUCTURE_TYPE = 2
# - TC_SPACE_SEC_HEADER.telecommandType
TC_TYPE_PACKET =   0
TC_TYPE_SEGMENT =  1
TC_TYPE_FRAME =    2
TC_TYPE_CLTU =     3
TC_TYPE_PHYSICAL = 4
# - TC_SPACE_SEC_HEADER.telecommandOrigin
# - TC_SCOE_SEC_HEADER.telecommandOrigin
TC_ORIGIN_LOCAL =    0
TC_ORIGIN_CCS =      1
TC_ORIGIN_OCC =      2 # only for (TC,SPACE)
TC_ORIGIN_OCC_NDIU = 3 # only for (TC,SPACE)
TC_ORIGIN_PLAYBACK = 4 # only for (TC,SPACE)
# - TC_SPACE_SEC_HEADER.telecommandProtMode
TC_PROT_MODE = 255
# - TC_SPACE_SEC_HEADER.ancillaryInformation
TC_ANCILLARY_INFORMATION = 0
# - TC_SPACE_SEC_HEADER.telecommandEchoStatus
# - TC_SCOE_SEC_HEADER.telecommandEchoStatus
TC_ECHO_STATUS_OK = 0
# - TC_SPACE_SEC_HEADER.sequenceFlags
TC_SEQUENCE_FLAGS_CONTINUATION = 0
TC_SEQUENCE_FLAGS_FIRST =        1
TC_SEQUENCE_FLAGS_LAST =         2
TC_SEQUENCE_FLAGS_UN_SEGMENTED = 3
# -----------------------------------------------------------------------------
# possible values for TM_SPACE_SEC_HEADER / TM_SCOE_SEC_HEADER
# - TM_SPACE_SEC_HEADER.structureType
TM_SPACE_STRUCTURE_TYPE = 1
# - TM_SCOE_SEC_HEADER.structureType
TM_SCOE_STRUCTURE_TYPE = 3

###########
# classes #
###########
# =============================================================================
class PDU(BinaryUnit):
  """Generic EDEN protocol data unit"""
  # ---------------------------------------------------------------------------
  def __init__(self, binaryString=None, attributesSize2=0, attributeMap2=None):
    """default constructor: initialise with header size"""
    BinaryUnit.__init__(self,
                        binaryString,
                        PDU_HEADER_BYTE_SIZE,
                        PDU_HEADER_ATTRIBUTES,
                        attributesSize2,
                        attributeMap2)
  # ---------------------------------------------------------------------------
  def initAttributes(self):
    """hook for initializing attributes, delegates to parent class"""
    BinaryUnit.initAttributes(self)
    self.pduType = PDU_TYPE_NULL
    self.subType = SUB_TYPE_NULL
    self.field1 = FIELD1_NULL
    self.setDataFieldLength()
  # ---------------------------------------------------------------------------
  def getDataField(self):
    """returns the dataField"""
    # the dataFieldSize must contain the correct size
    headerByteSize = PDU_HEADER_BYTE_SIZE
    return self.getBytes(headerByteSize, self.dataFieldLength)
  # ---------------------------------------------------------------------------
  def setDataField(self, dataField):
    """set the dataField and the dataFieldSize"""
    self.setLen(PDU_HEADER_BYTE_SIZE)
    self.append(dataField)
    self.dataFieldLength = len(dataField)
  # ---------------------------------------------------------------------------
  def setDataFieldLength(self):
    """set the dataFieldLength based on the PDU length"""
    self.dataFieldLength = len(self) - PDU_HEADER_BYTE_SIZE

# =============================================================================
class CCSDSpdu(PDU):
  """Superclass for different CCSDS PDUs"""
  # ---------------------------------------------------------------------------
  def __init__(self, binaryString=None, attributesSize2=0, attributeMap2=None):
    """default constructor"""
    PDU.__init__(self,
                 binaryString,
                 attributesSize2,
                 attributeMap2)
  # ---------------------------------------------------------------------------
  def getCCSDSpacket(self):
    """returns the CCSDS packet from data field"""
    # the dataFieldSize must contain the correct size
    headersByteSize = PDU_HEADER_BYTE_SIZE + CCSDS_PDU_SEC_HEADER_BYTE_SIZE
    return self.getBytes(headersByteSize,
                         self.dataFieldLength - CCSDS_PDU_SEC_HEADER_BYTE_SIZE)
  # ---------------------------------------------------------------------------
  def setCCSDSpacket(self, packet):
    """set the CCSDS packet in the dataField and the dataFieldSize"""
    self.setLen(PDU_HEADER_BYTE_SIZE + CCSDS_PDU_SEC_HEADER_BYTE_SIZE)
    self.append(packet)
    self.setDataFieldLength()

# =============================================================================
class TCspace(CCSDSpdu):
  """(TC,SPACE) PDU"""
  # ---------------------------------------------------------------------------
  def __init__(self, binaryString=None):
    """default constructor: initialise (TC,SPACE) secondary header"""
    CCSDSpdu.__init__(self,
                      binaryString,
                      TC_SPACE_SEC_HEADER_BYTE_SIZE,
                      TC_SPACE_SEC_HEADER_ATTRIBUTES)
  # ---------------------------------------------------------------------------
  def initAttributes(self):
    """hook for initializing attributes, delegates to parent class"""
    CCSDSpdu.initAttributes(self)
    self.pduType = PDU_TYPE_TC
    self.subType = SUB_TYPE_SPACE
    self.field1 = FIELD1_NULL
    self.structureType = TC_SPACE_STRUCTURE_TYPE
    self.telecommandType = TC_TYPE_PACKET
    self.telecommandOrigin = TC_ORIGIN_CCS
    self.telecommandProtMode = TC_PROT_MODE
    self.ancillaryInformation = TC_ANCILLARY_INFORMATION
    self.telecommandEchoStatus = TC_ECHO_STATUS_OK
    self.sequenceFlags = TC_SEQUENCE_FLAGS_UN_SEGMENTED

# =============================================================================
class TC_Espace(TCspace):
  """(TC_E,SPACE) PDU"""
  # ---------------------------------------------------------------------------
  def __init__(self, binaryString=None):
    """default constructor: delegates to TCspace"""
    TCspace.__init__(self, binaryString)
    # force this type also when the type in the binaryString is differently
    # this is needed when a (TC_E,SPACE) is cloned from a (TC,SPACE)
    self.pduType = PDU_TYPE_TC_E
  # ---------------------------------------------------------------------------
  def initAttributes(self):
    """hook for initializing attributes, delegates to parent class"""
    TCspace.initAttributes(self)
    self.pduType = PDU_TYPE_TC_E

# =============================================================================
class TCscoe(CCSDSpdu):
  """(TC,SCOE) PDU"""
  # ---------------------------------------------------------------------------
  def __init__(self, binaryString=None):
    """default constructor: initialise (TC,SCOE) secondary header"""
    CCSDSpdu.__init__(self,
                      binaryString,
                      TC_SCOE_SEC_HEADER_BYTE_SIZE,
                      TC_SCOE_SEC_HEADER_ATTRIBUTES)
  # ---------------------------------------------------------------------------
  def initAttributes(self):
    """hook for initializing attributes, delegates to parent class"""
    CCSDSpdu.initAttributes(self)
    self.setDataFieldLength()
    self.pduType = PDU_TYPE_TC
    self.subType = SUB_TYPE_SCOE
    self.field1 = FIELD1_NULL
    self.structureType = TC_SCOE_STRUCTURE_TYPE
    self.telecommandOrigin = TC_ORIGIN_CCS
    self.telecommandEchoStatus = TC_ECHO_STATUS_OK

# =============================================================================
class TC_Escoe(TCscoe):
  """(TC_E,SCOE) PDU"""
  # ---------------------------------------------------------------------------
  def __init__(self, binaryString=None):
    """default constructor: delegates to TCscoe"""
    TCscoe.__init__(self, binaryString)
    # force this type also when the type in the binaryString is differently
    # this is needed when a (TC_E,SCOE) is cloned from a (TC,SCOE)
    self.pduType = PDU_TYPE_TC_E
  # ---------------------------------------------------------------------------
  def initAttributes(self):
    """hook for initializing attributes, delegates to parent class"""
    TCscoe.initAttributes(self)
    self.pduType = PDU_TYPE_TC_E

# =============================================================================
class TMspace(CCSDSpdu):
  """(TM,SPACE) PDU"""
  # ---------------------------------------------------------------------------
  def __init__(self, binaryString=None):
    """default constructor: initialise (TM,SPACE) secondary header"""
    CCSDSpdu.__init__(self,
                      binaryString,
                      TM_SPACE_SEC_HEADER_BYTE_SIZE,
                      TM_SPACE_SEC_HEADER_ATTRIBUTES)
  # ---------------------------------------------------------------------------
  def initAttributes(self):
    """hook for initializing attributes, delegates to parent class"""
    CCSDSpdu.initAttributes(self)
    self.pduType = PDU_TYPE_TM
    self.subType = SUB_TYPE_SPACE
    self.field1 = FIELD1_NULL
    self.structureType = TM_SPACE_STRUCTURE_TYPE

# =============================================================================
class TMscoe(CCSDSpdu):
  """(TM,SCOE) PDU"""
  # ---------------------------------------------------------------------------
  def __init__(self, binaryString=None):
    """default constructor: initialise (TM,SCOE) secondary header"""
    CCSDSpdu.__init__(self,
                      binaryString,
                      TM_SCOE_SEC_HEADER_BYTE_SIZE,
                      TM_SCOE_SEC_HEADER_ATTRIBUTES)
  # ---------------------------------------------------------------------------
  def initAttributes(self):
    """hook for initializing attributes, delegates to parent class"""
    CCSDSpdu.initAttributes(self)
    self.pduType = PDU_TYPE_TM
    self.subType = SUB_TYPE_SCOE
    self.field1 = FIELD1_NULL
    self.structureType = TM_SCOE_STRUCTURE_TYPE
