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
# EGSE server GUI                                                             *
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
COLOR_ON_OK = "#00FF00"
COLOR_ON_NOK = "#FF0000"

###########
# classes #
###########
# =============================================================================
class GUIview(UI.TKI.GUItabView):
  """Implementation of the SCOE EGSE GUI layer"""
  # ---------------------------------------------------------------------------
  def __init__(self, master):
    """Initialise all GUI elements"""
    UI.TKI.GUItabView.__init__(self, master, "EGSE", "EGSE interface to CCS")
    # checkbuttons
    self.checkButtons = UI.TKI.Checkbuttons(self,
      [["ACK1", self.ack1Callback, True, COLOR_ON_OK],
       ["NAK1", self.nak1Callback, False, COLOR_ON_NOK],
       ["ACK2", self.ack2Callback, True, COLOR_ON_OK],
       ["NAK2", self.nak2Callback, False, COLOR_ON_NOK]])
    self.appGrid(self.checkButtons,
                 row=0,
                 columnspan=2,
                 rowweight=0,
                 columnweight=0,
                 sticky=tkinter.W)
    # EGSE protocol
    self.egseProtocolField = UI.TKI.ValueField(self, row=1, label="EGSE protocol:")
    self.egseProtocolField.set(EGSE.IF.s_serverConfiguration.egseProtocol)
    # CCS interface status
    self.ccsStatusField = UI.TKI.ValueField(self, row=2, label="CCS interface status:")
    self.ccsStatusField.set("INIT")
    self.ccsStatusField.setBackground(COLOR_INITIALISED)
    # CCS interface port
    self.ccsPortField = UI.TKI.ValueField(self, row=3, label="CCS interface port:")
    self.ccsPortField.set(EGSE.IF.s_serverConfiguration.ccsPort)
    # CCS interface status 2
    self.ccsStatusField2 = UI.TKI.ValueField(self, row=4, label="CCS interface status 2:")
    self.ccsStatusField2.set("INIT")
    self.ccsStatusField2.setBackground(COLOR_INITIALISED)
    # CCS interface port 2
    self.ccsPortField2 = UI.TKI.ValueField(self, row=5, label="CCS interface port 2:")
    self.ccsPortField2.set(EGSE.IF.s_serverConfiguration.ccsPort2)
    # log messages (default logger)
    self.messageLogger = UI.TKI.MessageLogger(self)
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
    implementation of UI.TKI.GUItabView.fillCommandMenuItems
    """
    self.addCommandMenuItem(label="EGSEenableAck1", command=self.egseEnableAck1Callback, enabled=False)
    self.addCommandMenuItem(label="EGSEenableNak1", command=self.egseEnableNak1Callback)
    self.addCommandMenuItem(label="EGSEdisableAck1", command=self.egseDisableAck1Callback)
    self.addCommandMenuItem(label="EGSEenableAck2", command=self.egseEnableAck2Callback, enabled=False)
    self.addCommandMenuItem(label="EGSEenableNak2", command=self.egseEnableNak2Callback)
    self.addCommandMenuItem(label="EGSEdisableAck2", command=self.egseDisableAck2Callback)
  # ---------------------------------------------------------------------------
  def egseEnableAck1Callback(self):
    """Called when the EGSEenableAck1 menu entry is selected"""
    self.notifyModelTask(["EGSEENABLEACK1"])
  def egseEnableNak1Callback(self):
    """Called when the EGSEenableNak1 menu entry is selected"""
    self.notifyModelTask(["EGSEENABLENAK1"])
  def egseDisableAck1Callback(self):
    """Called when the EGSEdisableAck1 menu entry is selected"""
    self.notifyModelTask(["EGSEDISABLEACK1"])
  def ack1Callback(self):
    """Called when the ACK1 checkbutton is pressed"""
    if self.checkButtons.getButtonPressed("ACK1"):
      self.notifyModelTask(["EGSEENABLEACK1"])
    else:
      self.notifyModelTask(["EGSEDISABLEACK1"])
  def nak1Callback(self):
    """Called when the NAK1 checkbutton is pressed"""
    if self.checkButtons.getButtonPressed("NAK1"):
      self.notifyModelTask(["EGSEENABLENAK1"])
    else:
      self.notifyModelTask(["EGSEDISABLEACK1"])
  # ---------------------------------------------------------------------------
  def egseEnableAck2Callback(self):
    """Called when the EGSEenableAck2 menu entry is selected"""
    self.notifyModelTask(["EGSEENABLEACK2"])
  def egseEnableNak2Callback(self):
    """Called when the EGSEenableNak2 menu entry is selected"""
    self.notifyModelTask(["EGSEENABLENAK2"])
  def egseDisableAck2Callback(self):
    """Called when the EGSEdisableAck2 menu entry is selected"""
    self.notifyModelTask(["EGSEDISABLEACK2"])
  def ack2Callback(self):
    """Called when the ACK2 checkbutton is pressed"""
    if self.checkButtons.getButtonPressed("ACK2"):
      self.notifyModelTask(["EGSEENABLEACK2"])
    else:
      self.notifyModelTask(["EGSEDISABLEACK2"])
  def nak2Callback(self):
    """Called when the NAK2 checkbutton is pressed"""
    if self.checkButtons.getButtonPressed("NAK2"):
      self.notifyModelTask(["EGSEENABLENAK2"])
    else:
      self.notifyModelTask(["EGSEDISABLEACK2"])
  # ---------------------------------------------------------------------------
  def notifyStatus(self, status):
    """Generic callback when something changes in the model"""
    if status == "CCS_CONNECTED":
      self.ccsConnectedNotify()
    elif status == "CCS_DISCONNECTED":
      self.ccsDisconnectedNotify()
    elif status == "CCS_CONNECTED2":
      self.ccsConnected2Notify()
    elif status == "CCS_DISCONNECTED2":
      self.ccsDisconnected2Notify()
    elif status == "EGSE_ENABLED_ACK1":
      self.egseEnabledAck1Notify()
    elif status == "EGSE_ENABLED_NAK1":
      self.egseEnabledNak1Notify()
    elif status == "EGSE_DISABLED_ACK1":
      self.egseDisabledAck1Notify()
    elif status == "EGSE_ENABLED_ACK2":
      self.egseEnabledAck2Notify()
    elif status == "EGSE_ENABLED_NAK2":
      self.egseEnabledNak2Notify()
    elif status == "EGSE_DISABLED_ACK2":
      self.egseDisabledAck2Notify()
  # ---------------------------------------------------------------------------
  def ccsConnectedNotify(self):
    """Called when the CCS connect function is successfully processed"""
    self.ccsStatusField.set("CONNECTED")
    self.ccsStatusField.setBackground(COLOR_CONNECTED)
  # ---------------------------------------------------------------------------
  def ccsDisconnectedNotify(self):
    """Called when the CCS disconnect function is successfully processed"""
    self.ccsStatusField.set("DISCONNECTED")
    self.ccsStatusField.setBackground(COLOR_INITIALISED)
  # ---------------------------------------------------------------------------
  def ccsConnected2Notify(self):
    """Called when the CCS 2nd connect function is successfully processed"""
    self.ccsStatusField2.set("CONNECTED")
    self.ccsStatusField2.setBackground(COLOR_CONNECTED)
  # ---------------------------------------------------------------------------
  def ccsDisconnected2Notify(self):
    """Called when the CCS 2nd disconnect function is successfully processed"""
    self.ccsStatusField2.set("DISCONNECTED")
    self.ccsStatusField2.setBackground(COLOR_INITIALISED)
  # ---------------------------------------------------------------------------
  def egseEnabledAck1Notify(self):
    """Called when the egseEnabledAck1 function is succsssfully processed"""
    self.disableCommandMenuItem("EGSEenableAck1")
    self.enableCommandMenuItem("EGSEenableNak1")
    self.enableCommandMenuItem("EGSEdisableAck1")
    self.checkButtons.setButtonPressed("ACK1", True)
    self.checkButtons.setButtonPressed("NAK1", False)
  def egseEnabledNak1Notify(self):
    """Called when the egseEnabledNak1 function is succsssfully processed"""
    self.enableCommandMenuItem("EGSEenableAck1")
    self.disableCommandMenuItem("EGSEenableNak1")
    self.enableCommandMenuItem("EGSEdisableAck1")
    self.checkButtons.setButtonPressed("ACK1", False)
    self.checkButtons.setButtonPressed("NAK1", True)
  def egseDisabledAck1Notify(self):
    """Called when the egseDisabledAck1 function is succsssfully processed"""
    self.enableCommandMenuItem("EGSEenableAck1")
    self.enableCommandMenuItem("EGSEenableNak1")
    self.disableCommandMenuItem("EGSEdisableAck1")
    self.checkButtons.setButtonPressed("ACK1", False)
    self.checkButtons.setButtonPressed("NAK1", False)
  # ---------------------------------------------------------------------------
  def egseEnabledAck2Notify(self):
    """Called when the egseEnabledAck2 function is succsssfully processed"""
    self.disableCommandMenuItem("EGSEenableAck2")
    self.enableCommandMenuItem("EGSEenableNak1")
    self.enableCommandMenuItem("EGSEdisableAck2")
    self.checkButtons.setButtonPressed("ACK2", True)
    self.checkButtons.setButtonPressed("NAK2", False)
  def egseEnabledNak2Notify(self):
    """Called when the egseEnabledNak2 function is succsssfully processed"""
    self.enableCommandMenuItem("EGSEenableAck2")
    self.disableCommandMenuItem("EGSEenableNak2")
    self.enableCommandMenuItem("EGSEdisableAck2")
    self.checkButtons.setButtonPressed("ACK2", False)
    self.checkButtons.setButtonPressed("NAK2", True)
  def egseDisabledAck2Notify(self):
    """Called when the egseDisabledAck2 function is succsssfully processed"""
    self.enableCommandMenuItem("EGSEenableAck2")
    self.enableCommandMenuItem("EGSEenableNak2")
    self.disableCommandMenuItem("EGSEdisableAck2")
    self.checkButtons.setButtonPressed("ACK2", False)
    self.checkButtons.setButtonPressed("NAK2", False)
