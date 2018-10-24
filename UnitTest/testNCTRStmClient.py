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
# Ground Simulation - Unit Tests                                              *
#******************************************************************************
import sys
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import UTIL.SYS
import GRND.NCTRS, GRND.NCTRSDU, GRND.NCTRSDUhelpers
import testData

###########
# classes #
###########
# =============================================================================
class TMreceiver(GRND.NCTRS.TMreceiver):
  """Subclass of GRND.NCTRS.TMreceiver"""
  def __init__(self, eventLoop):
    """Initialise attributes only"""
    GRND.NCTRS.TMreceiver.__init__(self, eventLoop)
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
    ["HOST", "10.0.0.100"],
    #["HOST", "192.168.178.46"],
    ["NCTRS_TM_SERVER_PORT", "2502"]])
# -----------------------------------------------------------------------------
def createTMreceiver():
  """create the NCTRS TM receiver"""
  tmReceiver = TMreceiver(UTIL.SYS.s_eventLoop)
  if not tmReceiver.connectToServer(
    serverHost=UTIL.SYS.s_configuration.HOST,
    serverPort=int(UTIL.SYS.s_configuration.NCTRS_TM_SERVER_PORT)):
    sys.exit(-1)
  return tmReceiver

########
# main #
########
if __name__ == "__main__":
  # initialise the system configuration
  initConfiguration()
  # create the NCTRS TM receiver
  LOG("Open the NCTRS TM receiver (client)")
  tmReceiver = createTMreceiver()
  # register a console handler for termination
  consoleHandler = UTIL.SYS.ConsoleHandler()
  # start the event loop
  LOG("Start the event loop...")
  UTIL.SYS.s_eventLoop.start()
  sys.exit(0)
