#!/usr/bin/env python
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
# PUS Services - Variable packet support - Unit Tests                         *
#                                                                             *
# For this is an example variable packet layout definition is used:           *
#                                                                             *
# StructDef - ID="XXXX1234"                                                   *
#  +-- s_1: Par1: uint(3,12) - 16 bits                                        *
#  +-- s_2: Par2: string(8,16) - 16 bytes                                     *
#  +-- s_3: Par3: uint(3,14) - 32 bit                                         *
#  +-- s_4: Par4: string(8,0) - variable bytes                                *
#  +-- s_5: ListDef                                                           *
#  |         +-- len: Par5: uint(3,4) - 8 bits (group repeater)               *
#  |         +-- [*]: StructDef                                               *
#  |                   +-- s_6: Par6: uint(3,14) - 32 bit                     *
#  |                   +-- s_7: Par7: string(8,0) - variable bytes            *
#  +-- s_8: Par8: uint(3,16) - 64 bits                                        *
#  +-- s_9: Par9: string(8,0) - variable bytes                                *
#                                                                             *
# Based on the packet definition the following variable packet instantiation  *
# is performed:                                                               *
#                                                                             *
# Struct                                                             BitWidth *
#  +-- s_1: Par1 = 123                                                     16 *
#  +-- s_2: Par2 = "This is a string"                                     144 *
#  +-- s_3: Par3 = 4193                                                   176 *
#  +-- s_4: Par4 = "This is a variable string"                            392 *
#  +-- s_5: List                                                              *
#  |         +-- len: Par5 = 3                                            400 *
#  |         +-- [0]: Struct                                                  *
#  |         |         +-- s_6: Par6 = 15362                              432 *
#  |         |         +-- s_7: Par7 = "This is also a variable string"   688 *
#  |         +-- [1]: Struct                                                  *
#  |         |         +-- s_6: Par6 = 15362                              944 *
#  |         |         +-- s_7: Par7 = "This is also a variable string"   976 *
#  |         +-- [2]: Struct                                                  *
#  |                   +-- s_6: Par6 = 15362                             1008 *
#  |                   +-- s_7: Par7 = "This is also a variable string"  1264 *
#  +-- s_8: Par8 = 182736489393276                                       1328 *
#  +-- s_9: Par9 = "This is the last variable string in the struct"      1712 *
#                                                                             *
# The variable packet is changed afterwards to the following structure:       *
#                                                                             *
# Struct                                                             BitWidth *
#  +-- s_1: Par1 = 65535                                                  16 *
#  +-- s_2: Par2 = "This is a string"                                     144 *
#  +-- s_3: Par3 = 4193                                                   176 *
#  +-- s_4: Par4 = "This is a variable string"                            392 *
#  +-- s_5: List                                                              *
#  |         +-- len: Par5 = 2                                            400 *
#  |         +-- [0]: Struct                                                  *
#  |         |         +-- s_6: Par6 = 101010                             432 *
#  |         |         +-- s_7: Par7 = "new value for s_7"                584 *
#  |         +-- [1]: Struct                                                  *
#  |                   +-- s_6: Par6 = 15362                              616 *
#  |                   +-- s_7: Par7 = "This is also a variable string"   872 *
#  +-- s_8: Par8 = 182736489393276                                        936 *
#  +-- s_9: Par9 = "This is the last variable string in the struct"      1320 *
#******************************************************************************
from __future__ import print_function
import sys
import PUS.VP
import UTIL.DU

#############
# MIB level #
#############
class MIBparamRecord(object):
  def __init__(self, paramName, paramType, bitWidth, defaultValue, isReadOnly):
    self.paramName = paramName
    self.paramType = paramType
    self.bitWidth = bitWidth
    self.defaultValue = defaultValue
    self.isReadOnly = isReadOnly

class MIBvarRecord(object):
  def __init__(self, structName, pos, slotName, paramName, groupSize):
    self.structName = structName
    self.pos = pos
    self.slotName = slotName
    self.paramName = paramName
    self.groupSize = groupSize

