#******************************************************************************
# (C) 2019, Stefan Korner, Austria                                            *
#                                                                             *
# The Space Python Library is free software; you can redistribute it and/or   *
# modify it under under the terms of the MIT License as published by the      *
# Massachusetts Institute of Technology.                                      *
#                                                                             *
# The Space Python Library is distributed in the hope that it will be useful, *
# but WITHOUT ANY WARRANTY; without even the implied warranty of              *
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the MIT License    *
# for more details.                                                           *
#******************************************************************************
# PUS Services - Variable packet support                                      *
#******************************************************************************
from UTIL.SYS import Error
import UTIL.DU, UTIL.TIME

####################
# definition level #
####################

# =============================================================================
class ParamDef(object):
  """Contains the most important definition data of a variable packet parameter"""
  # ---------------------------------------------------------------------------
  def __init__(self, paramName, defaultValue, isReadOnly):
    self.paramName = paramName
    self.defaultValue = defaultValue
    self.isReadOnly = isReadOnly
  # ---------------------------------------------------------------------------
  def __str__(self, indent="ParamDef"):
    """string representation"""
    if self.isReadOnly:
      return ("\n" + indent + "." + self.paramName + " = " + str(self.defaultValue) + " RO")
    else:
      return ("\n" + indent + "." + self.paramName + " = " + str(self.defaultValue) + " RW")
  # ---------------------------------------------------------------------------
  def getParamType(self):
    """accessor"""
    pass
  # ---------------------------------------------------------------------------
  def getBitWidth(self):
    """accessor"""
    pass

# =============================================================================
class SimpleParamDef(ParamDef):
  """Contains the most important definition data of a variable packet parameter"""
  # ---------------------------------------------------------------------------
  def __init__(self, paramName, paramType, bitWidth, defaultValue, isReadOnly):
    ParamDef.__init__(self, paramName, defaultValue, isReadOnly)
    self.paramType = paramType
    self.bitWidth = bitWidth
  # ---------------------------------------------------------------------------
  def __str__(self, indent="SimpleParamDef"):
    """string representation"""
    if self.isReadOnly:
      return ("\n" + indent + "." + self.paramName + " = " + UTIL.DU.fieldTypeStr(self.paramType) + ", " + str(self.bitWidth) + ", " + str(self.defaultValue) + " RO")
    else:
      return ("\n" + indent + "." + self.paramName + " = " + UTIL.DU.fieldTypeStr(self.paramType) + ", " + str(self.bitWidth) + ", " + str(self.defaultValue) + " RW")
  # ---------------------------------------------------------------------------
  def getParamType(self):
    """accessor"""
    return self.paramType
  # ---------------------------------------------------------------------------
  def getBitWidth(self):
    """accessor"""
    return self.bitWidth

# =============================================================================
class VariableParamDef(ParamDef):
  """Contains the most important definition data of a variable size packet parameter"""
  # ---------------------------------------------------------------------------
  def __init__(self, paramName, paramType, lengthBytes, defaultValue, isReadOnly):
    ParamDef.__init__(self, paramName, defaultValue, isReadOnly)
    self.paramType = paramType
    self.lengthBytes = lengthBytes
  # ---------------------------------------------------------------------------
  def __str__(self, indent="VariableParamDef"):
    """string representation"""
    if self.isReadOnly:
      return ("\n" + indent + "." + self.paramName + " = " + UTIL.DU.fieldTypeStr(self.paramType) + ", " + str(self.lengthBytes) + ", " + str(self.defaultValue) + " RO")
    else:
      return ("\n" + indent + "." + self.paramName + " = " + UTIL.DU.fieldTypeStr(self.paramType) + ", " + str(self.lengthBytes) + ", " + str(self.defaultValue) + " RW")
  # ---------------------------------------------------------------------------
  def getParamType(self):
    """accessor"""
    return self.paramType
  # ---------------------------------------------------------------------------
  def getBitWidth(self):
    """accessor"""
    return 0

