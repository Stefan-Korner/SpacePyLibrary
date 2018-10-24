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

###########
# classes #
###########
# =============================================================================
class ConsoleHandler(UTIL.SYS.ConsoleHandler):
  """Subclass of UTIL.SYS.ConsoleHandler"""
  def __init__(self, adminSender):
    """Initialise attributes only"""
    UTIL.SYS.ConsoleHandler.__init__(self)
    self.adminSender = adminSender
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
      elif cmd == "M1" or cmd == "TMMESSAGE1":
        self.tmMessage1Cmd(argv)
      elif cmd == "M2" or cmd == "TMMESSAGE2":
        self.tmMessage2Cmd(argv)
      elif cmd == "C1" or cmd == "TCMESSAGE1":
        self.tcMessage1Cmd(argv)
      elif cmd == "C3" or cmd == "TCMESSAGE3":
        self.tcMessage3Cmd(argv)
      elif cmd == "C4" or cmd == "TCMESSAGE4":
        self.tcMessage4Cmd(argv)
      elif cmd == "C5" or cmd == "TCMESSAGE5":
        self.tcMessage5Cmd(argv)
      elif cmd == "C6" or cmd == "TCMESSAGE6":
        self.tcMessage6Cmd(argv)
      elif cmd == "C7" or cmd == "TCMESSAGE7":
        self.tcMessage7Cmd(argv)
      elif cmd == "C9" or cmd == "TCMESSAGE9":
        self.tcMessage9Cmd(argv)
      elif cmd == "C13" or cmd == "TCMESSAGE13":
        self.tcMessage13Cmd(argv)
      elif cmd == "C14" or cmd == "TCMESSAGE14":
        self.tcMessage14Cmd(argv)
      elif cmd == "C15" or cmd == "TCMESSAGE15":
        self.tcMessage15Cmd(argv)
      else:
        LOG_WARNING("Invalid command " + argv[0])
    print("> ",  end='')
  # ---------------------------------------------------------------------------
  def helpCmd(self, argv):
    """Decoded help command"""
    LOG("Available commands:")
    LOG("-------------------")
    LOG("")
    LOG("h  | help ..........provides this information")
    LOG("q  | quit ..........terminates the application")
    LOG("m1 | tmmessage1 ....send ADMIN_MSG_TM_LINK_FLOW")
    LOG("m2 | tmmessage2 ....send ADMIN_MSG_TM_LINK_NOFLOW")
    LOG("c1 | tcmessage1 ....send ADMIN_MSG_TC_LINK_ESTABLISHED_TO_GS")
    LOG("c3 | tcmessage3 ....send ADMIN_MSG_TC_LINK_CLOSED_TO_GS")
    LOG("c4 | tcmessage4 ....send ADMIN_MSG_TC_LINK_ABORTED_TO_GS")
    LOG("c5 | tcmessage5 ....send ADMIN_MSG_TC_LINK_ABORTED_FROM_GS")
    LOG("c6 | tcmessage6 ....send ADMIN_MSG_TC_AD_SERVICE_AVAILABLE_FROM_GS")
    LOG("c7 | tcmessage7 ....send ADMIN_MSG_TC_AD_SERVICE_FAILE_IN_GS")
    LOG("c9 | tcmessage9 ....send ADMIN_MSG_TC_AD_SERVICE_TERMINATED_IN_GS")
    LOG("c13| tcmessage13 ...send ADMIN_MSG_TC_AD_SERVICE_WILL_TERM_IN_GS_BD")
    LOG("c14| tcmessage14 ...send ADMIN_MSG_TC_AD_SERVICE_WILL_TERM_IN_GS")
    LOG("c15| tcmessage15 ...send ADMIN_MSG_TC_ALL_SERVICES_WILL_TERM_IN_GS")
    LOG("")
  # ---------------------------------------------------------------------------
  def quitCmd(self, argv):
    """Decoded quit command"""
    UTIL.SYS.s_eventLoop.stop()
  # ---------------------------------------------------------------------------
  def tmMessage1Cmd(self, argv):
    """Decoded ADMIN_MSG_TM_LINK_FLOW command"""
    self.adminSender.sendAdminMessageTM(GRND.NCTRSDU.ADMIN_MSG_TM_LINK_FLOW)
  # ---------------------------------------------------------------------------
  def tmMessage2Cmd(self, argv):
    """Decoded ADMIN_MSG_TM_LINK_NOFLOW command"""
    self.adminSender.sendAdminMessageTM(GRND.NCTRSDU.ADMIN_MSG_TM_LINK_NOFLOW)
  # ---------------------------------------------------------------------------
  def tcMessage1Cmd(self, argv):
    """Decoded ADMIN_MSG_TC_LINK_ESTABLISHED_TO_GS command"""
    self.adminSender.sendAdminMessageTC(GRND.NCTRSDU.ADMIN_MSG_TC_LINK_ESTABLISHED_TO_GS)
  # ---------------------------------------------------------------------------
  def tcMessage3Cmd(self, argv):
    """Decoded ADMIN_MSG_TC_LINK_CLOSED_TO_GS command"""
    self.adminSender.sendAdminMessageTC(GRND.NCTRSDU.ADMIN_MSG_TC_LINK_CLOSED_TO_GS)
  # ---------------------------------------------------------------------------
  def tcMessage4Cmd(self, argv):
    """Decoded ADMIN_MSG_TC_LINK_ABORTED_TO_GS command"""
    self.adminSender.sendAdminMessageTC(GRND.NCTRSDU.ADMIN_MSG_TC_LINK_ABORTED_TO_GS)
  # ---------------------------------------------------------------------------
  def tcMessage5Cmd(self, argv):
    """Decoded ADMIN_MSG_TC_LINK_ABORTED_FROM_GS command"""
    self.adminSender.sendAdminMessageTC(GRND.NCTRSDU.ADMIN_MSG_TC_LINK_ABORTED_FROM_GS)
  # ---------------------------------------------------------------------------
  def tcMessage6Cmd(self, argv):
    """Decoded ADMIN_MSG_TC_AD_SERVICE_AVAILABLE_FROM_GS command"""
    self.adminSender.sendAdminMessageTC(GRND.NCTRSDU.ADMIN_MSG_TC_AD_SERVICE_AVAILABLE_FROM_GS)
  # ---------------------------------------------------------------------------
  def tcMessage7Cmd(self, argv):
    """Decoded ADMIN_MSG_TC_AD_SERVICE_FAILE_IN_GS command"""
    self.adminSender.sendAdminMessageTC(GRND.NCTRSDU.ADMIN_MSG_TC_AD_SERVICE_FAILE_IN_GS)
  # ---------------------------------------------------------------------------
  def tcMessage9Cmd(self, argv):
    """Decoded ADMIN_MSG_TC_AD_SERVICE_TERMINATED_IN_GS command"""
    self.adminSender.sendAdminMessageTC(GRND.NCTRSDU.ADMIN_MSG_TC_AD_SERVICE_TERMINATED_IN_GS)
  # ---------------------------------------------------------------------------
  def tcMessage13Cmd(self, argv):
    """Decoded ADMIN_MSG_TC_AD_SERVICE_WILL_TERM_IN_GS_BD command"""
    self.adminSender.sendAdminMessageTC(GRND.NCTRSDU.ADMIN_MSG_TC_AD_SERVICE_WILL_TERM_IN_GS_BD)
  # ---------------------------------------------------------------------------
  def tcMessage14Cmd(self, argv):
    """Decoded ADMIN_MSG_TC_AD_SERVICE_WILL_TERM_IN_GS command"""
    self.adminSender.sendAdminMessageTC(GRND.NCTRSDU.ADMIN_MSG_TC_AD_SERVICE_WILL_TERM_IN_GS)
  # ---------------------------------------------------------------------------
  def tcMessage15Cmd(self, argv):
    """Decoded ADMIN_MSG_TC_ALL_SERVICES_WILL_TERM_IN_GS command"""
    self.adminSender.sendAdminMessageTC(GRND.NCTRSDU.ADMIN_MSG_TC_ALL_SERVICES_WILL_TERM_IN_GS)

