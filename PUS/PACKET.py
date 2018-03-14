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
import CCSDS.PACKET, CCSDS.TIME

#############
# constants #
#############
VERSION_NUMBER = 0
PUS_VERSION_NUMBER = 1
# default structure of the TM packet datafield header:
#
# abs.pos | rel.pos. | unit attribute
# --------+----------+-----------------------------------------
#    6    |    0     | pusSpare1 + pusVersionNumber + pusSpare2
#    7    |    1     | serviceType
#    8    |    2     | serviceSubType
#    9    |    3     | spare
#  10-13  |   4-7    | timeTag - CUC coarse time
#  14-17  |   8-11   | timeTag - CUC fine time
#
# The position and format of the TM time tag are global properties
# that can be changed via setTMttTimeProperties()
DEFAULT_TM_TT_TIME_BYTE_OFFSET = 10
DEFAULT_TM_TT_TIME_FORMAT = CCSDS.TIME.TIME_FORMAT_CUC4
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

####################
# global variables #
####################
# The position and format of the TM time tag are global properties
# that can be changed via setTMttTimeProperties()
s_tmTTtimeByteOffset = DEFAULT_TM_TT_TIME_BYTE_OFFSET
s_tmTTtimeFormat = DEFAULT_TM_TT_TIME_FORMAT

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
    self.versionNumber = VERSION_NUMBER
    self.dataFieldHeaderFlag = 1
    self.segmentationFlags = CCSDS.PACKET.UNSEGMENTED
    self.pusVersionNumber = PUS_VERSION_NUMBER
  # ---------------------------------------------------------------------------
  def getTimeTag(self):
    """extracts the time tag (onboard time, not correlated)"""
    return self.getTime(s_tmTTtimeByteOffset, s_tmTTtimeFormat)
  # ---------------------------------------------------------------------------
  def setTimeTag(self, timeTag):
    """sets the time tag (onboard time, not correlated)"""
    self.setTime(s_tmTTtimeByteOffset, s_tmTTtimeFormat, timeTag)

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
    self.versionNumber = VERSION_NUMBER
    self.dataFieldHeaderFlag = 1
    self.segmentationFlags = CCSDS.PACKET.UNSEGMENTED
    self.pusVersionNumber = PUS_VERSION_NUMBER

#############
# functions #
#############
# -----------------------------------------------------------------------------
def setTMttTimeProperties(tmTTtimeFormatStr, tmTTtimeByteOffset):
  """changes the global (stringified) format and position of the TM time tag"""
  global s_tmTTtimeFormat, s_tmTTtimeByteOffset
  s_tmTTtimeFormat = CCSDS.TIME.timeFormat(tmTTtimeFormatStr)
  s_tmTTtimeByteOffset = tmTTtimeByteOffset

