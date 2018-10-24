#!/usr/bin/env python3
#******************************************************************************
# (C) 2017, Stefan Korner, Austria                                            *
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
import EGSE.CNC
import UTIL.SYS, UTIL.TASK
import testData

####################
# global variables #
####################
# CNC clients are singletons
s_client = None
s_client2 = None

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
      elif cmd == "1" or cmd == "CNC_COMMAND":
        self.cncCommand(argv)
      else:
        LOG_WARNING("Invalid command " + argv[0])
    return 0
  # ---------------------------------------------------------------------------
  def helpCmd(self, argv):
    """Decoded help command"""
    LOG("Available commands:")
    LOG("-------------------")
    LOG("")
    LOG("h | help ..........provides this information")
    LOG("q | quit ..........terminates the application")
    LOG("1 | cnc_command ...send TC via CNC (TC,SPACE)")
    LOG("")
  # ---------------------------------------------------------------------------
  def quitCmd(self, argv):
    """Decoded quit command"""
    UTIL.TASK.s_parentTask.stop()
  # ---------------------------------------------------------------------------
  def cncCommand(self, argv):
    """CnC command"""
    global s_client
    if len(argv) != 2:
      LOG_WARNING("Invalid command argument(s)")
      LOG("usage: cnc_command <message>")
      LOG("or:    1 <message>")
      return
    message = argv[1]
    cncTCpacketDU = EGSE.CNCPDU.TCpacket()
    cncTCpacketDU.applicationProcessId = 1234
    cncTCpacketDU.setCNCmessage(message)
    s_client.sendCNCpacket(cncTCpacketDU)

# =============================================================================
class TCclient(EGSE.CNC.TCclient):
  """Subclass of EGSE.CNC.TCclient"""
  def __init__(self):
    """Initialise attributes only"""
    EGSE.CNC.TCclient.__init__(self)

# =============================================================================
class TMclient(EGSE.CNC.TMclient):
  """Subclass of EGSE.CNC.TMclient"""
  def __init__(self):
    """Initialise attributes only"""
    EGSE.CNC.TMclient.__init__(self)

#############
# functions #
#############
# -----------------------------------------------------------------------------
def initConfiguration():
  """initialise the system configuration"""
  UTIL.SYS.s_configuration.setDefaults([
    ["HOST", "127.0.0.1"],
    ["CCS_SERVER_PORT", "48569"],
    ["CCS_SERVER_PORT2", "48570"]])
# -----------------------------------------------------------------------------
def createClients():
  """create the CNC clients"""
  global s_client, s_client2
  s_client = TCclient()
  if not s_client.connectToServer(
    serverHost=UTIL.SYS.s_configuration.HOST,
    serverPort=int(UTIL.SYS.s_configuration.CCS_SERVER_PORT)):
    sys.exit(-1)
  s_client2 = TMclient()
  if not s_client2.connectToServer(
    serverHost=UTIL.SYS.s_configuration.HOST,
    serverPort=int(UTIL.SYS.s_configuration.CCS_SERVER_PORT2)):
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
  # create the CNC clients
  LOG("Open the CNC clients")
  createClients()
  # start the tasks
  LOG("start modelTask...")
  modelTask.start()
