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
# EDEN client GUI                                                             *
#******************************************************************************
import tkinter
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
  """Implementation of the Control System EDEN GUI layer"""
  # ---------------------------------------------------------------------------
  def __init__(self, master):
    """Initialise all GUI elements"""
    UI.TKI.GUIwinView.__init__(self, master, "EDEN", "EDEN Interface")
    # menu buttons
    self.menuButtons = UI.TKI.MenuButtons(self,
      [["CONN", self.connectPortCallback, COLOR_BUTTON_FG, COLOR_BUTTON_BG],
       ["DCONN", self.disconnectPortCallback, COLOR_BUTTON_FG, COLOR_BUTTON_BG, tkinter.DISABLED],
       ["CONN2", self.connectPort2Callback, COLOR_BUTTON_FG, COLOR_BUTTON_BG],
       ["DCONN2", self.disconnectPort2Callback, COLOR_BUTTON_FG, COLOR_BUTTON_BG, tkinter.DISABLED]])
    self.appGrid(self.menuButtons,
                 row=0,
                 columnspan=2,
                 rowweight=0,
                 sticky=tkinter.EW)
    # EDEN interface host
    self.edenHostField = UI.TKI.ValueField(self, row=1, label="EDEN host:")
    self.edenHostField.set(EGSE.IF.s_edenClientConfiguration.edenHost)
    # EDEN interface status
    self.edenStatusField = UI.TKI.ValueField(self, row=2, label="EDEN interface status:")
    self.edenStatusField.set("INIT")
    self.edenStatusField.setBackground(COLOR_INITIALISED)
    # EDEN interface port
    self.edenPortField = UI.TKI.ValueField(self, row=3, label="EDEN interface port:")
    self.edenPortField.set(EGSE.IF.s_edenClientConfiguration.edenPort)
    # EDEN interface status 2
    self.edenStatusField2 = UI.TKI.ValueField(self, row=4, label="EDEN interface status 2:")
    self.edenStatusField2.set("INIT")
    self.edenStatusField2.setBackground(COLOR_INITIALISED)
    # EDEN interface port 2
    self.edenPortField2 = UI.TKI.ValueField(self, row=5, label="EDEN interface port 2:")
    self.edenPortField2.set(EGSE.IF.s_edenClientConfiguration.edenPort2)
    # log messages
    self.messageLogger = UI.TKI.MessageLogger(self, "EDEN")
    self.appGrid(self.messageLogger, row=6, columnspan=2)
    # message line
    self.messageline = tkinter.Message(self, relief=tkinter.GROOVE)
    self.appGrid(self.messageline,
                 row=7,
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
    implementation of UI.TKI.GUIwinView.fillCommandMenuItems
    """
    self.addCommandMenuItem(label="ConnectPort", command=self.connectPortCallback)
    self.addCommandMenuItem(label="DisconnectPort", command=self.disconnectPortCallback, enabled=False)
    self.addCommandMenuItem(label="ConnectPort2", command=self.connectPort2Callback)
    self.addCommandMenuItem(label="DisconnectPort2", command=self.disconnectPort2Callback, enabled=False)
  # ---------------------------------------------------------------------------
  def connectPortCallback(self):
    """Called when the ConnectPort menu entry is selected"""
    self.notifyModelTask(["CONNECTEDEN"])
  # ---------------------------------------------------------------------------
  def disconnectPortCallback(self):
    """Called when the DisconnectPort menu entry is selected"""
    self.notifyModelTask(["DISCONNECTEDEN"])
  # ---------------------------------------------------------------------------
  def connectPort2Callback(self):
    """Called when the ConnectPort2 menu entry is selected"""
    self.notifyModelTask(["CONNECTEDEN2"])
  # ---------------------------------------------------------------------------
  def disconnectPort2Callback(self):
    """Called when the DisconnectPort2 menu entry is selected"""
    self.notifyModelTask(["DISCONNECTEDEN2"])
  # ---------------------------------------------------------------------------
  def notifyStatus(self, status):
    """Generic callback when something changes in the model"""
    if status == "EDEN_CONNECTED":
      self.edenConnectedNotify()
    elif status == "EDEN_DISCONNECTED":
      self.edenDisconnectedNotify()
    elif status == "EDEN2_CONNECTED":
      self.edenConnected2Notify()
    elif status == "EDEN2_DISCONNECTED":
      self.edenDisconnected2Notify()
  # ---------------------------------------------------------------------------
  def edenConnectedNotify(self):
    """Called when the EDEN port connect function is successfully processed"""
    self.edenStatusField.set("CONNECTED")
    self.edenStatusField.setBackground(COLOR_CONNECTED)
    self.menuButtons.setState("CONN", tkinter.DISABLED)
    self.menuButtons.setState("DCONN", tkinter.NORMAL)
    self.disableCommandMenuItem("ConnectPort")
    self.enableCommandMenuItem("DisconnectPort")
  # ---------------------------------------------------------------------------
  def edenDisconnectedNotify(self):
    """Called when the EDEN port disconnect function is successfully processed"""
    self.edenStatusField.set("DISCONNECTED")
    self.edenStatusField.setBackground(COLOR_INITIALISED)
    self.menuButtons.setState("CONN", tkinter.NORMAL)
    self.menuButtons.setState("DCONN", tkinter.DISABLED)
    self.enableCommandMenuItem("ConnectPort")
    self.disableCommandMenuItem("DisconnectPort")
  # ---------------------------------------------------------------------------
  def edenConnected2Notify(self):
    """Called when the EDEN port 2 connect function is successfully processed"""
    self.edenStatusField2.set("CONNECTED")
    self.edenStatusField2.setBackground(COLOR_CONNECTED)
    self.menuButtons.setState("CONN2", tkinter.DISABLED)
    self.menuButtons.setState("DCONN2", tkinter.NORMAL)
    self.disableCommandMenuItem("ConnectPort2")
    self.enableCommandMenuItem("DisconnectPort2")
  # ---------------------------------------------------------------------------
  def edenDisconnected2Notify(self):
    """Called when the EDEN port 2 disconnect function is successfully processed"""
    self.edenStatusField2.set("DISCONNECTED")
    self.edenStatusField2.setBackground(COLOR_INITIALISED)
    self.menuButtons.setState("CONN2", tkinter.NORMAL)
    self.menuButtons.setState("DCONN2", tkinter.DISABLED)
    self.enableCommandMenuItem("ConnectPort2")
    self.disableCommandMenuItem("DisconnectPort2")
