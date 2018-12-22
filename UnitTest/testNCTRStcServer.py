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
import UTIL.SYS
import GRND.NCTRS
import CCSDS.SEGMENThelpers

###########
# classes #
###########
# =============================================================================
class ConsoleHandler(UTIL.SYS.ConsoleHandler):
  """Subclass of UTIL.SYS.ConsoleHandler"""
  def __init__(self, tcReceiver):
    """Initialise attributes only"""
    UTIL.SYS.ConsoleHandler.__init__(self)
    self.tcReceiver = tcReceiver
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
      elif cmd == "C" or cmd == "CLTURESPONSE":
        self.cltuResponseCmd(argv)
      elif cmd == "L" or cmd == "LINKSTATUS":
        self.linkStatusCmd(argv)
      else:
        LOG_WARNING("Invalid command " + argv[0])
    print("> ",  end='')
  # ---------------------------------------------------------------------------
  def helpCmd(self, argv):
    """Decoded help command"""
    LOG("Available commands:")
    LOG("-------------------")
    LOG("")
    LOG("h | help .............provides this information")
    LOG("q | quit .............terminates the application")
    LOG("p | packetresponse ...send NCTRS TC packet response")
    LOG("c | clturesponse .....send NCTRS TC CLTU response")
    LOG("l | linkstatus .......send NCTRS TC link status")
    LOG("")
  # ---------------------------------------------------------------------------
  def quitCmd(self, argv):
    """Decoded quit command"""
    UTIL.SYS.s_eventLoop.stop()
  # ---------------------------------------------------------------------------
  def packetResponseCmd(self, argv):
    """Decoded packet response command"""
    tcPktRespDu = GRND.NCTRSDU.TCpacketResponseDataUnit()
    self.tcReceiver.sendTcDataUnit(tcPktRespDu)
  # ---------------------------------------------------------------------------
  def cltuResponseCmd(self, argv):
    """Decoded cltu response command"""
    tcCltuRespDu = GRND.NCTRSDU.TCcltuResponseDataUnit()
    self.tcReceiver.sendTcDataUnit(tcCltuRespDu)
  # ---------------------------------------------------------------------------
  def linkStatusCmd(self, argv):
    """Decoded link status command"""
    tcLinkStatDu = GRND.NCTRSDU.TClinkStatusDataUnit()
    self.tcReceiver.sendTcDataUnit(tcLinkStatDu)

# =============================================================================
class TCreceiver(GRND.NCTRS.TCreceiver):
  """Subclass of GRND.NCTRS.TCreceiver"""
  def __init__(self, eventLoop, portNr, groundstationId):
    """Initialise attributes only"""
    GRND.NCTRS.TCreceiver.__init__(self, eventLoop, portNr, groundstationId)
  # ---------------------------------------------------------------------------
  def clientAccepted(self):
    LOG_INFO("NCTRS TC sender (client) accepted")
  # ---------------------------------------------------------------------------
  def notifyTCpacketDataUnit(self, tcPktDu):
    """AD packet / BD segment received"""
    LOG_INFO("notifyTCpacketDataUnit")
    LOG("tcPktDu = " + str(tcPktDu))
    GRND.NCTRS.TCreceiver.notifyTCpacketDataUnit(self, tcCltuDu)
  # ---------------------------------------------------------------------------
  def notifyTCcltuDataUnit(self, tcCltuDu):
    """CLTU received"""
    LOG_INFO("notifyTCcltuDataUnit")
    GRND.NCTRS.TCreceiver.notifyTCcltuDataUnit(self, tcCltuDu)
  # ---------------------------------------------------------------------------
  def notifyTCdirectivesDataUnit(self, tcDirDu):
    """COP1 directive received"""
    LOG_INFO("notifyTCdirectivesDataUnit")
    LOG("tcDirDu = " + str(tcDirDu))
  # ---------------------------------------------------------------------------
  def notifyError(self, errorMessage, data):
    """error notification"""
    LOG_ERROR(errorMessage)
    LOG(str(data))
  # ---------------------------------------------------------------------------
  def notifyCltu(self, cltu):
    """CLTU received"""
    LOG("- notifyCltu")
  # ---------------------------------------------------------------------------
  def notifyTCframe(self, tcFrameDu):
    """TC frame received"""
    LOG("- notifyTCframe")
  # ---------------------------------------------------------------------------
  def notifyTCsegment(self, tcSegmentDu):
    """TC segment received"""
    portionStr = CCSDS.SEGMENThelpers.portionStr(tcSegmentDu.sequenceFlags)
    LOG("- notifyTCsegment(" + portionStr + ")")
  # ---------------------------------------------------------------------------
  def notifyTCpacket(self, tcPacketDu):
    """TC packet received"""
    LOG("- notifyTCpacket")
    LOG("  APID =    " + str(tcPacketDu.applicationProcessId))
    LOG("  TYPE =    " + str(tcPacketDu.serviceType))
    LOG("  SUBTYPE = " + str(tcPacketDu.serviceSubType))
    LOG("  SSC =     " + str(tcPacketDu.sequenceControlCount))

#############
# functions #
#############
# -----------------------------------------------------------------------------
def initConfiguration():
  """initialise the system configuration"""
  UTIL.SYS.s_configuration.setDefaults([
    ["SYS_COLOR_LOG", "1"],
    ["NCTRS_TC_SERVER_PORT", "13007"],
    ["DEF_GROUND_STATION_ID", "10"]])
# -----------------------------------------------------------------------------
def createTCreceiver():
  """create the NCTRS TC receiver"""
  tcReceiver = TCreceiver(
    UTIL.SYS.s_eventLoop,
    portNr=int(UTIL.SYS.s_configuration.NCTRS_TC_SERVER_PORT),
    groundstationId=int(UTIL.SYS.s_configuration.DEF_GROUND_STATION_ID))
  if not tcReceiver.openConnectPort():
    sys.exit(-1)
  return tcReceiver

########
# main #
########
if __name__ == "__main__":
  # initialise the system configuration
  initConfiguration()
  # create the NCTRS TC receiver
  LOG("Open the NCTRS TC receiver (server)")
  tcReceiver = createTCreceiver()
  # register a console handler for interaction
  consoleHandler = ConsoleHandler(tcReceiver)
  # start the event loop
  LOG("Start the event loop...")
  consoleHandler.process([])
  UTIL.SYS.s_eventLoop.start()
  sys.exit(0)