# =============================================================================
class AdminSender(GRND.NCTRS.AdminMessageSender):
  """Subclass of GRND.NCTRS.AdminMessageSender"""
  def __init__(self, eventLoop, portNr, groundstationName):
    """Initialise attributes only"""
    GRND.NCTRS.AdminMessageSender.__init__(self, eventLoop, portNr, groundstationName)
  # ---------------------------------------------------------------------------
  def clientAccepted(self):
    LOG_INFO("NCTRS admin receiver (client) accepted")
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
    ["NCTRS_ADMIN_SERVER_PORT", "13006"],
    ["GROUND_STATION_NAME", "ESA G/S "]])
# -----------------------------------------------------------------------------
def createAdminSender():
  """create the NCTRS admin message sender"""
  adminSender = AdminSender(
    UTIL.SYS.s_eventLoop,
    portNr=int(UTIL.SYS.s_configuration.NCTRS_ADMIN_SERVER_PORT),
    groundstationName=UTIL.SYS.s_configuration.GROUND_STATION_NAME)
  if not adminSender.openConnectPort():
    sys.exit(-1)
  return adminSender

########
# main #
########
if __name__ == "__main__":
  # initialise the system configuration
  initConfiguration()
  # create the NCTRS admin message sender
  LOG("Open the NCTRS admin message sender (server)")
  adminSender = createAdminSender()
  # register a console handler for interaction
  consoleHandler = ConsoleHandler(adminSender)
  # start the event loop
  LOG("Start the event loop...")
  consoleHandler.process([])
  UTIL.SYS.s_eventLoop.start()
  sys.exit(0)
