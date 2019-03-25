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
# CCSDS Stack - Variable packet support                                       *
#******************************************************************************

####################
# definition level #
####################

# =============================================================================
class ParamDef(object):
  """Contains the most important definition data of a variable packet parameter"""
  # ---------------------------------------------------------------------------
  def __init__(self, paramName, paramType, bitWidth, defaultValue):
    self.paramName = paramName
    self.paramType = paramType
    self.bitWidth = bitWidth
    self.defaultValue = defaultValue
  # ---------------------------------------------------------------------------
  def __str__(self, indent="ParamDef"):
    """string representation"""
    return ("\n" + indent + "." + self.paramName + " = " + str(self.paramType) + ", " + str(self.bitWidth) + ", " + str(self.defaultValue))

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
    return self.paramDef.paramType

# =============================================================================
class Slot(object):
  """Slot in a struct"""
  # ---------------------------------------------------------------------------
  def __init__(self, slotDef=""):
    self.slotDef = slotDef
    # create the slot child depending on the slot child type in the definition
    childDef = slotDef.childDef
    childType = type(childDef)
    if childType == ParamDef:
      self.child = Param(paramDef=childDef)
    elif childType == ListDef:
      self.child = List(listDef=childDef)
    else:
      print("error: child type " + childType + " not supported")
      sys.exit(-1)
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
