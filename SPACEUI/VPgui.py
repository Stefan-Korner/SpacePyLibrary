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
from tkinter import ttk, simpledialog
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import SPACE.IF
import UTIL.DU

###########
# classes #
###########
# =============================================================================
class TreeView(ttk.Treeview):
  """Variable packet tree view"""
  # ---------------------------------------------------------------------------
  def __init__(self, root):
    ttk.Treeview.__init__(self, root)
    self.bind("<Double-1>", self.itemEvent)
    self["columns"]=("name","value")
    self.column("name", width=100 )
    self.column("value", width=200)
    self.heading("name", text="Name")
    self.heading("value", text="Value")
    self.treeMap = {}
    self.toplevelStruct = None
  # ---------------------------------------------------------------------------
  def fillTree(self, treeName, struct):
    """fills a toplevel VPstruct into the tree"""
    # delete the old contents
    self.treeMap = {}
    self.delete(*self.get_children())
    # fill the new contents
    self.toplevelStruct = struct
    self.fillStructInTree("", treeName, struct)
  # ---------------------------------------------------------------------------
  def fillParamInTree(self, parentNodeID, slotName, param):
    """fills a VPparam into the tree"""
    paramName = param.getParamName()
    paramValue = param.value
    nodeID = self.insert(parentNodeID, "end", text=slotName, values=(paramName, str(paramValue)))
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
    nodeID = self.insert(parentNodeID , "end", text=structName, values=("", ""))
    self.treeMap[nodeID] = struct
    for slot in struct.slots:
      self.fillSlotInTree(nodeID, slot)
  # ---------------------------------------------------------------------------
  def fillListInTree(self, parentNodeID, slotName, lst):
    """fills a VPlist into the tree"""
    lenParamName = lst.getLenParamName()
    nodeID = self.insert(parentNodeID, "end", text=slotName + " len", values=(lenParamName, str(len(lst))))
    self.treeMap[nodeID] = lst
    i = 0
    for entry in lst.entries:
      stuctName = "[" + str(i) + "]"
      self.fillStructInTree(nodeID, stuctName, struct=entry)
      i += 1
  # ---------------------------------------------------------------------------
  def itemEvent(self, event):
    """callback when an item in the tree is clicked"""
    nodeID = self.selection()[0]
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
    nodeKey = self.item(nodeID, "text")
    nodeValues = self.item(nodeID, "value")
    name = nodeValues[0]
    value = nodeValues[1]
    paramType = param.getParamType()
    if paramType == UTIL.DU.BITS or paramType == UTIL.DU.SBITS or \
       paramType == UTIL.DU.UNSIGNED or paramType == UTIL.DU.SIGNED:
      answer = simpledialog.askinteger("Param",
                                       nodeKey + ": " + name,
                                       parent=self,
                                       initialvalue=value)
    elif paramType == UTIL.DU.BYTES or paramType == UTIL.DU.FLOAT or \
         paramType == UTIL.DU.TIME or paramType == UTIL.DU.STRING:
      answer = simpledialog.askstring("Param",
                                      nodeKey + ": " + name,
                                      parent=self,
                                      initialvalue=value)
    else:
      answer = None
    if answer == None:
      return
    # new parameter value entered --> update param object and tree
    newValue = answer
    param.value = newValue
    self.set(nodeID, 1, newValue)
  # ---------------------------------------------------------------------------
  def structClicked(self, struct, nodeID):
    """callback when a VPstruct node is clicked"""
    pass
  # ---------------------------------------------------------------------------
  def listClicked(self, lst, nodeID):
    """callback when a VPlist node is clicked"""
    nodeKey = self.item(nodeID, "text")
    nodeValues = self.item(nodeID, "value")
    name = nodeValues[0]
    value = nodeValues[1]
    answer = simpledialog.askinteger("List",
                                     nodeKey + ": " + name,
                                     parent=self,
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
      children = list(self.get_children(nodeID))
      for child in children:
        if i >= newLen:
          self.delete(child)
        i += 1
    else:
      # do nothing
      return
    # update the len value in the display
    self.set(nodeID, 1, str(len(lst)))
  # ---------------------------------------------------------------------------
  def dumpData(self):
    """helper method"""
    LOG("TreeView.data = " + str(self.toplevelStruct), "SPACE")

# =============================================================================
class TreeBrowser(simpledialog.Dialog):
  """Variable packet tree browser"""
  # ---------------------------------------------------------------------------
  def __init__(self, master, treeName, struct):
    self.treeView = None
    self.treeName = treeName
    self.struct = struct
    simpledialog.Dialog.__init__(self, master, title="Variable Packet Tree Browser")
  # ---------------------------------------------------------------------------
  def body(self, master):
    """Intialise the dialog"""
    self.treeView = TreeView(self)
    self.treeView.fillTree(self.treeName, self.struct)
    self.treeView.pack()