# =============================================================================
class TimeParamDef(ParamDef):
  """Contains the most important definition data of a variable packet parameter"""
  # ---------------------------------------------------------------------------
  def __init__(self, paramName, timeFormat, defaultValue, isReadOnly):
    ParamDef.__init__(self, paramName, defaultValue, isReadOnly)
    self.timeFormat = timeFormat
  # ---------------------------------------------------------------------------
  def __str__(self, indent="TimeParamDef"):
    """string representation"""
    if self.isReadOnly:
      return ("\n" + indent + "." + self.paramName + " = " + CCSDS.TIME.timeFormatString(self.timeFormat) + ", " + str(self.defaultValue) + " RO")
    else:
      return ("\n" + indent + "." + self.paramName + " = " + CCSDS.TIME.timeFormatString(self.timeFormat) + ", " + str(self.defaultValue) + " RW")
  # ---------------------------------------------------------------------------
  def getParamType(self):
    """accessor"""
    return UTIL.DU.TIME
  # ---------------------------------------------------------------------------
  def getBitWidth(self):
    """accessor"""
    return CCSDS.TIME.byteArraySize(self.timeFormat) << 3 

# =============================================================================
class SlotDef(object):
  """Definition of a slot in a struct"""
  # ---------------------------------------------------------------------------
  def __init__(self, slotName, childDef):
    self.slotName = slotName
    self.childDef = childDef
  # ---------------------------------------------------------------------------
  def __str__(self, indent="SlotDef"):
    """string representation"""
    return self.childDef.__str__(indent + "." + self.slotName)

# =============================================================================
class StructDef(object):
  """Definition of a struct in a variable packet"""
  # ---------------------------------------------------------------------------
  def __init__(self, structName, sortedSlotDefs):
    self.structName = structName
    self.slotDefs = tuple(sortedSlotDefs)
    self.slotMap = {}
    slotPos = 0
    for slotDef in self.slotDefs:
      self.slotMap[slotDef.slotName] = slotPos
      slotPos += 1
  # ---------------------------------------------------------------------------
  def __str__(self, indent="StructDef"):
    """string representation"""
    if self.structName != "":
      indent = indent + "." + self.structName
    retStr = ""
    for slotDef in self.slotDefs:
      retStr += slotDef.__str__(indent)
    return retStr
  # ---------------------------------------------------------------------------
  def getSlotPos(self, slotName):
    """position of a slot in the struct"""
    return self.slotMap[slotName]

# =============================================================================
class ListDef(object):
  """Definition of a list in a variable packet"""
  # ---------------------------------------------------------------------------
  def __init__(self, lenParamDef, entryDef):
    self.lenParamDef = lenParamDef
    self.entryDef = entryDef
  # ---------------------------------------------------------------------------
  def __str__(self, indent="ListDef"):
    """string representation"""
    retStr = self.lenParamDef.__str__(indent + ".len")
    retStr += self.entryDef.__str__(indent + "[*]")
    return retStr

################
# entity level #
################

# =============================================================================
class Entity(object):
  """Superclass of all entities"""
  # ---------------------------------------------------------------------------
  def getBitWidth(self):
    """accessor, shall be implemented in derived classes"""
    pass
  # ---------------------------------------------------------------------------
  def encode(self, du, bitPos):
    """
    encodes the contens into a data unit, returns the new position
    shall be implemented in derived classes
    """
    pass
  # ---------------------------------------------------------------------------
  def decode(self, du, bitPos):
    """
    decodes the contens from a data unit, returns the new position
    shall be implemented in derived classes
    """
    pass

