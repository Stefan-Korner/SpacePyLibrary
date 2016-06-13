#******************************************************************************
# (C) 2016, Stefan Korner, Austria                                            *
#                                                                             *
# The Space Python Library is free software; you can redistribute it and/or   *
# modify it under the terms of the GNU Lesser General Public License as       *
# published by the Free Software Foundation; either version 2.1 of the        *
# License, or (at your option) any later version.                             *
#                                                                             *
# The Space Python Library is distributed in the hope that it will be useful, *
# but WITHOUT ANY WARRANTY; without even the implied warranty of              *
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser     *
# General Public License for more details.                                    *
#******************************************************************************
# MIL Bus Simulation GUI                                                      *
#******************************************************************************
import Tkinter
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
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
  """Implementation of the MIL Bus GUI layer"""
  # ---------------------------------------------------------------------------
  def __init__(self, master):
    """Initialise all GUI elements"""
    UI.TKI.GUIwinView.__init__(self, master, "MIL", "MIL Bus")
    # Remote Terminals
    self.rt00Field = UI.TKI.ValueField(self, row=0, column=0, label="RT00:", width=10)
    self.rt08Field = UI.TKI.ValueField(self, row=0, column=2, label="RT08:", width=10)
    self.rt16Field = UI.TKI.ValueField(self, row=0, column=4, label="RT16:", width=10)
    self.rt24Field = UI.TKI.ValueField(self, row=0, column=6, label="RT24:", width=10)
    self.rt01Field = UI.TKI.ValueField(self, row=1, column=0, label="RT01:", width=10)
    self.rt09Field = UI.TKI.ValueField(self, row=1, column=2, label="RT09:", width=10)
    self.rt17Field = UI.TKI.ValueField(self, row=1, column=4, label="RT17:", width=10)
    self.rt25Field = UI.TKI.ValueField(self, row=1, column=6, label="RT25:", width=10)
    self.rt02Field = UI.TKI.ValueField(self, row=2, column=0, label="RT02:", width=10)
    self.rt10Field = UI.TKI.ValueField(self, row=2, column=2, label="RT10:", width=10)
    self.rt18Field = UI.TKI.ValueField(self, row=2, column=4, label="RT18:", width=10)
    self.rt26Field = UI.TKI.ValueField(self, row=2, column=6, label="RT26:", width=10)
    self.rt03Field = UI.TKI.ValueField(self, row=3, column=0, label="RT03:", width=10)
    self.rt11Field = UI.TKI.ValueField(self, row=3, column=2, label="RT11:", width=10)
    self.rt19Field = UI.TKI.ValueField(self, row=3, column=4, label="RT19:", width=10)
    self.rt27Field = UI.TKI.ValueField(self, row=3, column=6, label="RT27:", width=10)
    self.rt04Field = UI.TKI.ValueField(self, row=4, column=0, label="RT04:", width=10)
    self.rt12Field = UI.TKI.ValueField(self, row=4, column=2, label="RT12:", width=10)
    self.rt20Field = UI.TKI.ValueField(self, row=4, column=4, label="RT20:", width=10)
    self.rt28Field = UI.TKI.ValueField(self, row=4, column=6, label="RT28:", width=10)
    self.rt05Field = UI.TKI.ValueField(self, row=5, column=0, label="RT05:", width=10)
    self.rt13Field = UI.TKI.ValueField(self, row=5, column=2, label="RT13:", width=10)
    self.rt21Field = UI.TKI.ValueField(self, row=5, column=4, label="RT21:", width=10)
    self.rt29Field = UI.TKI.ValueField(self, row=5, column=6, label="RT29:", width=10)
    self.rt06Field = UI.TKI.ValueField(self, row=6, column=0, label="RT06:", width=10)
    self.rt14Field = UI.TKI.ValueField(self, row=6, column=2, label="RT14:", width=10)
    self.rt22Field = UI.TKI.ValueField(self, row=6, column=4, label="RT22:", width=10)
    self.rt30Field = UI.TKI.ValueField(self, row=6, column=6, label="RT30:", width=10)
    self.rt07Field = UI.TKI.ValueField(self, row=7, column=0, label="RT07:", width=10)
    self.rt15Field = UI.TKI.ValueField(self, row=7, column=2, label="RT15:", width=10)
    self.rt23Field = UI.TKI.ValueField(self, row=7, column=4, label="RT23:", width=10)
    self.rt31Field = UI.TKI.ValueField(self, row=7, column=6, label="RT31:", width=10)
    # log messages (default logger)
    self.messageLogger = UI.TKI.MessageLogger(self, "MIL")
    self.appGrid(self.messageLogger, row=8, columnspan=8)
    # message line
    self.messageline = Tkinter.Message(self, relief=Tkinter.GROOVE)
    self.appGrid(self.messageline,
                 row=9,
                 columnspan=8,
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
    pass
  # ---------------------------------------------------------------------------
  def notifyStatus(self, status):
    """Generic callback when something changes in the model"""
    pass
