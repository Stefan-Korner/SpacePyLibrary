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
# CCSDS Stack - Data Unit                                                     *
# Implements accessors for CCSDS time attributes                              *
# and an optional CRC at the end of the data unit.                            *
#******************************************************************************
from UTIL.DU import BITS, BYTES, UNSIGNED, STRING, TIME, BinaryUnit
import CCSDS.TIME
import UTIL.CRC

#############
# constants #
#############
CRC_BYTE_SIZE = 2

###########
# classes #
###########
class DataUnit(BinaryUnit):
  """binary CCSDS data based unit"""
  # ---------------------------------------------------------------------------
  def __init__(self, binaryString=None, attributesSize1=0, attributeMap1=None, attributesSize2=0, attributeMap2=None):
    """initialise the date structure with binaryString and attribute maps"""
    BinaryUnit.__init__(self, binaryString, attributesSize1, attributeMap1, attributesSize2, attributeMap2)
  # ---------------------------------------------------------------------------
  def getTime(self, bytePos, timeFormat):
    """extracts a time"""
    byteSize = CCSDS.TIME.byteArraySize(timeFormat)
    timeData = self.getBytes(bytePos, byteSize)
    timeDU = CCSDS.TIME.createCCSDS(timeData, timeFormat)
    return CCSDS.TIME.convertFromCCSDS(timeDU, timeFormat)
  # ---------------------------------------------------------------------------
  def setTime(self, bytePos, timeFormat, value):
    """set a time"""
    timeDU = CCSDS.TIME.convertToCCSDS(value, timeFormat)
    byteSize = len(timeDU)
    timeData = timeDU.getBufferString()
    self.setBytes(bytePos, byteSize, timeData)
  # ---------------------------------------------------------------------------
  def setChecksum(self):
    """
    sets the checksum out of the binary data,
    buffer must be correctly initialised
    """
    crcPos = self.usedBufferSize - 2
    crc = UTIL.CRC.calculate(self.buffer[0:crcPos])
    self.setUnsigned(crcPos, 2, crc)
  # ---------------------------------------------------------------------------
  def checkChecksum(self):
    """
    checks the checksum out of the binary data,
    buffer must be correctly initialised
    """
    crcPos = self.usedBufferSize - 2
    crc = UTIL.CRC.calculate(self.buffer[0:crcPos])
    return self.getUnsigned(crcPos, 2) == crc
