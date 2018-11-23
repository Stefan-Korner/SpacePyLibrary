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
# EGSE client GUI                                                             *
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
class GUIview(UI.TKI.GUIwinView):
  """Implementation of the Control System EGSE GUI layer"""
  # ---------------------------------------------------------------------------
  def __init__(self, master):
    """Initialise all GUI elements"""
    UI.TKI.GUIwinView.__init__(self, master, "EGSE", "EGSE Interface")
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
    # EGSE interface status
    self.egseProtocolField = UI.TKI.ValueField(self, row=1, label="EGSE protocol:")
    self.egseProtocolField.set(EGSE.IF.s_clientConfiguration.egseProtocol)
    # SCOE interface host
    self.scoeHostField = UI.TKI.ValueField(self, row=2, label="SCOE host:")
    self.scoeHostField.set(EGSE.IF.s_clientConfiguration.scoeHost)
    # SCOE interface status
    self.scoeStatusField = UI.TKI.ValueField(self, row=3, label="SCOE interface status:")
    self.scoeStatusField.set("INIT")
    self.scoeStatusField.setBackground(COLOR_INITIALISED)
    # SCOE interface port
    self.scoePortField = UI.TKI.ValueField(self, row=4, label="SCOE interface port:")
    self.scoePortField.set(EGSE.IF.s_clientConfiguration.scoePort)
    # SCOE interface status 2
    self.scoeStatusField2 = UI.TKI.ValueField(self, row=5, label="SCOE interface status 2:")
    self.scoeStatusField2.set("INIT")
    self.scoeStatusField2.setBackground(COLOR_INITIALISED)
    # S interface port 2
    self.scoePortField2 = UI.TKI.ValueField(self, row=6, label="SCOE interface port 2:")
    self.scoePortField2.set(EGSE.IF.s_clientConfiguration.scoePort2)
    # log messages
    self.messageLogger = UI.TKI.MessageLogger(self, "EGSE")
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
    self.addCommandMenuItem(label="ConnectPort", command=self.connectPortCallback)
    self.addCommandMenuItem(label="DisconnectPort", command=self.disconnectPortCallback, enabled=False)
    self.addCommandMenuItem(label="ConnectPort2", command=self.connectPort2Callback)
    self.addCommandMenuItem(label="DisconnectPort2", command=self.disconnectPort2Callback, enabled=False)
  # ---------------------------------------------------------------------------
  def connectPortCallback(self):
    """Called when the ConnectPort menu entry is selected"""
    self.notifyModelTask(["CONNECTPORT"])
  # ---------------------------------------------------------------------------
  def disconnectPortCallback(self):
    """Called when the DisconnectPort menu entry is selected"""
    self.notifyModelTask(["DISCONNECTPORT"])
  # ---------------------------------------------------------------------------
  def connectPort2Callback(self):
    """Called when the ConnectPort2 menu entry is selected"""
    self.notifyModelTask(["CONNECTPORT2"])
  # ---------------------------------------------------------------------------
  def disconnectPort2Callback(self):
    """Called when the DisconnectPort2 menu entry is selected"""
    self.notifyModelTask(["DISCONNECTPORT2"])
  # ---------------------------------------------------------------------------
  def notifyStatus(self, status):
    """Generic callback when something changes in the model"""
    if status == "SCOE_CONNECTED":
      self.scoeConnectedNotify()
    elif status == "SCOE_DISCONNECTED":
      self.scoeDisconnectedNotify()
    elif status == "SCOE2_CONNECTED":
      self.scoeConnected2Notify()
    elif status == "SCOE2_DISCONNECTED":
      self.scoeDisconnected2Notify()
  # ---------------------------------------------------------------------------
  def scoeConnectedNotify(self):
    """Called when the SCOE port connect function is successfully processed"""
    self.scoeStatusField.set("CONNECTED")
    self.scoeStatusField.setBackground(COLOR_CONNECTED)
    self.menuButtons.setState("CONN", Tkinter.DISABLED)
    self.menuButtons.setState("DCONN", Tkinter.NORMAL)
    self.disableCommandMenuItem("ConnectPort")
    self.enableCommandMenuItem("DisconnectPort")
  # ---------------------------------------------------------------------------
  def scoeDisconnectedNotify(self):
    """Called when the SCOE port disconnect function is successfully processed"""
    self.scoeStatusField.set("DISCONNECTED")
    self.scoeStatusField.setBackground(COLOR_INITIALISED)
    self.menuButtons.setState("CONN", Tkinter.NORMAL)
    self.menuButtons.setState("DCONN", Tkinter.DISABLED)
    self.enableCommandMenuItem("ConnectPort")
    self.disableCommandMenuItem("DisconnectPort")
  # ---------------------------------------------------------------------------
  def scoeConnected2Notify(self):
    """Called when the SCOE port 2 connect function is successfully processed"""
    self.scoeStatusField2.set("CONNECTED")
    self.scoeStatusField2.setBackground(COLOR_CONNECTED)
    self.menuButtons.setState("CONN2", Tkinter.DISABLED)
    self.menuButtons.setState("DCONN2", Tkinter.NORMAL)
    self.disableCommandMenuItem("ConnectPort2")
    self.enableCommandMenuItem("DisconnectPort2")
  # ---------------------------------------------------------------------------
  def scoeDisconnected2Notify(self):
    """Called when the SCOE port 2 disconnect function is successfully processed"""
    self.scoeStatusField2.set("DISCONNECTED")
    self.scoeStatusField2.setBackground(COLOR_INITIALISED)
    self.menuButtons.setState("CONN2", Tkinter.NORMAL)
    self.menuButtons.setState("DCONN2", Tkinter.DISABLED)
    self.enableCommandMenuItem("ConnectPort2")
    self.disableCommandMenuItem("DisconnectPort2")
