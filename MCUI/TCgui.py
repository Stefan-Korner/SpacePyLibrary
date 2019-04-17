#******************************************************************************
# (C) 2018, Stefan Korner, Austria                                            *
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
# Monitoring and Control (M&C) - Control (TC) GUI                             *
#******************************************************************************
import tkinter
from tkinter import simpledialog
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import MC.IF
import PUS.VP
import SPACE.IF
import SPACEUI.VPgui
import UI.TKI

#############
# constants #
#############
COLOR_BUTTON_FG = "#FFFFFF"
COLOR_BUTTON_BG = "#808080"
COLOR_INITIALISED = "#FFFF00"
COLOR_CONNECTED = "#00FF00"

###########
# classes #
###########
# =============================================================================
class TCpacketDetails(tkinter.Frame, UI.TKI.AppGrid):
  """Displays the packet details, implemented as tkinter.Frame"""
  # ---------------------------------------------------------------------------
  def __init__(self, master):
    tkinter.Frame.__init__(self, master, relief=tkinter.GROOVE, borderwidth=1)
    # --- filler ---
    filler = tkinter.Label(self)
    self.appGrid(filler, row=0, columnspan=2, rowweight=0)
    # packet name
    self.pktNameField = UI.TKI.ValueField(self, row=1, label="Packet name:")
    # packet description
    self.pktDescrField = UI.TKI.ValueField(self, row=2, label="Packet description:")
    # packet description 2
    self.pktDescrField2 = UI.TKI.ValueField(self, row=3, label="Packet description 2:")
    # APID
    self.pktAPIDfield = UI.TKI.ValueField(self, row=4, label="Packet APID:")
    # Type
    self.pktTypeField = UI.TKI.ValueField(self, row=5, label="Packet Type:")
    # Subtype
    self.pktSubtypeField = UI.TKI.ValueField(self, row=6, label="Packet Subtype:")
    # PI1
    self.pktPI1field = UI.TKI.ValueField(self, row=7, label="Packet PI1:")
    # PI2
    self.pktPI2field = UI.TKI.ValueField(self, row=8, label="Packet PI2:")
    # --- parameter tree ---
    label = tkinter.Label(self, text="Parameters")
    self.appGrid(label, row=0, column=2, rowweight=0)
    self.parametersTreeview = SPACEUI.VPgui.TreeView(self)
    self.appGrid(self.parametersTreeview, row=1, column=2, rowspan=8, rowweight=0, columnweight=1)
    # --- filler ---
    filler = tkinter.Label(self)
    self.appGrid(filler, row=9, columnspan=3, rowweight=0)
    # --- route ---
    self.routeField = UI.TKI.InputField(self, row=10, label="route:")
    self.appGrid(self.routeField.field, row=10, column=1, columnspan=2, rowweight=0)
    # --- filler ---
    filler = tkinter.Label(self)
    self.appGrid(filler, row=11, columnspan=3, rowweight=0)
    # TC Struct for variable packet parameters
    self.tcStruct = None
  # ---------------------------------------------------------------------------
  def update(self, tcPktDef):
    """Update the packet fields"""
    # fetch the data
    pktName = ""
    pktDescr = ""
    pktDescr2 = ""
    pktAPID = ""
    pktType = ""
    pktSType = ""
    pktPI1val = ""
    pktPI2val = ""
    self.tcStruct = None
    if tcPktDef != None:
      pktName = tcPktDef.pktName
      pktDescr = tcPktDef.pktDescr
      pktDescr2 = tcPktDef.pktDescr2
      pktAPID = tcPktDef.pktAPID
      pktType = tcPktDef.pktType
      pktSType = tcPktDef.pktSType
      if tcPktDef.pktPI1val != None:
        pktPI1val = tcPktDef.pktPI1val
      if tcPktDef.pktPI2val != None:
        pktPI2val = tcPktDef.pktPI2val
      tcStructDef = tcPktDef.tcStructDef
      self.tcStruct = PUS.VP.Struct(tcStructDef)
    # write the data into the GUI
    self.pktNameField.set(pktName)
    self.pktDescrField.set(pktDescr)
    self.pktDescrField2.set(pktDescr2)
    self.pktAPIDfield.set(pktAPID)
    self.pktTypeField.set(pktType)
    self.pktSubtypeField.set(pktSType)
    self.pktPI1field.set(pktPI1val)
    self.pktPI2field.set(pktPI2val)
    self.parametersTreeview.fillTree(pktName, self.tcStruct)

