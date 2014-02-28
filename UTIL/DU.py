#******************************************************************************
# (C) 2014, Stefan Korner, Austria                                            *
#                                                                             *
# The Space Python Library is free software; you can redistribute it and/or   *
# modify it under the terms of the GNU Lesser General Public License as       *
# published by the Free Software Foundation; either version 2.1 of the        *
# License, or (at your option) any later version.                             *
#                                                                             *
# The Space C++ Library is distributed in the hope that it will be useful,    *
# but WITHOUT ANY WARRANTY; without even the implied warranty of              *
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser     *
# General Public License for more details.                                    *
#******************************************************************************
# Utilities - Data Unit                                                       *
#******************************************************************************
import array

#############
# constants #
#############
# field types
BITS = 0
BYTES = 1
UNSIGNED = 2

# index = [firstBitInBytePos][lastBitInBytePos]
BIT_FILTER = [
  [0x7F, 0x3F, 0x1F, 0x0F, 0x07, 0x03, 0x01, 0x00],
  [None, 0xBF, 0x9F, 0x8F, 0x87, 0x83, 0x81, 0x80],
  [None, None, 0xDF, 0xCF, 0xC7, 0xC3, 0xC1, 0xC0],
  [None, None, None, 0xEF, 0xE7, 0xE3, 0xE1, 0xE0],
  [None, None, None, None, 0xF7, 0xF3, 0xF1, 0xF0],
  [None, None, None, None, None, 0xFB, 0xF9, 0xF8],
  [None, None, None, None, None, None, 0xFD, 0xFC],
  [None, None, None, None, None, None, None, 0xFE]]
ARRAY_TYPE = type(array.array("B"))

