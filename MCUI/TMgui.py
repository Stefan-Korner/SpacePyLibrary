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
# Monitoring and Control (M&C) - Monitoring (TM) GUI                          *
#******************************************************************************
import Tkinter as tkinter
import tkFileDialog as filedialog
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import SCOS.ENV
import UI.TKI

#############
# constants #
#############
COLOR_BUTTON_FG = "#FFFFFF"
COLOR_BUTTON_BG = "#808080"

###########
# classes #
###########
# =============================================================================
class GUIview(UI.TKI.GUItabView):
  """Implementation of the M&C Monitoring GUI layer"""
  # ---------------------------------------------------------------------------
  def __init__(self, master):
    """Initialise all GUI elements"""
    UI.TKI.GUItabView.__init__(self, master, "TM", "M&C TM")
    # menu buttons
    self.menuButtons = UI.TKI.MenuButtons(self,
      [["REC+", self.recordPacketsCallback, COLOR_BUTTON_FG, COLOR_BUTTON_BG],
       ["REC-", self.stopPacketRecorderCallback, COLOR_BUTTON_FG, COLOR_BUTTON_BG, tkinter.DISABLED]])
    self.appGrid(self.menuButtons,
                 row=0,
                 columnspan=2,
                 rowweight=0,
                 sticky=tkinter.EW)
    # log messages (default logger)
    self.messageLogger = UI.TKI.MessageLogger(self, "TM")
    self.appGrid(self.messageLogger, row=1, columnspan=2)
    # message line
    self.messageline = tkinter.Message(self, relief=tkinter.GROOVE)
    self.appGrid(self.messageline,
                 row=2,
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
    self.addCommandMenuItem(label="RecordPackets", command=self.recordPacketsCallback)
    self.addCommandMenuItem(label="StopPacketRecorder", command=self.stopPacketRecorderCallback, enabled=False)
  # ---------------------------------------------------------------------------
  def recordPacketsCallback(self):
    """Called when the RecordPackets menu entry is selected"""
    fileName = filedialog.asksaveasfilename(title="Create TM Packet Record File",
                                            initialdir=SCOS.ENV.s_environment.tmFilesDir())
    if fileName != "" and fileName != ():
      self.notifyModelTask(["RECORDPACKETS", fileName])
  # ---------------------------------------------------------------------------
  def stopPacketRecorderCallback(self):
    """Called when the StopPacketRecorder menu entry is selected"""
    self.notifyModelTask(["STOPPACKETRECORDER"])
  # ---------------------------------------------------------------------------
  def notifyStatus(self, status):
    """Generic callback when something changes in the model"""
    if status == "PACKET_REC_STARTED":
      self.packetRecStarted()
    elif status == "PACKET_REC_STOPPED":
      self.packetRecStopped()
  # ---------------------------------------------------------------------------
  def packetRecStarted(self):
    """Called when the recordPackets function is successfully processed"""
    self.disableCommandMenuItem("RecordPackets")
    self.enableCommandMenuItem("StopPacketRecorder")
    self.menuButtons.setState("REC+", tkinter.DISABLED)
    self.menuButtons.setState("REC-", tkinter.NORMAL)
  # ---------------------------------------------------------------------------
  def packetRecStopped(self):
    """Called when the stopPacketRecorder function is successfully processed"""
    self.enableCommandMenuItem("RecordPackets")
    self.disableCommandMenuItem("StopPacketRecorder")
    self.menuButtons.setState("REC+", tkinter.NORMAL)
    self.menuButtons.setState("REC-", tkinter.DISABLED)