# =============================================================================
class Param(Entity):
  """Variable packet parameter"""
  # ---------------------------------------------------------------------------
  def __init__(self, paramDef):
    self.paramDef = paramDef
    self.value = paramDef.defaultValue
  # ---------------------------------------------------------------------------
  def __str__(self, indent="Param"):
    """string representation"""
    return ("\n" + indent + " = " + str(self.value))
  # ---------------------------------------------------------------------------
  def getParamName(self):
    """accessor"""
    return self.paramDef.paramName
  # ---------------------------------------------------------------------------
  def getParamType(self):
    """accessor"""
    return self.paramDef.getParamType()
  # ---------------------------------------------------------------------------
  def getBitWidth(self):
    """accessor, overloaded from Entity"""
    # special processing of variable size parameters
    defType = type(self.paramDef)
    if defType == VariableParamDef:
      byteWidth = self.paramDef.lengthBytes + len(self.value)
      return byteWidth << 3
    # default processing
    return self.paramDef.getBitWidth()
  # ---------------------------------------------------------------------------
  def isReadOnly(self):
    """accessor"""
    return self.paramDef.isReadOnly
  # ---------------------------------------------------------------------------
  def encode(self, du, bitPos):
    """
    encodes the contens into a data unit, returns the new position
    overloaded from Entity
    """
    paramType = self.getParamType()
    bitWidth = self.getBitWidth()
    value = self.value
    nextBitPos = bitPos + bitWidth
    # process bit oriented parameter types
    if paramType == UTIL.DU.BITS:
      du.setBits(bitPos, bitWidth, value)
      return nextBitPos
    if paramType == UTIL.DU.SBITS:
      du.setSBits(bitPos, bitWidth, value)
      return nextBitPos
    # process byte oriented parameter types
    if (bitPos % 8) != 0:
      raise Error("parameter " + self.getParamName() + " position is not byte aligned")
    if (bitWidth % 8) != 0:
      raise Error("parameter " + self.getParamName() + " size is not byte aligned")
    bytePos = bitPos >> 3
    byteWidth = bitWidth >> 3
    defType = type(self.paramDef)
    if defType == VariableParamDef:
      # for variable length parameters: encode the length bytes first
      lengthBytes = self.paramDef.lengthBytes
      byteLength = len(value)
      du.setUnsigned(bytePos, lengthBytes, byteLength)
      bytePos += lengthBytes
      byteWidth = byteLength      
    if paramType == UTIL.DU.BYTES:
      du.setBytes(bytePos, byteWidth, value)
      return nextBitPos
    if paramType == UTIL.DU.UNSIGNED:
      du.setUnsigned(bytePos, byteWidth, value)
      return nextBitPos
    if paramType == UTIL.DU.SIGNED:
      du.setSigned(bytePos, byteWidth, value)
      return nextBitPos
    if paramType == UTIL.DU.FLOAT:
      du.setFloat(bytePos, byteWidth, value)
      return nextBitPos
    if paramType == UTIL.DU.TIME:
      timeFormat = self.paramDef.timeFormat
      du.setTime(bytePos, timeFormat, value)
      return nextBitPos
    if paramType == UTIL.DU.STRING:
      du.setString(bytePos, byteWidth, value)
      return nextBitPos
    raise Error("unexpected paramType for parameter " + self.getParamName())
  # ---------------------------------------------------------------------------
  def decode(self, du, bitPos):
    """
    decodes the contens from a data unit, returns the new position
    overloaded from Entity
    """
    paramType = self.getParamType()
    bitWidth = self.getBitWidth()
    value = self.value
    nextBitPos = bitPos + bitWidth
    # process bit oriented parameter types
    if paramType == UTIL.DU.BITS:
      self.value = du.getBits(bitPos, bitWidth)
      return nextBitPos
    if paramType == UTIL.DU.SBITS:
      self.value = du.getSBits(bitPos, bitWidth)
      return nextBitPos
    # process byte oriented parameter types
    if (bitPos % 8) != 0:
      raise Error("parameter " + self.getParamName() + " position is not byte aligned")
    if (bitWidth % 8) != 0:
      raise Error("parameter " + self.getParamName() + " size is not byte aligned")
    bytePos = bitPos >> 3
    byteWidth = bitWidth >> 3
    defType = type(self.paramDef)
    if defType == VariableParamDef:
      # for variable length parameters: encode the length bytes first
      lengthBytes = self.paramDef.lengthBytes
      byteLength = du.getUnsigned(bytePos, lengthBytes)
      bytePos += lengthBytes
      byteWidth = byteLength
      nextBytePos = bytePos + byteWidth
      nextBitPos = nextBytePos << 3
    if paramType == UTIL.DU.BYTES:
      self.value = du.getBytes(bytePos, byteWidth)
      return nextBitPos
    if paramType == UTIL.DU.UNSIGNED:
      self.value = du.getUnsigned(bytePos, byteWidth)
      return nextBitPos
    if paramType == UTIL.DU.SIGNED:
      self.value = du.getSigned(bytePos, byteWidth)
      return nextBitPos
    if paramType == UTIL.DU.FLOAT:
      self.value = du.getFloat(bytePos, byteWidth)
      return nextBitPos
    if paramType == UTIL.DU.TIME:
      timeFormat = self.paramDef.timeFormat
      self.value = du.getTime(bytePos, timeFormat)
      return nextBitPos
    if paramType == UTIL.DU.STRING:
      self.value = du.getString(bytePos, byteWidth)
      return nextBitPos
    raise Error("unexpected paramType for parameter " + self.getParamName())

