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
# Onboard Queue Simulation GUI                                                *
#******************************************************************************
import Tkinter
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import SPACE.DEF, SPACE.IF
import UI.TKI
import UTIL.TIME

#############
# constants #
#############
COLOR_BUTTON_BG = "#808080"
COLOR_NORMAL = "#FFFFFF"
COLOR_CONNECTED = "#FFFF00"
COLOR_PACKET_DEFINED = "#00FFFF"
COLOR_ON_OK = "#00FF00"
COLOR_ON_NOK = "#FF0000"
QUEUE_HEADER1 = "       EXECUTION TIME | APID | TYPE | STYPE | SCOUNT"
QUEUE_HEADER2 = "----------------------|------|------|-------|-------"
QUEUE_ROW_FORMAT = "%21s | %4d |  %3d |   %3d |  %5d"

###########
# classes #
###########
# =============================================================================
class GUIview(UI.TKI.GUIwinView):
  """Implementation of the SIM Onboard Queue GUI layer"""
  # ---------------------------------------------------------------------------
  def __init__(self, master):
    """Initialise all GUI elements"""
    UI.TKI.GUIwinView.__init__(self, master, "OBQ", "Onboard Queue")
    # checkbuttons
    self.checkButtons = UI.TKI.Checkbuttons(self,
      [["ACK1", self.ack1Callback, True, COLOR_ON_OK],
       ["NAK1", self.nak1Callback, False, COLOR_ON_NOK],
       ["ACK2", self.ack2Callback, True, COLOR_ON_OK],
       ["NAK2", self.nak2Callback, False, COLOR_ON_NOK],
       ["ACK3", self.ack3Callback, True, COLOR_ON_OK],
       ["NAK3", self.nak3Callback, False, COLOR_ON_NOK],
       ["ACK4", self.ack4Callback, True, COLOR_ON_OK],
       ["NAK4", self.nak4Callback, False, COLOR_ON_NOK]])
    self.appGrid(self.checkButtons,
                 row=0,
                 rowweight=0,
                 columnweight=0,
                 sticky=Tkinter.W)
    # use the filler to force correct resizing of all GUI elements
    filler = Tkinter.Label(self, text="")
    self.appGrid(filler,
                 row=0,
                 column=1,
                 rowweight=0,
                 columnweight=1,
                 sticky=Tkinter.W)
    # onboard queue contents
    label = Tkinter.Label(self, text="Onboard Queue Contents")
    self.appGrid(label,
                 row=1,
                 columnspan=2,
                 rowweight=0,
                 columnweight=0,
                 sticky=Tkinter.EW)
    self.queueContents = UI.TKI.ScrolledListbox(self, selectmode=Tkinter.SINGLE)
    self.queueContents.list().configure(font="courier")
    self.queueContents.list().insert(0, QUEUE_HEADER1)
    self.queueContents.list().insert(1, QUEUE_HEADER2)
    self.appGrid(self.queueContents, row=2, columnspan=2)
    # log messages
    self.messageLogger = UI.TKI.MessageLogger(self, "OBQ")
    self.appGrid(self.messageLogger, row=3, columnspan=2)
    # message line
    self.messageline = Tkinter.Message(self, relief=Tkinter.GROOVE)
    self.appGrid(self.messageline,
                 row=4,
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
    self.addCommandMenuItem(label="OBQenableAck1", command=self.obqEnableAck1Callback, enabled=False)
    self.addCommandMenuItem(label="OBQenableNak1", command=self.obqEnableNak1Callback)
    self.addCommandMenuItem(label="OBQdisableAck1", command=self.obqDisableAck1Callback)
    self.addCommandMenuItem(label="OBQenableAck2", command=self.obqEnableAck2Callback, enabled=False)
    self.addCommandMenuItem(label="OBQenableNak2", command=self.obqEnableNak2Callback)
    self.addCommandMenuItem(label="OBQdisableAck2", command=self.obqDisableAck2Callback)
    self.addCommandMenuItem(label="OBQenableAck3", command=self.obqEnableAck3Callback, enabled=False)
    self.addCommandMenuItem(label="OBQenableNak3", command=self.obqEnableNak3Callback)
    self.addCommandMenuItem(label="OBQdisableAck3", command=self.obqDisableAck3Callback)
    self.addCommandMenuItem(label="OBQenableAck4", command=self.obqEnableAck4Callback, enabled=False)
    self.addCommandMenuItem(label="OBQenableNak4", command=self.obqEnableNak4Callback)
    self.addCommandMenuItem(label="OBQdisableAck4", command=self.obqDisableAck4Callback)
  # ---------------------------------------------------------------------------
  def obqEnableAck1Callback(self):
    """Called when the OBQenableAck1 menu entry is selected"""
    self.notifyModelTask(["OBQENABLEACK1"])
  def obqEnableNak1Callback(self):
    """Called when the OBQenableNak1 menu entry is selected"""
    self.notifyModelTask(["OBQENABLENAK1"])
  def obqDisableAck1Callback(self):
    """Called when the OBQdisableAck1 menu entry is selected"""
    self.notifyModelTask(["OBQDISABLEACK1"])
  def ack1Callback(self):
    """Called when the ACK1 checkbutton is pressed"""
    if self.checkButtons.getButtonPressed("ACK1"):
      self.notifyModelTask(["OBQENABLEACK1"])
    else:
      self.notifyModelTask(["OBQDISABLEACK1"])
  def nak1Callback(self):
    """Called when the NAK1 checkbutton is pressed"""
    if self.checkButtons.getButtonPressed("NAK1"):
      self.notifyModelTask(["OBQENABLENAK1"])
    else:
      self.notifyModelTask(["OBQDISABLEACK1"])
  # ---------------------------------------------------------------------------
  def obqEnableAck2Callback(self):
    """Called when the OBQenableAck2 menu entry is selected"""
    self.notifyModelTask(["OBQENABLEACK2"])
  def obqEnableNak2Callback(self):
    """Called when the OBQenableNak2 menu entry is selected"""
    self.notifyModelTask(["OBQENABLENAK2"])
  def obqDisableAck2Callback(self):
    """Called when the OBQdisableAck2 menu entry is selected"""
    self.notifyModelTask(["OBQDISABLEACK2"])
  def ack2Callback(self):
    """Called when the ACK2 checkbutton is pressed"""
    if self.checkButtons.getButtonPressed("ACK2"):
      self.notifyModelTask(["OBQENABLEACK2"])
    else:
      self.notifyModelTask(["OBQDISABLEACK2"])
  def nak2Callback(self):
    """Called when the NAK2 checkbutton is pressed"""
    if self.checkButtons.getButtonPressed("NAK2"):
      self.notifyModelTask(["OBQENABLENAK2"])
    else:
      self.notifyModelTask(["OBQDISABLEACK2"])
  # ---------------------------------------------------------------------------
  def obqEnableAck3Callback(self):
    """Called when the OBQenableAck3 menu entry is selected"""
    self.notifyModelTask(["OBQENABLEACK3"])
  def obqEnableNak3Callback(self):
    """Called when the OBQenableNak3 menu entry is selected"""
    self.notifyModelTask(["OBQENABLENAK3"])
  def obqDisableAck3Callback(self):
    """Called when the OBQdisableAck3 menu entry is selected"""
    self.notifyModelTask(["OBQDISABLEACK3"])
  def ack3Callback(self):
    """Called when the ACK3 checkbutton is pressed"""
    if self.checkButtons.getButtonPressed("ACK3"):
      self.notifyModelTask(["OBQENABLEACK3"])
    else:
      self.notifyModelTask(["OBQDISABLEACK3"])
  def nak3Callback(self):
    """Called when the NAK3 checkbutton is pressed"""
    if self.checkButtons.getButtonPressed("NAK3"):
      self.notifyModelTask(["OBQENABLENAK3"])
    else:
      self.notifyModelTask(["OBQDISABLEACK3"])
  # ---------------------------------------------------------------------------
  def obqEnableAck4Callback(self):
    """Called when the OBQenableAck4 menu entry is selected"""
    self.notifyModelTask(["OBQENABLEACK4"])
  def obqEnableNak4Callback(self):
    """Called when the OBQenableNak4 menu entry is selected"""
    self.notifyModelTask(["OBQENABLENAK4"])
  def obqDisableAck4Callback(self):
    """Called when the OBQdisableAck4 menu entry is selected"""
    self.notifyModelTask(["OBQDISABLEACK4"])
  def ack4Callback(self):
    """Called when the ACK4 checkbutton is pressed"""
    if self.checkButtons.getButtonPressed("ACK4"):
      self.notifyModelTask(["OBQENABLEACK4"])
    else:
      self.notifyModelTask(["OBQDISABLEACK4"])
  def nak4Callback(self):
    """Called when the NAK4 checkbutton is pressed"""
    if self.checkButtons.getButtonPressed("NAK4"):
      self.notifyModelTask(["OBQENABLENAK4"])
    else:
      self.notifyModelTask(["OBQDISABLEACK4"])
  # ---------------------------------------------------------------------------
  def notifyStatus(self, status):
    """Generic callback when something changes in the model"""
    if status == "TT_PACKET":
      self.ttPacketNotify()
    elif status == "OBQ_ENABLED_ACK1":
      self.obqEnabledAck1Notify()
    elif status == "OBQ_ENABLED_NAK1":
      self.obqEnabledNak1Notify()
    elif status == "OBQ_DISABLED_ACK1":
      self.obqDisabledAck1Notify()
    elif status == "OBQ_ENABLED_ACK2":
      self.obqEnabledAck2Notify()
    elif status == "OBQ_ENABLED_NAK2":
      self.obqEnabledNak2Notify()
    elif status == "OBQ_DISABLED_ACK2":
      self.obqDisabledAck2Notify()
    elif status == "OBQ_ENABLED_ACK3":
      self.obqEnabledAck3Notify()
    elif status == "OBQ_ENABLED_NAK3":
      self.obqEnabledNak3Notify()
    elif status == "OBQ_DISABLED_ACK3":
      self.obqDisabledAck3Notify()
    elif status == "OBQ_ENABLED_ACK4":
      self.obqEnabledAck4Notify()
    elif status == "OBQ_ENABLED_NAK4":
      self.obqEnabledNak4Notify()
    elif status == "OBQ_DISABLED_ACK4":
      self.obqDisabledAck4Notify()
  # ---------------------------------------------------------------------------
  def ttPacketNotify(self):
    """Called when a time tagged packet is added to / removed from the queue"""
    self.queueContents.list().delete(0, Tkinter.END)
    self.queueContents.list().insert(0, QUEUE_HEADER1)
    self.queueContents.list().insert(1, QUEUE_HEADER2)
    entryPos = 2
    ttQueue = SPACE.IF.s_onboardQueue.getQueue()
    ttExecTimes = ttQueue.keys()
    ttExecTimes.sort()
    for ttExecTime in ttExecTimes:
      ttPacketDu = ttQueue[ttExecTime]
      rowText = QUEUE_ROW_FORMAT % (UTIL.TIME.getASDtimeStr(ttExecTime),
                                    ttPacketDu.applicationProcessId,
                                    ttPacketDu.serviceType,
                                    ttPacketDu.serviceSubType,
                                    ttPacketDu.sequenceControlCount)
      self.queueContents.list().insert(entryPos, rowText)
      entryPos += 1
  # ---------------------------------------------------------------------------
  def obqEnabledAck1Notify(self):
    """Called when the obqEnabledAck1 function is succsssfully processed"""
    self.disableCommandMenuItem("OBQenableAck1")
    self.enableCommandMenuItem("OBQenableNak1")
    self.enableCommandMenuItem("OBQdisableAck1")
    self.checkButtons.setButtonPressed("ACK1", True)
    self.checkButtons.setButtonPressed("NAK1", False)
  def obqEnabledNak1Notify(self):
    """Called when the obqEnabledNak1 function is succsssfully processed"""
    self.enableCommandMenuItem("OBQenableAck1")
    self.disableCommandMenuItem("OBQenableNak1")
    self.enableCommandMenuItem("OBQdisableAck1")
    self.checkButtons.setButtonPressed("ACK1", False)
    self.checkButtons.setButtonPressed("NAK1", True)
  def obqDisabledAck1Notify(self):
    """Called when the obqDisabledAck1 function is succsssfully processed"""
    self.enableCommandMenuItem("OBQenableAck1")
    self.enableCommandMenuItem("OBQenableNak1")
    self.disableCommandMenuItem("OBQdisableAck1")
    self.checkButtons.setButtonPressed("ACK1", False)
    self.checkButtons.setButtonPressed("NAK1", False)
  # ---------------------------------------------------------------------------
  def obqEnabledAck2Notify(self):
    """Called when the obqEnabledAck2 function is succsssfully processed"""
    self.disableCommandMenuItem("OBQenableAck2")
    self.enableCommandMenuItem("OBQenableNak1")
    self.enableCommandMenuItem("OBQdisableAck2")
    self.checkButtons.setButtonPressed("ACK2", True)
    self.checkButtons.setButtonPressed("NAK2", False)
  def obqEnabledNak2Notify(self):
    """Called when the obqEnabledNak2 function is succsssfully processed"""
    self.enableCommandMenuItem("OBQenableAck2")
    self.disableCommandMenuItem("OBQenableNak2")
    self.enableCommandMenuItem("OBQdisableAck2")
    self.checkButtons.setButtonPressed("ACK2", False)
    self.checkButtons.setButtonPressed("NAK2", True)
  def obqDisabledAck2Notify(self):
    """Called when the obqDisabledAck2 function is succsssfully processed"""
    self.enableCommandMenuItem("OBQenableAck2")
    self.enableCommandMenuItem("OBQenableNak2")
    self.disableCommandMenuItem("OBQdisableAck2")
    self.checkButtons.setButtonPressed("ACK2", False)
    self.checkButtons.setButtonPressed("NAK2", False)
  # ---------------------------------------------------------------------------
  def obqEnabledAck3Notify(self):
    """Called when the obqEnabledAck3 function is succsssfully processed"""
    self.disableCommandMenuItem("OBQenableAck3")
    self.enableCommandMenuItem("OBQenableNak3")
    self.enableCommandMenuItem("OBQdisableAck3")
    self.checkButtons.setButtonPressed("ACK3", True)
    self.checkButtons.setButtonPressed("NAK3", False)
  def obqEnabledNak3Notify(self):
    """Called when the obqEnabledNak3 function is succsssfully processed"""
    self.enableCommandMenuItem("OBQenableAck3")
    self.disableCommandMenuItem("OBQenableNak3")
    self.enableCommandMenuItem("OBQdisableAck3")
    self.checkButtons.setButtonPressed("ACK3", False)
    self.checkButtons.setButtonPressed("NAK3", True)
  def obqDisabledAck3Notify(self):
    """Called when the obqDisabledAck3 function is succsssfully processed"""
    self.enableCommandMenuItem("OBQenableAck3")
    self.enableCommandMenuItem("OBQenableNak3")
    self.disableCommandMenuItem("OBQdisableAck3")
    self.checkButtons.setButtonPressed("ACK3", False)
    self.checkButtons.setButtonPressed("NAK3", False)
  # ---------------------------------------------------------------------------
  def obqEnabledAck4Notify(self):
    """Called when the obqEnabledAck4 function is succsssfully processed"""
    self.disableCommandMenuItem("OBQenableAck4")
    self.enableCommandMenuItem("OBQenableNak4")
    self.enableCommandMenuItem("OBQdisableAck4")
    self.checkButtons.setButtonPressed("ACK4", True)
    self.checkButtons.setButtonPressed("NAK4", False)
  def obqEnabledNak4Notify(self):
    """Called when the obqEnabledNak4 function is succsssfully processed"""
    self.enableCommandMenuItem("OBQenableAck4")
    self.disableCommandMenuItem("OBQenableNak4")
    self.enableCommandMenuItem("OBQdisableAck4")
    self.checkButtons.setButtonPressed("ACK4", False)
    self.checkButtons.setButtonPressed("NAK4", True)
  def obqDisabledAck4Notify(self):
    """Called when the obqDisabledAck4 function is succsssfully processed"""
    self.enableCommandMenuItem("OBQenableAck4")
    self.enableCommandMenuItem("OBQenableNak4")
    self.disableCommandMenuItem("OBQdisableAck4")
    self.checkButtons.setButtonPressed("ACK4", False)
    self.checkButtons.setButtonPressed("NAK4", False)
