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
# Control System (CS) implementation                                          *
#                                                                             *
# The system can act as Central Checkout System (CCS)                         *
# or as Mission Control System (MCS).                                         *
#                                                                             *
# The systen supports the following EGSE_PROTOCOLs for CCS connection:        *
# - CNC:  implements CAIT-03474-ASTR_issue_3_EGSE_IRD.pdf                     *
# - EDEN: implements Core_EGSE_AD03_GAL_REQ_ALS_SA_R_0002_EGSE_IRD_issue2.pdf *
# The system supports the following protocol for MCS connection:              *
# - NCTRS/NIS: implements EGOS-NIS-NCTR-ICD-0002-i4r0.2 (Signed).pdf          *
#******************************************************************************
import sys, os
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import CS.CNCclient, CS.CNCgui, CS.EDENclient, CS.EDENgui, CS.FRAMEgui, CS.NCTRSgui
import EGSE.IF
import MC.IF, MC.TCmodel, MC.TMmodel
import MCUI.CFGgui, MCUI.TMgui, MCUI.TCgui
import SCOS.ENV
import SPACE.DEF, SPACE.IF
import UI.TKI
import UTIL.SYS, UTIL.TCO, UTIL.TASK

#############
# constants #
#############
SYS_CONFIGURATION = [
  ["CNC_HOST", "127.0.0.1"],
  ["CNC_SERVER_PORT", "48569"],
  ["CNC_SERVER_PORT2", "48570"],
  ["EDEN_HOST", "127.0.0.1"],
  ["EDEN_SERVER_PORT", "48569"],
  ["EDEN_SERVER_PORT2", "-1"],
  ["SYS_COLOR_LOG", "1"],
  ["SYS_APP_MNEMO", "CS"],
  ["SYS_APP_NAME", "Control System"],
  ["SYS_APP_VERSION", "3.0"]]

