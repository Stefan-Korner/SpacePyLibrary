#******************************************************************************
# (C) 2014, Stefan Korner, Austria                                            *
#                                                                             *
# The Space Python Library is free software; you can redistribute it and/or   *
# modify it under the terms of the GNU Lesser General Public License as       *
# published by the Free Software Foundation; either version 2.1 of the        *
# License, or (at your option) any later version.                             *
#                                                                             *
# The Space C++ Library is distributed in the hope that it will be useful,    *
# but WITHOUT ANY WARRANTY; without even the implied warranty of              *
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser     *
# General Public License for more details.                                    *
#******************************************************************************
# Ground Segment Simulation GUI                                               *
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
COLOR_ON_OK = "#00FF00"
COLOR_ON_NOK = "#FF0000"

###########
# classes #
###########
# =============================================================================
class GUIview(UI.TKI.GUIwinView):
  """Implementation of the SIM Ground GUI layer"""
  # ---------------------------------------------------------------------------
  def __init__(self, master):
    """Initialise all GUI elements"""
    UI.TKI.GUIwinView.__init__(self, master, "GRND", "Ground Segment")
    # menu buttons
    self.menuButtons = UI.TKI.MenuButtons(self,
      [["AD-I", self.initialiseADcallback, COLOR_BUTTON_FG, COLOR_BUTTON_BG]])
    self.appGrid(self.menuButtons,
                 row=0,
                 columnspan=2,
                 rowweight=0,
                 sticky=Tkinter.EW)
    # checkbuttons
    self.checkButtons = UI.TKI.Checkbuttons(self,
      [["ACK1", self.ack1Callback, True, COLOR_ON_OK],
       ["NAK1", self.nak1Callback, False, COLOR_ON_NOK],
       ["ACK2", self.ack2Callback, True, COLOR_ON_OK],
       ["NAK2", self.nak2Callback, False, COLOR_ON_NOK]])
    self.appGrid(self.checkButtons,
                 row=1,
                 columnspan=2,
                 rowweight=0,
                 columnweight=0,
                 sticky=Tkinter.W)
    # tm status
    self.tmStatusField = UI.TKI.ValueField(self, row=2, label="NCTRS TM status:")
    self.tmStatusField.set("INIT")
    self.tmStatusField.setBackground(COLOR_INITIALISED)
    # tm port
    self.tmPortField = UI.TKI.ValueField(self, row=3, label="NCTRS TM port:")
    self.tmPortField.set(GRND.IF.s_configuration.nctrsTMport)
    # tc status
    self.tcStatusField = UI.TKI.ValueField(self, row=4, label="NCTRS TC status:")
    self.tcStatusField.set("INIT")
    self.tcStatusField.setBackground(COLOR_INITIALISED)
    # tc port
    self.tcPortField = UI.TKI.ValueField(self, row=5, label="NCTRS TC port:")
    self.tcPortField.set(GRND.IF.s_configuration.nctrsTCport)
    # admin status
    self.adminStatusField = UI.TKI.ValueField(self, row=6, label="NCTRS admin message status:")
    self.adminStatusField.set("INIT")
    self.adminStatusField.setBackground(COLOR_INITIALISED)
    # admin port
    self.adminPortField = UI.TKI.ValueField(self, row=7, label="NCTRS admin message port:")
    self.adminPortField.set(GRND.IF.s_configuration.nctrsAdminPort)
    # log messages (default logger)
    self.messageLogger = UI.TKI.MessageLogger(self)
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
    implementation of UI.TKI.GUIwinView.fillCommandMenuItems
    """
    self.addCommandMenuItem(label="InitialiseAD", command=self.initialiseADcallback)
    self.addCommandMenuItem(label="GRNDenableAck1", command=self.grndEnableAck1Callback, enabled=False)
    self.addCommandMenuItem(label="GRNDenableNak1", command=self.grndEnableNak1Callback)
    self.addCommandMenuItem(label="GRNDdisableAck1", command=self.grndDisableAck1Callback)
    self.addCommandMenuItem(label="GRNDenableAck2", command=self.grndEnableAck2Callback, enabled=False)
    self.addCommandMenuItem(label="GRNDenableNak2", command=self.grndEnableNak2Callback)
    self.addCommandMenuItem(label="GRNDdisableAck2", command=self.grndDisableAck2Callback)
  # ---------------------------------------------------------------------------
  def initialiseADcallback(self):
    """Called when the InitialiseAD menu entry is selected"""
    self.notifyModelTask(["INITIALISEAD"])
  # ---------------------------------------------------------------------------
  def grndEnableAck1Callback(self):
    """Called when the GRNDenableAck1 menu entry is selected"""
    self.notifyModelTask(["GRNDENABLEACK1"])
  def grndEnableNak1Callback(self):
    """Called when the GRNDenableNak1 menu entry is selected"""
    self.notifyModelTask(["GRNDENABLENAK1"])
  def grndDisableAck1Callback(self):
    """Called when the GRNDdisableAck1 menu entry is selected"""
    self.notifyModelTask(["GRNDDISABLEACK1"])
  def ack1Callback(self):
    """Called when the ACK1 checkbutton is pressed"""
    if self.checkButtons.getButtonPressed("ACK1"):
      self.notifyModelTask(["GRNDENABLEACK1"])
    else:
      self.notifyModelTask(["GRNDDISABLEACK1"])
  def nak1Callback(self):
    """Called when the NAK1 checkbutton is pressed"""
    if self.checkButtons.getButtonPressed("NAK1"):
      self.notifyModelTask(["GRNDENABLENAK1"])
    else:
      self.notifyModelTask(["GRNDDISABLEACK1"])
  # ---------------------------------------------------------------------------
  def grndEnableAck2Callback(self):
    """Called when the GRNDenableAck2 menu entry is selected"""
    self.notifyModelTask(["GRNDENABLEACK2"])
  def grndEnableNak2Callback(self):
    """Called when the GRNDenableNak2 menu entry is selected"""
    self.notifyModelTask(["GRNDENABLENAK2"])
  def grndDisableAck2Callback(self):
    """Called when the GRNDdisableAck2 menu entry is selected"""
    self.notifyModelTask(["GRNDDISABLEACK2"])
  def ack2Callback(self):
    """Called when the ACK2 checkbutton is pressed"""
    if self.checkButtons.getButtonPressed("ACK2"):
      self.notifyModelTask(["GRNDENABLEACK2"])
    else:
      self.notifyModelTask(["GRNDDISABLEACK2"])
  def nak2Callback(self):
    """Called when the NAK2 checkbutton is pressed"""
    if self.checkButtons.getButtonPressed("NAK2"):
      self.notifyModelTask(["GRNDENABLENAK2"])
    else:
      self.notifyModelTask(["GRNDDISABLEACK2"])
  # ---------------------------------------------------------------------------
  def notifyStatus(self, status):
    """Generic callback when something changes in the model"""
    if status == "TM_CONNECTED":
      self.tmConnectedNotify()
    elif status == "TC_CONNECTED":
      self.tcConnectedNotify()
    elif status == "ADMIN_CONNECTED":
      self.adminConnectedNotify()
    elif status == "GRND_ENABLED_ACK1":
      self.grndEnabledAck1Notify()
    elif status == "GRND_ENABLED_NAK1":
      self.grndEnabledNak1Notify()
    elif status == "GRND_DISABLED_ACK1":
      self.grndDisabledAck1Notify()
    elif status == "GRND_ENABLED_ACK2":
      self.grndEnabledAck2Notify()
    elif status == "GRND_ENABLED_NAK2":
      self.grndEnabledNak2Notify()
    elif status == "GRND_DISABLED_ACK2":
      self.grndDisabledAck2Notify()
  # ---------------------------------------------------------------------------
  def tmConnectedNotify(self):
    """Called when the TM connect function is successfully processed"""
    self.tmStatusField.set("CONNECTED")
    self.tmStatusField.setBackground(COLOR_CONNECTED)
  # ---------------------------------------------------------------------------
  def tcConnectedNotify(self):
    """Called when the TC connect function is successfully processed"""
    self.tcStatusField.set("CONNECTED")
    self.tcStatusField.setBackground(COLOR_CONNECTED)
  # ---------------------------------------------------------------------------
  def adminConnectedNotify(self):
    """Called when the admin connect function is successfully processed"""
    self.adminStatusField.set("CONNECTED")
    self.adminStatusField.setBackground(COLOR_CONNECTED)
  # ---------------------------------------------------------------------------
  def grndEnabledAck1Notify(self):
    """Called when the grndEnabledAck1 function is succsssfully processed"""
    self.disableCommandMenuItem("GRNDenableAck1")
    self.enableCommandMenuItem("GRNDenableNak1")
    self.enableCommandMenuItem("GRNDdisableAck1")
    self.checkButtons.setButtonPressed("ACK1", True)
    self.checkButtons.setButtonPressed("NAK1", False)
  def grndEnabledNak1Notify(self):
    """Called when the grndEnabledNak1 function is succsssfully processed"""
    self.enableCommandMenuItem("GRNDenableAck1")
    self.disableCommandMenuItem("GRNDenableNak1")
    self.enableCommandMenuItem("GRNDdisableAck1")
    self.checkButtons.setButtonPressed("ACK1", False)
    self.checkButtons.setButtonPressed("NAK1", True)
  def grndDisabledAck1Notify(self):
    """Called when the grndDisabledAck1 function is succsssfully processed"""
    self.enableCommandMenuItem("GRNDenableAck1")
    self.enableCommandMenuItem("GRNDenableNak1")
    self.disableCommandMenuItem("GRNDdisableAck1")
    self.checkButtons.setButtonPressed("ACK1", False)
    self.checkButtons.setButtonPressed("NAK1", False)
  # ---------------------------------------------------------------------------
  def grndEnabledAck2Notify(self):
    """Called when the grndEnabledAck2 function is succsssfully processed"""
    self.disableCommandMenuItem("GRNDenableAck2")
    self.enableCommandMenuItem("GRNDenableNak1")
    self.enableCommandMenuItem("GRNDdisableAck2")
    self.checkButtons.setButtonPressed("ACK2", True)
    self.checkButtons.setButtonPressed("NAK2", False)
  def grndEnabledNak2Notify(self):
    """Called when the grndEnabledNak2 function is succsssfully processed"""
    self.enableCommandMenuItem("GRNDenableAck2")
    self.disableCommandMenuItem("GRNDenableNak2")
    self.enableCommandMenuItem("GRNDdisableAck2")
    self.checkButtons.setButtonPressed("ACK2", False)
    self.checkButtons.setButtonPressed("NAK2", True)
  def grndDisabledAck2Notify(self):
    """Called when the grndDisabledAck2 function is succsssfully processed"""
    self.enableCommandMenuItem("GRNDenableAck2")
    self.enableCommandMenuItem("GRNDenableNak2")
    self.disableCommandMenuItem("GRNDdisableAck2")
    self.checkButtons.setButtonPressed("ACK2", False)
    self.checkButtons.setButtonPressed("NAK2", False)
