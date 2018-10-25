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
# TASK framework - Unit Test: customized Model Task with specifc behaviour    *
#******************************************************************************
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import UTIL.TASK

###########
# classes #
###########
# =============================================================================
class ModelTask(UTIL.TASK.ProcessingTask):
  """Only one task: the processing model"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """Initialise the Task as processing model"""
    UTIL.TASK.ProcessingTask.__init__(self, isParent=True)
  # ---------------------------------------------------------------------------
  def notifyCommand(self, argv):
    """Entry point for processing"""
    if len(argv) > 0:
      # decode the command
      cmd = argv[0].upper()
      if cmd == "C" or cmd == "CUSTOM":
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
    LOG("h  | help .....provides this information")
    LOG("q  | quit .....terminates TEST application")
    LOG("c  | custom ...custom command, implemented in ModeTask")
    LOG("")
  # ---------------------------------------------------------------------------
  def customCmd(self, argv):
    """Decoded custom command"""
    LOG_INFO("This is the custom command")

########
# main #
########
if __name__ == "__main__":
  # initialise the console handler
  consoleHandler = UTIL.TASK.ConsoleHandler()
  # initialise the model
  modelTask = ModelTask()
  # register the console handler
  modelTask.registerConsoleHandler(consoleHandler)
  # start the tasks
  LOG("start modelTask...")
  modelTask.start()
