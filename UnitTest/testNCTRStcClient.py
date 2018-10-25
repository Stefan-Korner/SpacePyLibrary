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
import sys
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import UTIL.SYS
import GRND.NCTRS, GRND.NCTRSDU, GRND.NCTRSDUhelpers
import CCSDS.CLTU
import testData

###########
# classes #
###########
# =============================================================================
class ConsoleHandler(UTIL.SYS.ConsoleHandler):
  """Subclass of UTIL.SYS.ConsoleHandler"""
  def __init__(self, tcSender):
    """Initialise attributes only"""
    UTIL.SYS.ConsoleHandler.__init__(self)
    self.tcSender = tcSender
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
      elif cmd == "F" or cmd == "FRAME":
        self.frameCmd(argv)
      elif cmd == "C" or cmd == "CLTU1":
        self.cltu1Cmd(argv)
      elif cmd == "Z" or cmd == "CLTU2":
        self.cltu2Cmd(argv)
      elif cmd == "D" or cmd == "DIRECTIVE":
        self.directiveCmd(argv)
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
    LOG("p | packet1 .....send TC packet via NCTRS TC packet DU")
    LOG("b | packet2 .....send TC packet via NCTRS TC CLTU DU")
    LOG("f | frame .......send TC frame via NCTRS TC CLTU DU (segment 1st part)")
    LOG("c | cltu1 .......send TC CLTU via NCTRS TC CLTU (segment 1st part)")
    LOG("z | cltu2 .......send NCTRS TC CLTU (segment 2nd part)")
    LOG("d | directive ...send NCTRS TC directive")
    LOG("")
  # ---------------------------------------------------------------------------
  def quitCmd(self, argv):
    """Decoded quit command"""
    UTIL.SYS.s_eventLoop.stop()
  # ---------------------------------------------------------------------------
  def packet1Cmd(self, argv):
    """Decoded packet1 command"""
    tcPktDu = GRND.NCTRSDU.TCpacketDataUnit()
    print "tcPktDu =", tcPktDu
    self.tcSender.sendTcDataUnit(tcPktDu)
  # ---------------------------------------------------------------------------
  def packet2Cmd(self, argv):
    """Decoded packet2 command"""
    LOG_WARNING("Command not implemented: " + argv[0])
  # ---------------------------------------------------------------------------
  def frameCmd(self, argv):
    """Decoded frame command"""
    frame = testData.TC_FRAME_01
    cltu = CCSDS.CLTU.encodeCLTU(frame)
    okState, msg = CCSDS.CLTU.checkCLTU(cltu)
    if not okState:
      LOG_ERROR("CLTU check failed: " + msg)
      print "cltu =", cltu
      return
    tcCltuDu = GRND.NCTRSDU.TCcltuDataUnit()
    tcCltuDu.setCltu(cltu)
    tcCltuDu.spacecraftId = testData.NCTRS_CLTU_01_spacecraftId
    tcCltuDu.delay = testData.NCTRS_CLTU_01_delay
    tcCltuDu.latestProdTime = testData.NCTRS_CLTU_01_latestProdTime
    tcCltuDu.serviceType = testData.NCTRS_CLTU_01_serviceType
    tcCltuDu.earliestProdTime = testData.NCTRS_CLTU_01_earliestProdTime
    tcCltuDu.virtualChannelId = testData.NCTRS_CLTU_01_virtualChannelId
    tcCltuDu.mapId = testData.NCTRS_CLTU_01_mapId
    tcCltuDu.aggregationFlag = testData.NCTRS_CLTU_01_aggregationFlag
    tcCltuDu.tcId = testData.NCTRS_CLTU_01_tcId
    tcCltuDu.earliestProdTimeFlag = testData.NCTRS_CLTU_01_earliestProdTimeFlag
    tcCltuDu.latestProdTimeFlag = testData.NCTRS_CLTU_01_latestProdTimeFlag
    print "tcCltuDu =", tcCltuDu
    self.tcSender.sendTcDataUnit(tcCltuDu)
  # ---------------------------------------------------------------------------
  def cltu1Cmd(self, argv):
    """Decoded cltu1 command"""
    cltu = testData.CLTU_01
    okState, msg = CCSDS.CLTU.checkCltu(cltu)
    if not okState:
      LOG_ERROR("CLTU check failed: " + msg)
      print "cltu =", cltu
      return
    tcCltuDu = GRND.NCTRSDU.TCcltuDataUnit()
    tcCltuDu.setCltu(cltu)
    tcCltuDu.spacecraftId = testData.NCTRS_CLTU_01_spacecraftId
    tcCltuDu.delay = testData.NCTRS_CLTU_01_delay
    tcCltuDu.latestProdTime = testData.NCTRS_CLTU_01_latestProdTime
    tcCltuDu.serviceType = testData.NCTRS_CLTU_01_serviceType
    tcCltuDu.earliestProdTime = testData.NCTRS_CLTU_01_earliestProdTime
    tcCltuDu.virtualChannelId = testData.NCTRS_CLTU_01_virtualChannelId
    tcCltuDu.mapId = testData.NCTRS_CLTU_01_mapId
    tcCltuDu.aggregationFlag = testData.NCTRS_CLTU_01_aggregationFlag
    tcCltuDu.tcId = testData.NCTRS_CLTU_01_tcId
    tcCltuDu.earliestProdTimeFlag = testData.NCTRS_CLTU_01_earliestProdTimeFlag
    tcCltuDu.latestProdTimeFlag = testData.NCTRS_CLTU_01_latestProdTimeFlag
    print "tcCltuDu =", tcCltuDu
    self.tcSender.sendTcDataUnit(tcCltuDu)
  # ---------------------------------------------------------------------------
  def cltu2Cmd(self, argv):
    """Decoded cltu2 command"""
    nctrsCltu = testData.NCTRS_CLTU_02
    tcCltuDu = GRND.NCTRSDU.TCcltuDataUnit(nctrsCltu)
    print "tcCltuDu =", tcCltuDu
    self.tcSender.sendTcDataUnit(tcCltuDu)
  # ---------------------------------------------------------------------------
  def directiveCmd(self, argv):
    """Decoded directive command"""
    tcDirDu = GRND.NCTRSDU.TCdirectivesDataUnit()
    print "tcDirDu =", tcDirDu
    self.tcSender.sendTcDataUnit(tcDirDu)