###########
# classes #
###########
# =============================================================================
class ModelTask(UTIL.TASK.ProcessingTask):
  """The CS is the processing model"""
  # ---------------------------------------------------------------------------
  def __init__(self, isParent):
    """Initialise the Task as processing model"""
    UTIL.TASK.ProcessingTask.__init__(self, isParent=isParent)
  # ---------------------------------------------------------------------------
  def notifyGUItask(self, status):
    """Update the GUI task"""
    # pass the view event to the event queue of the parent task
    event = UTIL.TASK.ViewEvent(status)
    event.enable(UTIL.TASK.s_parentTask)
  # ---------------------------------------------------------------------------
  def notifyCommand(self, argv):
    """Entry point for processing"""
    if len(argv) == 0:
      # echo command ---> allways OK
      LOG("echo command")
      return 0
    # decode the command
    cmd = argv[0].upper()
    retStatus = False;
    if (cmd == "H") or (cmd == "HELP"):
      retStatus = self.helpCmd(argv)
    elif (cmd == "Q") or (cmd == "QUIT"):
      retStatus = self.quitCmd(argv)
    elif (cmd == "U") or (cmd == "DUMPCONFIGURATION"):
      retStatus = self.dumpConfigurationCmd(argv)
    elif (cmd == "L") or (cmd == "LISTPACKETS"):
      retStatus = self.listPacketsCmd(argv)
    elif (cmd == "G") or (cmd == "GENERATE"):
      retStatus = self.generateCmd(argv)
    elif (cmd == "C1") or (cmd == "CONNECTCNC"):
      retStatus = self.connectCNCcmd(argv)
    elif (cmd == "D1") or (cmd == "DISCONNECTCNC"):
      retStatus = self.disconnectCNCcmd(argv)
    elif (cmd == "C2") or (cmd == "CONNECTCNC2"):
      retStatus = self.connectCNC2cmd(argv)
    elif (cmd == "D2") or (cmd == "DISCONNECTCNC2"):
      retStatus = self.disconnectCNC2cmd(argv)
    elif (cmd == "E1") or (cmd == "CONNECTEDEN"):
      retStatus = self.connectEDENcmd(argv)
    elif (cmd == "F1") or (cmd == "DISCONNECTEDEN"):
      retStatus = self.disconnectEDENcmd(argv)
    elif (cmd == "E2") or (cmd == "CONNECTEDEN2"):
      retStatus = self.connectEDEN2cmd(argv)
    elif (cmd == "F2") or (cmd == "DISCONNECTEDEN2"):
      retStatus = self.disconnectEDEN2cmd(argv)
    else:
      LOG_WARNING("invalid command " + argv[0])
      return -1
    if retStatus:
      # processing successful
      return 0
    # processing error
    return -2
  # ---------------------------------------------------------------------------
  def helpCmd(self, argv):
    """Decoded help command"""
    LOG_INFO("Available configuration commands:", "CFG")
    LOG("", "CFG")
    LOG("x  | exit ...............terminates client connection (only for TCP/IP clients)", "CFG")
    LOG("h  | help ...............provides this information", "CFG")
    LOG("q  | quit ...............terminates SIM application", "CFG")
    LOG("u  | dumpConfiguration...dumps the configuration", "CFG")
    LOG("l  | listPackets.........lists available packets", "CFG")
    LOG("g  | generate............generates the testdata.sim file in testbin directory", "CFG")
    LOG_INFO("Available monitoring commands:", "TM")
    LOG("", "TM")
    LOG("x  | exit ...............terminates client connection (only for TCP/IP clients)", "TM")
    LOG("h  | help ...............provides this information", "TM")
    LOG("q  | quit ...............terminates SIM application", "TM")
    LOG("u  | dumpConfiguration...dumps the configuration", "TM")
    LOG_INFO("Available control commands:", "TC")
    LOG("", "TC")
    LOG("x  | exit ...............terminates client connection (only for TCP/IP clients)", "TC")
    LOG("h  | help ...............provides this information", "TC")
    LOG("q  | quit ...............terminates SIM application", "TC")
    LOG("u  | dumpConfiguration...dumps the configuration", "TC")
    LOG_INFO("Available control commands:", "CNC")
    LOG("", "CNC")
    LOG("x  | exit ...............terminates client connection (only for TCP/IP clients)", "CNC")
    LOG("h  | help ...............provides this information", "CNC")
    LOG("q  | quit ...............terminates SIM application", "CNC")
    LOG("u  | dumpConfiguration...dumps the configuration", "CNC")
    LOG("c1 | connectCNC..........connect to CNC port 1", "CNC")
    LOG("d1 | disconnectCNC.......disconnect from CNC port 1", "CNC")
    LOG("c2 | connectCNC2.........connect to CNC port 2", "CNC")
    LOG("d2 | disconnectCNC2......disconnect from CNC port 2", "CNC")
    LOG_INFO("Available control commands:", "EDEN")
    LOG("", "EDEN")
    LOG("x  | exit ...............terminates client connection (only for TCP/IP clients)", "EDEN")
    LOG("h  | help ...............provides this information", "EDEN")
    LOG("q  | quit ...............terminates SIM application", "EDEN")
    LOG("u  | dumpConfiguration...dumps the configuration", "EDEN")
    LOG("e1 | connectEDEN.........connect to EDEN port 1", "EDEN")
    LOG("f1 | disconnectEDEN......disconnect from EDEN port 1", "EDEN")
    LOG("e2 | connectEDEN2........connect to EDEN port 2", "EDEN")
    LOG("f2 | disconnectEDEN2.....disconnect from EDEN port 2", "EDEN")
    LOG_INFO("Available control commands:", "FRAME")
    LOG("", "FRAME")
    LOG("x  | exit ...............terminates client connection (only for TCP/IP clients)", "FRAME")
    LOG("h  | help ...............provides this information", "FRAME")
    LOG("q  | quit ...............terminates SIM application", "FRAME")
    LOG("u  | dumpConfiguration...dumps the configuration", "FRAME")
    LOG_INFO("Available control commands:", "NCTRS")
    LOG("", "NCTRS")
    LOG("x  | exit ...............terminates client connection (only for TCP/IP clients)", "NCTRS")
    LOG("h  | help ...............provides this information", "NCTRS")
    LOG("q  | quit ...............terminates SIM application", "NCTRS")
    LOG("u  | dumpConfiguration...dumps the configuration", "NCTRS")
    return True
  # ---------------------------------------------------------------------------
  def quitCmd(self, argv):
    """Decoded quit command"""
    self.logMethod("quitCmd")
    UTIL.TASK.s_parentTask.stop()
    return True
  # ---------------------------------------------------------------------------
  def dumpConfigurationCmd(self, argv):
    """Decoded dumpConfiguration command"""
    self.logMethod("dumpConfigurationCmd")
    MC.IF.s_configuration.dump()
    EGSE.IF.s_cncClientConfiguration.dump()
    EGSE.IF.s_edenClientConfiguration.dump()
    return True
  # ---------------------------------------------------------------------------
  def listPacketsCmd(self, argv):
    """Decoded listPackets command"""
    self.logMethod("listPacketsCmd", "CFG")
    # consistency check
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed", "CFG")
      return False
    # read the MIB 
    try:
      for tcPktDef in SPACE.IF.s_definitions.getTCpktDefs():
        LOG(tcPktDef.pktName + " (" + str(tcPktDef.pktAPID) + "," + str(tcPktDef.pktType) + "," + str(tcPktDef.pktSType) + ") - " + tcPktDef.pktDescr, "CFG")
    except Exception as ex:
      LOG_ERROR("MIB Error: " + str(ex), "CFG")
      return False
    return True
  # ---------------------------------------------------------------------------
  def generateCmd(self, argv):
    """Decoded generate command"""
    self.logMethod("generateCmd", "CFG")
    # consistency check
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed", "CFG")
      return False
    # generate the testdata.sim file
    definitionFileName = SCOS.ENV.s_environment.definitionFileName()
    LOG("generate to " + definitionFileName, "CFG")
    try:
      # update the TM definitions to ensure an actual testdata.sim
      SPACE.IF.s_definitions.createDefinitions()
      LOG(definitionFileName + " generated", "CFG")
    except Exception as ex:
      LOG_ERROR("Generation Error: " + str(ex), "CFG")
      return False
    return True
  # ---------------------------------------------------------------------------
  def connectCNCcmd(self, argv):
    """Decoded connectCNC command"""
    self.logMethod("connectCNCcmd", "CNC")
    CS.CNCclient.connectCNC()
  # ---------------------------------------------------------------------------
  def disconnectCNCcmd(self, argv):
    """Decoded disconnectCNC command"""
    self.logMethod("disconnectCNCcmd", "CNC")
    CS.CNCclient.disconnectCNC()
  # ---------------------------------------------------------------------------
  def connectCNC2cmd(self, argv):
    """Decoded connectCNC2 command"""
    self.logMethod("connectCNC2cmd", "CNC")
    CS.CNCclient.connectCNC2()
  # ---------------------------------------------------------------------------
  def disconnectCNC2cmd(self, argv):
    """Decoded disconnectCNC2 command"""
    self.logMethod("disconnectCNC2cmd", "CNC")
    CS.CNCclient.disconnectCNC2()
  # ---------------------------------------------------------------------------
  def connectEDENcmd(self, argv):
    """Decoded connectEDEN command"""
    self.logMethod("connectEDENcmd", "EDEN")
    CS.EDENclient.connectEDEN()
  # ---------------------------------------------------------------------------
  def disconnectEDENcmd(self, argv):
    """Decoded disconnectEDEN command"""
    self.logMethod("disconnectEDENcmd", "EDEN")
    CS.EDENclient.disconnectEDEN()
  # ---------------------------------------------------------------------------
  def connectEDEN2cmd(self, argv):
    """Decoded connectEDEN2 command"""
    self.logMethod("connectEDEN2cmd", "EDEN")
    CS.EDENclient.connectEDEN2()
  # ---------------------------------------------------------------------------
  def disconnectEDEN2cmd(self, argv):
    """Decoded disconnectEDEN2 command"""
    self.logMethod("disconnectEDEN2cmd", "EDEN")
    CS.EDENclient.disconnectEDEN2()
  # ---------------------------------------------------------------------------
  def notifyCNCconnected(self):
    """CNC connection established"""
    self.notifyGUItask("CNC_CONNECTED")
    MC.IF.s_configuration.connected = True
    self.notifyGUItask("TC_CONNECTED")
  # ---------------------------------------------------------------------------
  def notifyCNCdisconnected(self):
    """CNC connection terminated"""
    self.notifyGUItask("CNC_DISCONNECTED")
  # ---------------------------------------------------------------------------
  def notifyCNC2connected(self):
    """CNC 2nd connection established"""
    self.notifyGUItask("CNC2_CONNECTED")
  # ---------------------------------------------------------------------------
  def notifyCNC2disconnected(self):
    """CNC 2nd connection terminated"""
    self.notifyGUItask("CNC2_DISCONNECTED")
  # ---------------------------------------------------------------------------
  def notifyEDENconnected(self):
    """EDEN connection established"""
    self.notifyGUItask("EDEN_CONNECTED")
    MC.IF.s_configuration.connected = True
    self.notifyGUItask("TC_CONNECTED")
  # ---------------------------------------------------------------------------
  def notifyEDENdisconnected(self):
    """EDEN connection terminated"""
    self.notifyGUItask("EDEN_DISCONNECTED")
  # ---------------------------------------------------------------------------
  def notifyEDEN2connected(self):
    """EDEN 2nd connection established"""
    self.notifyGUItask("EDEN_CONNECTED")
    MC.IF.s_configuration.connected = True
    self.notifyGUItask("TC_CONNECTED")
  # ---------------------------------------------------------------------------
  def notifyEDEN2disconnected(self):
    """EDEN 2nd connection terminated"""
    self.notifyGUItask("EDEN_DISCONNECTED")

