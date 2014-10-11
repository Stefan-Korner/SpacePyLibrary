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
# EGSE interfaces - Unit Tests                                                *
#******************************************************************************
import sys
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import UTIL.SYS
import EGSE.EDEN

###########
# classes #
###########
# =============================================================================
class ConsoleHandler(UTIL.SYS.ConsoleHandler):
  """Subclass of UTIL.SYS.ConsoleHandler"""
  def __init__(self, server):
    """Initialise attributes only"""
    UTIL.SYS.ConsoleHandler.__init__(self)
    self.server = server
  # ---------------------------------------------------------------------------
  def process(self, argv):
    """Callback for processing the input arguments"""
    if len(argv) > 0:
      # decode the command
      cmd = argv[0].upper()
      if cmd == "H" or cmd == "HELP":
        self.helpCmd(argv)
      elif cmd == "Q" or cmd == "QUIT":
        self.quitCmd(argv)
      elif cmd == "P" or cmd == "PACKETRESPONSE":
        self.packetResponseCmd(argv)
      else:
        LOG_WARNING("Invalid command " + argv[0])
    print "> ",
  # ---------------------------------------------------------------------------
  def helpCmd(self, argv):
    """Decoded help command"""
    LOG("Available commands:")
    LOG("-------------------")
    LOG("")
    LOG("h | help .............provides this information")
    LOG("q | quit .............terminates the application")
    LOG("p | packetresponse ...send NCTRS TC packet response")
    LOG("")
  # ---------------------------------------------------------------------------
  def quitCmd(self, argv):
    """Decoded quit command"""
    UTIL.SYS.s_eventLoop.stop()
  # ---------------------------------------------------------------------------
  def packetResponseCmd(self, argv):
    """Decoded packet response command"""
    tcPktRespDu = EGSE.EDEN.TCpacketResponseDataUnit()
    self.server.sendTcDataUnit(tcPktRespDu)

# =============================================================================
class Server(EGSE.EDEN.Server):
  """Subclass of EGSE.EDEN.Server"""
  def __init__(self, eventLoop, portNr):
    """Initialise attributes only"""
    EGSE.EDEN.Server.__init__(self, eventLoop, portNr)
  # ---------------------------------------------------------------------------
  def clientAccepted(self):
    LOG_INFO("Client accepted")
  # ---------------------------------------------------------------------------
  def notifyTCpacketDataUnit(self, tcPktDu):
    """AD packet / BD segment received"""
    #LOG_INFO("notifyTCpacketDataUnit")
    #LOG("tcPktDu = " + str(tcPktDu))
    #GRND.NCTRS.TCreceiver.notifyTCpacketDataUnit(self, tcCltuDu)
    sys.exit(-1)
  # ---------------------------------------------------------------------------
  def notifyError(self, errorMessage, data):
    """error notification"""
    LOG_ERROR(errorMessage)
    LOG(str(data))
  # ---------------------------------------------------------------------------
  def notifyTCpacket(self, tcPacketDu):
    """TC packet received"""
    #LOG("- notifyTCpacket")
    #LOG("  APID =    " + str(tcPacketDu.applicationProcessId))
    #LOG("  TYPE =    " + str(tcPacketDu.serviceType))
    #LOG("  SUBTYPE = " + str(tcPacketDu.serviceSubType))
    #LOG("  SSC =     " + str(tcPacketDu.sequenceControlCount))
    sys.exit(-1)

#############
# functions #
#############
# -----------------------------------------------------------------------------
def initConfiguration():
  """initialise the system configuration"""
  UTIL.SYS.s_configuration.setDefaults([
    ["SYS_COLOR_LOG", "1"],
    ["EDEN_SERVER_PORT", "13007"]])
# -----------------------------------------------------------------------------
def createServer():
  """create the EDEN server"""
  server = Server(
    UTIL.SYS.s_eventLoop,
    portNr=int(UTIL.SYS.s_configuration.EDEN_SERVER_PORT))
  if not server.openConnectPort():
    sys.exit(-1)
  return server

########
# main #
########
if __name__ == "__main__":
  # initialise the system configuration
  initConfiguration()
  # create the EDEN server
  LOG("Open the EDEN server")
  server = createServer()
  # register a console handler for interaction
  consoleHandler = ConsoleHandler(server)
  # start the event loop
  LOG("Start the event loop...")
  consoleHandler.process([])
  UTIL.SYS.s_eventLoop.start()
  sys.exit(0)
