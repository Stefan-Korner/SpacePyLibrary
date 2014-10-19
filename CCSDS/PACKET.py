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
# CCSDS Stack - CCSDS Packet Module                                           *
#******************************************************************************
from UTIL.DU import BITS, BYTES, UNSIGNED, BinaryUnit
import UTIL.CRC

#############
# constants #
#############
# =============================================================================
# the attribute dictionaries contain for each data unit attribute:
# - key: attribute name
# - value: fieldOffset, fieldLength, fieldType
# -----------------------------------------------------------------------------
TM_PACKET_TYPE = 0
TC_PACKET_TYPE = 1
CRC_BYTE_SIZE = 2
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

###########
# classes #
###########
# =============================================================================
class Packet(BinaryUnit):
  """telemetry or telecommand packet"""
  # ---------------------------------------------------------------------------
  def __init__(self, binaryString=None):
    """default constructor: initialise with header size"""
    emptyData = (binaryString == None)
    if emptyData:
      binaryString = "\0" * PRIMARY_HEADER_BYTE_SIZE
    BinaryUnit.__init__(self,
                        binaryString,
                        PRIMARY_HEADER_BYTE_SIZE,
                        PRIMARY_HEADER_ATTRIBUTES)
    if emptyData:
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
    crcPos = self.usedBufferSize - 2
    crc = UTIL.CRC.calculate(self.buffer[0:crcPos])
    self.setUnsigned(crcPos, 2, crc)
  # ---------------------------------------------------------------------------
  def checkChecksum(self):
    """
    checks the checksum out of the binary data,
    buffer and, packetLength must be correctly initialised
    """
    if not self.checkPacketLength():
      return False
    crcPos = self.usedBufferSize - 2
    crc = UTIL.CRC.calculate(self.buffer[0:crcPos])
    return self.getUnsigned(crcPos, 2) == crc

# =============================================================================
class TMpacket(Packet):
  """telemetry packet"""
  # ---------------------------------------------------------------------------
  def __init__(self, binaryString=None):
    """default constructor"""
    emptyData = (binaryString == None)
    Packet.__init__(self, binaryString)
    if emptyData:
      self.packetType = TM_PACKET_TYPE
      self.dataFieldHeaderFlag = 0

# =============================================================================
class TCpacket(Packet):
  """telecommand packet"""
  # ---------------------------------------------------------------------------
  def __init__(self, binaryString=None):
    """default constructor"""
    emptyData = (binaryString == None)
    Packet.__init__(self, binaryString)
    if emptyData:
      self.packetType = TC_PACKET_TYPE
      self.dataFieldHeaderFlag = 0
