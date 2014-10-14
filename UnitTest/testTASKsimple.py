#!/usr/bin/env python
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
# TASK framework - Unit Test: empty Model Task with default behaviour         *
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
      if cmd == "H" or cmd == "HELP":
        self.helpCmd(argv)
      elif cmd == "Q" or cmd == "QUIT":
        self.quitCmd(argv)
      else:
        LOG_WARNING("invalid command " + argv[0])
        self.helpCmd([])
    return 0
  # ---------------------------------------------------------------------------
  def helpCmd(self, argv):
    """Decoded help command"""
    LOG_INFO("Available commands:")
    LOG("")
    LOG("h  | help ...provides this information")
    LOG("q  | quit ...terminates TEST application")
    LOG("")
  # ---------------------------------------------------------------------------
  def quitCmd(self, argv):
    """Decoded quit command"""
    UTIL.TASK.s_parentTask.stop()

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