# =============================================================================
class Slot(Entity):
  """Slot in a struct"""
  # ---------------------------------------------------------------------------
  def __init__(self, slotDef=""):
    self.slotDef = slotDef
    # create the slot child depending on the slot child type in the definition
    childDef = slotDef.childDef
    childType = type(childDef)
    if childType == SimpleParamDef or childType == VariableParamDef or \
       childType == TimeParamDef:
      self.child = Param(paramDef=childDef)
    elif childType == ListDef:
      self.child = List(listDef=childDef)
    else:
      raise Error("child type " + str(childType) + " not supported")
  # ---------------------------------------------------------------------------
  def __str__(self, indent="Slot"):
    """string representation"""
    return self.child.__str__(indent + "." + self.slotDef.slotName)
  # ---------------------------------------------------------------------------
  def getSlotName(self):
    """accessor"""
    return self.slotDef.slotName
  # ---------------------------------------------------------------------------
  def getBitWidth(self):
    """accessor, overloaded from Entity"""
    return self.child.getBitWidth()
  # ---------------------------------------------------------------------------
  def encode(self, du, bitPos):
    """
    encodes the contens into a data unit, returns the new position
    overloaded from Entity
    """
    return self.child.encode(du, bitPos)
  # ---------------------------------------------------------------------------
  def decode(self, du, bitPos):
    """
    decodes the contens from a data unit, returns the new position
    overloaded from Entity
    """
    return self.child.decode(du, bitPos)

# =============================================================================
class Struct(Entity):
  """Struct in a variable packet"""
  # ---------------------------------------------------------------------------
  def __init__(self, structDef):
    self.structDef = structDef
    self.slots = tuple(Slot(slotDef) for slotDef in structDef.slotDefs)
  # ---------------------------------------------------------------------------
  def __str__(self, indent="Struct"):
    """string representation"""
    retStr = ""
    for slot in self.slots:
      retStr += slot.__str__(indent)
    return retStr
  # ---------------------------------------------------------------------------
  def __getattr__(self, slotName):
    """struct attribute simulation"""
    slotPos = self.structDef.getSlotPos(slotName)
    return self.slots[slotPos].child
  # ---------------------------------------------------------------------------
  def getBitWidth(self):
    """accessor, overloaded from Entity"""
    bitWidth = 0
    for slot in self.slots:
      bitWidth += slot.getBitWidth()
    return bitWidth
  # ---------------------------------------------------------------------------
  def encode(self, du, bitPos):
    """
    encodes the contens into a data unit, returns the new position
    overloaded from Entity
    """
    for slot in self.slots:
      bitPos = slot.encode(du, bitPos)
    return bitPos
  # ---------------------------------------------------------------------------
  def decode(self, du, bitPos):
    """
    decodes the contens from a data unit, returns the new position
    overloaded from Entity
    """
    for slot in self.slots:
      bitPos = slot.decode(du, bitPos)
    return bitPos
    
