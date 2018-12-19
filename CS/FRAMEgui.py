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
# FRAME layer GUI                                                             *
#******************************************************************************
import Tkinter, tkFileDialog
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import CS.FRAMErply
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
class GUIview(UI.TKI.GUIwinView):
  """Implementation of the Control System FRAME GUI layer"""
  # ---------------------------------------------------------------------------
  def __init__(self, master):
    """Initialise all GUI elements"""
    UI.TKI.GUIwinView.__init__(self, master, "FRAME", "FRAME Layer")
    # menu buttons
    self.menuButtons = UI.TKI.MenuButtons(self,
      [["RPLY", self.replayFramesCallback, COLOR_BUTTON_FG, COLOR_BUTTON_BG]])
    self.appGrid(self.menuButtons,
                 row=0,
                 columnspan=2,
                 rowweight=0,
                 sticky=Tkinter.EW)
    # replay TM frames
    self.replayTMframesField = UI.TKI.ValueField(self, row=1, label="Replay TM frames:")
    # log messages (default logger)
    self.messageLogger = UI.TKI.MessageLogger(self, "FRAME")
    self.appGrid(self.messageLogger, row=2, columnspan=2)
    # message line
    self.messageline = Tkinter.Message(self, relief=Tkinter.GROOVE)
    self.appGrid(self.messageline,
                 row=3,
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
    self.addCommandMenuItem(label="ReplayFrames", command=self.replayFramesCallback)
  # ---------------------------------------------------------------------------
  def replayFramesCallback(self):
    """Called when the ReplayFrames menu entry is selected"""
    fileName = tkFileDialog.askopenfilename(title="Open TM Frame Replay File",
                                            initialdir=SCOS.ENV.s_environment.tmFilesDir())
    if fileName != "" and fileName != ():
      self.notifyModelTask(["REPLAYFRAMES", fileName])
  # ---------------------------------------------------------------------------
  def notifyStatus(self, status):
    """Generic callback when something changes in the model"""
    if status == "UPDATE_REPLAY":
      self.updateReplayNotify()
    if status == "UPDATE_REPLAY_NR":
      self.updateReplayNrNotify()
  # ---------------------------------------------------------------------------
  def updateReplayNotify(self):
    """Called when the replay state has changed"""
    if CS.FRAMErply.s_frameReplayer.running:
      self.disableCommandMenuItem("ReplayFrames")
      self.menuButtons.setState("RPLY", Tkinter.DISABLED)
      self.replayTMframesField.set("Running")
      self.lastFrameNr = 0
    else:
      self.enableCommandMenuItem("ReplayFrames")
      self.menuButtons.setState("RPLY", Tkinter.NORMAL)
      self.replayTMframesField.set("Stopped: Nr. frames = " + str(CS.FRAMErply.s_frameReplayer.frameNr))
  # ---------------------------------------------------------------------------
  def updateReplayNrNotify(self):
    """Called when the next replay frame has been processed"""
    self.replayTMframesField.set("Running: Nr. frames = " + str(CS.FRAMErply.s_frameReplayer.frameNr))
