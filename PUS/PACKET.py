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
from UTIL.DU import BITS, BYTES, UNSIGNED, BinaryUnit
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
    """default constructor: initialise with header size"""
    emptyData = (binaryString == None)
    if emptyData:
      binaryString = "\0" * (CCSDS.PACKET.PRIMARY_HEADER_BYTE_SIZE +
                             TM_PACKET_DATAFIELD_HEADER_BYTE_SIZE)
    BinaryUnit.__init__(self,
                        binaryString,
                        CCSDS.PACKET.PRIMARY_HEADER_BYTE_SIZE,
                        CCSDS.PACKET.PRIMARY_HEADER_ATTRIBUTES,
                        TM_PACKET_DATAFIELD_HEADER_ATTRIBUTES)
    if emptyData:
      self.setPacketLength()
      self.packetType = CCSDS.PACKET.TM_PACKET_TYPE
      self.dataFieldHeaderFlag = 1

# =============================================================================
class TCpacket(CCSDS.PACKET.TCpacket):
  """telecommand PUS packet (with datafield header)"""
  # ---------------------------------------------------------------------------
  def __init__(self, binaryString=None):
    """default constructor: initialise with header size"""
    emptyData = (binaryString == None)
    if emptyData:
      binaryString = "\0" * (CCSDS.PACKET.PRIMARY_HEADER_BYTE_SIZE +
                             TC_PACKET_DATAFIELD_HEADER_BYTE_SIZE)
    BinaryUnit.__init__(self,
                        binaryString,
                        CCSDS.PACKET.PRIMARY_HEADER_BYTE_SIZE,
                        CCSDS.PACKET.PRIMARY_HEADER_ATTRIBUTES,
                        TC_PACKET_DATAFIELD_HEADER_ATTRIBUTES)
    if emptyData:
      self.setPacketLength()
      self.packetType = CCSDS.PACKET.TC_PACKET_TYPE
      self.dataFieldHeaderFlag = 1
