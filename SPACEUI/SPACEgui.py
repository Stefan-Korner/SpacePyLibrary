#******************************************************************************
# (C) 2014, Stefan Korner, Austria                                            *
#                                                                             *
# The Space Python Library is free software; you can redistribute it and/or   *
# modify it under the terms of the GNU Lesser General Public License as       *
# published by the Free Software Foundation; either version 2.1 of the        *
# License, or (at your option) any later version.                             *
#                                                                             *
# The Space Python Library is distributed in the hope that it will be useful, *
# but WITHOUT ANY WARRANTY; without even the implied warranty of              *
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser     *
# General Public License for more details.                                    *
#******************************************************************************
# Space Segment Simulation GUI                                                *
#******************************************************************************
import Tkinter, tkFileDialog, tkSimpleDialog
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import SCOS.ENV
import SPACE.IF
import UI.TKI
import UTIL.TIME

#############
# constants #
#############
COLOR_BUTTON_FG = "#FFFFFF"
COLOR_BUTTON_BG = "#808080"
COLOR_INITIALISED = "#FFFF00"
COLOR_CONNECTED = "#00FF00"
COLOR_ON_OK = "#00FF00"
COLOR_ON_NOK = "#FF0000"

###########
# classes #
###########
# =============================================================================
class TMpacketDetails(Tkinter.Frame, UI.TKI.AppGrid):
  """Displays the packet details, implemented as Tkinter.Frame"""
  # ---------------------------------------------------------------------------
  def __init__(self, master):
    Tkinter.Frame.__init__(self, master, relief=Tkinter.GROOVE, borderwidth=1)
    # --- filler ---
    filler = Tkinter.Label(self)
    self.appGrid(filler, row=0, columnspan=2, rowweight=0)
    # packet name
    self.pktNameField = UI.TKI.ValueField(self, row=1, label="Packet name:")
    # packet description
    self.pktDescrField = UI.TKI.ValueField(self, row=2, label="Packet description:")
    # SPID
    self.pktSPIDfield = UI.TKI.ValueField(self, row=3, label="Packet SPID:")
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
    # --- parameter listbox ---
    label = Tkinter.Label(self, text="Parameters")
    self.appGrid(label, row=0, column=2, rowweight=0)
    self.parametersListbox = UI.TKI.ScrolledListbox(self, selectmode=Tkinter.SINGLE)
    self.appGrid(self.parametersListbox, row=1, column=2, rowspan=8, rowweight=0, columnweight=1)
    # --- filler ---
    filler = Tkinter.Label(self)
    self.appGrid(filler, row=9, columnspan=3, rowweight=0)
    # parameter names
    self.parameterNamesField = UI.TKI.InputField(self, row=10, label="Parameter names: optional")
    self.appGrid(self.parameterNamesField.field, row=10, column=1, columnspan=2, rowweight=0)
    # parameter values
    self.parameterValuesField = UI.TKI.InputField(self, row=11, label="Parameter value: optional")
    self.appGrid(self.parameterValuesField.field, row=11, column=1, columnspan=2, rowweight=0)
    # --- filler ---
    filler = Tkinter.Label(self)
    self.appGrid(filler, row=12, columnspan=3, rowweight=0)
  # ---------------------------------------------------------------------------
  def update(self, tmPktDef):
    """Update the packet fields"""
    # fetch the data
    pktName = ""
    pktDescr = ""
    pktSPID = ""
    pktAPID = ""
    pktType = ""
    pktSType = ""
    pktPI1val = ""
    pktPI2val = ""
    tmParamExtractions = []
    if tmPktDef != None:
      pktName = tmPktDef.pktName
      pktDescr = tmPktDef.pktDescr
      pktSPID = tmPktDef.pktSPID
      pktAPID = tmPktDef.pktAPID
      pktType = tmPktDef.pktType
      pktSType = tmPktDef.pktSType
      if tmPktDef.pktPI1val != None:
        pktPI1val = tmPktDef.pktPI1val
      if tmPktDef.pktPI2val != None:
        pktPI2val = tmPktDef.pktPI2val
      tmParamExtractions = tmPktDef.getParamExtractions()
    # write the data into the GUI
    self.pktNameField.set(pktName)
    self.pktDescrField.set(pktDescr)
    self.pktSPIDfield.set(pktSPID)
    self.pktAPIDfield.set(pktAPID)
    self.pktTypeField.set(pktType)
    self.pktSubtypeField.set(pktSType)
    self.pktPI1field.set(pktPI1val)
    self.pktPI2field.set(pktPI2val)
    lrow = 0
    self.parametersListbox.list().delete(0, Tkinter.END)
    for tmParamExtraction in tmParamExtractions:
      if tmParamExtraction.piValue:
        continue
      text = tmParamExtraction.name + " ---> " + tmParamExtraction.descr
      self.parametersListbox.list().insert(lrow, text)
      lrow += 1

