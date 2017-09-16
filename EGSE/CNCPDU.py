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

###########
# classes #
###########
# =============================================================================
class TMpacket(CCSDS.PACKET.TMpacket):
  """telemetry CnC packet"""
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
class TCpacket(CCSDS.PACKET.TCpacket):
  """telecommand CnC packet"""
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