#############
# functions #
#############
# global shortcut functions for test commands
def help(*argv): UTIL.TASK.s_processingTask.helpCmd(("", ) + argv)
def quit(*argv): UTIL.TASK.s_processingTask.quitCmd(("", ) + argv)
def dumpConfiguration(*argv): UTIL.TASK.s_processingTask.dumpConfigurationCmd(("", ) + argv)
# -----------------------------------------------------------------------------
def printUsage(launchScriptName):
  """Prints the possible commandline options of the test driver"""
  print("")
  print("usage:")
  print("------")
  print("")
  print(launchScriptName)
  print("\t[ -i | -interpreter | -c | -cmdprompt | -bg | -background ]")
  print("\t[ -n | -nogui ] [ -p <port> | -port <port> ]")
  print("\t[ -l <logfile> | -logfile <logfile> ] [ -h | -help ]")
  print("")

########
# main #
########
# detect if the application is launched with or without python prompt
if sys.argv[0] == "":
  interpreter = True
  sys.argv = os.getenv("ARGS").split()
  launchScriptName = sys.argv[0]
else:
  interpreter = False
  launchScriptName = sys.argv[1]
# initialise the system configuration
UTIL.SYS.s_configuration.setDefaults(SYS_CONFIGURATION)
MC.IF.s_configuration = MC.IF.Configuration()
EGSE.IF.s_cncClientConfiguration = EGSE.IF.CNCclientConfiguration()
EGSE.IF.s_edenClientConfiguration = EGSE.IF.EDENclientConfiguration()
# initialise the request handler
requestHandler = UTIL.TASK.RequestHandler(sys.argv)
if requestHandler.helpRequested:
  printUsage(launchScriptName)
  sys.exit(0)
