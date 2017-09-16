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
# PUS Services - Packet Module                                                *
#******************************************************************************
from UTIL.DU import BITS, BYTES, UNSIGNED, STRING, TIME
import CCSDS.PACKET

#############
# constants #
#############
# =============================================================================
# the attribute dictionaries contain for each data unit attribute:
# - key: attribute name
# - value: fieldOffset, fieldLength, fieldType
# -----------------------------------------------------------------------------
TM_PACKET_DATAFIELD_HEADER_BYTE_SIZE = 3
TM_PACKET_DATAFIELD_HEADER_ATTRIBUTES = {
  "pusSpare1":            ( 0,  1, BITS),
  "pusVersionNumber":     ( 1,  3, BITS),
  "pusSpare2":            ( 4,  4, BITS),
  "serviceType":          ( 1,  1, UNSIGNED),
  "serviceSubType":       ( 2,  1, UNSIGNED)}
# -----------------------------------------------------------------------------
TC_PACKET_DATAFIELD_HEADER_BYTE_SIZE = 3
TC_PACKET_DATAFIELD_HEADER_ATTRIBUTES = {
  "pusSpare1":            ( 0,  1, BITS),
  "pusVersionNumber":     ( 1,  3, BITS),
  "ack":                  ( 4,  4, BITS),
  "serviceType":          ( 1,  1, UNSIGNED),
  "serviceSubType":       ( 2,  1, UNSIGNED)}

###########
# classes #
###########
# =============================================================================
class TMpacket(CCSDS.PACKET.TMpacket):
  """telemetry PUS packet (with datafield header)"""
  # ---------------------------------------------------------------------------
  def __init__(self, binaryString=None):
    """default constructor: initialise datafield header"""
    CCSDS.PACKET.TMpacket.__init__(self,
                                   binaryString,
                                   TM_PACKET_DATAFIELD_HEADER_BYTE_SIZE,
                                   TM_PACKET_DATAFIELD_HEADER_ATTRIBUTES)
  # ---------------------------------------------------------------------------
  def initAttributes(self):
    """hook for initializing attributes, delegates to parent class"""
    CCSDS.PACKET.TMpacket.initAttributes(self)
    self.dataFieldHeaderFlag = 1

# =============================================================================
class TCpacket(CCSDS.PACKET.TCpacket):
  """telecommand PUS packet (with datafield header)"""
  # ---------------------------------------------------------------------------
  def __init__(self, binaryString=None):
    """default constructor: initialise datafield header"""
    CCSDS.PACKET.TCpacket.__init__(self,
                                   binaryString,
                                   TC_PACKET_DATAFIELD_HEADER_BYTE_SIZE,
                                   TC_PACKET_DATAFIELD_HEADER_ATTRIBUTES)
  # ---------------------------------------------------------------------------
  def initAttributes(self):
    """hook for initializing attributes, delegates to parent class"""
    CCSDS.PACKET.TCpacket.initAttributes(self)
    self.dataFieldHeaderFlag = 1
