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
  def getTime(self, bytePos, timeFormat):
    """extracts a time"""
    # must be implemented in derived class
    raise AttributeError("time access not supported")
  # ---------------------------------------------------------------------------
  def setTime(self, bytePos, timeFormat, value):
    """set a time"""
    # must be implemented in derived class
    raise AttributeError("time access not supported")
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
