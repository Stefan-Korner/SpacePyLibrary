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
# CCSDS Stack - CCSDS Packet Module                                           *
#******************************************************************************
from UTIL.DU import BITS, BYTES, UNSIGNED, STRING, TIME
from UTIL.SYS import Error
import CCSDS.DU

#############
# constants #
#############
TM_PACKET_TYPE = 0
TC_PACKET_TYPE = 1
PACKET_MIN_BYTE_SIZE = 7
MIN_DATA_FIELD_BYTE_SIZE = 0x0000 + 1
MAX_DATA_FIELD_BYTE_SIZE = 0xFFFF + 1
IDLE_PKT_APID = 2047
# packet segmentation
FIRST_SEGMENT = 1
CONTINUATION_SEGMENT = 0
LAST_SEGMENT = 2
UNSEGMENTED = 3

# =============================================================================
# the attribute dictionaries contain for each data unit attribute:
# - key: attribute name
# - value: fieldOffset, fieldLength, fieldType
# -----------------------------------------------------------------------------
PRIMARY_HEADER_BYTE_SIZE = 6
PRIMARY_HEADER_ATTRIBUTES = {
  "versionNumber":        ( 0,  3, BITS),
  "packetType":           ( 3,  1, BITS),
  "dataFieldHeaderFlag":  ( 4,  1, BITS),
  "applicationProcessId": ( 5, 11, BITS),
  # byte 2
  "segmentationFlags":    (16,  2, BITS),
  "sequenceControlCount": (18, 14, BITS),
  "packetLength":         ( 4,  2, UNSIGNED)}

#############
# functions #
#############
# -----------------------------------------------------------------------------
def getDataFieldHeaderFlag(binaryString, startPos=0):
  """returns the data field header flag field"""
  if (len(binaryString) - startPos) < PRIMARY_HEADER_BYTE_SIZE:
    raise Error("packet header is too small")
  return ((binaryString[startPos + 0] & 0x08) > 0)
# -----------------------------------------------------------------------------
def getApplicationProcessId(binaryString, startPos=0):
  """returns the application process id field"""
  if (len(binaryString) - startPos) < PRIMARY_HEADER_BYTE_SIZE:
    raise Error("packet header is too small")
  return (((binaryString[startPos + 0] * 256) + binaryString[startPos + 1]) & 0x07FF)
# -----------------------------------------------------------------------------
def getPacketLength(binaryString, startPos=0):
  """returns the packet length field"""
  if (len(binaryString) - startPos) < PRIMARY_HEADER_BYTE_SIZE:
    raise Error("packet header is too small")
  return ((binaryString[startPos + 4] * 256) + binaryString[startPos + 5])
# -----------------------------------------------------------------------------
def getPacketSize(binaryString, startPos=0):
  """returns the packet size derived from the packet length field"""
  return (getPacketLength(binaryString, startPos) + 7)
# -----------------------------------------------------------------------------
def createIdlePacket(packetByteSize=PACKET_MIN_BYTE_SIZE):
  """creates an idle packet for filling space in the frame"""
  # the idle packet is a TM packet without a secondary header (CCSDS)
  # and zeros in the data field and 0 in the sequence counter
  minimumSize = PACKET_MIN_BYTE_SIZE
  if packetByteSize < PACKET_MIN_BYTE_SIZE:
    raise ValueError("binary size too small, must be >= " + str(PACKET_MIN_BYTE_SIZE))
  binaryString = "\0" * packetByteSize
  idlePacket = CCSDS.PACKET.TMpacket(binaryString)
  idlePacket.packetType = CCSDS.PACKET.TM_PACKET_TYPE
  idlePacket.setPacketLength()
  idlePacket.versionNumber = 0
  idlePacket.dataFieldHeaderFlag = 0
  idlePacket.segmentationFlags = CCSDS.PACKET.UNSEGMENTED
  idlePacket.applicationProcessId = CCSDS.PACKET.IDLE_PKT_APID
  idlePacket.sequenceControlCount = 0
  return idlePacket

