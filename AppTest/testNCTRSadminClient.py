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
import GRND.NCTRS, GRND.NCTRSDU

####################
# global variables #
####################
# Admin receiver is a singletons
s_adminReceiver = None

###########
# classes #
###########
# =============================================================================
class AdminReceiver(GRND.NCTRS.AdminMessageReceiver):
  """Subclass of GRND.NCTRS.AdminMessageReceiver"""
  def __init__(self):
    """Initialise attributes only"""
    GRND.NCTRS.AdminMessageReceiver.__init__(self)
  # ---------------------------------------------------------------------------
  def notifyAdminMessageDataUnit(self, messageDu):
    """Admin message response received"""
    LOG("")
    LOG("*** notifyAdminMessageDataUnit ***")
    LOG("message = " + messageDu.getMessage())
    LOG("messageDu = " + str(messageDu))

#############
# functions #
#############
# -----------------------------------------------------------------------------
def initConfiguration():
  """initialise the system configuration"""
  UTIL.SYS.s_configuration.setDefaults([
    ["SYS_COLOR_LOG", "1"],
    ["HOST", "127.0.0.1"],
    ["NCTRS_ADMIN_SERVER_PORT", "13006"]])
# -----------------------------------------------------------------------------
def createAdminReceiver():
  """create the NCTRS admin receiver"""
  global s_adminReceiver
  s_adminReceiver = AdminReceiver()
  if not s_adminReceiver.connectToServer(
    serverHost=UTIL.SYS.s_configuration.HOST,
    serverPort=int(UTIL.SYS.s_configuration.NCTRS_ADMIN_SERVER_PORT)):
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
  # create the NCTRS admin receiver
  LOG("Open the NCTRS admin receiver (client)")
  createAdminReceiver()
  # start the tasks
  LOG("start modelTask...")
  modelTask.start()
