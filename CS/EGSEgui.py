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
      [["CONN1", self.connectPort1Callback, COLOR_BUTTON_FG, COLOR_BUTTON_BG],
       ["CONN2", self.connectPort2Callback, COLOR_BUTTON_FG, COLOR_BUTTON_BG]])
    self.appGrid(self.menuButtons,
                 row=0,
                 columnspan=2,
                 rowweight=0,
                 sticky=tkinter.EW)
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
    self.messageline = tkinter.Message(self, relief=tkinter.GROOVE)
    self.appGrid(self.messageline,
                 row=8,
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
    self.addCommandMenuItem(label="ConnectPort1", command=self.connectPort1Callback)
    self.addCommandMenuItem(label="ConnectPort2", command=self.connectPort2Callback)
  # ---------------------------------------------------------------------------
  def connectPort1Callback(self):
    """Called when the ConnectPort1 menu entry is selected"""
    LOG_WARNING("EGSEgui.GUIview.connectPort1Callback not implemented", "EGSE")
  # ---------------------------------------------------------------------------
  def connectPort2Callback(self):
    """Called when the ConnectPort2 menu entry is selected"""
    LOG_WARNING("EGSEgui.GUIview.connectPort2Callback not implemented", "EGSE")
  # ---------------------------------------------------------------------------
  def notifyStatus(self, status):
    """Generic callback when something changes in the model"""
    LOG_WARNING("EGSEgui.GUIview.notifyStatus not implemented", "EGSE")
