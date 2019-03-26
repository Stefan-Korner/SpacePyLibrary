#!/usr/bin/env python3
import sys
import CCSDS.VP
import SPACEUI.VPgui
import UTIL.DU

#############
# MIB level #
#############
class MIBparamRecord(object):
  def __init__(self, paramName, paramType, defaultValue):
    self.paramName = paramName
    self.paramType = paramType
    self.defaultValue = defaultValue

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
    bitWidth = 0
    return CCSDS.VP.SimpleParamDef(paramRecord.paramName,
                                   paramRecord.paramType,
                                   bitWidth,
                                   paramRecord.defaultValue)
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
    return (CCSDS.VP.SlotDef(slotName, childDef), varRecordsPos)
  def createStructDef(self, structName, sortedVarRecords, varRecordsPos, varRecordsEnd):
    sortedSlotDefs = []
    while varRecordsPos < varRecordsEnd:
      nextSlotDef, varRecordsPos = self.createSlotDef(sortedVarRecords, varRecordsPos)
      sortedSlotDefs.append(nextSlotDef)
    return (CCSDS.VP.StructDef(structName, sortedSlotDefs), varRecordsPos)
  def createListDef(self, sortedVarRecords, varRecordsPos):
    nextVarRecord = sortedVarRecords[varRecordsPos]
    lenParamName = nextVarRecord.paramName
    lenParamDef = self.createParamDef(lenParamName)
    varRecordsPos += 1
    varRecordsEnd = varRecordsPos + nextVarRecord.groupSize
    entryDef, varRecordsPos = self.createStructDef("", sortedVarRecords, varRecordsPos, varRecordsEnd)
    return (CCSDS.VP.ListDef(lenParamDef, entryDef), varRecordsPos)
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

#******************************************************************************
# This is an example variable packet layout definition                        *
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
# This is an example variable packet instantiation                            *
#                                                                             *
# Struct                                                                      *
#  +-- s_1: Par1 = 123                                                        *
#  +-- s_2: Par2 = "This is a string"                                         *
#  +-- s_3: Par3 = 4193                                                       *
#  +-- s_4: Par4 = "This is a variable string"                                *
#  +-- s_5: List                                                              *
#  |         +-- len: Par5 = 3                                                *
#  |         +-- [0]: Struct                                                  *
#  |         |         +-- s_6: Par6 = 15362                                  *
#  |         |         +-- s_7: Par7 = "This is also a variable string"       *
#  |         +-- [1]: Struct                                                  *
#  |         |         +-- s_6: Par6 = 15362                                  *
#  |         |         +-- s_7: Par7 = "This is also a variable string"       *
#  |         +-- [2]: Struct                                                  *
#  |                   +-- s_6: Par6 = 15362                                  *
#  |                   +-- s_7: Par7 = "This is also a variable string"       *
#  +-- s_8: Par8 = 182736489393276                                            *
#  +-- s_9: Par9 = "This is the last variable string in the struct"           *
#                                                                             *
#******************************************************************************
mibParamRecords = [
  MIBparamRecord("Par1", UTIL.DU.UNSIGNED, 123),
  MIBparamRecord("Par2", UTIL.DU.STRING, "This is a string"),
  MIBparamRecord("Par3", UTIL.DU.UNSIGNED, 4193),
  MIBparamRecord("Par4", UTIL.DU.STRING, "This is a variable string"),
  MIBparamRecord("Par5", UTIL.DU.UNSIGNED, 3),
  MIBparamRecord("Par6", UTIL.DU.UNSIGNED, 15362),
  MIBparamRecord("Par7", UTIL.DU.STRING, "This is also a variable string"),
  MIBparamRecord("Par8", UTIL.DU.UNSIGNED, 182736489393276),
  MIBparamRecord("Par9", UTIL.DU.STRING, "This is the last variable string in the struct")]
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
structDef = defManager.createToplevelStructDef("XXXX1234")
print("structDef:", structDef)
struct = CCSDS.VP.Struct(structDef)
print("struct-->", struct)
print("struct.s_1.value = " + str(struct.s_1.value))
struct.s_1.value = 111222
print("struct-->", struct)
print("struct.s_1.value = " + str(struct.s_1.value))
print("struct.s_5[0]:", struct.s_5[0])
struct.s_5[0].s_6.value = "new value for s_6"
struct.s_5[0].s_7.value = 101010
print("struct-->", struct)
print("len(struct.s_5) = " + str(len(struct.s_5)))
struct.s_5.setLen(4)
print("struct-->", struct)
struct.s_5.setLen(2)
print("struct-->", struct)

#******************************************************************************
# GUI with tree widget                                                        *
#******************************************************************************
import tkinter

root = tkinter.Tk()
root.withdraw()
dialog = SPACEUI.VPgui.TreeBrowser(root, "Packet_01", struct)