# =============================================================================
class TMpacketBrowser(tkSimpleDialog.Dialog, UI.TKI.AppGrid):
  """Browser for TM packets"""
  # ---------------------------------------------------------------------------
  def __init__(self, master, title, prompt=""):
    """Read the MIB for obtaining the initialisation data"""
    # initialise the dialog
    self.prompt = prompt
    self.listboxCurrent = None
    self.afterID = None
    tkSimpleDialog.Dialog.__init__(self, master, title=title)
    if self.afterID != None:
      self.after_cancel(self.afterID)
  # ---------------------------------------------------------------------------
  def body(self, master):
    """Intialise the dialog"""
    row=0
    if self.prompt != "":
      label = Tkinter.Label(master, text=self.prompt)
      label.grid(row=row, column=0, columnspan=4)
      row += 1
      label = Tkinter.Label(master)
      label.grid(row=row, column=0, columnspan=4)
      row += 1
    # scrolled list box
    self.slistbox = UI.TKI.ScrolledListbox(master, selectmode=Tkinter.SINGLE)
    self.appGrid(self.slistbox, row=row, column=0, columnweight=1)
    lrow = 0
    for tmPktDef in SPACE.IF.s_definitions.getTMpktDefs():
      packetName = tmPktDef.pktName
      self.insertListboxRow(lrow, packetName)
      lrow += 1
    self.pollListbox()
    # details
    self.details = TMpacketDetails(master)
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
      tmPktDef = SPACE.IF.s_definitions.getTMpktDefByIndex(pos)
      self.details.update(tmPktDef)
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
      paramNames = self.details.parameterNamesField.get()
      paramValues = self.details.parameterValuesField.get()
      self.result = [packetName, paramNames, paramValues]

