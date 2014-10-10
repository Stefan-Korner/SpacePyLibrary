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
from GDP.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import GDP.SYS
import EGSE.EDEN
import testData

###########
# classes #
###########
# =============================================================================
class ConsoleHandler(GDP.SYS.ConsoleHandler):
  """Subclass of GDP.SYS.ConsoleHandler"""
  def __init__(self, client):
    """Initialise attributes only"""
    GDP.SYS.ConsoleHandler.__init__(self)
    self.client = client
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
      elif cmd == "P" or cmd == "PACKET1":
        self.packet1Cmd(argv)
      elif cmd == "B" or cmd == "PACKET2":
        self.packet2Cmd(argv)
      else:
        LOG_WARNING("Invalid command " + argv[0])
    print "> ",
  # ---------------------------------------------------------------------------
  def helpCmd(self, argv):
    """Decoded help command"""
    LOG("Available commands:")
    LOG("-------------------")
    LOG("")
    LOG("h | help ........provides this information")
    LOG("q | quit ........terminates the application")
    LOG("p | packet1 .....send TC packet via EDEN TC SCOE DU")
    LOG("b | packet2 .....send TC packet via EDEN TC SPACE DU")
    LOG("")
  # ---------------------------------------------------------------------------
  def quitCmd(self, argv):
    """Decoded quit command"""
    GDP.SYS.s_eventLoop.stop()
  # ---------------------------------------------------------------------------
  def packet1Cmd(self, argv):
    """Decoded packet1 command"""
    tcPktDu = GRND.NCTRSDU.TCpacketDataUnit()
    print "tcPktDu =", tcPktDu
    self.client.sendTcDataUnit(tcPktDu)
  # ---------------------------------------------------------------------------
  def packet2Cmd(self, argv):
    """Decoded packet2 command"""
    LOG_WARNING("Command not implemented: " + argv[0])

# =============================================================================
class Client(EGSE.EDEN.Client):
  """Subclass of EGSE.EDEN.Client"""
  def __init__(self, eventLoop):
    """Initialise attributes only"""
    EGSE.EDEN.Client.__init__(self, eventLoop)
  # ---------------------------------------------------------------------------
  def notifyTCpacketResponseDataUnit(self, tcPktRespDu):
    """AD packet / BD segment response received"""
    #LOG("")
    #LOG("*** notifyTCpacketResponseDataUnit ***")
    #LOG("tcPktRespDu.acknowledgement = " +
    #         GRND.NCTRSDUhelpers.ackStr(tcPktRespDu.acknowledgement))
    #LOG("tcPktRespDu = " + str(tcPktRespDu))
	sys.exit(-1)

#############
# functions #
#############
# -----------------------------------------------------------------------------
def initConfiguration():
  """initialise the system configuration"""
  GDP.SYS.s_configuration.setDefaults([
    ["SYS_COLOR_LOG", "1"],
    ["HOST", "10.0.0.100"],
    #["HOST", "192.168.178.46"],
    ["EDEN_SERVER_PORT", "13007"]])
# -----------------------------------------------------------------------------
def createClient():
  """create the EDEN client"""
  client = Client(GDP.SYS.s_eventLoop)
  if not client.connectToServer(
    serverHost=GDP.SYS.s_configuration.HOST,
    serverPort=int(GDP.SYS.s_configuration.EDEN_SERVER_PORT)):
    sys.exit(-1)
  return client

########
# main #
########
if __name__ == "__main__":
  # initialise the system configuration
  initConfiguration()
  # create the EDEN client
  LOG("Open the EDEN client")
  client = createClient()
  # register a console handler for interaction
  consoleHandler = ConsoleHandler(client)
  # start the event loop
  LOG("Start the event loop...")
  consoleHandler.process([])
  GDP.SYS.s_eventLoop.start()
  sys.exit(0)
