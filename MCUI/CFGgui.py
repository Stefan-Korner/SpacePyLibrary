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
# Monitoring and Control (M&C) Confiuration GUI                               *
#******************************************************************************
import tkinter
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
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
  """Implementation of the M&C Configuration GUI layer"""
  # ---------------------------------------------------------------------------
  def __init__(self, master):
    """Initialise all GUI elements"""
    UI.TKI.GUIwinView.__init__(self, master, "CFG", "M&C Config")
    # menu buttons
    self.menuButtons = UI.TKI.MenuButtons(self,
      [["LIST", self.listPacketsCallback, COLOR_BUTTON_FG, COLOR_BUTTON_BG],
       ["GEN", self.generateCallback, COLOR_BUTTON_FG, COLOR_BUTTON_BG]])
    self.appGrid(self.menuButtons,
                 row=0,
                 columnspan=2,
                 rowweight=0,
                 sticky=tkinter.EW)
    # log messages (default logger)
    self.messageLogger = UI.TKI.MessageLogger(self)
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
    implementation of UI.TKI.GUIwinView.fillCommandMenuItems
    """
    self.addCommandMenuItem(label="ListPackets", command=self.listPacketsCallback)
    self.addCommandMenuItem(label="Generate", command=self.generateCallback)
  # ---------------------------------------------------------------------------
  def listPacketsCallback(self):
    """Called when the ListPackets menu entry is selected"""
    # disable the button during generation,
    # because generation could take some time
    self.menuButtons.setState("LIST", tkinter.DISABLED)
    self.notifyModelTask(["LISTPACKETS"])
    self.menuButtons.setState("LIST", tkinter.NORMAL)
  # ---------------------------------------------------------------------------
  def generateCallback(self):
    """Called when the Generate menu entry is selected"""
    # disable the button during generation,
    # because generation could take some time
    self.menuButtons.setState("GEN", tkinter.DISABLED)
    self.notifyModelTask(["GENERATE"])
    self.menuButtons.setState("GEN", tkinter.NORMAL)
  # ---------------------------------------------------------------------------
  def notifyStatus(self, status):
    """Generic callback when something changes in the model"""
    LOG_WARNING("CFGgui.GUIview.notifyStatus not implemented", "CFG")
