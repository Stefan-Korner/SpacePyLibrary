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
  def __init__(self, paramName, defaultValue):
    self.paramName = paramName
    self.defaultValue = defaultValue
  # ---------------------------------------------------------------------------
  def __str__(self, indent="ParamDef"):
    """string representation"""
    return ("\n" + indent + "." + self.paramName + " = " + str(self.defaultValue))
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
  def __init__(self, paramName, paramType, bitWidth, defaultValue):
    ParamDef.__init__(self, paramName, defaultValue)
    self.paramType = paramType
    self.bitWidth = bitWidth
  # ---------------------------------------------------------------------------
  def __str__(self, indent="SimpleParamDef"):
    """string representation"""
    return ("\n" + indent + "." + self.paramName + " = " + UTIL.DU.fieldTypeStr(self.paramType) + ", " + str(self.bitWidth) + ", " + str(self.defaultValue))
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
  def __init__(self, paramName, paramType, lengthBytes, defaultValue):
    ParamDef.__init__(self, paramName, defaultValue)
    self.paramType = paramType
    self.lengthBytes = lengthBytes
  # ---------------------------------------------------------------------------
  def __str__(self, indent="VariableParamDef"):
    """string representation"""
    return ("\n" + indent + "." + self.paramName + " = " + UTIL.DU.fieldTypeStr(self.paramType) + ", " + str(self.lengthBytes) + ", " + str(self.defaultValue))
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
  def __init__(self, paramName, timeFormat, defaultValue):
    ParamDef.__init__(self, paramName, defaultValue)
    self.timeFormat = timeFormat
  # ---------------------------------------------------------------------------
  def __str__(self, indent="TimeParamDef"):
    """string representation"""
    return ("\n" + indent + "." + self.paramName + " = " + CCSDS.TIME.timeFormatString(self.timeFormat) + ", " + str(self.defaultValue))
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

##################
# instance level #
##################

# =============================================================================
class Param(object):
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
    """accessor"""
    # special processing of variable size parameters
    defType = type(self.paramDef)
    if defType == VariableParamDef:
      byteWidth = self.paramDef.lengthBytes + len(self.value)
      return byteWidth << 3
    # default processing
    return self.paramDef.getBitWidth()

# =============================================================================
class Slot(object):
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
      raise Error("error: child type " + str(childType) + " not supported")
  # ---------------------------------------------------------------------------
  def __str__(self, indent="Slot"):
    """string representation"""
    return self.child.__str__(indent + "." + self.slotDef.slotName)
  # ---------------------------------------------------------------------------
  def getSlotName(self):
    """accessor"""
    return self.slotDef.slotName

# =============================================================================
class Struct(object):
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
    
# =============================================================================
class List(object):
  """Definition of a list in a variable packet"""
  # ---------------------------------------------------------------------------
  def __init__(self, listDef):
    self.listDef = listDef
    length = listDef.lenParamDef.defaultValue
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

#############
# functions #
#############
# -----------------------------------------------------------------------------
def getParamBitWidth(param):
  """calculates the bitWidth of a parameter"""
  return param.getBitWidth()
# -----------------------------------------------------------------------------
def getSlotBitWidth(slot):
  """calculates the bitWidth of a slot"""
  slotDef = slot.slotDef
  # calculate the bitWidth depending on the slot child type in the definition
  child = slot.child
  childType = type(child)
  if childType == Param:
    return getParamBitWidth(param=child)
  elif childType == List:
    return getListBitWidth(lst=child)
  else:
    raise Error("error: child type " + childType + " not supported")
# -----------------------------------------------------------------------------
def getStructBitWidth(struct):
  """calculates the bitWidth of a struct"""
  bitWidth = 0
  for slot in struct.slots:
    bitWidth += getSlotBitWidth(slot)
  return bitWidth
# -----------------------------------------------------------------------------
def getListBitWidth(lst):
  """calculates the bitWidth of a list"""
  bitWidth = lst.listDef.lenParamDef.bitWidth
  for entry in lst.entries:
    bitWidth += getStructBitWidth(entry)
  return bitWidth