###########
# classes #
###########
# =============================================================================
class BinaryUnit(object):
  """immutable binary data unit"""
  # ---------------------------------------------------------------------------
  def __init__(self, binaryString="", attributesSize1=None, attributeMap1=None, attributeMap2=None):
    """initialise the date structure with binaryString and attribute maps"""
    # special notation  to allow oberloading of __getattr__ and __setattr__
    if type(binaryString) == ARRAY_TYPE:
      object.__setattr__(self, "buffer", binaryString)
    else:
      object.__setattr__(self, "buffer", array.array("B", binaryString))
    object.__setattr__(self, "usedBufferSize", len(self.buffer))
    object.__setattr__(self, "attributesSize1", attributesSize1)
    object.__setattr__(self, "attributeMap1", attributeMap1)
    object.__setattr__(self, "attributeMap2", attributeMap2)
  # ---------------------------------------------------------------------------
  def getBufferString(self):
    """returns the used elements of the buffer as binary string"""
    return self.buffer[0:self.usedBufferSize].tostring()
  # ---------------------------------------------------------------------------
  def __lt__(self, other):
    """compares if self < other"""
    if other == None:
      return False
    return self.getBufferString().__lt__(other.getBufferString())
  # ---------------------------------------------------------------------------
  def __le__(self, other):
    """compares if self <= other"""
    if other == None:
      return False
    return self.getBufferString().__le__(other.getBufferString())
  # ---------------------------------------------------------------------------
  def __eq__(self, other):
    """compares if self == other"""
    if other == None:
      return False
    return self.getBufferString().__eq__(other.getBufferString())
  # ---------------------------------------------------------------------------
  def __ne__(self, other):
    """compares if self != other"""
    if other == None:
      return True
    return self.getBufferString().__ne__(other.getBufferString())
  # ---------------------------------------------------------------------------
  def __gt__(self, other):
    """compares self > other"""
    if other == None:
      return False
    return self.getBufferString().__gt__(other.getBufferString())
  # ---------------------------------------------------------------------------
  def __ge__(self, other):
    """compares if self >= other"""
    if other == None:
      return False
    return self.getBufferString().__ge-_(other.getBufferString())
  # ---------------------------------------------------------------------------
  def __str__(self):
    """returns a read-able representation"""
    retStr = array2str(self.buffer, self.usedBufferSize)
    if self.attributeMap1 != None:
      for name, fieldSpec in self.attributeMap1.iteritems():
        retStr += "\n" + name + " = "
        fieldOffset, fieldLength, fieldType = fieldSpec
        if fieldType == BITS:
          retStr += str(self.getBits(fieldOffset, fieldLength))
        elif fieldType == BYTES:
          retStr += str(self.getBytes(fieldOffset, fieldLength))
        else:
          retStr += str(self.getUnsigned(fieldOffset, fieldLength))
    if self.attributeMap2 != None:
      for name, fieldSpec in self.attributeMap2.iteritems():
        retStr += "\n" + name + " = "
        fieldOffset, fieldLength, fieldType = fieldSpec
        if fieldType == BITS:
          fieldOffset += (self.attributesSize1 << 3)
          retStr += str(self.getBits(fieldOffset, fieldLength))
        else:
          fieldOffset += self.attributesSize1
          if fieldType == BYTES:
            retStr += str(self.getBytes(fieldOffset, fieldLength))
          else:
            retStr += str(self.getUnsigned(fieldOffset, fieldLength))
    return retStr
  # ---------------------------------------------------------------------------
  def __len__(self):
    """returns the byteSize of the field"""
    return self.usedBufferSize
  # ---------------------------------------------------------------------------
  def setLen(self, byteSize):
    """change the size of the field"""
    bufferSize = len(self.buffer)
    if byteSize > bufferSize:
      # buffer must be enlarged
      enlargeSize = byteSize - bufferSize
      self.buffer.extend(array.array("B", "\0" * enlargeSize))
    object.__setattr__(self, "usedBufferSize", byteSize)
  # ---------------------------------------------------------------------------
  def append(self, binaryString, attributeMap2=None):
    """appends a binary string to the field"""
    if self.usedBufferSize > len(self.buffer):
      # unused data must be removed
      object.__setattr__(self, "buffer", self.buffer[:self.usedBufferSize])
    if type(binaryString) == ARRAY_TYPE:
      self.buffer.extend(binaryString)
    else:
      self.buffer.extend(array.array("B", binaryString))
    object.__setattr__(self, "usedBufferSize", len(self.buffer))
    if attributeMap2 != None:
      object.__setattr__(self, "attributeMap2", attributeMap2)
  # ---------------------------------------------------------------------------
  def getBits(self, bitPos, bitLength):
    """extracts bits as numerical unsigned value"""
    # performance optimizations:
    # - divide by 8 is replaced by >> 3 (performance)
    # - modulo 8 is replaced by & 7 (performance)
    # consistency checks
    if bitPos < 0:
      raise IndexError("invalid bitPos")
    if bitLength <= 0:
      raise IndexError("invalid bitLength")
    lastBitPos = bitPos + bitLength - 1
    lastBytePos = lastBitPos >> 3
    if lastBytePos >= self.usedBufferSize:
      raise IndexError("bitPos/bitLength out of buffer")
    # accumulate the number starting with the first byte
    bytePos = bitPos >> 3
    byte = self.buffer[bytePos]
    # first byte: filter the highest bits that do not belong to the value
    firstBitInBytePos = bitPos & 7
    bitFilter = (1 << (8 - firstBitInBytePos)) - 1
    value = byte & bitFilter
    # next bytes...
    bytePos += 1
    while bytePos <= lastBytePos:
      byte = self.buffer[bytePos]
      value = (value << 8) + byte
      bytePos += 1
    # last byte: remove the lowest bits that do not belong to the value
    lastBitInBytePos = lastBitPos & 7
    value >>= 7 - lastBitInBytePos
    return value
  # ---------------------------------------------------------------------------
  def setBits(self, bitPos, bitLength, value):
    """sets bits as numerical unsigned value"""
    try:
      value = long(value)
    except:
      raise ValueError("value is not an integer/long")
    # performance optimizations:
    # - divide by 8 is replaced by >> 3 (performance)
    # - modulo 8 is replaced by & 7 (performance)
    # consistency checks
    if bitPos < 0:
      raise IndexError("invalid bitPos")
    if bitLength <= 0:
      raise IndexError("invalid bitLength")
    maxValue = (1L << bitLength) - 1
    if value > maxValue:
      raise ValueError("value out of range")
    lastBitPos = bitPos + bitLength - 1
    lastBytePos = lastBitPos >> 3
    if lastBytePos >= self.usedBufferSize:
      raise IndexError("bitPos/bitLength out of buffer")
    # set zero-bits in the buffer where the value aligns
    firstBytePos = bitPos >> 3
    firstBitInBytePos = bitPos & 7
    lastBitInBytePos = lastBitPos & 7
    if firstBytePos == lastBytePos:
      bytePos = firstBytePos
      self.buffer[bytePos] &= BIT_FILTER[firstBitInBytePos][lastBitInBytePos]
    else:
      self.buffer[firstBytePos] &= BIT_FILTER[firstBitInBytePos][7]
      bytePos = firstBytePos + 1
      while bytePos < lastBytePos:
        self.buffer[bytePos] = 0
        bytePos += 1
      self.buffer[lastBytePos] &= BIT_FILTER[0][lastBitInBytePos]
    # fill value with trailing zero-bits to align with the position
    value <<= 7 - lastBitInBytePos
    # decompose the value and add it to the buffer
    # starting at bytePos, which is at the last byte
    while bytePos >= firstBytePos:
      byte = value & 0xFF
      self.buffer[bytePos] += byte
      value >>= 8
      bytePos -= 1
  # ---------------------------------------------------------------------------
  def getBytes(self, bytePos, byteLength):
    """extracts bytes"""
    # consistency checks
    if bytePos < 0:
      raise IndexError("invalid bytePos")
    if byteLength <= 0:
      raise IndexError("invalid byteLength")
    if bytePos + byteLength > self.usedBufferSize:
      raise IndexError("bytePos/byteLength out of buffer")
    return self.buffer[bytePos:bytePos+byteLength]
  # ---------------------------------------------------------------------------
  def setBytes(self, bytePos, byteLength, byteArray):
    """set bytes"""
    if type(byteArray) != ARRAY_TYPE:
      byteArray = array.array("B", byteArray)
    # consistency checks
    if bytePos < 0:
      raise IndexError("invalid bytePos")
    if byteLength <= 0:
      raise IndexError("invalid byteLength")
    if len(byteArray) > byteLength:
      raise ValueError("byteArraySize out of range")
    if bytePos + byteLength > self.usedBufferSize:
      raise IndexError("bytePos/byteLength out of buffer")
    i = 0
    while i < byteLength:
      self.buffer[bytePos + i] = byteArray[i]
      i += 1
  # ---------------------------------------------------------------------------
  def getUnsigned(self, bytePos, byteLength):
    """extracts a numerical unsigned value byte aligned"""
    # consistency checks
    if bytePos < 0:
      raise IndexError("invalid bytePos")
    if byteLength <= 0:
      raise IndexError("invalid byteLength")
    lastBytePos = bytePos + byteLength - 1
    if lastBytePos >= self.usedBufferSize:
      raise IndexError("bytePos/byteLength out of buffer")
    # accumulate the number starting with the first byte
    value = 0
    while bytePos <= lastBytePos:
      byte = self.buffer[bytePos]
      value = (value << 8) + byte
      bytePos += 1
    return value
  # ---------------------------------------------------------------------------
  def setUnsigned(self, bytePos, byteLength, value):
    """set a numerical value byte aligned"""
    # performance optimizations:
    # - multiply with 8 is replaced by << 3 (performance)
    # consistency checks
    if bytePos < 0:
      raise IndexError("invalid bytePos")
    if byteLength <= 0:
      raise IndexError("invalid byteLength")
    if value > ((1L << (byteLength << 3)) - 1):
      raise ValueError("value out of range")
    if bytePos + byteLength > self.usedBufferSize:
      raise IndexError("bytePos/byteLength out of buffer")
    # decompose the value and add it to the buffer
    # starting at bytePos, which is at the last byte
    firstBytePos = bytePos
    bytePos = firstBytePos + byteLength - 1
    while bytePos >= firstBytePos:
      byte = value & 0xFF
      self.buffer[bytePos] = byte
      value >>= 8
      bytePos -= 1
  # ---------------------------------------------------------------------------
  def __getattr__(self, name):
    """read access to the data unit attributes"""
    # try first access to fields from attribute map 1
    if self.attributeMap1 == None:
      raise AttributeError("attributeMap1 is empty")
    if name in self.attributeMap1:
      fieldOffset, fieldLength, fieldType = self.attributeMap1[name]
      if fieldType == BITS:
        return self.getBits(fieldOffset, fieldLength)
      elif fieldType == BYTES:
        return self.getBytes(fieldOffset, fieldLength)
      else:
        return self.getUnsigned(fieldOffset, fieldLength)
    # attribute not in first attribute map ---> try the second one
    if self.attributeMap2 == None:
      raise AttributeError("attribute not found")
    if self.attributesSize1 == None:
      raise AttributeError("attributeMap2 not initialised")
    if name in self.attributeMap2:
      fieldOffset, fieldLength, fieldType = self.attributeMap2[name]
      if fieldType == BITS:
        fieldOffset += (self.attributesSize1 << 3)
        return self.getBits(fieldOffset, fieldLength)
      else:
        fieldOffset += self.attributesSize1
        if fieldType == BYTES:
          return self.getBytes(fieldOffset, fieldLength)
        else:
          return self.getUnsigned(fieldOffset, fieldLength)
    # attribute not in first and second attribute map
    raise AttributeError("attribute not found")
  # ---------------------------------------------------------------------------
  def __setattr__(self, name, value):
    """write access to the data unit attributes"""
    # try first access to fields from attribute map 1
    if self.attributeMap1 == None:
      raise AttributeError("attributeMap1 is empty")
    if name in self.attributeMap1:
      fieldOffset, fieldLength, fieldType = self.attributeMap1[name]
      if fieldType == BITS:
        self.setBits(fieldOffset, fieldLength, value)
      elif fieldType == BYTES:
        self.setBytes(fieldOffset, fieldLength, value)
      else:
        self.setUnsigned(fieldOffset, fieldLength, value)
      return
    # attribute not in first attribute map ---> try the second one
    if self.attributeMap2 == None:
      raise AttributeError("attribute not found")
    if self.attributesSize1 == None:
      raise AttributeError("attributeMap2 not initialised")
    if name in self.attributeMap2:
      fieldOffset, fieldLength, fieldType = self.attributeMap2[name]
      if fieldType == BITS:
        fieldOffset += (self.attributesSize1 << 3)
        self.setBits(fieldOffset, fieldLength, value)
      else:
        fieldOffset += self.attributesSize1
        if fieldType == BYTES:
          self.setBytes(fieldOffset, fieldLength, value)
        else:
          self.setUnsigned(fieldOffset, fieldLength, value)
      return
    # attribute not in first and second attribute map
    raise AttributeError("attribute not found")

#############
# functions #
#############
def array2str(binaryString, maxLen=65536):
  """converts a binaryString into a readable data dump"""
  if type(binaryString) != ARRAY_TYPE:
    binaryString = array.array("B", binaryString)
  binaryStringSize = len(binaryString)
  if binaryStringSize == 0:
    # special output format if binaryString is empty
    return "EMPTY"
  retStr = ""
  retStr2 = ""
  i = 0
  for byte in binaryString:
    if i >= binaryStringSize:
      break
    if i >= maxLen:
      break
    if i >= 65536:
      # stop here to display only the first 64K bytes
      break
    if i % 16 == 0:
      # next 16 bytes are started
      retStr += retStr2
      retStr += ("\n%04X " % i)
      retStr2 = ""
    retStr += ("%02X " % byte)
    if byte >= 32 and byte < 127:
      # printable character
      retStr2 += chr(byte)
    else:
      # special character
      retStr2 += "."
    i += 1
  fillerSize = 15 - ((i - 1) % 16)
  filler = "   " * fillerSize
  retStr += filler + retStr2
  return retStr
