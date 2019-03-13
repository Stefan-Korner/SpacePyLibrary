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
# CNC client GUI                                                              *
#******************************************************************************
import Tkinter
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import EGSE.IF
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
class GUIview(UI.TKI.GUItabView):
  """Implementation of the Control System CNC GUI layer"""
  # ---------------------------------------------------------------------------
  def __init__(self, master):
    """Initialise all GUI elements"""
    UI.TKI.GUItabView.__init__(self, master, "CNC", "CNC Interface")
    # menu buttons
    self.menuButtons = UI.TKI.MenuButtons(self,
      [["CONN", self.connectPortCallback, COLOR_BUTTON_FG, COLOR_BUTTON_BG],
       ["DCONN", self.disconnectPortCallback, COLOR_BUTTON_FG, COLOR_BUTTON_BG, Tkinter.DISABLED],
       ["CONN2", self.connectPort2Callback, COLOR_BUTTON_FG, COLOR_BUTTON_BG],
       ["DCONN2", self.disconnectPort2Callback, COLOR_BUTTON_FG, COLOR_BUTTON_BG, Tkinter.DISABLED]])
    self.appGrid(self.menuButtons,
                 row=0,
                 columnspan=2,
                 rowweight=0,
                 sticky=Tkinter.EW)
    # CNC interface host
    self.cncHostField = UI.TKI.ValueField(self, row=1, label="CNC host:")
    self.cncHostField.set(EGSE.IF.s_cncClientConfiguration.cncHost)
    # CNC interface status
    self.cncStatusField = UI.TKI.ValueField(self, row=2, label="CNC interface status:")
    self.cncStatusField.set("INIT")
    self.cncStatusField.setBackground(COLOR_INITIALISED)
    # CNC interface port
    self.cncPortField = UI.TKI.ValueField(self, row=3, label="CNC interface port:")
    self.cncPortField.set(EGSE.IF.s_cncClientConfiguration.cncPort)
    # CNC interface status 2
    self.cncStatusField2 = UI.TKI.ValueField(self, row=4, label="CNC interface status 2:")
    self.cncStatusField2.set("INIT")
    self.cncStatusField2.setBackground(COLOR_INITIALISED)
    # CNC interface port 2
    self.cncPortField2 = UI.TKI.ValueField(self, row=5, label="CNC interface port 2:")
    self.cncPortField2.set(EGSE.IF.s_cncClientConfiguration.cncPort2)
    # log messages
    self.messageLogger = UI.TKI.MessageLogger(self, "CNC")
    self.appGrid(self.messageLogger, row=6, columnspan=2)
    # message line
    self.messageline = Tkinter.Message(self, relief=Tkinter.GROOVE)
    self.appGrid(self.messageline,
                 row=7,
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
    implementation of UI.TKI.GUItabView.fillCommandMenuItems
    """
    self.addCommandMenuItem(label="ConnectPort", command=self.connectPortCallback)
    self.addCommandMenuItem(label="DisconnectPort", command=self.disconnectPortCallback, enabled=False)
    self.addCommandMenuItem(label="ConnectPort2", command=self.connectPort2Callback)
    self.addCommandMenuItem(label="DisconnectPort2", command=self.disconnectPort2Callback, enabled=False)
  # ---------------------------------------------------------------------------
  def connectPortCallback(self):
    """Called when the ConnectPort menu entry is selected"""
    self.notifyModelTask(["CONNECTCNC"])
  # ---------------------------------------------------------------------------
  def disconnectPortCallback(self):
    """Called when the DisconnectPort menu entry is selected"""
    self.notifyModelTask(["DISCONNECTCNC"])
  # ---------------------------------------------------------------------------
  def connectPort2Callback(self):
    """Called when the ConnectPort2 menu entry is selected"""
    self.notifyModelTask(["CONNECTCNC2"])
  # ---------------------------------------------------------------------------
  def disconnectPort2Callback(self):
    """Called when the DisconnectPort2 menu entry is selected"""
    self.notifyModelTask(["DISCONNECTCNC2"])
  # ---------------------------------------------------------------------------
  def notifyStatus(self, status):
    """Generic callback when something changes in the model"""
    if status == "CNC_CONNECTED":
      self.cncConnectedNotify()
    elif status == "CNC_DISCONNECTED":
      self.cncDisconnectedNotify()
    elif status == "CNC2_CONNECTED":
      self.cncConnected2Notify()
    elif status == "CNC2_DISCONNECTED":
      self.cncDisconnected2Notify()
  # ---------------------------------------------------------------------------
  def cncConnectedNotify(self):
    """Called when the CNC port connect function is successfully processed"""
    self.cncStatusField.set("CONNECTED")
    self.cncStatusField.setBackground(COLOR_CONNECTED)
    self.menuButtons.setState("CONN", Tkinter.DISABLED)
    self.menuButtons.setState("DCONN", Tkinter.NORMAL)
    self.disableCommandMenuItem("ConnectPort")
    self.enableCommandMenuItem("DisconnectPort")
  # ---------------------------------------------------------------------------
  def cncDisconnectedNotify(self):
    """Called when the CNC port disconnect function is successfully processed"""
    self.cncStatusField.set("DISCONNECTED")
    self.cncStatusField.setBackground(COLOR_INITIALISED)
    self.menuButtons.setState("CONN", Tkinter.NORMAL)
    self.menuButtons.setState("DCONN", Tkinter.DISABLED)
    self.enableCommandMenuItem("ConnectPort")
    self.disableCommandMenuItem("DisconnectPort")
  # ---------------------------------------------------------------------------
  def cncConnected2Notify(self):
    """Called when the CNC port 2 connect function is successfully processed"""
    self.cncStatusField2.set("CONNECTED")
    self.cncStatusField2.setBackground(COLOR_CONNECTED)
    self.menuButtons.setState("CONN2", Tkinter.DISABLED)
    self.menuButtons.setState("DCONN2", Tkinter.NORMAL)
    self.disableCommandMenuItem("ConnectPort2")
    self.enableCommandMenuItem("DisconnectPort2")
  # ---------------------------------------------------------------------------
  def cncDisconnected2Notify(self):
    """Called when the CNC port 2 disconnect function is successfully processed"""
    self.cncStatusField2.set("DISCONNECTED")
    self.cncStatusField2.setBackground(COLOR_INITIALISED)
    self.menuButtons.setState("CONN2", Tkinter.NORMAL)
    self.menuButtons.setState("DCONN2", Tkinter.DISABLED)
    self.enableCommandMenuItem("ConnectPort2")
    self.disableCommandMenuItem("DisconnectPort2")