# check specific command line switches
guiMode = True
cmdPrompt = False
for arg in sys.argv:
  cmdSwitch = arg.upper()
  if cmdSwitch == "-N" or cmdSwitch == "-NOGUI":
    guiMode = False
  if cmdSwitch == "-C" or cmdSwitch == "-CMDPROMPT":
    if not interpreter:
      cmdPrompt = True
# initialise the model and the GUI on demand
if guiMode:
  # keep the order: tasks must exist before the gui views are created
  UI.TKI.createGUI()
  guiTask = UI.TKI.GUItask()
  modelTask = ModelTask(isParent=False)
  win0 = UI.TKI.createWindow()
  win1 = UI.TKI.createWindow()
  win2 = UI.TKI.createWindow()
  win3 = UI.TKI.createWindow()
  win4 = UI.TKI.createWindow()
  win5 = UI.TKI.createWindow()
  win6 = UI.TKI.createWindow()
  gui0view = MCUI.CFGgui.GUIview(win0)
  gui1view = MCUI.TMgui.GUIview(win1)
  gui2view = MCUI.TCgui.GUIview(win2)
  gui3view = CS.CNCgui.GUIview(win3)
  gui4view = CS.EDENgui.GUIview(win4)
  gui5view = CS.FRAMEgui.GUIview(win5)
  gui6view = CS.NCTRSgui.GUIview(win6)
  UI.TKI.finaliseGUIcreation()
else:
  modelTask = ModelTask(isParent=True)
# register the TCP/IP server socket for remote control
if requestHandler.portNr != 0:
  print("register connect port...")
  if not requestHandler.openConnectPort(UTIL.SYS.s_configuration.HOST):
    sys.exit(-1)
  connectSocket = requestHandler.connectSocket
  modelTask.createFileHandler(connectSocket, requestHandler.tcpConnectCallback)
# register the requestHandler as console handler if requested
if cmdPrompt:
  print("register console handler...")
  modelTask.registerConsoleHandler(requestHandler)

# initialise singletons
SPACE.DEF.init()

# create the CNC clients
print("Create the CNCclients")
CS.CNCclient.createClients()
# create the EDEN clients
print("Create the EDENclients")
CS.EDENclient.createClients()
# create the TC model
print("Create the TC model")
MC.TCmodel.init()
# create the TM model
print("Create the TM model")
MC.TMmodel.init()

# load the definition data
print("load definition data (take some time) ...")
SPACE.IF.s_definitions.initDefinitions()
print("definition data loaded")

# start the tasks
print("start modelTask...")
modelTask.start()
if guiMode:
  print("start guiTask...")
  guiTask.start()
  print("guiTask terminated")
  modelTask.join()
print("modelTask terminated")
