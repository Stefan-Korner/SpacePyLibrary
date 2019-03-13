#!/usr/bin/env python
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
# TASK + TKI framework - Unit Test: customized Model Task with TKinter GUI    *
#******************************************************************************
from __future__ import print_function
import Tkinter
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import UI.TKI
import UTIL.TASK

#############
# functions #
#############
# -----------------------------------------------------------------------------
def initConfiguration():
  """initialise the system configuration"""
  UTIL.SYS.s_configuration.setDefaults([
  ["SYS_APP_MNEMO", "GUI"],
  ["SYS_APP_NAME", "Test GUI"],
  ["SYS_APP_VERSION", "1.0"]])

###########
# classes #
###########
# =============================================================================
class GUIview(UI.TKI.GUItabView):
  """Implementation of the SCOE EGSE GUI layer"""
  # ---------------------------------------------------------------------------
  def __init__(self, master):
    """Initialise all GUI elements"""
    UI.TKI.GUItabView.__init__(self, master, "GUI", "Test GUI")
    # log messages (default logger)
    self.messageLogger = UI.TKI.MessageLogger(self)
    self.appGrid(self.messageLogger, row=0, columnspan=2)
    # message line
    self.messageline = Tkinter.Message(self, relief=Tkinter.GROOVE)
    self.appGrid(self.messageline,
                 row=1,
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
    implementation of UI.TKI.GUItabView.fillCommandMenuItems
    """
    self.addCommandMenuItem(label="Custom", command=self.customCallback, enabled=True)
  # ---------------------------------------------------------------------------
  def customCallback(self):
    """Called when the Custom menu entry is selected"""
    self.notifyModelTask(["CUSTOM"])
  # ---------------------------------------------------------------------------
  def notifyStatus(self, status):
    """Generic callback when something changes in the model"""
    pass

# =============================================================================
class ModelTask(UTIL.TASK.ProcessingTask):
  """Only one task: the processing model"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """Initialise the Task as processing model"""
    UTIL.TASK.ProcessingTask.__init__(self, isParent=False)
  # ---------------------------------------------------------------------------
  def notifyCommand(self, argv):
    """Entry point for processing"""
    if len(argv) > 0:
      # decode the command
      cmd = argv[0].upper()
      if cmd == "D" or cmd == "DUMPCONFIGURATION":
        self.dumpConfigurationCmd(argv)
      elif cmd == "C" or cmd == "CUSTOM":
        self.customCmd(argv)
      else:
        # delegate to the parent implementation (help & quit command)
        return UTIL.TASK.ProcessingTask.notifyCommand(self, argv)
    return 0
  # ---------------------------------------------------------------------------
  def helpCmd(self, argv):
    """Decoded help command"""
    # overloaded from UTIL.TASK.ProcessingTask
    LOG_INFO("Available commands:")
    LOG("")
    LOG("h  | help ................provides this information")
    LOG("q  | quit ................terminates TEST application")
    LOG("d  | dumpConfiguration ...dumps the configuration")
    LOG("c  | custom ..............custom command, implemented in ModeTask")
    LOG("")
  # ---------------------------------------------------------------------------
  def dumpConfigurationCmd(self, argv):
    """Decoded dumpConfiguration command"""
    self.logMethod("dumpConfigurationCmd")
  # ---------------------------------------------------------------------------
  def customCmd(self, argv):
    """Decoded custom command"""
    LOG_INFO("This is the custom command")

########
# main #
########
if __name__ == "__main__":
  # initialise the system configuration
  initConfiguration()
  # initialise the console handler
  consoleHandler = UTIL.TASK.ConsoleHandler()
  # initialise the model and the GUI
  # keep the order: tasks must exist before the gui views are created
  UI.TKI.createGUI()
  guiTask = UI.TKI.GUItask()
  modelTask = ModelTask()
  tab0 = UI.TKI.createTab()
  gui0view = GUIview(tab0)
  UI.TKI.finaliseGUIcreation()
  # register the console handler
  modelTask.registerConsoleHandler(consoleHandler)
  # start the tasks
  print("start modelTask...")
  modelTask.start()
  print("start guiTask...")
  guiTask.start()
  print("guiTask terminated")
  modelTask.join()
  print("modelTask terminated")
