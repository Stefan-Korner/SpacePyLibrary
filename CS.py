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
from __future__ import print_function
import sys, os
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import CS.CNCclient, CS.CNCgui, CS.EDENclient, CS.EDENgui, CS.FRAMEgui, CS.FRAMEmodel, CS.FRAMErply, CS.NCTRSclient, CS.NCTRSgui
import EGSE.IF
import GRND.IF
import MC.IF, MC.TCGEN, MC.TCmodel, MC.TMmodel
import MCUI.CFGgui, MCUI.TMgui, MCUI.TCgui
import SUPP.DEF, SUPP.IF, SUPP.TMrecorder
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
  ["NCTRS_HOST", "127.0.0.1"],
  ["NCTRS_ADMIN_SERVER_PORT", "32010"],
  ["NCTRS_TC_SERVER_PORT", "32009"],
  ["NCTRS_TM_SERVER_PORT", "22104"],
  ["NCTRS_TM_DU_VERSION", "V0"],
  ["ERT_MISSION_EPOCH_STR", UTIL.TCO.TAI_MISSION_EPOCH_STR],
  ["ERT_LEAP_SECONDS", str(UTIL.TCO.GPS_LEAP_SECONDS_2017)],
  ["SYS_COLOR_LOG", "1"],
  ["SYS_APP_MNEMO", "CS"],
  ["SYS_APP_NAME", "Control System"],
  ["SYS_APP_VERSION", "2.2"],
  ["TC_PARAM_LENGTH_BYTES", "2"],
  ["TM_TRANSFER_FRAME_VCID", "0"],
  ["TM_PARAM_LENGTH_BYTES", "2"],
  ["IGNORE_IDLE_PACKETS", "1"]]

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
  def notifyCommand(self, argv, extraData):
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
    elif (cmd == "RP") or (cmd == "RECORDPACKETS"):
      retStatus = self.recordPacketsCmd(argv)
    elif (cmd == "SP") or (cmd == "STOPPACKETRECORDER"):
      retStatus = self.stopPacketRecorderCmd(argv)
    elif (cmd == "P") or (cmd == "SETPACKETDATA"):
      retStatus = self.setPacketDataCmd(argv, extraData)
    elif (cmd == "S") or (cmd == "SENDPACKET"):
      retStatus = self.sendPacketCmd(argv, extraData)
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
    elif (cmd == "PF") or (cmd == "REPLAYFRAMES"):
      retStatus = self.replayFramesCmd(argv)
    elif (cmd == "N1") or (cmd == "CONNECTNCTRS1"):
      retStatus = self.connectNCTRS1cmd(argv)
    elif (cmd == "O1") or (cmd == "DISCONNECTNCTRS1"):
      retStatus = self.disconnectNCTRS1cmd(argv)
    elif (cmd == "N2") or (cmd == "CONNECTNCTRS2"):
      retStatus = self.connectNCTRS2cmd(argv)
    elif (cmd == "O2") or (cmd == "DISCONNECTNCTRS2"):
      retStatus = self.disconnectNCTRS2cmd(argv)
    elif (cmd == "N3") or (cmd == "CONNECTNCTRS3"):
      retStatus = self.connectNCTRS3cmd(argv)
    elif (cmd == "O3") or (cmd == "DISCONNECTNCTRS3"):
      retStatus = self.disconnectNCTRS3cmd(argv)
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
    LOG("x  | exit ................terminates client connection (only for TCP/IP clients)", "TM")
    LOG("h  | help ................provides this information", "TM")
    LOG("q  | quit ................terminates SIM application", "TM")
    LOG("u  | dumpConfiguration....dumps the configuration", "TM")
    LOG("rp | recordPackets <recordFile> records TM packets", "TM")
    LOG("sp | stopPacketRecorder...stops recording of TM packets", "TM")
    LOG_INFO("Available control commands:", "TC")
    LOG("", "TC")
    LOG("x  | exit ...............terminates client connection (only for TCP/IP clients)", "TC")
    LOG("h  | help ...............provides this information", "TC")
    LOG("q  | quit ...............terminates SIM application", "TC")
    LOG("u  | dumpConfiguration...dumps the configuration", "TC")
    LOG("p  | setPacketData <pktMnemonic> <route>", "TC")
    LOG("                         predefine data for the next TC packet", "TC")
    LOG("s  | sendPacket [<pktMnemonic> <route>]", "TC")
    LOG("                         send predefined or specific TC packet", "TC")
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
    LOG("pf | replayFrames <replayFile> replays NCTRS frames", "FRAME")
    LOG_INFO("Available control commands:", "NCTRS")
    LOG("", "NCTRS")
    LOG("x  | exit ...............terminates client connection (only for TCP/IP clients)", "NCTRS")
    LOG("h  | help ...............provides this information", "NCTRS")
    LOG("q  | quit ...............terminates SIM application", "NCTRS")
    LOG("u  | dumpConfiguration...dumps the configuration", "NCTRS")
    LOG("n1 | connectNCTRS1.......connect to NCTRS port 1", "NCTRS")
    LOG("o1 | disconnectNCTRS1....disconnect from NCTRS port 1", "NCTRS")
    LOG("n2 | connectNCTRS2.......connect to NCTRS port 2", "NCTRS")
    LOG("o2 | disconnectNCTRS2....disconnect from NCTRS port 2", "NCTRS")
    LOG("n3 | connectNCTRS3.......connect to NCTRS port 3", "NCTRS")
    LOG("o3 | disconnectNCTRS3....disconnect from NCTRS port 3", "NCTRS")
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
    # dump the packet definitions
    try:
      for tmPktDef in SUPP.IF.s_definitions.getTMpktDefs():
        LOG("TM: " + tmPktDef.pktName + " (SPID = " + str(tmPktDef.pktSPID) + ") - " + tmPktDef.pktDescr, "CFG")
      for tcPktDef in SUPP.IF.s_definitions.getTCpktDefs():
        LOG("TC: " + tcPktDef.pktName + " (APID = " + str(tcPktDef.pktAPID) + ", TYPE = " + str(tcPktDef.pktType) + ", STPYE = " + str(tcPktDef.pktSType) + ") - " + tcPktDef.pktDescr, "CFG")
    except Exception, ex:
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
    definitionFileName = SUPP.IF.s_definitions.getDefinitionFileName()
    LOG("generate to " + definitionFileName, "CFG")
    try:
      # update the TM definitions to ensure an actual testdata.sim
      SUPP.IF.s_definitions.createDefinitions()
      LOG(definitionFileName + " generated", "CFG")
    except Exception, ex:
      LOG_ERROR("Generation Error: " + str(ex), "CFG")
      return False
    return True
  # ---------------------------------------------------------------------------
  def recordPacketsCmd(self, argv):
    """Decoded recordPackets command"""
    self.logMethod("recordPacketsCmd", "TM")
    # consistency check
    if SUPP.IF.s_tmRecorder.isRecording():
      LOG_WARNING("Packet recording already started", "TM")
      return False
    if len(argv) != 2:
      LOG_WARNING("invalid parameters passed for recordPackets", "TM")
      return False
    # extract the arguments
    recordFileName = argv[1]
    SUPP.IF.s_tmRecorder.startRecording(recordFileName);
    return True
  # ---------------------------------------------------------------------------
  def stopPacketRecorderCmd(self, argv):
    """Decoded stopPacketRecorder command"""
    self.logMethod("stopPacketRecorderCmd", "TM")
    # consistency check
    if not SUPP.IF.s_tmRecorder.isRecording():
      LOG_WARNING("Packet recording not started", "TM")
      return False
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed for stopPacketRecorder", "TM")
      return False
    SUPP.IF.s_tmRecorder.stopRecording();
    return True
  # ---------------------------------------------------------------------------
  def setPacketDataCmd(self, argv, extraData):
    """Decoded setPacketData command"""
    self.logMethod("setPacketDataCmd", "TC")

    # consistency check
    if len(argv) != 3:
      LOG_WARNING("invalid parameters passed for setPacketData", "TC")
      return False

    # extract the arguments
    pktMnemonic = argv[1]
    route = argv[2]
    tcStruct = extraData
    # check the packet data
    tcPacketData = SUPP.IF.s_definitions.getTCpacketInjectData(pktMnemonic, route, tcStruct)
    if tcPacketData == None:
      LOG_WARNING("invalid data passed for setPacketData", "TC")
      return False
    # initialise the packet data
    MC.IF.s_configuration.tcPacketData = tcPacketData
    LOG("Packet = " + MC.IF.s_configuration.tcPacketData.pktName, "TC")

    # notify the GUI
    self.notifyGUItask("PACKETDATA_SET")
    return True
  # ---------------------------------------------------------------------------
  def sendPacketCmd(self, argv, extraData):
    """Decoded sendPacket command"""
    self.logMethod("sendPacketCmd", "TC")

    # consistency check
    if len(argv) != 1 and len(argv) != 3:
      LOG_WARNING("invalid parameters passed for sendPacket", "TC")
      return False

    # extract the arguments
    if len(argv) == 1:
      if MC.IF.s_configuration.tcPacketData == None:
        LOG_WARNING("packet data not initialised", "TC")
        return False
      tcPacketData = MC.IF.s_configuration.tcPacketData
    else:
      pktMnemonic = argv[1]
      route = argv[2]
      tcStruct = extraData
      # check the packet data
      tcPacketData = SUPP.IF.s_definitions.getTCpacketInjectData(pktMnemonic, route, tcStruct)
      if tcPacketData == None:
        LOG_WARNING("invalid data passed for sendPacket", "TC")
        return False

    # send the packet
    try:
      MC.IF.s_tcModel.generateTCpacket(tcPacketData)
    except Exception, ex:
      LOG_WARNING("cannot send packet: " + str(ex), "TC")
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
  def replayFramesCmd(self, argv):
    """Decoded replayFramesCmd command"""
    self.logMethod("replayFramesCmd", "FRAME")

    # consistency check
    if len(argv) != 2:
      LOG_WARNING("invalid parameters passed for replayFrames", "FRAME")
      return False

    # extract the arguments
    replayFile = argv[1]

    # start replay
    frameRateMs = 1000.0
    CS.FRAMErply.s_frameReplayer.startReplay(replayFile, frameRateMs)
  # ---------------------------------------------------------------------------
  def connectNCTRS1cmd(self, argv):
    """Decoded connectNCTRS1cmd command"""
    self.logMethod("connectNCTRS1cmd", "NCTRS")
    CS.NCTRSclient.connectNCTRS1()
  # ---------------------------------------------------------------------------
  def disconnectNCTRS1cmd(self, argv):
    """Decoded disconnectNCTRS1cmd command"""
    self.logMethod("disconnectNCTRS1cmd", "NCTRS")
    CS.NCTRSclient.disconnectNCTRS1()
  # ---------------------------------------------------------------------------
  def connectNCTRS2cmd(self, argv):
    """Decoded connectNCTRS2cmd command"""
    self.logMethod("connectNCTRS2cmd", "NCTRS")
    CS.NCTRSclient.connectNCTRS2()
  # ---------------------------------------------------------------------------
  def disconnectNCTRS2cmd(self, argv):
    """Decoded disconnectNCTRS2cmd command"""
    self.logMethod("disconnectNCTRS2cmd", "NCTRS")
    CS.NCTRSclient.disconnectNCTRS2()
  # ---------------------------------------------------------------------------
  def connectNCTRS3cmd(self, argv):
    """Decoded connectNCTRS3cmd command"""
    self.logMethod("connectNCTRS3cmd", "NCTRS")
    CS.NCTRSclient.connectNCTRS3()
  # ---------------------------------------------------------------------------
  def disconnectNCTRS3cmd(self, argv):
    """Decoded disconnectNCTRS3cmd command"""
    self.logMethod("disconnectNCTRS3cmd", "NCTRS")
    CS.NCTRSclient.disconnectNCTRS3()
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
  # ---------------------------------------------------------------------------
  def notifyNCTRS1connected(self):
    """NCTRS 1st connection established"""
    self.notifyGUItask("NCTRS1_CONNECTED")
  # ---------------------------------------------------------------------------
  def notifyNCTRS1disconnected(self):
    """NCTRS 1st connection terminated"""
    self.notifyGUItask("NCTRS1_DISCONNECTED")
  # ---------------------------------------------------------------------------
  def notifyNCTRS2connected(self):
    """NCTRS 2nd connection established"""
    self.notifyGUItask("NCTRS2_CONNECTED")
    MC.IF.s_configuration.connected = True
    self.notifyGUItask("TC_CONNECTED")
  # ---------------------------------------------------------------------------
  def notifyNCTRS2disconnected(self):
    """NCTRS 2nd connection terminated"""
    self.notifyGUItask("NCTRS2_DISCONNECTED")
  # ---------------------------------------------------------------------------
  def notifyNCTRS3connected(self):
    """NCTRS 3rd connection established"""
    self.notifyGUItask("NCTRS3_CONNECTED")
  # ---------------------------------------------------------------------------
  def notifyNCTRS3disconnected(self):
    """NCTRS 3rd connection terminated"""
    self.notifyGUItask("NCTRS3_DISCONNECTED")

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
UTIL.TCO.setERTmissionEpochStr(UTIL.SYS.s_configuration.ERT_MISSION_EPOCH_STR)
UTIL.TCO.setERTleapSeconds(int(UTIL.SYS.s_configuration.ERT_LEAP_SECONDS))