# =============================================================================
class GUIview(UI.TKI.GUIwinView):
  """Implementation of the SIM Space GUI layer"""
  # ---------------------------------------------------------------------------
  def __init__(self, master):
    """Initialise all GUI elements"""
    UI.TKI.GUIwinView.__init__(self, master, "SPACE", "Space Segment")
    # menu buttons
    self.menuButtons = UI.TKI.MenuButtons(self,
      [["PKT", self.setPacketDataCallback, COLOR_BUTTON_FG, COLOR_BUTTON_BG, Tkinter.DISABLED],
       ["SND", self.sendPacketCallback, COLOR_BUTTON_FG, COLOR_BUTTON_BG, Tkinter.DISABLED],
       ["ACK", self.sendAckCallback, COLOR_BUTTON_FG, COLOR_BUTTON_BG, Tkinter.DISABLED],
       ["RPLY", self.replayPacketsCallback, COLOR_BUTTON_FG, COLOR_BUTTON_BG, Tkinter.DISABLED],
       ["LIST", self.listPacketsCallback, COLOR_BUTTON_FG, COLOR_BUTTON_BG],
       ["GEN", self.generateCallback, COLOR_BUTTON_FG, COLOR_BUTTON_BG]])
    self.appGrid(self.menuButtons,
                 row=0,
                 columnspan=2,
                 rowweight=0,
                 sticky=Tkinter.EW)
    # checkbuttons
    self.checkButtons = UI.TKI.Checkbuttons(self,
      [["TM", self.cyclicCallback, False, COLOR_ON_OK],
       ["ACK1", self.ack1Callback, True, COLOR_ON_OK],
       ["NAK1", self.nak1Callback, False, COLOR_ON_NOK],
       ["ACK2", self.ack2Callback, True, COLOR_ON_OK],
       ["NAK2", self.nak2Callback, False, COLOR_ON_NOK],
       ["ACK3", self.ack3Callback, True, COLOR_ON_OK],
       ["NAK3", self.nak3Callback, False, COLOR_ON_NOK],
       ["ACK4", self.ack4Callback, True, COLOR_ON_OK],
       ["NAK4", self.nak4Callback, False, COLOR_ON_NOK]])
    self.appGrid(self.checkButtons,
                 row=1,
                 columnspan=2,
                 rowweight=0,
                 columnweight=0,
                 sticky=Tkinter.W)
    # tm status
    self.tmStatusField = UI.TKI.ValueField(self, row=2, label="TM status:")
    self.tmStatusField.set("INIT")
    self.tmStatusField.setBackground(COLOR_INITIALISED)
    # packet
    self.packetField = UI.TKI.ValueField(self, row=3, label="Packet:")
    # SPID
    self.spidField = UI.TKI.ValueField(self, row=4, label="SPID:")
    # parameter values
    self.parameterValuesField = UI.TKI.ValueField(self, row=5, label="Parameters and values:")
    # replay TM packets
    self.replayTMpacketsField = UI.TKI.ValueField(self, row=6, label="Replay TM packets:")
    # log messages
    self.messageLogger = UI.TKI.MessageLogger(self, "SPACE")
    self.appGrid(self.messageLogger, row=7, columnspan=2)
    # message line
    self.messageline = Tkinter.Message(self, relief=Tkinter.GROOVE)
    self.appGrid(self.messageline,
                 row=8,
                 columnspan=2,
                 rowweight=0,
                 columnweight=0,
                 sticky=Tkinter.EW)
    self.grid(row=0, column=0, sticky=Tkinter.EW+Tkinter.NS)
    self.master.rowconfigure(0, weight=1)
    self.master.columnconfigure(0, weight=1)
  # ---------------------------------------------------------------------------
  def fillCommandMenuItems(self):
    """
    fill the command menu bar,
    implementation of UI.TKI.GUIwinView.fillCommandMenuItems
    """
    self.addCommandMenuItem(label="SetPacketData", command=self.setPacketDataCallback, enabled=False)
    self.addCommandMenuItem(label="SendPacket", command=self.sendPacketCallback, enabled=False)
    self.addCommandMenuItem(label="EnableCyclic", command=self.enableCyclicCallback)
    self.addCommandMenuItem(label="DisableCyclic", command=self.disableCyclicCallback, enabled=False)
    self.addCommandMenuItem(label="OBCenableAck1", command=self.obcEnableAck1Callback, enabled=False)
    self.addCommandMenuItem(label="OBCenableNak1", command=self.obcEnableNak1Callback)
    self.addCommandMenuItem(label="OBCdisableAck1", command=self.obcDisableAck1Callback)
    self.addCommandMenuItem(label="OBCenableAck2", command=self.obcEnableAck2Callback, enabled=False)
    self.addCommandMenuItem(label="OBCenableNak2", command=self.obcEnableNak2Callback)
    self.addCommandMenuItem(label="OBCdisableAck2", command=self.obcDisableAck2Callback)
    self.addCommandMenuItem(label="OBCenableAck3", command=self.obcEnableAck3Callback, enabled=False)
    self.addCommandMenuItem(label="OBCenableNak3", command=self.obcEnableNak3Callback)
    self.addCommandMenuItem(label="OBCdisableAck3", command=self.obcDisableAck3Callback)
    self.addCommandMenuItem(label="OBCenableAck4", command=self.obcEnableAck4Callback, enabled=False)
    self.addCommandMenuItem(label="OBCenableNak4", command=self.obcEnableNak4Callback)
    self.addCommandMenuItem(label="OBCdisableAck4", command=self.obcDisableAck4Callback)
    self.addCommandMenuItem(label="SendAck", command=self.sendAckCallback, enabled=False)
    self.addCommandMenuItem(label="ReplayPackets", command=self.replayPacketsCallback, enabled=False)
    self.addCommandMenuItem(label="ListPackets", command=self.listPacketsCallback)
    self.addCommandMenuItem(label="Generate", command=self.generateCallback)
  # ---------------------------------------------------------------------------
  def setPacketDataCallback(self):
    """Called when the SetPacketData menu entry is selected"""
    # do the dialog
    dialog = TMpacketBrowser(self,
      title="Set Packet Data Dialog",
      prompt="Please select a packet and enter virtual channel and parameter name/values.")
    if dialog.result != None:
      packetName, paramNames, paramValues = dialog.result
      if paramNames == "" or paramValues == "":
        self.notifyModelTask(["SETPACKETDATA", packetName])
      else:
        self.notifyModelTask(["SETPACKETDATA", packetName, paramNames, paramValues])
  # ---------------------------------------------------------------------------
  def sendPacketCallback(self):
    """Called when the SendPacket menu entry is selected"""
    self.notifyModelTask(["SENDPACKET"])
  # ---------------------------------------------------------------------------
  def enableCyclicCallback(self):
    """Called when the EnableCyclic menu entry is selected"""
    self.notifyModelTask(["ENABLECYCLIC"])
  def disableCyclicCallback(self):
    """Called when the DisableCyclic menu entry is selected"""
    self.notifyModelTask(["DISABLECYCLIC"])
  def cyclicCallback(self):
    """Called when the TM checkbutton is pressed"""
    if self.checkButtons.getButtonPressed("TM"):
      self.notifyModelTask(["ENABLECYCLIC"])
    else:
      self.notifyModelTask(["DISABLECYCLIC"])
  # ---------------------------------------------------------------------------
  def obcEnableAck1Callback(self):
    """Called when the OBCenableAck1 menu entry is selected"""
    self.notifyModelTask(["OBCENABLEACK1"])
  def obcEnableNak1Callback(self):
    """Called when the OBCenableNak1 menu entry is selected"""
    self.notifyModelTask(["OBCENABLENAK1"])
  def obcDisableAck1Callback(self):
    """Called when the OBCdisableAck1 menu entry is selected"""
    self.notifyModelTask(["OBCDISABLEACK1"])
  def ack1Callback(self):
    """Called when the ACK1 checkbutton is pressed"""
    if self.checkButtons.getButtonPressed("ACK1"):
      self.notifyModelTask(["OBCENABLEACK1"])
    else:
      self.notifyModelTask(["OBCDISABLEACK1"])
  def nak1Callback(self):
    """Called when the NAK1 checkbutton is pressed"""
    if self.checkButtons.getButtonPressed("NAK1"):
      self.notifyModelTask(["OBCENABLENAK1"])
    else:
      self.notifyModelTask(["OBCDISABLEACK1"])
  # ---------------------------------------------------------------------------
  def obcEnableAck2Callback(self):
    """Called when the OBCenableAck2 menu entry is selected"""
    self.notifyModelTask(["OBCENABLEACK2"])
  def obcEnableNak2Callback(self):
    """Called when the OBCenableNak2 menu entry is selected"""
    self.notifyModelTask(["OBCENABLENAK2"])
  def obcDisableAck2Callback(self):
    """Called when the OBCdisableAck2 menu entry is selected"""
    self.notifyModelTask(["OBCDISABLEACK2"])
  def ack2Callback(self):
    """Called when the ACK2 checkbutton is pressed"""
    if self.checkButtons.getButtonPressed("ACK2"):
      self.notifyModelTask(["OBCENABLEACK2"])
    else:
      self.notifyModelTask(["OBCDISABLEACK2"])
  def nak2Callback(self):
    """Called when the NAK2 checkbutton is pressed"""
    if self.checkButtons.getButtonPressed("NAK2"):
      self.notifyModelTask(["OBCENABLENAK2"])
    else:
      self.notifyModelTask(["OBCDISABLEACK2"])
  # ---------------------------------------------------------------------------
  def obcEnableAck3Callback(self):
    """Called when the OBCenableAck3 menu entry is selected"""
    self.notifyModelTask(["OBCENABLEACK3"])
  def obcEnableNak3Callback(self):
    """Called when the OBCenableNak3 menu entry is selected"""
    self.notifyModelTask(["OBCENABLENAK3"])
  def obcDisableAck3Callback(self):
    """Called when the OBCdisableAck3 menu entry is selected"""
    self.notifyModelTask(["OBCDISABLEACK3"])
  def ack3Callback(self):
    """Called when the ACK3 checkbutton is pressed"""
    if self.checkButtons.getButtonPressed("ACK3"):
      self.notifyModelTask(["OBCENABLEACK3"])
    else:
      self.notifyModelTask(["OBCDISABLEACK3"])
  def nak3Callback(self):
    """Called when the NAK3 checkbutton is pressed"""
    if self.checkButtons.getButtonPressed("NAK3"):
      self.notifyModelTask(["OBCENABLENAK3"])
    else:
      self.notifyModelTask(["OBCDISABLEACK3"])
  # ---------------------------------------------------------------------------
  def obcEnableAck4Callback(self):
    """Called when the OBCenableAck4 menu entry is selected"""
    self.notifyModelTask(["OBCENABLEACK4"])
  def obcEnableNak4Callback(self):
    """Called when the OBCenableNak4 menu entry is selected"""
    self.notifyModelTask(["OBCENABLENAK4"])
  def obcDisableAck4Callback(self):
    """Called when the OBCdisableAck4 menu entry is selected"""
    self.notifyModelTask(["OBCDISABLEACK4"])
  def ack4Callback(self):
    """Called when the ACK4 checkbutton is pressed"""
    if self.checkButtons.getButtonPressed("ACK4"):
      self.notifyModelTask(["OBCENABLEACK4"])
    else:
      self.notifyModelTask(["OBCDISABLEACK4"])
  def nak4Callback(self):
    """Called when the NAK4 checkbutton is pressed"""
    if self.checkButtons.getButtonPressed("NAK4"):
      self.notifyModelTask(["OBCENABLENAK4"])
    else:
      self.notifyModelTask(["OBCDISABLEACK4"])
  # ---------------------------------------------------------------------------
  def sendAckCallback(self):
    """Called when the SendAck menu entry is selected"""
    dialog = UI.TKI.InputDialog(master=self,
      title="TC Acknowledgement",
      prompt="Enter data for TC Acknowledgement Report (PUS service 1)",
      fieldsSpec = [["InputField", "TC APID:"],
                    ["InputField", "TC SSC:"],
                    ["Radiobuttons", "Subtype 1 - Accept Success:|" +
                                     "Subtype 2 - Accept Fail:|" +
                                     "Subtype 3 - Exec Start Success:|" +
                                     "Subtype 4 - Exec Start Fail:|" +
                                     "Subtype 5 - Exec Proceed Success:|" +
                                     "Subtype 6 - Exec Proceed Fail:|" +
                                     "Subtype 7 - Exec Finish Success:|" +
                                     "Subtype 8 - Exec Finish Fail:"]])
    if dialog.result != None:
      apidStr = dialog.result[0]
      sscStr = dialog.result[1]
      subtypeStr = str(dialog.result[2] + 1)
      self.notifyModelTask(["SENDACK", apidStr, sscStr, subtypeStr])
  # ---------------------------------------------------------------------------
  def replayPacketsCallback(self):
    """Called when the ReplayPackets menu entry is selected"""
    fileName = tkFileDialog.askopenfilename(title="Open TM Packet Replay File",
                                            initialdir=SCOS.ENV.s_environment.tmFilesDir())
    if fileName != "" and fileName != ():
      self.notifyModelTask(["REPLAYPACKETS", fileName])
  # ---------------------------------------------------------------------------
  def listPacketsCallback(self):
    """Called when the ListPackets menu entry is selected"""
    # disable the button during generation,
    # because generation could take some time
    self.menuButtons.setState("LIST", Tkinter.DISABLED)
    self.notifyModelTask(["LISTPACKETS"])
    self.menuButtons.setState("LIST", Tkinter.NORMAL)
  # ---------------------------------------------------------------------------
  def generateCallback(self):
    """Called when the Generate menu entry is selected"""
    # disable the button during generation,
    # because generation could take some time
    self.menuButtons.setState("GEN", Tkinter.DISABLED)
    self.notifyModelTask(["GENERATE"])
    self.menuButtons.setState("GEN", Tkinter.NORMAL)
  # ---------------------------------------------------------------------------
  def notifyStatus(self, status):
    """Generic callback when something changes in the model"""
    if status == "TM_CONNECTED":
      self.tmConnectedNotify()
    elif status == "TM_RECORDING":
      self.tmRecordingNotify()
    elif status == "PACKETDATA_SET":
      self.packetDataSetNotify()
    elif status == "UPDATE_REPLAY":
      self.updateReplayNotify()
    elif status == "ENABLED_CYCLIC":
      self.enabledCyclicNotify()
    elif status == "DISABLED_CYCLIC":
      self.disabledCyclicNotify()
    elif status == "OBC_ENABLED_ACK1":
      self.obcEnabledAck1Notify()
    elif status == "OBC_ENABLED_NAK1":
      self.obcEnabledNak1Notify()
    elif status == "OBC_DISABLED_ACK1":
      self.obcDisabledAck1Notify()
    elif status == "OBC_ENABLED_ACK2":
      self.obcEnabledAck2Notify()
    elif status == "OBC_ENABLED_NAK2":
      self.obcEnabledNak2Notify()
    elif status == "OBC_DISABLED_ACK2":
      self.obcDisabledAck2Notify()
    elif status == "OBC_ENABLED_ACK3":
      self.obcEnabledAck3Notify()
    elif status == "OBC_ENABLED_NAK3":
      self.obcEnabledNak3Notify()
    elif status == "OBC_DISABLED_ACK3":
      self.obcDisabledAck3Notify()
    elif status == "OBC_ENABLED_ACK4":
      self.obcEnabledAck4Notify()
    elif status == "OBC_ENABLED_NAK4":
      self.obcEnabledNak4Notify()
    elif status == "OBC_DISABLED_ACK4":
      self.obcDisabledAck4Notify()
    elif status == "FRAME_REC_STARTED":
      self.frameRecStarted()
    elif status == "FRAME_REC_STOPPED":
      self.frameRecStopped()
  # ---------------------------------------------------------------------------
  def tmConnectedNotify(self):
    """Called when the TM connect function is succsssfully processed"""
    self.enableCommandMenuItem("SetPacketData")
    self.enableCommandMenuItem("EnableCyclic")
    self.enableCommandMenuItem("SendAck")
    self.enableCommandMenuItem("ReplayPackets")
    self.menuButtons.setState("PKT", Tkinter.NORMAL)
    self.menuButtons.setState("ACK", Tkinter.NORMAL)
    self.menuButtons.setState("RPLY", Tkinter.NORMAL)
    self.updateTMstatusField()
  # ---------------------------------------------------------------------------
  def packetDataSetNotify(self):
    """Called when the setPacketData function is succsssfully processed"""
    self.enableCommandMenuItem("SendPacket")
    self.menuButtons.setState("SND", Tkinter.NORMAL)
    self.updateTMstatusField()
    self.packetField.set(SPACE.IF.s_configuration.tmPacketData.pktName)
    self.spidField.set(SPACE.IF.s_configuration.tmPacketData.pktSPID)
    nameValueStr = ""
    for nameValue in SPACE.IF.s_configuration.tmPacketData.parameterValuesList:
      if nameValueStr != "":
        nameValueStr += ", "
      nameValueStr += nameValue[0] + "=" + nameValue[1]
    self.parameterValuesField.set(nameValueStr)
  # ---------------------------------------------------------------------------
  def updateReplayNotify(self):
    """Called when the replay state has changed"""
    replayItems = SPACE.IF.s_tmPacketReplayer.getItems()
    nrPackets = len(replayItems)
    if nrPackets == 0:
      txt = ""
    else:
      txt = str(nrPackets) + ": "
      # item 0
      item0 = replayItems[0]
      itemType0, itemVal0 = item0
      if itemType0 == SPACE.IF.RPLY_PKT:
        txt += itemVal0.pktName
      elif itemType0 == SPACE.IF.RPLY_RAWPKT:
        txt += "raw"
      elif itemType0 == SPACE.IF.RPLY_SLEEP:
        txt += "sleep(" + str(itemVal0) + ")"
      elif itemType0 == SPACE.IF.RPLY_OBT:
        txt += "obt(" + UTIL.TIME.getASDtimeStr(itemVal0) + ")"
      else:
        txt += "ert(" + UTIL.TIME.getASDtimeStr(itemVal0) + ")"
      # item 1
      if nrPackets > 1:
        item1 = replayItems[1]
        itemType1, itemVal1 = item1
        if itemType1 == SPACE.IF.RPLY_PKT:
          txt += ", " + itemVal1.pktName
        elif itemType1 == SPACE.IF.RPLY_RAWPKT:
          txt += ", raw"
        elif itemType1 == SPACE.IF.RPLY_SLEEP:
          txt += ", sleep(" + str(itemVal1) + ")"
        elif itemType1 == SPACE.IF.RPLY_OBT:
          txt += ", obt(" + UTIL.TIME.getASDtimeStr(itemVal1) + ")"
        else:
          txt += ", ert(" + UTIL.TIME.getASDtimeStr(itemVal1) + ")"
      # item 2
      if nrPackets > 2:
        item2 = replayItems[2]
        itemType2, itemVal2 = item2
        if itemType2 == SPACE.IF.RPLY_PKT:
          txt += ", " + itemVal2.pktName
        elif itemType2 == SPACE.IF.RPLY_RAWPKT:
          txt += ", raw"
        elif itemType2 == SPACE.IF.RPLY_SLEEP:
          txt += ", sleep(" + str(itemVal2) + ")"
        elif itemType2 == SPACE.IF.RPLY_OBT:
          txt += ", obt(" + UTIL.TIME.getASDtimeStr(itemVal2) + ")"
        else:
          txt += ", ert(" + UTIL.TIME.getASDtimeStr(itemVal2) + ")"
      if nrPackets > 3:
        txt += ", ..."
    self.replayTMpacketsField.set(txt)
  # ---------------------------------------------------------------------------
  def enabledCyclicNotify(self):
    """Called when the enableCyclic function is succsssfully processed"""
    self.disableCommandMenuItem("EnableCyclic")
    self.enableCommandMenuItem("DisableCyclic")
    self.checkButtons.setButtonPressed("TM", True)
  def disabledCyclicNotify(self):
    """Called when the disableCyclic function is succsssfully processed"""
    self.enableCommandMenuItem("EnableCyclic")
    self.disableCommandMenuItem("DisableCyclic")
    self.checkButtons.setButtonPressed("TM", False)
  # ---------------------------------------------------------------------------
  def obcEnabledAck1Notify(self):
    """Called when the obcEnabledAck1 function is succsssfully processed"""
    self.disableCommandMenuItem("OBCenableAck1")
    self.enableCommandMenuItem("OBCenableNak1")
    self.enableCommandMenuItem("OBCdisableAck1")
    self.checkButtons.setButtonPressed("ACK1", True)
    self.checkButtons.setButtonPressed("NAK1", False)
  def obcEnabledNak1Notify(self):
    """Called when the obcEnabledNak1 function is succsssfully processed"""
    self.enableCommandMenuItem("OBCenableAck1")
    self.disableCommandMenuItem("OBCenableNak1")
    self.enableCommandMenuItem("OBCdisableAck1")
    self.checkButtons.setButtonPressed("ACK1", False)
    self.checkButtons.setButtonPressed("NAK1", True)
  def obcDisabledAck1Notify(self):
    """Called when the obcDisabledAck1 function is succsssfully processed"""
    self.enableCommandMenuItem("OBCenableAck1")
    self.enableCommandMenuItem("OBCenableNak1")
    self.disableCommandMenuItem("OBCdisableAck1")
    self.checkButtons.setButtonPressed("ACK1", False)
    self.checkButtons.setButtonPressed("NAK1", False)
  # ---------------------------------------------------------------------------
  def obcEnabledAck2Notify(self):
    """Called when the obcEnabledAck2 function is succsssfully processed"""
    self.disableCommandMenuItem("OBCenableAck2")
    self.enableCommandMenuItem("OBCenableNak1")
    self.enableCommandMenuItem("OBCdisableAck2")
    self.checkButtons.setButtonPressed("ACK2", True)
    self.checkButtons.setButtonPressed("NAK2", False)
  def obcEnabledNak2Notify(self):
    """Called when the obcEnabledNak2 function is succsssfully processed"""
    self.enableCommandMenuItem("OBCenableAck2")
    self.disableCommandMenuItem("OBCenableNak2")
    self.enableCommandMenuItem("OBCdisableAck2")
    self.checkButtons.setButtonPressed("ACK2", False)
    self.checkButtons.setButtonPressed("NAK2", True)
  def obcDisabledAck2Notify(self):
    """Called when the obcDisabledAck2 function is succsssfully processed"""
    self.enableCommandMenuItem("OBCenableAck2")
    self.enableCommandMenuItem("OBCenableNak2")
    self.disableCommandMenuItem("OBCdisableAck2")
    self.checkButtons.setButtonPressed("ACK2", False)
    self.checkButtons.setButtonPressed("NAK2", False)
  # ---------------------------------------------------------------------------
  def obcEnabledAck3Notify(self):
    """Called when the obcEnabledAck3 function is succsssfully processed"""
    self.disableCommandMenuItem("OBCenableAck3")
    self.enableCommandMenuItem("OBCenableNak3")
    self.enableCommandMenuItem("OBCdisableAck3")
    self.checkButtons.setButtonPressed("ACK3", True)
    self.checkButtons.setButtonPressed("NAK3", False)
  def obcEnabledNak3Notify(self):
    """Called when the obcEnabledNak3 function is succsssfully processed"""
    self.enableCommandMenuItem("OBCenableAck3")
    self.disableCommandMenuItem("OBCenableNak3")
    self.enableCommandMenuItem("OBCdisableAck3")
    self.checkButtons.setButtonPressed("ACK3", False)
    self.checkButtons.setButtonPressed("NAK3", True)
  def obcDisabledAck3Notify(self):
    """Called when the obcDisabledAck3 function is succsssfully processed"""
    self.enableCommandMenuItem("OBCenableAck3")
    self.enableCommandMenuItem("OBCenableNak3")
    self.disableCommandMenuItem("OBCdisableAck3")
    self.checkButtons.setButtonPressed("ACK3", False)
    self.checkButtons.setButtonPressed("NAK3", False)
  # ---------------------------------------------------------------------------
  def obcEnabledAck4Notify(self):
    """Called when the obcEnabledAck4 function is succsssfully processed"""
    self.disableCommandMenuItem("OBCenableAck4")
    self.enableCommandMenuItem("OBCenableNak4")
    self.enableCommandMenuItem("OBCdisableAck4")
    self.checkButtons.setButtonPressed("ACK4", True)
    self.checkButtons.setButtonPressed("NAK4", False)
  def obcEnabledNak4Notify(self):
    """Called when the obcEnabledNak4 function is succsssfully processed"""
    self.enableCommandMenuItem("OBCenableAck4")
    self.disableCommandMenuItem("OBCenableNak4")
    self.enableCommandMenuItem("OBCdisableAck4")
    self.checkButtons.setButtonPressed("ACK4", False)
    self.checkButtons.setButtonPressed("NAK4", True)
  def obcDisabledAck4Notify(self):
    """Called when the obcDisabledAck4 function is succsssfully processed"""
    self.enableCommandMenuItem("OBCenableAck4")
    self.enableCommandMenuItem("OBCenableNak4")
    self.disableCommandMenuItem("OBCdisableAck4")
    self.checkButtons.setButtonPressed("ACK4", False)
    self.checkButtons.setButtonPressed("NAK4", False)
  # ---------------------------------------------------------------------------
  def frameRecStarted(self):
    """Called when the recordFrames function is succsssfully processed"""
    self.enableCommandMenuItem("SetPacketData")
    self.enableCommandMenuItem("EnableCyclic")
    self.enableCommandMenuItem("SendAck")
    self.enableCommandMenuItem("ReplayPackets")
    self.menuButtons.setState("PKT", Tkinter.NORMAL)
    self.menuButtons.setState("ACK", Tkinter.NORMAL)
    self.menuButtons.setState("RPLY", Tkinter.NORMAL)
  # ---------------------------------------------------------------------------
  def frameRecStopped(self):
    """Called when the stopFrameRecorder function is succsssfully processed"""
    if SPACE.IF.s_configuration.connected:
      self.enableCommandMenuItem("SetPacketData")
      self.enableCommandMenuItem("EnableCyclic")
      self.enableCommandMenuItem("SendAck")
      self.enableCommandMenuItem("ReplayPackets")
      self.menuButtons.setState("PKT", Tkinter.NORMAL)
      self.menuButtons.setState("ACK", Tkinter.NORMAL)
      self.menuButtons.setState("RPLY", Tkinter.NORMAL)
    else:
      self.disableCommandMenuItem("SetPacketData")
      self.disableCommandMenuItem("EnableCyclic")
      self.disableCommandMenuItem("SendAck")
      self.disableCommandMenuItem("ReplayPackets")
      self.menuButtons.setState("PKT", Tkinter.DISABLED)
      self.menuButtons.setState("ACK", Tkinter.DISABLED)
      self.menuButtons.setState("RPLY", Tkinter.DISABLED)
  # ---------------------------------------------------------------------------
  def updateTMstatusField(self):
    """updated the TM status field depending on the SPACE.IF.s_configuration"""
    if SPACE.IF.s_configuration.connected:
      txt = "CONNECTED"
      bgColor = COLOR_CONNECTED
    else:
      txt = "INIT"
    if SPACE.IF.s_configuration.tmPacketData != None:
      txt += " + PKT DEFINED"
    self.tmStatusField.set(txt)
    if SPACE.IF.s_configuration.connected:
      self.tmStatusField.setBackground(bgColor)
