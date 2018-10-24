#!/usr/bin/env python3
#******************************************************************************
# (C) 2014, Stefan Korner, Austria                                            *
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
# EGSE interfaces - Unit Tests                                                *
#******************************************************************************
import sys
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import EGSE.EDEN
import UTIL.SYS, UTIL.TASK

####################
# global variables #
####################
# EDEN server is a singleton
s_server = None

###########
# classes #
###########
# =============================================================================
class ModelTask(UTIL.TASK.ProcessingTask):
  """Subclass of UTIL.SYS.ConsoleHandler"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """Initialise attributes only"""
    UTIL.TASK.ProcessingTask.__init__(self, isParent=True)
  # ---------------------------------------------------------------------------
  def notifyCommand(self, argv):
    """Callback for processing the input arguments"""
    if len(argv) > 0:
      # decode the command
      cmd = argv[0].upper()
      if cmd == "H" or cmd == "HELP":
        self.helpCmd(argv)
      elif cmd == "Q" or cmd == "QUIT":
        self.quitCmd(argv)
      elif cmd == "1" or cmd == "CMD_ANSW":
        self.cmdAnswCmd(argv)
      else:
        LOG_WARNING("Invalid command " + argv[0])
        self.helpCmd([])
    return 0
  # ---------------------------------------------------------------------------
  def helpCmd(self, argv):
    """Decoded help command"""
    LOG_INFO("Available commands:")
    LOG("")
    LOG("h | help .......provides this information")
    LOG("q | quit .......terminates the application")
    LOG("1 | cmd_answ ...send message via EDEN (CMD,ANSW)")
    LOG("")
  # ---------------------------------------------------------------------------
  def quitCmd(self, argv):
    """Decoded quit command"""
    UTIL.TASK.s_parentTask.stop()
  # ---------------------------------------------------------------------------
  def cmdAnswCmd(self, argv):
    """Decoded (CMD,ANSW) command"""
    global s_client
    if len(argv) != 2:
      LOG_WARNING("Invalid command argument(s)")
      LOG("usage: cmd_answ <message>")
      LOG("or:    1 <message>")
      return
    message = argv[1]
    s_server.sendCmdAnsw(message)

# =============================================================================
class Server(EGSE.EDEN.Server):
  """Subclass of EGSE.EDEN.Server"""
  # ---------------------------------------------------------------------------
  def __init__(self, portNr):
    """Initialise attributes only"""
    EGSE.EDEN.Server.__init__(self, portNr)
  # ---------------------------------------------------------------------------
  def clientAccepted(self):
    LOG_INFO("Client accepted")

#############
# functions #
#############
# -----------------------------------------------------------------------------
def initConfiguration():
  """initialise the system configuration"""
  UTIL.SYS.s_configuration.setDefaults([
    ["HOST", "127.0.0.1"],
    ["CCS_SERVER_PORT", "48569"]])
# -----------------------------------------------------------------------------
def createServer():
  """create the EDEN server"""
  global s_server
  s_server = Server(portNr=int(UTIL.SYS.s_configuration.CCS_SERVER_PORT))
  if not s_server.openConnectPort(UTIL.SYS.s_configuration.HOST):
    sys.exit(-1)

########
# main #
########
if __name__ == "__main__":
  # initialise the system configuration
  initConfiguration()
  # initialise the console handler
  consoleHandler = UTIL.TASK.ConsoleHandler()
  # initialise the model
  modelTask = ModelTask()
  # register the console handler
  modelTask.registerConsoleHandler(consoleHandler)
  # create the EDEN server
  LOG("Open the EDEN server")
  createServer()
  # start the tasks
  LOG("start modelTask...")
  modelTask.start()
