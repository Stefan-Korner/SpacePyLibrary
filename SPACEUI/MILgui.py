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
COLOR_MESSAGE = "#00FFFF"

###########
# classes #
###########
# =============================================================================
class GUIview(UI.TKI.GUItabView):
  """Implementation of the MIL Bus GUI layer"""
  # ---------------------------------------------------------------------------
  def __init__(self, master):
    """Initialise all GUI elements"""
    UI.TKI.GUItabView.__init__(self, master, "MIL", "MIL Bus")
    # Bus Controller status
    self.bcField = UI.TKI.ValueField(self, row=0, column=0, label="BC:", fieldColumnspan=7)
    self.bcField.set("UNINIT")
    # multi Remote Terminals status
    self.mrtField = UI.TKI.ValueField(self, row=1, column=0, label="mRT:", fieldColumnspan=7)
    self.mrtField.set("UNINIT")
    # Remote Terminals
    self.rtFields = [None] * 32
    self.rtFields[0] = UI.TKI.ValueField(self, row=2, column=0, label="RT00:", width=10)
    self.rtFields[1] = UI.TKI.ValueField(self, row=3, column=0, label="RT01:", width=10)
    self.rtFields[2] = UI.TKI.ValueField(self, row=4, column=0, label="RT02:", width=10)
    self.rtFields[3] = UI.TKI.ValueField(self, row=5, column=0, label="RT03:", width=10)
    self.rtFields[4] = UI.TKI.ValueField(self, row=6, column=0, label="RT04:", width=10)
    self.rtFields[5] = UI.TKI.ValueField(self, row=7, column=0, label="RT05:", width=10)
    self.rtFields[6] = UI.TKI.ValueField(self, row=8, column=0, label="RT06:", width=10)
    self.rtFields[7] = UI.TKI.ValueField(self, row=9, column=0, label="RT07:", width=10)
    self.rtFields[8] = UI.TKI.ValueField(self, row=2, column=2, label="RT08:", width=10)
    self.rtFields[9] = UI.TKI.ValueField(self, row=3, column=2, label="RT09:", width=10)
    self.rtFields[10] = UI.TKI.ValueField(self, row=4, column=2, label="RT10:", width=10)
    self.rtFields[11] = UI.TKI.ValueField(self, row=5, column=2, label="RT11:", width=10)
    self.rtFields[12] = UI.TKI.ValueField(self, row=6, column=2, label="RT12:", width=10)
    self.rtFields[13] = UI.TKI.ValueField(self, row=7, column=2, label="RT13:", width=10)
    self.rtFields[14] = UI.TKI.ValueField(self, row=8, column=2, label="RT14:", width=10)
    self.rtFields[15] = UI.TKI.ValueField(self, row=9, column=2, label="RT15:", width=10)
    self.rtFields[16] = UI.TKI.ValueField(self, row=2, column=4, label="RT16:", width=10)
    self.rtFields[17] = UI.TKI.ValueField(self, row=3, column=4, label="RT17:", width=10)
    self.rtFields[18] = UI.TKI.ValueField(self, row=4, column=4, label="RT18:", width=10)
    self.rtFields[19] = UI.TKI.ValueField(self, row=5, column=4, label="RT19:", width=10)
    self.rtFields[20] = UI.TKI.ValueField(self, row=6, column=4, label="RT20:", width=10)
    self.rtFields[21] = UI.TKI.ValueField(self, row=7, column=4, label="RT21:", width=10)
    self.rtFields[22] = UI.TKI.ValueField(self, row=8, column=4, label="RT22:", width=10)
    self.rtFields[23] = UI.TKI.ValueField(self, row=9, column=4, label="RT23:", width=10)
    self.rtFields[24] = UI.TKI.ValueField(self, row=2, column=6, label="RT24:", width=10)
    self.rtFields[25] = UI.TKI.ValueField(self, row=3, column=6, label="RT25:", width=10)
    self.rtFields[26] = UI.TKI.ValueField(self, row=4, column=6, label="RT26:", width=10)
    self.rtFields[27] = UI.TKI.ValueField(self, row=5, column=6, label="RT27:", width=10)
    self.rtFields[28] = UI.TKI.ValueField(self, row=6, column=6, label="RT28:", width=10)
    self.rtFields[29] = UI.TKI.ValueField(self, row=7, column=6, label="RT29:", width=10)
    self.rtFields[30] = UI.TKI.ValueField(self, row=8, column=6, label="RT30:", width=10)
    self.rtFields[31] = UI.TKI.ValueField(self, row=9, column=6, label="RT31:", width=10)
    # log messages (default logger)
    self.messageLogger = UI.TKI.MessageLogger(self, "MIL")
    self.appGrid(self.messageLogger, row=10, columnspan=8)
    # message line
    self.messageline = Tkinter.Message(self, relief=Tkinter.GROOVE)
    self.appGrid(self.messageline,
                 row=11,
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
    implementation of UI.TKI.GUItabView.fillCommandMenuItems
    """
    pass
  # ---------------------------------------------------------------------------
  def writeBcMessage(self, message):
    """write a message into the Bus Controller message field"""
    self.bcField.set(message)
    self.bcField.setBackground(COLOR_MESSAGE)
  # ---------------------------------------------------------------------------
  def writeMRtMessage(self, message):
    """write a message into the multi Remote Terminals message field"""
    self.mrtField.set(message)
    self.mrtField.setBackground(COLOR_MESSAGE)
  # ---------------------------------------------------------------------------
  def writeMessage(self, rtAddress, message):
    """write a message into the relared message field"""
    self.rtFields[rtAddress].set(message)
    self.rtFields[rtAddress].setBackground(COLOR_MESSAGE)
  # ---------------------------------------------------------------------------
  def notifyStatus(self, status):
    """Generic callback when something changes in the model"""
    if status == "CCS_CONNECTED":
      self.writeBcMessage("CONNECTED")
    elif status == "CCS_CONNECTED2":
      self.writeMRtMessage("CONNECTED")
    else:
      tokens = status.split()
      if len(tokens) >= 3:
        token0 = tokens[0]
        token1 = tokens[1]
        if token0 == "RT":
          rtAddress = int(token1)
          message = " ".join(tokens[2:])
          self.writeMessage(rtAddress, message)