######################
# Definition Manager #
######################
class DefManager:
  def __init__(self, mibParamRecords, mibVarRecords):
    self.mibParamRecordMap = {}
    self.mibVarRecordMap = {}
    for mibParamRecord in mibParamRecords:
      paramName = mibParamRecord.paramName
      self.mibParamRecordMap[paramName] = mibParamRecord
    for mibVarRecord in mibVarRecords:
      structName = mibVarRecord.structName
      if not structName in self.mibVarRecordMap:
        self.mibVarRecordMap[structName] = []
      self.mibVarRecordMap[structName].append(mibVarRecord)
  def createParamDef(self, paramName):
    try:
      paramRecord = self.mibParamRecordMap[paramName]
    except:
      print("error: param name " + paramName + " not found in s_mibParamRecordMap")
      sys.exit(-1)
    # special handling of variable size parameters
    if paramRecord.paramType == UTIL.DU.STRING and paramRecord.bitWidth == 0:
      lengthBytes = 2
      return PUS.VP.VariableParamDef(paramRecord.paramName,
                                     paramRecord.paramType,
                                     lengthBytes,
                                     paramRecord.defaultValue,
                                     paramRecord.isReadOnly)
    # default handling of other parameters
    return PUS.VP.SimpleParamDef(paramRecord.paramName,
                                 paramRecord.paramType,
                                 paramRecord.bitWidth,
                                 paramRecord.defaultValue,
                                 paramRecord.isReadOnly)
  def createSlotDef(self, sortedVarRecords, varRecordsPos):
    nextVarRecord = sortedVarRecords[varRecordsPos]
    slotName = nextVarRecord.slotName
    if nextVarRecord.groupSize > 0:
      # group repeater definition
      childDef, varRecordsPos = self.createListDef(sortedVarRecords, varRecordsPos)
    else:
      # parameter definition
      paramName = nextVarRecord.paramName
      childDef = self.createParamDef(paramName)
      varRecordsPos += 1
    return (PUS.VP.SlotDef(slotName, childDef), varRecordsPos)
  def createStructDef(self, structName, sortedVarRecords, varRecordsPos, varRecordsEnd):
    sortedSlotDefs = []
    while varRecordsPos < varRecordsEnd:
      nextSlotDef, varRecordsPos = self.createSlotDef(sortedVarRecords, varRecordsPos)
      sortedSlotDefs.append(nextSlotDef)
    return (PUS.VP.StructDef(structName, sortedSlotDefs), varRecordsPos)
  def createListDef(self, sortedVarRecords, varRecordsPos):
    nextVarRecord = sortedVarRecords[varRecordsPos]
    lenParamName = nextVarRecord.paramName
    lenParamDef = self.createParamDef(lenParamName)
    varRecordsPos += 1
    varRecordsEnd = varRecordsPos + nextVarRecord.groupSize
    entryDef, varRecordsPos = self.createStructDef("", sortedVarRecords, varRecordsPos, varRecordsEnd)
    return (PUS.VP.ListDef(lenParamDef, entryDef), varRecordsPos)
  def createToplevelStructDef(self, structName):
    try:
      varRecords = self.mibVarRecordMap[structName]
    except:
      print("error: struct name " + structName + " not found in s_mibVarRecordMap")
      sys.exit(-1)
    sortedVarRecords = sorted(varRecords, key=lambda varRecord: varRecord.pos)
    varRecordsPos = 0
    varRecordsEnd = len(sortedVarRecords)
    structDef, varRecordsPos = self.createStructDef(structName, sortedVarRecords, varRecordsPos, varRecordsEnd)
    return structDef

#############
# functions #
#############
# -----------------------------------------------------------------------------
def createStruct1Definition():
  mibParamRecords = [
    MIBparamRecord("Par1", UTIL.DU.UNSIGNED, 16, 123, False),
    MIBparamRecord("Par2", UTIL.DU.STRING, 128, "This is a string", True),
    MIBparamRecord("Par3", UTIL.DU.UNSIGNED, 32, 4193, True),
    MIBparamRecord("Par4", UTIL.DU.STRING, 0, "This is a variable string", True),
    MIBparamRecord("Par5", UTIL.DU.UNSIGNED, 8, 3, False),
    MIBparamRecord("Par6", UTIL.DU.UNSIGNED, 32, 15362, False),
    MIBparamRecord("Par7", UTIL.DU.STRING, 0, "This is also a variable string", False),
    MIBparamRecord("Par8", UTIL.DU.UNSIGNED, 64, 182736489393276, True),
    MIBparamRecord("Par9", UTIL.DU.STRING, 0, "This is the last variable string in the struct", True)]
  mibVarRecords = [
    MIBvarRecord("XXXX1234", 1, "s_1", "Par1", 0),
    MIBvarRecord("XXXX1234", 2, "s_2", "Par2", 0),
    MIBvarRecord("XXXX1234", 3, "s_3", "Par3", 0),
    MIBvarRecord("XXXX1234", 4, "s_4", "Par4", 0),
    MIBvarRecord("XXXX1234", 5, "s_5", "Par5", 2),
    MIBvarRecord("XXXX1234", 6, "s_6", "Par6", 0),
    MIBvarRecord("XXXX1234", 7, "s_7", "Par7", 0),
    MIBvarRecord("XXXX1234", 8, "s_8", "Par8", 0),
    MIBvarRecord("XXXX1234", 9, "s_9", "Par9", 0)]
  defManager = DefManager(mibParamRecords, mibVarRecords)
  return defManager.createToplevelStructDef("XXXX1234")