# =============================================================================
class TCpacketBrowser(simpledialog.Dialog, UI.TKI.AppGrid):
  """Browser for TC packets"""
  # ---------------------------------------------------------------------------
  def __init__(self, master, title, prompt=""):
    """Read the MIB for obtaining the initialisation data"""
    # initialise the dialog
    self.prompt = prompt
    self.listboxCurrent = None
    self.afterID = None
    simpledialog.Dialog.__init__(self, master, title=title)
    if self.afterID != None:
      self.after_cancel(self.afterID)
  # ---------------------------------------------------------------------------
  def body(self, master):
    """Intialise the dialog"""
    row=0
    if self.prompt != "":
      label = tkinter.Label(master, text=self.prompt)
      label.grid(row=row, column=0, columnspan=4)
      row += 1
      label = tkinter.Label(master)
      label.grid(row=row, column=0, columnspan=4)
      row += 1
    # scrolled list box
    self.slistbox = UI.TKI.ScrolledListbox(master, selectmode=tkinter.SINGLE)
    self.appGrid(self.slistbox, row=row, column=0, columnweight=1)
    lrow = 0
    for tcPktDef in SPACE.IF.s_definitions.getTCpktDefs():
      packetName = tcPktDef.pktName
      self.insertListboxRow(lrow, packetName)
      lrow += 1
    self.pollListbox()
    # details
    self.details = TCpacketDetails(master)
    self.appGrid(self.details, row=row, column=1, columnweight=0)
  # ---------------------------------------------------------------------------
  def insertListboxRow(self, row, text):
    """Inserts a row into self.slistbox"""
    self.slistbox.list().insert(row, text)
  # ---------------------------------------------------------------------------
  def listboxHasChanged(self, pos):
    """Callback when the selection of self.slistbox has been changed"""
    if pos != None:
      # display the packet data
      tcPktDef = SPACE.IF.s_definitions.getTCpktDefByIndex(pos)
      self.details.update(tcPktDef)
  # ---------------------------------------------------------------------------
  def pollListbox(self):
    """Polls if the selection of self.slistbox has been changed"""
    now = self.slistbox.list().curselection()
    if now != self.listboxCurrent:
      if len(now) > 0:
        self.listboxHasChanged(int(now[0]))
      else:
        self.listboxHasChanged(None)
      self.listboxCurrent = now
    self.afterID = self.after(250, self.pollListbox)
  # ---------------------------------------------------------------------------
  def apply(self):
    """Callback when the OK button is pressed"""
    packetName = self.details.pktNameField.get()
    if packetName != "":
      route = self.details.routeField.get()
      tcStruct = self.details.tcStruct
      self.result = [packetName, route, tcStruct]

