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
# Ground Simulation - Unit Tests                                              *
#******************************************************************************
from __future__ import print_function
import sys
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import UTIL.SYS, UTIL.TASK
import GRND.NCTRS
import testData

####################
# global variables #
####################
# TM sender is a singleton
s_tmSender = None

###########
# classes #
###########
# =============================================================================
class ModelTask(UTIL.TASK.ProcessingTask):
  """Subclass of UTIL.TASK.ProcessingTask"""
  def __init__(self):
    """Initialise attributes only"""
    UTIL.TASK.ProcessingTask.__init__(self, isParent=True)
  # ---------------------------------------------------------------------------
  def notifyCommand(self, argv, extraData):
    """Callback for processing the input arguments"""
    if len(argv) > 0:
      # decode the command
      cmd = argv[0].upper()
      if cmd == "H" or cmd == "HELP":
        self.helpCmd(argv)
      elif cmd == "Q" or cmd == "QUIT":
        self.quitCmd(argv)
      elif cmd == "F" or cmd == "FRAME1":
        self.frame1Cmd(argv)
      elif cmd == "V" or cmd == "FRAME2":
        self.frame2Cmd(argv)
      else:
        LOG_WARNING("Invalid command " + argv[0])
        self.helpCmd([])
    return 0
  # ---------------------------------------------------------------------------
  def helpCmd(self, argv):
    """Decoded help command"""
    LOG("Available commands:")
    LOG("-------------------")
    LOG("")
    LOG("h | help .....provides this information")
    LOG("q | quit .....terminates the application")
    LOG("f | frame1 ...send TM frame via NCTRS TM frame")
    LOG("v | frame2 ...send NCTRS TM frame")
    LOG("")
  # ---------------------------------------------------------------------------
  def quitCmd(self, argv):
    """Decoded quit command"""
    UTIL.TASK.s_parentTask.stop()
  # ---------------------------------------------------------------------------
  def frame1Cmd(self, argv):
    """Decoded frame1 command"""
    global s_tmSender
    frame = testData.TM_FRAME_01
    tmDu = GRND.NCTRSDU.TMdataUnit()
    tmDu.setFrame(frame)
    tmDu.spacecraftId = testData.NCTRS_TM_FRAME_01_spacecraftId
    tmDu.dataStreamType = testData.NCTRS_TM_FRAME_01_dataStreamType
    tmDu.virtualChannelId = testData.NCTRS_TM_FRAME_01_virtualChannelId
    tmDu.routeId = testData.NCTRS_TM_FRAME_01_routeId
    tmDu.earthReceptionTime = testData.NCTRS_TM_FRAME_01_earthReceptionTime
    tmDu.sequenceFlag = testData.NCTRS_TM_FRAME_01_sequenceFlag
    tmDu.qualityFlag = testData.NCTRS_TM_FRAME_01_qualityFlag
    print("tmDu =", tmDu)
    s_tmSender.sendTmDataUnit(tmDu)
  # ---------------------------------------------------------------------------
  def frame2Cmd(self, argv):
    """Decoded frame2 command"""
    frame = testData.TM_FRAME_01
    s_tmSender.sendFrame(frame)

# =============================================================================
class TMsender(GRND.NCTRS.TMsender):
  """Subclass of GRND.NCTRS.TMsender"""
  def __init__(self, portNr, nctrsTMfields):
    """Initialise attributes only"""
    GRND.NCTRS.TMsender.__init__(self, portNr, nctrsTMfields)
  # ---------------------------------------------------------------------------
  def clientAccepted(self):
    LOG_INFO("NCTRS TM receiver (client) accepted")

#############
# functions #
#############
# -----------------------------------------------------------------------------
def initConfiguration():
  """initialise the system configuration"""
  UTIL.SYS.s_configuration.setDefaults([
    ["SYS_COLOR_LOG", "1"],
    ["HOST", "127.0.0.1"],
    ["NCTRS_TM_SERVER_PORT", "2502"],
    ["NCTRS_TM_DU_VERSION", "V0"],
    ["SPACECRAFT_ID", "758"]])
# -----------------------------------------------------------------------------
def createTMsender():
  """create the NCTRS TM sender"""
  global s_tmSender
  nctrsTMfields = GRND.NCTRS.NCTRStmFields()
  nctrsTMfields.spacecraftId = int(UTIL.SYS.s_configuration.SPACECRAFT_ID)
  s_tmSender = TMsender(
    portNr=int(UTIL.SYS.s_configuration.NCTRS_TM_SERVER_PORT),
    nctrsTMfields=nctrsTMfields)
  if not s_tmSender.openConnectPort(UTIL.SYS.s_configuration.HOST):
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
  # create the NCTRS TM sender
  LOG("Open the NCTRS TM sender (server)")
  createTMsender()
  # start the tasks
  LOG("start modelTask...")
  modelTask.start()
