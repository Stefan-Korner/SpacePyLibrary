#!/usr/bin/env python
import sys
import SPACE.IF

#############
# MIB level #
#############
# parameter type
PARAM_NUMBER = "PARAM_NUMBER"
PARAM_STRING = "PARAM_STRING"

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
    return SPACE.IF.VPparamDef(paramRecord.paramName,
                               paramRecord.paramType,
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
    return (SPACE.IF.VPslotDef(slotName, childDef), varRecordsPos)
  def createStructDef(self, structName, sortedVarRecords, varRecordsPos, varRecordsEnd):
    sortedSlotDefs = []
    while varRecordsPos < varRecordsEnd:
      nextSlotDef, varRecordsPos = self.createSlotDef(sortedVarRecords, varRecordsPos)
      sortedSlotDefs.append(nextSlotDef)
    return (SPACE.IF.VPstructDef(structName, sortedSlotDefs), varRecordsPos)
  def createListDef(self, sortedVarRecords, varRecordsPos):
    nextVarRecord = sortedVarRecords[varRecordsPos]
    lenParamName = nextVarRecord.paramName
    lenParamDef = self.createParamDef(lenParamName)
    varRecordsPos += 1
    varRecordsEnd = varRecordsPos + nextVarRecord.groupSize
    entryDef, varRecordsPos = self.createStructDef("", sortedVarRecords, varRecordsPos, varRecordsEnd)
    return (SPACE.IF.VPlistDef(lenParamDef, entryDef), varRecordsPos)
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
  MIBparamRecord("Par1", PARAM_NUMBER, 123),
  MIBparamRecord("Par2", PARAM_STRING, "This is a string"),
  MIBparamRecord("Par3", PARAM_NUMBER, 4193),
  MIBparamRecord("Par4", PARAM_STRING, "This is a variable string"),
  MIBparamRecord("Par5", PARAM_NUMBER, 3),
  MIBparamRecord("Par6", PARAM_NUMBER, 15362),
  MIBparamRecord("Par7", PARAM_STRING, "This is also a variable string"),
  MIBparamRecord("Par8", PARAM_NUMBER, 182736489393276),
  MIBparamRecord("Par9", PARAM_STRING, "This is the last variable string in the struct")]
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
struct = SPACE.IF.VPstruct(structDef)
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
import Tkinter, ttk, tkSimpleDialog

################
# Tree Manager #
################
class TreeManager:
  def __init__(self, root):
    self.tree = ttk.Treeview(root)
    self.tree.bind("<Double-1>", self.itemEvent)
    self.tree["columns"]=("name","value")
    self.tree.column("name", width=100 )
    self.tree.column("value", width=200)
    self.tree.heading("name", text="Name")
    self.tree.heading("value", text="Value")
    self.treeMap = {}
    self.toplevelStruct = None
  def fillTree(self, treeName, struct):
    self.toplevelStruct = struct
    self.fillStructInTree("", treeName, struct)
    self.tree.pack()
  def fillParamInTree(self, parentNodeID, slotName, param):
    paramName = param.getParamName()
    paramValue = param.value
    nodeID = self.tree.insert(parentNodeID, "end", text=slotName, values=(paramName, str(paramValue)))
    self.treeMap[nodeID] = param
  def fillSlotInTree(self, parentNodeID, slot):
    slotName = slot.getSlotName()
    child = slot.child
    childType = type(child)
    if childType == SPACE.IF.VPparam:
      self.fillParamInTree(parentNodeID, slotName, param=child)
    elif childType == SPACE.IF.VPlist:
      self.fillListInTree(parentNodeID, slotName, lst=child)
    else:
      print("error: child type " + childType + " not supported")
      sys.exit(-1)
  def fillStructInTree(self, parentNodeID, structName, struct):
    nodeID = self.tree.insert(parentNodeID , "end", text=structName, values=("", ""))
    self.treeMap[nodeID] = struct
    for slot in struct.slots:
      self.fillSlotInTree(nodeID, slot)
  def fillListInTree(self, parentNodeID, slotName, lst):
    lenParamName = lst.getLenParamName()
    nodeID = self.tree.insert(parentNodeID, "end", text=slotName + " len", values=(lenParamName, str(len(lst))))
    self.treeMap[nodeID] = lst
    i = 0
    for entry in lst.entries:
      stuctName = "[" + str(i) + "]"
      self.fillStructInTree(nodeID, stuctName, struct=entry)
      i += 1
  def itemEvent(self, event):
    nodeID = self.tree.selection()[0]
    nodeObject = self.treeMap[nodeID]
    if type(nodeObject) == SPACE.IF.VPparam:
      self.paramClicked(nodeObject, nodeID)
    elif type(nodeObject) == SPACE.IF.VPstruct:
      self.structClicked(nodeObject, nodeID)
    elif type(nodeObject) == SPACE.IF.VPlist:
      self.listClicked(nodeObject, nodeID)
    return "break"
  def paramClicked(self, param, nodeID):
    nodeKey = self.tree.item(nodeID, "text")
    nodeValues = self.tree.item(nodeID, "value")
    name = nodeValues[0]
    value = nodeValues[1]
    paramType = param.getParamType()
    if paramType == PARAM_NUMBER:
      answer = simpledialog.askinteger("Param",
                                       nodeKey + ": " + name,
                                       initialvalue=value)
    elif paramType == PARAM_STRING:
      answer = simpledialog.askstring("Param",
                                      nodeKey + ": " + name,
                                      initialvalue=value)
    else:
      answer = None
    if answer == None:
      return
    # new parameter value entered --> update param object and tree
    newValue = answer
    param.value = newValue
    self.tree.set(nodeID, 1, newValue)
  def structClicked(self, struct, nodeID):
    pass
  def listClicked(self, lst, nodeID):
    nodeKey = self.tree.item(nodeID, "text")
    nodeValues = self.tree.item(nodeID, "value")
    name = nodeValues[0]
    value = nodeValues[1]
    answer = tkSimpleDialog.askinteger("List",
                                       nodeKey + ": " + name,
                                       initialvalue=value,
                                       minvalue=0)
    if answer == None:
      return
    # new list length entered --> update list object and tree
    oldLen = len(lst)
    newLen = answer
    if oldLen < newLen:
      # enlarge the list object and list display
      lst.setLen(newLen)
      i = oldLen
      while i < newLen:
        entry = lst[i]
        stuctName = "[" + str(i) + "]"
        self.fillStructInTree(nodeID, stuctName, struct=entry)
        i += 1
    elif oldLen > newLen:
      # shrink the list object and list display
      lst.setLen(newLen)
      # iterate over a list copy, because tree is changed during interation
      i = 0
      children = list(self.tree.get_children(nodeID))
      for child in children:
        if i >= newLen:
          self.tree.delete(child)
        i += 1
    else:
      # do nothing
      return
    # update the len value in the display
    self.tree.set(nodeID, 1, str(len(lst)))
  def dumpData(self):
    print("TreeManager.data =", self.toplevelStruct)

root = Tkinter.Tk()
treeManager = TreeManager(root)
treeManager.fillTree("Packet_01", struct)
root.mainloop()
