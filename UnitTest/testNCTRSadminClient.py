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
# Ground Simulation - Unit Tests                                              *
#******************************************************************************
import sys
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import UTIL.SYS
import GRND.NCTRS, GRND.NCTRSDU

###########
# classes #
###########
# =============================================================================
class ConsoleHandler(UTIL.SYS.ConsoleHandler):
  """Subclass of UTIL.SYS.ConsoleHandler"""
  def __init__(self):
    """Initialise attributes only"""
    UTIL.SYS.ConsoleHandler.__init__(self)
  # ---------------------------------------------------------------------------
  def process(self, argv):
    """Callback for processing the input arguments"""
    UTIL.SYS.s_eventLoop.stop()

# =============================================================================
class AdminReceiver(GRND.NCTRS.AdminMessageReceiver):
  """Subclass of GRND.NCTRS.AdminMessageReceiver"""
  def __init__(self, eventLoop):
    """Initialise attributes only"""
    GRND.NCTRS.AdminMessageReceiver.__init__(self, eventLoop)
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
    ["HOST", "10.0.0.100"],
    #["HOST", "192.168.178.46"],
    ["NCTRS_ADMIN_SERVER_PORT", "13006"]])
# -----------------------------------------------------------------------------
def createAdminReceiver():
  """create the NCTRS admin receiver"""
  adminReceiver = AdminReceiver(UTIL.SYS.s_eventLoop)
  if not adminReceiver.connectToServer(
    serverHost=UTIL.SYS.s_configuration.HOST,
    serverPort=int(UTIL.SYS.s_configuration.NCTRS_ADMIN_SERVER_PORT)):
    sys.exit(-1)
  return adminReceiver

########
# main #
########
if __name__ == "__main__":
  # initialise the system configuration
  initConfiguration()
  # create the NCTRS admin receiver
  LOG("Open the NCTRS admin receiver (client)")
  adminReceiver = createAdminReceiver()
  # register a console handler for interaction
  consoleHandler = ConsoleHandler()
  # start the event loop
  LOG("Start the event loop...")
  consoleHandler.process([])
  UTIL.SYS.s_eventLoop.start()
  sys.exit(0)