# -----------------------------------------------------------------------------
def testStruct1(struct):
  if struct.s_1.getBitWidth() != 16:
    return False
  if struct.s_2.getBitWidth() != 128:
    return False
  if struct.s_3.getBitWidth() != 32:
    return False
  if struct.s_4.getBitWidth() != 216:
    return False
  if struct.s_5[0].s_6.getBitWidth() != 32:
    return False
  if struct.s_5[0].s_7.getBitWidth() != 256:
    return False
  if struct.s_5[0].getBitWidth() != 288:
    return False
  if struct.s_5[1].s_6.getBitWidth() != 32:
    return False
  if struct.s_5[1].s_7.getBitWidth() != 256:
    return False
  if struct.s_5[1].getBitWidth() != 288:
    return False
  if struct.s_5[2].s_6.getBitWidth() != 32:
    return False
  if struct.s_5[2].s_7.getBitWidth() != 256:
    return False
  if struct.s_5[2].getBitWidth() != 288:
    return False
  if struct.s_5.getBitWidth() != 872:
    return False
  if struct.s_8.getBitWidth() != 64:
    return False
  if struct.s_9.getBitWidth() != 384:
    return False
  if struct.getBitWidth() != 1712:
    return False
  return True
# -----------------------------------------------------------------------------
def changeStruct1(struct):
  struct.s_1.value = 65535
  struct.s_5[0].s_6.value = 101010
  struct.s_5[0].s_7.value = "new value for s_7"
  struct.s_5.setLen(4)
  struct.s_5.setLen(2)
# -----------------------------------------------------------------------------
def testStruct2(struct):
  if struct.s_1.getBitWidth() != 16:
    return False
  if struct.s_2.getBitWidth() != 128:
    return False
  if struct.s_3.getBitWidth() != 32:
    return False
  if struct.s_4.getBitWidth() != 216:
    return False
  if struct.s_5[0].s_6.getBitWidth() != 32:
    return False
  if struct.s_5[0].s_7.getBitWidth() != 152:
    return False
  if struct.s_5[0].getBitWidth() != 184:
    return False
  if struct.s_5[1].s_6.getBitWidth() != 32:
    return False
  if struct.s_5[1].s_7.getBitWidth() != 256:
    return False
  if struct.s_5[1].getBitWidth() != 288:
    return False
  if struct.s_5.getBitWidth() != 480:
    return False
  if struct.s_8.getBitWidth() != 64:
    return False
  if struct.s_9.getBitWidth() != 384:
    return False
  if struct.getBitWidth() != 1320:
    return False
  return True
# -----------------------------------------------------------------------------
def encodeDecode(struct, structDef):
  bitWidth = struct.getBitWidth()
  byteWidth = bitWidth >> 3
  du = UTIL.DU.BinaryUnit()
  du.setLen(byteWidth)
  struct.encode(du, 0)
  dStruct = PUS.VP.Struct(structDef)
  dStruct.decode(du, 0)
  return dStruct

structDef = createStruct1Definition()
print("structDef:", structDef)
struct = PUS.VP.Struct(structDef)
print("struct-->", struct)
if not testStruct1(struct):
  print("struct1 has invalid structure")
  sys.exit(-1)
dStruct = encodeDecode(struct, structDef)
print("dStruct-->", dStruct)
if not testStruct1(dStruct):
  print("encoded & decoded struct1 has invalid structure")
  sys.exit(-1)
changeStruct1(struct)
print("struct-->", struct)
if not testStruct2(struct):
  print("struct2 has invalid structure")
  sys.exit(-1)
dStruct = encodeDecode(struct, structDef)
print("dStruct-->", dStruct)
if not testStruct2(dStruct):
  print("encoded & decoded struct2 has invalid structure")
  sys.exit(-1)
