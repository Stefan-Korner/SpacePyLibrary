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
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import MC.IF
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
  """Implementation of the M&C Control layer"""
  # ---------------------------------------------------------------------------
  def __init__(self, master):
    """Initialise all GUI elements"""
    UI.TKI.GUIwinView.__init__(self, master, "TC", "M&C TC")
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
    # log messages (default logger)
    self.messageLogger = UI.TKI.MessageLogger(self, "TC")
    self.appGrid(self.messageLogger, row=3, columnspan=2)
    # message line
    self.messageline = tkinter.Message(self, relief=tkinter.GROOVE)
    self.appGrid(self.messageline,
                 row=4,
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
    self.addCommandMenuItem(label="SetPacketData", command=self.setPacketDataCallback, enabled=False)
    self.addCommandMenuItem(label="SendPacket", command=self.sendPacketCallback, enabled=False)
  # ---------------------------------------------------------------------------
  def setPacketDataCallback(self):
    """Called when the SetPacketData menu entry is selected"""
    LOG_WARNING("TCgui.setPacketDataCallback not implemented", "TC")
  # ---------------------------------------------------------------------------
  def sendPacketCallback(self):
    """Called when the SendPacket menu entry is selected"""
    LOG_WARNING("TCgui.sendPacketCallback not implemented", "TC")
  # ---------------------------------------------------------------------------
  def notifyStatus(self, status):
    """Generic callback when something changes in the model"""
    if status == "TC_CONNECTED":
      self.tcConnectedNotify()
    elif status == "PACKETDATA_SET":
      self.packetDataSetNotify()
  # ---------------------------------------------------------------------------
  def tcConnectedNotify(self):
    """Called when the TC connect function is succsssfully processed"""
    self.enableCommandMenuItem("SetPacketData")
    self.menuButtons.setState("PKT", tkinter.NORMAL)
    self.updateTCstatusField()
  # ---------------------------------------------------------------------------
  def packetDataSetNotify(self):
    """Called when the setPacketData function is succsssfully processed"""
    self.enableCommandMenuItem("SendPacket")
    self.menuButtons.setState("SND", tkinter.NORMAL)
    self.updateTMstatusField()
    self.packetField.set(MC.IF.s_configuration.tcPacketData.pktName)
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
