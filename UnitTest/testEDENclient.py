#!/usr/bin/env python
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
import testData

####################
# global variables #
####################
# EDEN client is a singleton
s_client = None

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
      elif cmd == "1" or cmd == "TC_SPACE":
        self.tcSpaceCmd(argv)
      elif cmd == "2" or cmd == "TC_SCOE":
        self.tcScoeCmd(argv)
      elif cmd == "3" or cmd == "CMD_EXEC":
        self.cmdExecCmd(argv)
      else:
        LOG_WARNING("Invalid command " + argv[0])
    return 0
  # ---------------------------------------------------------------------------
  def helpCmd(self, argv):
    """Decoded help command"""
    LOG("Available commands:")
    LOG("-------------------")
    LOG("")
    LOG("h | help .......provides this information")
    LOG("q | quit .......terminates the application")
    LOG("1 | tc_space ...send TC via EDEN (TC,SPACE)")
    LOG("2 | tc_scoe ....send TC via EDEN (TC,SCOE)")
    LOG("3 | cmd_exec ...send message via EDEN (CMD,EXEC)")
    LOG("")
  # ---------------------------------------------------------------------------
  def quitCmd(self, argv):
    """Decoded quit command"""
    UTIL.TASK.s_parentTask.stop()
  # ---------------------------------------------------------------------------
  def tcSpaceCmd(self, argv):
    """Decoded (TC,SPACE) command"""
    global s_client
    if len(argv) != 1:
      LOG_WARNING("Invalid command argument(s)")
      LOG("usage: tc_space")
      LOG("or:    1")
      return
    s_client.sendTcSpace(testData.TC_PACKET_01)
  # ---------------------------------------------------------------------------
  def tcScoeCmd(self, argv):
    """Decoded (TC,SCOE) command"""
    global s_client
    if len(argv) != 1:
      LOG_WARNING("Invalid command argument(s)")
      LOG("usage: tc_scoe")
      LOG("or:    2")
      return
    s_client.sendTcScoe(testData.TC_PACKET_01)
  # ---------------------------------------------------------------------------
  def cmdExecCmd(self, argv):
    """Decoded (CMD,EXEC) command"""
    global s_client
    if len(argv) != 2:
      LOG_WARNING("Invalid command argument(s)")
      LOG("usage: cmd_exec <message>")
      LOG("or:    3 <message>")
      return
    message = argv[1]
    s_client.sendCmdExec(message)

# =============================================================================
class Client(EGSE.EDEN.Client):
  """Subclass of EGSE.EDEN.Client"""
  def __init__(self):
    """Initialise attributes only"""
    EGSE.EDEN.Client.__init__(self)

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
def createClient():
  """create the EDEN client"""
  global s_client
  s_client = Client()
  if not s_client.connectToServer(
    serverHost=UTIL.SYS.s_configuration.HOST,
    serverPort=int(UTIL.SYS.s_configuration.CCS_SERVER_PORT)):
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
  # create the EDEN client
  LOG("Open the EDEN client")
  createClient()
  # start the tasks
  LOG("start modelTask...")
  modelTask.start()