MC.IF.s_configuration = MC.IF.Configuration()
EGSE.IF.s_cncClientConfiguration = EGSE.IF.CNCclientConfiguration()
EGSE.IF.s_edenClientConfiguration = EGSE.IF.EDENclientConfiguration()
GRND.IF.s_clientConfiguration = GRND.IF.ClientConfiguration()
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
  tab0 = UI.TKI.createTab()
  tab1 = UI.TKI.createTab()
  tab2 = UI.TKI.createTab()
  tab3 = UI.TKI.createTab()
  tab4 = UI.TKI.createTab()
  tab5 = UI.TKI.createTab()
  tab6 = UI.TKI.createTab()
  gui0view = MCUI.CFGgui.GUIview(tab0)
  gui1view = MCUI.TMgui.GUIview(tab1)
  gui2view = MCUI.TCgui.GUIview(tab2)
  gui3view = CS.CNCgui.GUIview(tab3)
  gui4view = CS.EDENgui.GUIview(tab4)
  gui5view = CS.FRAMEgui.GUIview(tab5)
  gui6view = CS.NCTRSgui.GUIview(tab6)
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
SUPP.DEF.init()
MC.TCGEN.init()

# create the CNC clients
print("Create the CNCclients")
CS.CNCclient.createClients()
# create the EDEN clients
print("Create the EDENclients")
CS.EDENclient.createClients()
# create the NCTRS clients
print("Create the NCTRSclients")
CS.NCTRSclient.createClients()
# create the TC model
print("Create the TC model")
MC.TCmodel.init()
# create the TM model
print("Create the TM model")
MC.TMmodel.init()
# create the TM recorder
print("Create the TM recorder")
SUPP.TMrecorder.init()
# create the frame model
print("Create the frame model")
CS.FRAMEmodel.init()
# create the frame replayer
print("Create the frame replayer")
CS.FRAMErply.init()

# load the definition data
print("load definition data (take some time) ...")
SUPP.IF.s_definitions.initDefinitions()
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
