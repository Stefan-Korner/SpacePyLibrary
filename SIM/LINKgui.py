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
# Space Link Simulation GUI                                                   *
#******************************************************************************
import tkinter
from tkinter import simpledialog
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import LINK.IF
import UI.TKI
import UTIL.TIME

#############
# constants #
#############
COLOR_BUTTON_FG = "#FFFFFF"
COLOR_BUTTON_BG = "#808080"
COLOR_ON_OK = "#00FF00"
COLOR_ON_NOK = "#FF0000"
QUEUE_HEADER1 = "       RECEPTION TIME |SNR"
QUEUE_HEADER2 = "----------------------|---"
QUEUE_ROW_FORMAT = "%21s |%3d"

###########
# classes #
###########
# =============================================================================
class GUIview(UI.TKI.GUIwinView):
  """Implementation of the SIM Link GUI layer"""
  # ---------------------------------------------------------------------------
  def __init__(self, master):
    """Initialise all GUI elements"""
    UI.TKI.GUIwinView.__init__(self, master, "LINK", "Space Link")
    # menu buttons
    self.menuButtons = UI.TKI.MenuButtons(self,
      [["CLCW", self.setCLCWcallback, COLOR_BUTTON_FG, COLOR_BUTTON_BG]])
    self.appGrid(self.menuButtons,
                 row=0,
                 columnspan=2,
                 rowweight=0,
                 sticky=tkinter.EW)
    # checkbuttons
    self.checkButtons = UI.TKI.Checkbuttons(self,
      [["CLCW", self.clcwCallback, True, COLOR_ON_OK],
       ["LOCK", self.lockoutCallback, False, COLOR_ON_NOK]])
    self.appGrid(self.checkButtons,
                 row=1,
                 columnspan=2,
                 rowweight=0,
                 columnweight=0,
                 sticky=tkinter.W)
    # tm status
    self.clcwStatusField = UI.TKI.ValueField(self, row=2, label="CLCW status:")
    self.clcwStatusField.set("CLCW=0")
    # uplink and downlink queue contents
    self.subFrame = UI.TKI.SubFrame(self)
    uplinkQueueLabel = tkinter.Label(self.subFrame, text="Uplink Queue Contents")
    self.subFrame.appGrid(uplinkQueueLabel,
                          row=0,
                          column=0,
                          rowweight=0,
                          columnweight=0,
                          sticky=tkinter.EW)
    self.uplinkQueueContents = UI.TKI.ScrolledListbox(self.subFrame, selectmode=tkinter.SINGLE)
    self.uplinkQueueContents.list().configure(font="courier")
    self.uplinkQueueContents.list().insert(0, QUEUE_HEADER1)
    self.uplinkQueueContents.list().insert(1, QUEUE_HEADER2)
    self.subFrame.appGrid(self.uplinkQueueContents, row=1, column=0)
    downlinkQueueLabel = tkinter.Label(self.subFrame, text="Downlink Queue Contents")
    self.subFrame.appGrid(downlinkQueueLabel,
                          row=0,
                          column=1,
                          rowweight=0,
                          columnweight=0,
                          sticky=tkinter.EW)
    self.downlinkQueueContents = UI.TKI.ScrolledListbox(self.subFrame, selectmode=tkinter.SINGLE)
    self.downlinkQueueContents.list().configure(font="courier")
    self.downlinkQueueContents.list().insert(0, QUEUE_HEADER1)
    self.downlinkQueueContents.list().insert(1, QUEUE_HEADER2)
    self.subFrame.appGrid(self.downlinkQueueContents, row=1, column=1)
    self.appGrid(self.subFrame, row=3, columnspan=2)
    # log messages
    self.messageLogger = UI.TKI.MessageLogger(self, "LINK")
    self.appGrid(self.messageLogger, row=5, columnspan=2)
    # message line
    self.messageline = tkinter.Message(self, relief=tkinter.GROOVE)
    self.appGrid(self.messageline,
                 row=6,
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
    self.addCommandMenuItem(label="SetCLCW", command=self.setCLCWcallback)
    self.addCommandMenuItem(label="EnableCLCW", command=self.enableCLCWcallback, enabled=False)
    self.addCommandMenuItem(label="DisableCLCW", command=self.disableCLCWcallback)
    self.addCommandMenuItem(label="SetLockout", command=self.setLockoutCallback)
    self.addCommandMenuItem(label="ResetLockout", command=self.resetLockoutCallback, enabled=False)
  # ---------------------------------------------------------------------------
  def setCLCWcallback(self):
    """Called when the SetCLCW menu entry is selected"""
    clcwStr = simpledialog.askstring(title="CLCW Dialog",
                                     prompt="CLCW Report Value (0...255):",
                                     initialvalue="0")
    if clcwStr != None:
      self.notifyModelTask(["SETCLCW", clcwStr])
  # ---------------------------------------------------------------------------
  def enableCLCWcallback(self):
    """Called when the EnableCLCW menu entry is selected"""
    self.notifyModelTask(["ENABLECLCW"])
  def disableCLCWcallback(self):
    """Called when the DisableCLCW menu entry is selected"""
    self.notifyModelTask(["DISABLECLCW"])
  def clcwCallback(self):
    """Called when the CLCW checkbutton is pressed"""
    if self.checkButtons.getButtonPressed("CLCW"):
      self.notifyModelTask(["ENABLECLCW"])
    else:
      self.notifyModelTask(["DISABLECLCW"])
  # ---------------------------------------------------------------------------
  def setLockoutCallback(self):
    """Called when the SetLockout menu entry is selected"""
    self.notifyModelTask(["SETLOCKOUT"])
  def resetLockoutCallback(self):
    """Called when the ResetLockout menu entry is selected"""
    self.notifyModelTask(["RESETLOCKOUT"])
  def lockoutCallback(self):
    """Called when the LOCK checkbutton is pressed"""
    if self.checkButtons.getButtonPressed("LOCK"):
      self.notifyModelTask(["SETLOCKOUT"])
    else:
      self.notifyModelTask(["RESETLOCKOUT"])
  # ---------------------------------------------------------------------------
  def notifyStatus(self, status):
    """Generic callback when something changes in the model"""
    if status == "TC_FRAME":
      self.tcFrameNotify()
    elif status == "TM_FRAME":
      self.tmFrameNotify()
    elif status == "ENABLED_CLCW":
      self.enabledCLCWnotify()
    elif status == "DISABLED_CLCW":
      self.disabledCLCWnotify()
    elif status == "LOCKOUT_SET":
      self.lockoutSetNotify()
    elif status == "LOCKOUT_RESET":
      self.lockoutResetNotify()
  # ---------------------------------------------------------------------------
  def tcFrameNotify(self):
    """Called when a TC frame is added to / removed from the queue"""
    # update the CLCW status field
    clcw = LINK.IF.s_tmFrameGenerator.getCLCW()
    txt = "CLCW=" + str(clcw.reportValue)
    self.clcwStatusField.set(txt)
    # update the queue display
    self.uplinkQueueContents.list().delete(0, tkinter.END)
    self.uplinkQueueContents.list().insert(0, QUEUE_HEADER1)
    self.uplinkQueueContents.list().insert(1, QUEUE_HEADER2)
    entryPos = 2
    uplinkQueue = LINK.IF.s_spaceLink.getUplinkQueue()
    receptionTimes = uplinkQueue.keys()
    receptionTimes = sorted(receptionTimes)
    for receptionTime in receptionTimes:
      tcFrameDu = uplinkQueue[receptionTime]
      rowText = QUEUE_ROW_FORMAT % (UTIL.TIME.getASDtimeStr(receptionTime),
                                    tcFrameDu.sequenceNumber)
      self.uplinkQueueContents.list().insert(entryPos, rowText)
      entryPos += 1
  # ---------------------------------------------------------------------------
  def tmFrameNotify(self):
    """Called when a TC frame is added to / removed from the queue"""
    # update the queue display
    self.downlinkQueueContents.list().delete(0, tkinter.END)
    self.downlinkQueueContents.list().insert(0, QUEUE_HEADER1)
    self.downlinkQueueContents.list().insert(1, QUEUE_HEADER2)
    entryPos = 2
    downlinkQueue = LINK.IF.s_spaceLink.getDownlinkQueue()
    receptionTimes = downlinkQueue.keys()
    receptionTimes = sorted(receptionTimes)
    for receptionTime in receptionTimes:
      tmFrameDu, ertUTC = downlinkQueue[receptionTime]
      if ertUTC == None:
        displayTime = receptionTime
      else:
        displayTime = ertUTC
      rowText = QUEUE_ROW_FORMAT % (UTIL.TIME.getASDtimeStr(displayTime),
                                    tmFrameDu.masterChannelFrameCount)
      self.downlinkQueueContents.list().insert(entryPos, rowText)
      entryPos += 1
  # ---------------------------------------------------------------------------
  def enabledCLCWnotify(self):
    """Called when the enabledCLCW function is succsssfully processed"""
    self.disableCommandMenuItem("EnableCLCW")
    self.enableCommandMenuItem("DisableCLCW")
    self.checkButtons.setButtonPressed("CLCW", True)
  # ---------------------------------------------------------------------------
  def disabledCLCWnotify(self):
    """Called when the disabledCLCW function is succsssfully processed"""
    self.enableCommandMenuItem("EnableCLCW")
    self.disableCommandMenuItem("DisableCLCW")
    self.checkButtons.setButtonPressed("CLCW", False)
  # ---------------------------------------------------------------------------
  def lockoutSetNotify(self):
    """Called when the setLockout function is succsssfully processed"""
    self.disableCommandMenuItem("SetLockout")
    self.enableCommandMenuItem("ResetLockout")
    self.checkButtons.setButtonPressed("LOCK", True)
  # ---------------------------------------------------------------------------
  def lockoutResetNotify(self):
    """Called when the resetLockout function is succsssfully processed"""
    self.enableCommandMenuItem("SetLockout")
    self.disableCommandMenuItem("ResetLockout")
    self.checkButtons.setButtonPressed("LOCK", False)
