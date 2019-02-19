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
# Ground Simulation - Unit Tests                                              *
#******************************************************************************
import sys
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import UTIL.SYS, UTIL.TASK
import GRND.NCTRS, GRND.NCTRSDU, GRND.NCTRSDUhelpers
import testData

####################
# global variables #
####################
# TM receiver is a singletons
s_tmReceiver = None

###########
# classes #
###########
# =============================================================================
class TMreceiver(GRND.NCTRS.TMreceiver):
  """Subclass of GRND.NCTRS.TMreceiver"""
  def __init__(self):
    """Initialise attributes only"""
    GRND.NCTRS.TMreceiver.__init__(self)
  # ---------------------------------------------------------------------------
  def notifyTMdataUnit(self, tmDu):
    """TM frame received"""
    LOG_INFO("notifyTMdataUnit")
    LOG("tmDu = " + str(tmDu))
  # ---------------------------------------------------------------------------
  def notifyError(self, errorMessage, data):
    """error notification"""
    LOG_ERROR(errorMessage)
    LOG(str(data))

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
    ["NCTRS_TM_DU_VERSION", "V0"]])
# -----------------------------------------------------------------------------
def createTMreceiver():
  """create the NCTRS TM receiver"""
  global s_tmReceiver
  s_tmReceiver = TMreceiver()
  if not s_tmReceiver.connectToServer(
    serverHost=UTIL.SYS.s_configuration.HOST,
    serverPort=int(UTIL.SYS.s_configuration.NCTRS_TM_SERVER_PORT)):
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
  modelTask = UTIL.TASK.ProcessingTask(isParent=True)
  # register the console handler
  modelTask.registerConsoleHandler(consoleHandler)
  # create the NCTRS TM receiver
  LOG("Open the NCTRS TM receiver (client)")
  createTMreceiver()
  # start the tasks
  LOG("start modelTask...")
  modelTask.start()
