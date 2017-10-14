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
import CCSDS.PACKET

#############
# constants #
#############
VERSION_NUMBER = 3
TC_ACK_NAK_TYPE = 1
TC_ACK_SUBTYPE = 129
TC_NAK_SUBTYPE = 130
# =============================================================================
# the attribute dictionaries contain for each data unit attribute:
# - key: attribute name
# - value: fieldOffset, fieldLength, fieldType
# -----------------------------------------------------------------------------
TC_ACKNAK_DATAFIELD_HEADER_BYTE_SIZE = 3
TC_ACKNAK_DATAFIELD_HEADER_ATTRIBUTES = {
  "pusSpare1":            ( 0,  1, BITS),
  "pusVersionNumber":     ( 1,  3, BITS),
  "pusSpare2":            ( 4,  4, BITS),
  "serviceType":          ( 1,  1, UNSIGNED),
  "serviceSubType":       ( 2,  1, UNSIGNED)}

###########
# classes #
###########
# =============================================================================
class CNCcommand(CCSDS.PACKET.TCpacket):
  """CnC command"""
  # ---------------------------------------------------------------------------
  def __init__(self, binaryString=None):
    """default constructor"""
    CCSDS.PACKET.TCpacket.__init__(self, binaryString)
  # ---------------------------------------------------------------------------
  def initAttributes(self):
    """hook for initializing attributes, delegates to parent class"""
    CCSDS.PACKET.TCpacket.initAttributes(self)
    self.versionNumber = VERSION_NUMBER
  # ---------------------------------------------------------------------------
  def getCNCmessage(self):
    """extracts a string"""
    return self.getDataField().tostring()
  # ---------------------------------------------------------------------------
  def setCNCmessage(self, message):
    """set a string"""
    self.setDataField(message)

# =============================================================================
class CNCackNak(CCSDS.PACKET.TMpacket):
  """CnC command ACK/NAK response"""
  # ---------------------------------------------------------------------------
  def __init__(self, binaryString=None):
    """default constructor"""
    CCSDS.PACKET.TMpacket.__init__(self, binaryString)
  # ---------------------------------------------------------------------------
  def initAttributes(self):
    """hook for initializing attributes, delegates to parent class"""
    CCSDS.PACKET.TMpacket.initAttributes(self)
    self.versionNumber = VERSION_NUMBER
  # ---------------------------------------------------------------------------
  def getCNCmessage(self):
    """extracts a string"""
    return self.getDataField().tostring()
  # ---------------------------------------------------------------------------
  def setCNCmessage(self, message):
    """set a string"""
    self.setDataField(message)

# =============================================================================
class TCackNak(PUS.PACKET.TMpacket):
  """generic TC ACK/NAK packet"""
  # ---------------------------------------------------------------------------
  def __init__(self, binaryString=None):
    """default constructor: initialise with header size"""
    PUS.PACKET.TMpacket.__init__(self, binaryString)
  # ---------------------------------------------------------------------------
  def initAttributes(self):
    """hook for initializing attributes, delegates to parent class"""
    # resize the packet in order that it can hold the TC APID, TC SSC and CRC
    minPacketSize = PUS.SERVICES.service1_getTCackMinPacketSize()
    self.setLen(minPacketSize)
    PUS.PACKET.TMpacket.initAttributes(self)
  # ---------------------------------------------------------------------------
  def setACK(self):
    """sets ACK state"""
    self.serviceSubType = TC_ACK_SUBTYPE
  # ---------------------------------------------------------------------------
  def setNAK(self):
    """sets NAK state"""
    self.serviceSubType = TC_NAK_SUBTYPE
  # ---------------------------------------------------------------------------
  def isACK(self):
    """checks ACK state"""
    return (self.serviceSubType == TC_ACK_SUBTYPE)
  # ---------------------------------------------------------------------------
  def isNAK(self):
    """checks NAK state"""
    return (self.serviceSubType == TC_NAK_SUBTYPE)