###########
# classes #
###########
# =============================================================================
class Packet(CCSDS.DU.DataUnit):
  """telemetry or telecommand packet"""
  # ---------------------------------------------------------------------------
  def __init__(self, binaryString=None, attributesSize2=0, attributeMap2=None):
    """default constructor: initialise primary header"""
    CCSDS.DU.DataUnit.__init__(self,
                               binaryString,
                               PRIMARY_HEADER_BYTE_SIZE,
                               PRIMARY_HEADER_ATTRIBUTES,
                               attributesSize2,
                               attributeMap2)
  # ---------------------------------------------------------------------------
  def initAttributes(self):
    """hook for initializing attributes, delegates to parent class"""
    CCSDS.DU.DataUnit.initAttributes(self)
    self.dataFieldHeaderFlag = 0
    self.setPacketLength()
  # ---------------------------------------------------------------------------
  def getDataField(self):
    """extracts the data field"""
    if not self.checkPacketLength():
      raise AttributeError("inconsistent packetLength")
    dataFieldLength = self.packetLength + 1
    return self.getBytes(PRIMARY_HEADER_BYTE_SIZE, dataFieldLength)
  # ---------------------------------------------------------------------------
  def setDataField(self, dataField):
    """sets the data field"""
    dataFieldLength = len(dataField)
    if dataFieldLength < MIN_DATA_FIELD_BYTE_SIZE:
      raise AttributeError("data field must contain at least 1 character")
    if dataFieldLength > MAX_DATA_FIELD_BYTE_SIZE:
      raise AttributeError("data field must contain at most 65536 characters")
    # resize according to the data field length
    self.setLen(PRIMARY_HEADER_BYTE_SIZE + dataFieldLength)
    # fill in the data field
    self.setBytes(PRIMARY_HEADER_BYTE_SIZE, dataFieldLength, dataField)
    # update CCSDS header
    self.setPacketLength()
  # ---------------------------------------------------------------------------
  def setPacketLength(self):
    """sets the packetLength according to the data unit's buffer size"""
    self.packetLength = len(self) - PRIMARY_HEADER_BYTE_SIZE - 1
  # ---------------------------------------------------------------------------
  def checkPacketLength(self):
    """checks the packetLength according to the data unit's buffer size"""
    return self.packetLength == len(self) - PRIMARY_HEADER_BYTE_SIZE - 1
  # ---------------------------------------------------------------------------
  def setChecksum(self):
    """
    sets the checksum out of the binary data,
    buffer and packetLength must be correctly initialised
    """
    if not self.checkPacketLength():
      raise IndexError("inconsistent packetLength")
    CCSDS.DU.DataUnit.setChecksum(self)
  # ---------------------------------------------------------------------------
  def checkChecksum(self):
    """
    checks the checksum out of the binary data,
    buffer and packetLength must be correctly initialised
    """
    if not self.checkPacketLength():
      return False
    return CCSDS.DU.DataUnit.checkChecksum(self)

# =============================================================================
class TMpacket(Packet):
  """telemetry packet"""
  # ---------------------------------------------------------------------------
  def __init__(self, binaryString=None, attributesSize2=0, attributeMap2=None):
    """default constructor"""
    Packet.__init__(self, binaryString, attributesSize2, attributeMap2)
  # ---------------------------------------------------------------------------
  def initAttributes(self):
    """hook for initializing attributes, delegates to parent class"""
    Packet.initAttributes(self)
    self.packetType = TM_PACKET_TYPE

# =============================================================================
class TCpacket(Packet):
  """telecommand packet"""
  # ---------------------------------------------------------------------------
  def __init__(self, binaryString=None, attributesSize2=0, attributeMap2=None):
    """default constructor"""
    Packet.__init__(self, binaryString, attributesSize2, attributeMap2)
  # ---------------------------------------------------------------------------
  def initAttributes(self):
    """hook for initializing attributes, delegates to parent class"""
    Packet.initAttributes(self)
    self.packetType = TC_PACKET_TYPE
