#******************************************************************************
# (C) 2017, Stefan Korner, Austria                                            *
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
# EGSE interfaces - CnC protocol Data Units Module                            *
# implements CAIT-03474-ASTR_issue_3_EGSE_IRD.pdf                             *
# The CnC packets are special CCSDS packets:                                  *
# - with version number 3                                                     *
# - without a datafield header                                                *
# - with an ASCII string as datafield                                         *
# - without a CRC                                                             *
#******************************************************************************
from UTIL.DU import BITS, BYTES, UNSIGNED, STRING, BinaryUnit
import CCSDS.PACKET

#############
# constants #
#############
VERSION_NUMBER = 3
MIN_MESSAGE_LENGTH = 0x0000 + 1
MAX_MESSAGE_LENGTH = 0xFFFF + 1

###########
# classes #
###########
# =============================================================================
class TMpacket(CCSDS.PACKET.TMpacket):
  """telemetry CnC packet"""
  # ---------------------------------------------------------------------------
  def __init__(self, binaryString=None):
    """default constructor: initialise with header size"""
    emptyData = (binaryString == None)
    CCSDS.PACKET.TMpacket.__init__(self, binaryString)
    if emptyData:
      self.versionNumber = VERSION_NUMBER
  # ---------------------------------------------------------------------------
  def getCNCmessage(self):
    """extracts a string"""
    if not self.checkPacketLength():
      raise AttributeError("inconsistent packetLength")
    stringLength = self.packetLength + 1
    return self.getString(CCSDS.PACKET.PRIMARY_HEADER_BYTE_SIZE, stringLength)
  # ---------------------------------------------------------------------------
  def setCNCmessage(self, message):
    """set a string"""
    msgLength = len(message)
    if msgLength < MIN_MESSAGE_LENGTH:
      raise AttributeError("message must contain at least 1 character")
    if msgLength > MAX_MESSAGE_LENGTH:
      raise AttributeError("message must contain at most 65536 characters")
    # resize according to the message length
    self.setLen(CCSDS.PACKET.PRIMARY_HEADER_BYTE_SIZE + msgLength)
    # fill in the message
    self.setString(CCSDS.PACKET.PRIMARY_HEADER_BYTE_SIZE, msgLength, message)
    # update CCSDS header
    self.setPacketLength()

# =============================================================================
class TCpacket(CCSDS.PACKET.TCpacket):
  """telecommand CnC packet"""
  # ---------------------------------------------------------------------------
  def __init__(self, binaryString=None):
    """default constructor: initialise with header size"""
    emptyData = (binaryString == None)
    CCSDS.PACKET.TCpacket.__init__(self, binaryString)
    if emptyData:
      self.versionNumber = VERSION_NUMBER
  # ---------------------------------------------------------------------------
  def getCNCmessage(self):
    """extracts a string"""
    if not self.checkPacketLength():
      raise AttributeError("inconsistent packetLength")
    stringLength = self.packetLength + 1
    return self.getString(CCSDS.PACKET.PRIMARY_HEADER_BYTE_SIZE, stringLength)
  # ---------------------------------------------------------------------------
  def setCNCmessage(self, message):
    """set a string"""
    msgLength = len(message)
    if msgLength < MIN_MESSAGE_LENGTH:
      raise AttributeError("message must contain at least 1 character")
    if msgLength > MAX_MESSAGE_LENGTH:
      raise AttributeError("message must contain at most 65536 characters")
    # resize according to the message length
    self.setLen(CCSDS.PACKET.PRIMARY_HEADER_BYTE_SIZE + msgLength)
    # fill in the message
    self.setString(CCSDS.PACKET.PRIMARY_HEADER_BYTE_SIZE, msgLength, message)
    # update CCSDS header
    self.setPacketLength()
