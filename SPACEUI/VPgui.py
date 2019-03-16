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
# Variable Packet GUI                                                         *
#******************************************************************************
import ttk, tkSimpleDialog
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import SPACE.IF

###########
# classes #
###########
# =============================================================================
class TreeBrowser(object):
  """Variable packet tree browser"""
  # ---------------------------------------------------------------------------
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
  # ---------------------------------------------------------------------------
  def fillTree(self, treeName, struct):
    """fills a toplevel VPstruct into the tree"""
    self.toplevelStruct = struct
    self.fillStructInTree("", treeName, struct)
    self.tree.pack()
  # ---------------------------------------------------------------------------
  def fillParamInTree(self, parentNodeID, slotName, param):
    """fills a VPparam into the tree"""
    paramName = param.getParamName()
    paramValue = param.value
    nodeID = self.tree.insert(parentNodeID, "end", text=slotName, values=(paramName, str(paramValue)))
    self.treeMap[nodeID] = param
  # ---------------------------------------------------------------------------
  def fillSlotInTree(self, parentNodeID, slot):
    """fills a VPslot into the tree"""
    slotName = slot.getSlotName()
    child = slot.child
    childType = type(child)
    if childType == SPACE.IF.VPparam:
      self.fillParamInTree(parentNodeID, slotName, param=child)
    elif childType == SPACE.IF.VPlist:
      self.fillListInTree(parentNodeID, slotName, lst=child)
    else:
      raise Error("child type " + childType + " not supported")
  # ---------------------------------------------------------------------------
  def fillStructInTree(self, parentNodeID, structName, struct):
    """fills a VPstruct into the tree"""
    nodeID = self.tree.insert(parentNodeID , "end", text=structName, values=("", ""))
    self.treeMap[nodeID] = struct
    for slot in struct.slots:
      self.fillSlotInTree(nodeID, slot)
  # ---------------------------------------------------------------------------
  def fillListInTree(self, parentNodeID, slotName, lst):
    """fills a VPlist into the tree"""
    lenParamName = lst.getLenParamName()
    nodeID = self.tree.insert(parentNodeID, "end", text=slotName + " len", values=(lenParamName, str(len(lst))))
    self.treeMap[nodeID] = lst
    i = 0
    for entry in lst.entries:
      stuctName = "[" + str(i) + "]"
      self.fillStructInTree(nodeID, stuctName, struct=entry)
      i += 1
  # ---------------------------------------------------------------------------
  def itemEvent(self, event):
    """callback when an item in the tree is clicked"""
    nodeID = self.tree.selection()[0]
    nodeObject = self.treeMap[nodeID]
    if type(nodeObject) == SPACE.IF.VPparam:
      self.paramClicked(nodeObject, nodeID)
    elif type(nodeObject) == SPACE.IF.VPstruct:
      self.structClicked(nodeObject, nodeID)
    elif type(nodeObject) == SPACE.IF.VPlist:
      self.listClicked(nodeObject, nodeID)
    return "break"
  # ---------------------------------------------------------------------------
  def paramClicked(self, param, nodeID):
    """callback when a VPparam node is clicked"""
    nodeKey = self.tree.item(nodeID, "text")
    nodeValues = self.tree.item(nodeID, "value")
    name = nodeValues[0]
    value = nodeValues[1]
    paramType = param.getParamType()
    if paramType == SPACE.IF.VP_PARAM_NUMBER:
      answer = tkSimpleDialog.askinteger("Param",
                                         nodeKey + ": " + name,
                                         initialvalue=value)
    elif paramType == SPACE.IF.VP_PARAM_STRING:
      answer = tkSimpleDialog.askstring("Param",
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
  # ---------------------------------------------------------------------------
  def structClicked(self, struct, nodeID):
    """callback when a VPstruct node is clicked"""
    pass
  # ---------------------------------------------------------------------------
  def listClicked(self, lst, nodeID):
    """callback when a VPlist node is clicked"""
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
  # ---------------------------------------------------------------------------
  def dumpData(self):
    """helper method"""
    LOG("TreeBrowser.data = " + str(self.toplevelStruct), "SPACE")