# =============================================================================
class List(Entity):
  """Definition of a list in a variable packet"""
  # ---------------------------------------------------------------------------
  def __init__(self, listDef):
    self.listDef = listDef
    length = int(listDef.lenParamDef.defaultValue)
    entryDef = listDef.entryDef
    self.entries = [Struct(entryDef) for _ in range(0, length)]
  # ---------------------------------------------------------------------------
  def __str__(self, indent="List"):
    """string representation"""
    retStr =  "\n" + indent + ".len = " + str(len(self.entries))
    i = 0
    for entry in self.entries:
      retStr += entry.__str__(indent + "[" + str(i) + "]")
      i += 1
    return retStr
  # ---------------------------------------------------------------------------
  def __len__(self):
    """length operator"""
    return len(self.entries)
  # ---------------------------------------------------------------------------
  def setLen(self, length):
    """change the length of the list (number of entries)"""
    oldLen = len(self.entries)
    if length < oldLen:
      # list must be shrinked
      self.entries = self.entries[:length - oldLen]
    elif length > oldLen:
      # list must be expanded
      entryDef = self.listDef.entryDef
      while len(self.entries) < length:
        self.entries.append(Struct(entryDef))
  # ---------------------------------------------------------------------------
  def __getitem__(self, key):
    """index operator"""
    return self.entries[key]
  # ---------------------------------------------------------------------------
  def getLenParamName(self):
    """accessor"""
    return self.listDef.lenParamDef.paramName
  # ---------------------------------------------------------------------------
  def getBitWidth(self):
    """accessor, overloaded from Entity"""
    bitWidth = self.listDef.lenParamDef.bitWidth
    for entry in self.entries:
      bitWidth += entry.getBitWidth()
    return bitWidth
  # ---------------------------------------------------------------------------
  def isReadOnly(self):
    """accessor"""
    return self.listDef.lenParamDef.isReadOnly
  # ---------------------------------------------------------------------------
  def encode(self, du, bitPos):
    """
    encodes the contens into a data unit, returns the new position
    overloaded from Entity
    """
    # encode the length
    lengthValueBitPos = bitPos
    if (lengthValueBitPos % 8) != 0:
      raise Error("parameter " + self.getLenParamName() + " position is not byte aligned")
    lengthValueBitWidth = self.listDef.lenParamDef.bitWidth
    if (lengthValueBitWidth % 8) != 0:
      raise Error("parameter " + self.getLenParamName() + " size is not byte aligned")
    lengthValueBytePos = lengthValueBitPos >> 3
    lengthValueByteWidth = lengthValueBitWidth >> 3
    lengthValue = len(self.entries)
    du.setUnsigned(lengthValueBytePos, lengthValueByteWidth, lengthValue)
    bitPos += lengthValueBitWidth
    # encode the list entries
    for entry in self.entries:
      bitPos = entry.encode(du, bitPos)
    return bitPos
  # ---------------------------------------------------------------------------
  def decode(self, du, bitPos):
    """
    decodes the contens from a data unit, returns the new position
    overloaded from Entity
    """
    # decode the length
    lengthValueBitPos = bitPos
    if (lengthValueBitPos % 8) != 0:
      raise Error("parameter " + self.getLenParamName() + " position is not byte aligned")
    lengthValueBitWidth = self.listDef.lenParamDef.bitWidth
    if (lengthValueBitWidth % 8) != 0:
      raise Error("parameter " + self.getLenParamName() + " size is not byte aligned")
    lengthValueBytePos = lengthValueBitPos >> 3
    lengthValueByteWidth = lengthValueBitWidth >> 3
    lengthValue = du.getUnsigned(lengthValueBytePos, lengthValueByteWidth)
    bitPos += lengthValueBitWidth
    # decode the list entries
    self.setLen(lengthValue)
    for entry in self.entries:
      bitPos = entry.decode(du, bitPos)
    return bitPos
