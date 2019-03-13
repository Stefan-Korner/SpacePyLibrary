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
# NCTRS client GUI                                                            *
#******************************************************************************
import Tkinter
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import GRND.IF
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
  """Implementation of the Control System EGSE GUI layer"""
  # ---------------------------------------------------------------------------
  def __init__(self, master):
    """Initialise all GUI elements"""
    UI.TKI.GUItabView.__init__(self, master, "NCTRS", "NCTRS Interface")
    # menu buttons
    self.menuButtons = UI.TKI.MenuButtons(self,
      [["CONN1", self.connectPort1Callback, COLOR_BUTTON_FG, COLOR_BUTTON_BG],
       ["DCONN1", self.disconnectPort1Callback, COLOR_BUTTON_FG, COLOR_BUTTON_BG, Tkinter.DISABLED],
       ["CONN2", self.connectPort2Callback, COLOR_BUTTON_FG, COLOR_BUTTON_BG],
       ["DCONN2", self.disconnectPort2Callback, COLOR_BUTTON_FG, COLOR_BUTTON_BG, Tkinter.DISABLED],
       ["CONN3", self.connectPort3Callback, COLOR_BUTTON_FG, COLOR_BUTTON_BG],
       ["DCONN3", self.disconnectPort3Callback, COLOR_BUTTON_FG, COLOR_BUTTON_BG, Tkinter.DISABLED]])
    self.appGrid(self.menuButtons,
                 row=0,
                 columnspan=2,
                 rowweight=0,
                 sticky=Tkinter.EW)
    # NCTRS interface host
    self.nctrsHostField = UI.TKI.ValueField(self, row=1, label="NCTRS host:")
    self.nctrsHostField.set(GRND.IF.s_clientConfiguration.nctrsHost)
    # NCTRS interface status
    self.nctrsStatusField1 = UI.TKI.ValueField(self, row=2, label="NCTRS interface status 1:")
    self.nctrsStatusField1.set("INIT")
    self.nctrsStatusField1.setBackground(COLOR_INITIALISED)
    # NCTRS interface port
    self.nctrsPortField1 = UI.TKI.ValueField(self, row=3, label="NCTRS interface port 1:")
    self.nctrsPortField1.set(GRND.IF.s_clientConfiguration.nctrsTMport)
    # NCTRS interface status 2
    self.nctrsStatusField2 = UI.TKI.ValueField(self, row=4, label="NCTRS interface status 2:")
    self.nctrsStatusField2.set("INIT")
    self.nctrsStatusField2.setBackground(COLOR_INITIALISED)
    # NCTRS interface port 2
    self.nctrsPortField2 = UI.TKI.ValueField(self, row=5, label="NCTRS interface port 2:")
    self.nctrsPortField2.set(GRND.IF.s_clientConfiguration.nctrsTCport)
    # NCTRS interface status 3
    self.nctrsStatusField3 = UI.TKI.ValueField(self, row=6, label="NCTRS interface status 3:")
    self.nctrsStatusField3.set("INIT")
    self.nctrsStatusField3.setBackground(COLOR_INITIALISED)
    # NCTRS interface port 3
    self.nctrsPortField3 = UI.TKI.ValueField(self, row=7, label="NCTRS interface port 3:")
    self.nctrsPortField3.set(GRND.IF.s_clientConfiguration.nctrsAdminPort)
    # log messages
    self.messageLogger = UI.TKI.MessageLogger(self, "NCTRS")
    self.appGrid(self.messageLogger, row=8, columnspan=2)
    # message line
    self.messageline = Tkinter.Message(self, relief=Tkinter.GROOVE)
    self.appGrid(self.messageline,
                 row=9,
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
    self.addCommandMenuItem(label="ConnectPort1", command=self.connectPort1Callback)
    self.addCommandMenuItem(label="DisconnectPort1", command=self.disconnectPort1Callback, enabled=False)
    self.addCommandMenuItem(label="ConnectPort2", command=self.connectPort2Callback)
    self.addCommandMenuItem(label="DisconnectPort2", command=self.disconnectPort2Callback, enabled=False)
    self.addCommandMenuItem(label="ConnectPort3", command=self.connectPort3Callback)
    self.addCommandMenuItem(label="DisconnectPort3", command=self.disconnectPort3Callback, enabled=False)
  # ---------------------------------------------------------------------------
  def connectPort1Callback(self):
    """Called when the ConnectPort1 menu entry is selected"""
    self.notifyModelTask(["CONNECTNCTRS1"])
  # ---------------------------------------------------------------------------
  def disconnectPort1Callback(self):
    """Called when the DisconnectPort1 menu entry is selected"""
    self.notifyModelTask(["DISCONNECTNCTRS1"])
  # ---------------------------------------------------------------------------
  def connectPort2Callback(self):
    """Called when the ConnectPort2 menu entry is selected"""
    self.notifyModelTask(["CONNECTNCTRS2"])
  # ---------------------------------------------------------------------------
  def disconnectPort2Callback(self):
    """Called when the DisconnectPort2 menu entry is selected"""
    self.notifyModelTask(["DISCONNECTNCTRS2"])
  # ---------------------------------------------------------------------------
  def connectPort3Callback(self):
    """Called when the ConnectPort3 menu entry is selected"""
    self.notifyModelTask(["CONNECTNCTRS3"])
  # ---------------------------------------------------------------------------
  def disconnectPort3Callback(self):
    """Called when the DisconnectPort3 menu entry is selected"""
    self.notifyModelTask(["DISCONNECTNCTRS3"])
  # ---------------------------------------------------------------------------
  def notifyStatus(self, status):
    """Generic callback when something changes in the model"""
    if status == "NCTRS1_CONNECTED":
      self.nctrsConnected1Notify()
    elif status == "NCTRS1_DISCONNECTED":
      self.nctrsDisconnected1Notify()
    elif status == "NCTRS2_CONNECTED":
      self.nctrsConnected2Notify()
    elif status == "NCTRS2_DISCONNECTED":
      self.nctrsDisconnected2Notify()
    elif status == "NCTRS3_CONNECTED":
      self.nctrsConnected3Notify()
    elif status == "NCTRS3_DISCONNECTED":
      self.nctrsDisconnected3Notify()
  # ---------------------------------------------------------------------------
  def nctrsConnected1Notify(self):
    """Called when the NCTRS port 1 connect function is successfully processed"""
    self.nctrsStatusField1.set("CONNECTED")
    self.nctrsStatusField1.setBackground(COLOR_CONNECTED)
    self.menuButtons.setState("CONN1", Tkinter.DISABLED)
    self.menuButtons.setState("DCONN1", Tkinter.NORMAL)
    self.disableCommandMenuItem("ConnectPort1")
    self.enableCommandMenuItem("DisconnectPort1")
  # ---------------------------------------------------------------------------
  def nctrsDisconnected1Notify(self):
    """Called when the NCTRS port 1 disconnect function is successfully processed"""
    self.nctrsStatusField1.set("DISCONNECTED")
    self.nctrsStatusField1.setBackground(COLOR_INITIALISED)
    self.menuButtons.setState("CONN1", Tkinter.NORMAL)
    self.menuButtons.setState("DCONN1", Tkinter.DISABLED)
    self.enableCommandMenuItem("ConnectPort1")
    self.disableCommandMenuItem("DisconnectPort1")
  # ---------------------------------------------------------------------------
  def nctrsConnected2Notify(self):
    """Called when the NCTRS port 2 connect function is successfully processed"""
    self.nctrsStatusField2.set("CONNECTED")
    self.nctrsStatusField2.setBackground(COLOR_CONNECTED)
    self.menuButtons.setState("CONN2", Tkinter.DISABLED)
    self.menuButtons.setState("DCONN2", Tkinter.NORMAL)
    self.disableCommandMenuItem("ConnectPort2")
    self.enableCommandMenuItem("DisconnectPort2")
  # ---------------------------------------------------------------------------
  def nctrsDisconnected2Notify(self):
    """Called when the NCTRS port 2 disconnect function is successfully processed"""
    self.nctrsStatusField2.set("DISCONNECTED")
    self.nctrsStatusField2.setBackground(COLOR_INITIALISED)
    self.menuButtons.setState("CONN2", Tkinter.NORMAL)
    self.menuButtons.setState("DCONN2", Tkinter.DISABLED)
    self.enableCommandMenuItem("ConnectPort2")
    self.disableCommandMenuItem("DisconnectPort2")
  # ---------------------------------------------------------------------------
  def nctrsConnected3Notify(self):
    """Called when the NCTRS port 3 connect function is successfully processed"""
    self.nctrsStatusField3.set("CONNECTED")
    self.nctrsStatusField3.setBackground(COLOR_CONNECTED)
    self.menuButtons.setState("CONN3", Tkinter.DISABLED)
    self.menuButtons.setState("DCONN3", Tkinter.NORMAL)
    self.disableCommandMenuItem("ConnectPort3")
    self.enableCommandMenuItem("DisconnectPort3")
  # ---------------------------------------------------------------------------
  def nctrsDisconnected3Notify(self):
    """Called when the NCTRS port 3 disconnect function is successfully processed"""
    self.nctrsStatusField3.set("DISCONNECTED")
    self.nctrsStatusField3.setBackground(COLOR_INITIALISED)
    self.menuButtons.setState("CONN3", Tkinter.NORMAL)
    self.menuButtons.setState("DCONN3", Tkinter.DISABLED)
    self.enableCommandMenuItem("ConnectPort3")
    self.disableCommandMenuItem("DisconnectPort3")
