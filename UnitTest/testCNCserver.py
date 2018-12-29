#!/usr/bin/env python3
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
# EGSE interfaces - Unit Tests                                                *
#******************************************************************************
import sys
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import CCSDS.PACKET
import EGSE.CNC
import UTIL.SYS, UTIL.TASK
import testData

####################
# global variables #
####################
# CNC servers are singletons
s_server = None
s_server2 = None

###########
# classes #
###########
# =============================================================================
class ModelTask(UTIL.TASK.ProcessingTask):
  """Subclass of UTIL.TASK.ProcessingTask"""
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
      elif cmd == "1" or cmd == "TM_PKT":
        self.tmPktCmd(argv)
      else:
        LOG_WARNING("Invalid command " + argv[0])
        self.helpCmd([])
    return 0
  # ---------------------------------------------------------------------------
  def helpCmd(self, argv):
    """Decoded help command"""
    LOG_INFO("Available commands:")
    LOG("")
    LOG("h | help .....provides this information")
    LOG("q | quit .....terminates the application")
    LOG("1 | tm_pkt ...send a CCSDS TM packet")
    LOG("")
  # ---------------------------------------------------------------------------
  def quitCmd(self, argv):
    """Decoded quit command"""
    UTIL.TASK.s_parentTask.stop()
  # ---------------------------------------------------------------------------
  def tmPktCmd(self, argv):
    """Decoded TM-packet command"""
    global s_client1
    if len(argv) != 1:
      LOG_WARNING("Invalid command argument(s)")
      LOG("usage: tm_pkt")
      LOG("or:    1")
      return
    tmPacketDU = CCSDS.PACKET.TMpacket(testData.TM_PACKET_01)
    s_server2.sendTMpacket(tmPacketDU.getBufferString())

# =============================================================================
class TCserver(EGSE.CNC.TCserver):
  """Subclass of EGSE.CNC.TCserver"""
  # ---------------------------------------------------------------------------
  def __init__(self, portNr):
    """Initialise attributes only"""
    EGSE.CNC.TCserver.__init__(self, portNr)
  # ---------------------------------------------------------------------------
  def clientAccepted(self):
    LOG_INFO("Client accepted")

# =============================================================================
class TMserver(EGSE.CNC.TMserver):
  """Subclass of EGSE.CNC.TMserver"""
  # ---------------------------------------------------------------------------
  def __init__(self, portNr):
    """Initialise attributes only"""
    EGSE.CNC.TMserver.__init__(self, portNr)
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
    ["CCS_SERVER_PORT", "48569"],
    ["CCS_SERVER_PORT2", "48570"]])
# -----------------------------------------------------------------------------
def createServers():
  """create the CNC servers"""
  global s_server, s_server2
  s_server = TCserver(portNr=int(UTIL.SYS.s_configuration.CCS_SERVER_PORT))
  if not s_server.openConnectPort(UTIL.SYS.s_configuration.HOST):
    sys.exit(-1)
  s_server2 = TMserver(portNr=int(UTIL.SYS.s_configuration.CCS_SERVER_PORT2))
  if not s_server2.openConnectPort(UTIL.SYS.s_configuration.HOST):
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
  # create the CNC servers
  LOG("Open the CNC servers")
  createServers()
  # start the tasks
  LOG("start modelTask...")
  modelTask.start()