# =============================================================================
class TCsender(GRND.NCTRS.TCsender):
  """Subclass of GRND.NCTRS.TCsender"""
  def __init__(self, eventLoop):
    """Initialise attributes only"""
    GRND.NCTRS.TCsender.__init__(self, eventLoop)
  # ---------------------------------------------------------------------------
  def notifyTCpacketResponseDataUnit(self, tcPktRespDu):
    """AD packet / BD segment response received"""
    LOG("")
    LOG("*** notifyTCpacketResponseDataUnit ***")
    LOG("tcPktRespDu.acknowledgement = " +
             GRND.NCTRSDUhelpers.ackStr(tcPktRespDu.acknowledgement))
    LOG("tcPktRespDu = " + str(tcPktRespDu))
  # ---------------------------------------------------------------------------
  def notifyTCcltuResponseDataUnit(self, tcCltuRespDu):
    """CLTU response received"""
    LOG("")
    LOG("*** notifyTCcltuResponseDataUnit ***")
    LOG("tcCltuRespDu.acknowledgement = " +
        GRND.NCTRSDUhelpers.ackStr(tcCltuRespDu.acknowledgement))
    LOG("tcCltuRespDu = " + str(tcCltuRespDu))
  # ---------------------------------------------------------------------------
  def notifyTClinkStatusDataUnit(self, tcLinkStatDu):
    """Link status received"""
    LOG("*** notifyTClinkStatusDataUnit ***")
    LOG("tcLinkStatDu = " + str(tcLinkStatDu))

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
    ["NCTRS_TC_SERVER_PORT", "13007"]])
# -----------------------------------------------------------------------------
def createTCsender():
  """create the NCTRS TC receiver"""
  tcSender = TCsender(UTIL.SYS.s_eventLoop)
  if not tcSender.connectToServer(
    serverHost=UTIL.SYS.s_configuration.HOST,
    serverPort=int(UTIL.SYS.s_configuration.NCTRS_TC_SERVER_PORT)):
    sys.exit(-1)
  return tcSender

########
# main #
########
if __name__ == "__main__":
  # initialise the system configuration
  initConfiguration()
  # create the NCTRS TC sender
  LOG("Open the NCTRS TC sender (client)")
  tcSender = createTCsender()
  # register a console handler for interaction
  consoleHandler = ConsoleHandler(tcSender)
  # start the event loop
  LOG("Start the event loop...")
  consoleHandler.process([])
  UTIL.SYS.s_eventLoop.start()
  sys.exit(0)