# =============================================================================
class GUIview(UI.TKI.GUItabView):
  """Implementation of the M&C Control layer"""
  # ---------------------------------------------------------------------------
  def __init__(self, master):
    """Initialise all GUI elements"""
    UI.TKI.GUItabView.__init__(self, master, "TC", "M&C TC")
    # menu buttons
    self.menuButtons = UI.TKI.MenuButtons(self,
      [["PKT", self.setPacketDataCallback, COLOR_BUTTON_FG, COLOR_BUTTON_BG, tkinter.DISABLED],
       ["SND", self.sendPacketCallback, COLOR_BUTTON_FG, COLOR_BUTTON_BG, tkinter.DISABLED]])
    self.appGrid(self.menuButtons,
                 row=0,
                 columnspan=2,
                 rowweight=0,
                 sticky=tkinter.EW)
    # tc status
    self.tcStatusField = UI.TKI.ValueField(self, row=1, label="TC status:")
    self.tcStatusField.set("INIT")
    self.tcStatusField.setBackground(COLOR_INITIALISED)
    # packet
    self.packetField = UI.TKI.ValueField(self, row=2, label="Packet:")
    # route
    self.routeField = UI.TKI.ValueField(self, row=3, label="Route:")
    # log messages (default logger)
    self.messageLogger = UI.TKI.MessageLogger(self, "TC")
    self.appGrid(self.messageLogger, row=4, columnspan=2)
    # message line
    self.messageline = tkinter.Message(self, relief=tkinter.GROOVE)
    self.appGrid(self.messageline,
                 row=5,
                 columnspan=2,
                 rowweight=0,
                 columnweight=0,
                 sticky=tkinter.EW)
    self.grid(row=0, column=0, sticky=tkinter.EW+tkinter.NS)
    self.master.rowconfigure(0, weight=1)
    self.master.columnconfigure(0, weight=1)
  # ---------------------------------------------------------------------------
  def fillCommandMenuItems(self):
    """
    fill the command menu bar,
    implementation of UI.TKI.GUItabView.fillCommandMenuItems
    """
    self.addCommandMenuItem(label="SetPacketData", command=self.setPacketDataCallback, enabled=False)
    self.addCommandMenuItem(label="SendPacket", command=self.sendPacketCallback, enabled=False)
  # ---------------------------------------------------------------------------
  def setPacketDataCallback(self):
    """Called when the SetPacketData menu entry is selected"""
    # do the dialog
    dialog = TCpacketBrowser(self,
      title="Set Packet Data Dialog",
      prompt="Please select a packet.")
    if dialog.result != None:
      packetName, route, tcStruct = dialog.result
      self.notifyModelTask(["SETPACKETDATA", packetName, route], tcStruct)
  # ---------------------------------------------------------------------------
  def sendPacketCallback(self):
    """Called when the SendPacket menu entry is selected"""
    self.notifyModelTask(["SENDPACKET"])
  # ---------------------------------------------------------------------------
  def notifyStatus(self, status):
    """Generic callback when something changes in the model"""
    if status == "TC_CONNECTED":
      self.tcConnectedNotify()
    elif status == "PACKETDATA_SET":
      self.packetDataSetNotify()
  # ---------------------------------------------------------------------------
  def tcConnectedNotify(self):
    """Called when the TC connect function is successfully processed"""
    self.enableCommandMenuItem("SetPacketData")
    self.menuButtons.setState("PKT", tkinter.NORMAL)
    self.updateTCstatusField()
  # ---------------------------------------------------------------------------
  def packetDataSetNotify(self):
    """Called when the setPacketData function is successfully processed"""
    self.enableCommandMenuItem("SendPacket")
    self.menuButtons.setState("SND", tkinter.NORMAL)
    self.updateTCstatusField()
    self.packetField.set(MC.IF.s_configuration.tcPacketData.pktName)
    self.routeField.set(MC.IF.s_configuration.tcPacketData.route)
  # ---------------------------------------------------------------------------
  def updateTCstatusField(self):
    """updated the TC status field depending on the MC.IF.s_configuration"""
    if MC.IF.s_configuration.connected:
      txt = "CONNECTED"
      bgColor = COLOR_CONNECTED
    else:
      txt = "INIT"
    if MC.IF.s_configuration.tcPacketData != None:
      txt += " + PKT DEFINED"
    self.tcStatusField.set(txt)
    if MC.IF.s_configuration.connected:
      self.tcStatusField.setBackground(bgColor)
