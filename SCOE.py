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
# SCOE reference implementation                                               *
# supports one of the following EGSE_PROTOCOLs for CCS connection:            *
# - CNC:  implements CAIT-03474-ASTR_issue_3_EGSE_IRD.pdf                     *
# - EDEN: implements Core_EGSE_AD03_GAL_REQ_ALS_SA_R_0002_EGSE_IRD_issue2.pdf *
#******************************************************************************
from __future__ import print_function
import sys, os
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import EGSE.IF
import PUS.PACKET, PUS.SERVICES
import SCOE.EGSEserver, SCOE.EGSEgui
import SPACE.ASW, SPACE.IF, SPACE.MIL, SPACE.OBC, SPACE.TMGEN, SPACE.TMRPLY
import SPACEUI.SPACEgui, SPACEUI.MILgui
import SUPP.DEF, SUPP.IF, SUPP.TMrecorder
import UI.TKI
import UTIL.SYS, UTIL.TCO, UTIL.TASK

#############
# constants #
#############
SYS_CONFIGURATION = [
  ["EGSE_PROTOCOL", "EDEN"],
  ["HOST", "127.0.0.1"],
  ["CCS_SERVER_PORT", "48569"],
  ["CCS_SERVER_PORT2", "-1"],
  ["ASW_MISSION", "S4"],
  ["TC_ACK_ACCEPT_SUCC_MNEMO", "<<shall be passed as environment variable>>"],
  ["TC_ACK_ACCEPT_FAIL_MNEMO", "<<shall be passed as environment variable>>"],
  ["TC_ACK_EXESTA_SUCC_MNEMO", "<<shall be passed as environment variable>>"],
  ["TC_ACK_EXESTA_FAIL_MNEMO", "<<shall be passed as environment variable>>"],
  ["TC_ACK_EXEPRO_SUCC_MNEMO", "<<shall be passed as environment variable>>"],
  ["TC_ACK_EXEPRO_FAIL_MNEMO", "<<shall be passed as environment variable>>"],
  ["TC_ACK_EXECUT_SUCC_MNEMO", "<<shall be passed as environment variable>>"],
  ["TC_ACK_EXECUT_FAIL_MNEMO", "<<shall be passed as environment variable>>"],
  ["TC_ACK_APID_PARAM_BYTE_OFFSET", "<<shall be passed as environment variable>>"],
  ["TC_ACK_SSC_PARAM_BYTE_OFFSET", "<<shall be passed as environment variable>>"],
  ["TC_FKT_ID_BYTE_OFFSET", "<<shall be passed as environment variable>>"],
  ["TC_FKT_ID_BYTE_SIZE", "<<shall be passed as environment variable>>"],
  ["TC_PARAM_LENGTH_BYTES", "2"],
  ["TM_CYCLIC_MNEMO", "<<shall be passed as environment variable>>"],
  ["TM_CYCLIC_PERIOD_MS", "5000"],
  ["TM_PKT_SIZE_ADD", "0"],
  ["TM_TT_TIME_FORMAT", "CUC4"],
  ["TM_TT_TIME_BYTE_OFFSET", "<<shall be passed as environment variable>>"],
  ["TM_REPLAY_KEY", "SPID"],
  ["TM_PARAM_LENGTH_BYTES", "2"],
  ["OBT_MISSION_EPOCH_STR", UTIL.TCO.UNIX_MISSION_EPOCH_STR],
  ["OBT_LEAP_SECONDS", "0"],
  ["SYS_COLOR_LOG", "1"],
  ["SYS_APP_MNEMO", "SCOE"],
  ["SYS_APP_NAME", "Special Checkout Equipment"],
  ["SYS_APP_VERSION", "2.2"]]

###########
# classes #
###########
# =============================================================================
class ModelTask(UTIL.TASK.ProcessingTask):
  """The SCOE is the processing model"""
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
    elif (cmd == "AA") or (cmd == "EGSEENABLEACK1"):
      retStatus = self.egseEnableAck1Cmd(argv)
    elif (cmd == "NA") or (cmd == "EGSEENABLENAK1"):
      retStatus = self.egseEnableNak1Cmd(argv)
    elif (cmd == "DA") or (cmd == "EGSEDISABLEACK1"):
      retStatus = self.egseDisableAck1Cmd(argv)
    elif (cmd == "AB") or (cmd == "EGSEENABLEACK2"):
      retStatus = self.egseEnableAck2Cmd(argv)
    elif (cmd == "NB") or (cmd == "EGSEENABLENAK2"):
      retStatus = self.egseEnableNak2Cmd(argv)
    elif (cmd == "DB") or (cmd == "EGSEDISABLEACK2"):
      retStatus = self.egseDisableAck2Cmd(argv)
    elif (cmd == "P") or (cmd == "SETPACKETDATA"):
      retStatus = self.setPacketDataCmd(argv, extraData)
    elif (cmd == "S") or (cmd == "SENDPACKET"):
      retStatus = self.sendPacketCmd(argv, extraData)
    elif (cmd == "E") or (cmd == "ENABLECYCLIC"):
      retStatus = self.enableCyclicCmd(argv)
    elif (cmd == "D") or (cmd == "DISABLECYCLIC"):
      retStatus = self.disableCyclicCmd(argv)
    elif (cmd == "A1") or (cmd == "OBCENABLEACK1"):
      retStatus = self.obcEnableAck1Cmd(argv)
    elif (cmd == "N1") or (cmd == "OBCENABLENAK1"):
      retStatus = self.obcEnableNak1Cmd(argv)
    elif (cmd == "D1") or (cmd == "OBCDISABLEACK1"):
      retStatus = self.obcDisableAck1Cmd(argv)
    elif (cmd == "A2") or (cmd == "OBCENABLEACK2"):
      retStatus = self.obcEnableAck2Cmd(argv)
    elif (cmd == "N2") or (cmd == "OBCENABLENAK2"):
      retStatus = self.obcEnableNak2Cmd(argv)
    elif (cmd == "D2") or (cmd == "OBCDISABLEACK2"):
      retStatus = self.obcDisableAck2Cmd(argv)
    elif (cmd == "A3") or (cmd == "OBCENABLEACK3"):
      retStatus = self.obcEnableAck3Cmd(argv)
    elif (cmd == "N3") or (cmd == "OBCENABLENAK3"):
      retStatus = self.obcEnableNak3Cmd(argv)
    elif (cmd == "D3") or (cmd == "OBCDISABLEACK3"):
      retStatus = self.obcDisableAck3Cmd(argv)
    elif (cmd == "A4") or (cmd == "OBCENABLEACK4"):
      retStatus = self.obcEnableAck4Cmd(argv)
    elif (cmd == "N4") or (cmd == "OBCENABLENAK4"):
      retStatus = self.obcEnableNak4Cmd(argv)
    elif (cmd == "D4") or (cmd == "OBCDISABLEACK4"):
      retStatus = self.obcDisableAck4Cmd(argv)
    elif (cmd == "A") or (cmd == "SENDACK"):
      retStatus = self.sendAckCmd(argv)
    elif (cmd == "RP") or (cmd == "RECORDPACKETS"):
      retStatus = self.recordPacketsCmd(argv)
    elif (cmd == "SP") or (cmd == "STOPPACKETRECORDER"):
      retStatus = self.stopPacketRecorderCmd(argv)
    elif (cmd == "PP") or (cmd == "REPLAYPACKETS"):
      retStatus = self.replayPacketsCmd(argv)
    elif (cmd == "L") or (cmd == "LISTPACKETS"):
      retStatus = self.listPacketsCmd(argv)
    elif (cmd == "G") or (cmd == "GENERATE"):
      retStatus = self.generateCmd(argv)
    elif (cmd == "T") or (cmd == "TEST"):
      retStatus = self.testCmd(argv)
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
    LOG_INFO("Available EGSE interface commands:", "EGSE")
    LOG("", "EGSE")
    LOG("x  | exit ...............terminates client connection (only for TCP/IP clients)", "EGSE")
    LOG("h  | help ...............provides this information", "EGSE")
    LOG("q  | quit ...............terminates SIM application", "EGSE")
    LOG("u  | dumpConfiguration...dumps the configuration", "EGSE")
    LOG("aa | egseEnableAck1......enables autom. sending of ACK1 for TCs", "EGSE")
    LOG("na | egseEnableNak1......enables autom. sending of NAK1 for TCs", "EGSE")
    LOG("da | egseDisableAck1.....disables autom. sending of ACK1 for TCs", "EGSE")
    LOG("ab | egseEnableAck2......enables autom. sending of ACK2 for TCs", "EGSE")
    LOG("nb | egseEnableNak2......enables autom. sending of NAK2 for TCs", "EGSE")
    LOG("db | egseDisableAck2.....disables autom. sending of ACK2 for TCs", "EGSE")
    LOG_INFO("Available space segment commands:", "SPACE")
    LOG("", "SPACE")
    LOG("x  | exit ...............terminates client connection (only for TCP/IP clients)", "SPACE")
    LOG("h  | help ...............provides this information", "SPACE")
    LOG("q  | quit ...............terminates SIM application", "SPACE")
    LOG("u  | dumpConfiguration...dumps the configuration", "SPACE")
    LOG("p  | setPacketData <pktMnemonic> [<params> <values>]", "SPACE")
    LOG("                         predefine data for the next TM packet", "SPACE")
    LOG("s  | sendPacket [<pktMnemonic> [<params> <values>]]", "SPACE")
    LOG("                         send predefined or specific TM packet", "SPACE")
    LOG("e  | enableCyclic........enables cyclic sending of TM packet", "SPACE")
    LOG("d  | disableCyclic.......disables cyclic sending of TM packet", "SPACE")
    LOG("a1 | obcEnableAck1.......enables autom. sending of ACK1 for TCs", "SPACE")
    LOG("n1 | obcEnableNak1.......enables autom. sending of NAK1 for TCs", "SPACE")
    LOG("d1 | obcDisableAck1......disables autom. sending of ACK1 for TCs", "SPACE")
    LOG("a2 | obcEnableAck2.......enables autom. sending of ACK2 for TCs", "SPACE")
    LOG("n2 | obcEnableNak2.......enables autom. sending of NAK2 for TCs", "SPACE")
    LOG("d2 | obcDisableAck2......disables autom. sending of ACK2 for TCs", "SPACE")
    LOG("a3 | obcEnableAck3.......enables autom. sending of ACK3 for TCs", "SPACE")
    LOG("n3 | obcEnableNak3.......enables autom. sending of NAK3 for TCs", "SPACE")
    LOG("d3 | obcDisableAck3......disables autom. sending of ACK3 for TCs", "SPACE")
    LOG("a4 | obcEnableAck4.......enables autom. sending of ACK4 for TCs", "SPACE")
    LOG("n4 | obcEnableNak4.......enables autom. sending of NAK4 for TCs", "SPACE")
    LOG("d4 | obcDisableAck4......disables autom. sending of ACK4 for TCs", "SPACE")
    LOG("a  | sendAck <apid> <ssc> <stype> sends a TC acknowledgement", "SPACE")
    LOG("sp | stopPacketRecorder..stops recording of TM packets", "SPACE")
    LOG("pp | replayPackets <replayFile> replays TM packets", "SPACE")
    LOG("pp | replayPackets <replayFile> replays TM packets", "SPACE")
    LOG("l  | listPackets.........lists available packets", "SPACE")
    LOG("g  | generate............generates the testdata.sim file in testbin directory", "SPACE")
    LOG("t  | test <testMode>.....executes a test command", "SPACE")
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
    EGSE.IF.s_serverConfiguration.dump()
    return True
  # ---------------------------------------------------------------------------
  def egseEnableAck1Cmd(self, argv):
    """Decoded egseEnableAck1 command"""
    self.logMethod("egseEnableAck1Cmd", "EGSE")
    # consistency check
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed for egseEnableAck1", "EGSE")
      return False
    # enable the ack sending
    EGSE.IF.s_serverConfiguration.egseAck1 = EGSE.IF.ENABLE_ACK
    # notify the GUI
    self.notifyGUItask("EGSE_ENABLED_ACK1")
    return True
  def egseEnableNak1Cmd(self, argv):
    """Decoded egseEnableNak1 command"""
    self.logMethod("egseEnableNak1Cmd", "EGSE")
    # consistency check
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed for egseEnableNak1", "EGSE")
      return False
    # enable the ack sending
    EGSE.IF.s_serverConfiguration.egseAck1 = EGSE.IF.ENABLE_NAK
    # notify the GUI
    self.notifyGUItask("EGSE_ENABLED_NAK1")
    return True
  def egseDisableAck1Cmd(self, argv):
    """Decoded egseDisableAck1 command"""
    self.logMethod("egseDisableAck1Cmd", "EGSE")
    # consistency check
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed for egseDisableAck1", "EGSE")
      return False
    # enable the ack sending
    EGSE.IF.s_serverConfiguration.egseAck1 = EGSE.IF.DISABLE_ACK
    # notify the GUI
    self.notifyGUItask("EGSE_DISABLED_ACK1")
    return True
  # ---------------------------------------------------------------------------
  def egseEnableAck2Cmd(self, argv):
    """Decoded egseEnableAck2 command"""
    self.logMethod("egseEnableAck2Cmd", "EGSE")
    # consistency check
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed for egseEnableAck2", "EGSE")
      return False
    # enable the ack sending
    EGSE.IF.s_serverConfiguration.egseAck2 = EGSE.IF.ENABLE_ACK
    # notify the GUI
    self.notifyGUItask("EGSE_ENABLED_ACK2")
    return True
  def egseEnableNak2Cmd(self, argv):
    """Decoded egseEnableNak2 command"""
    self.logMethod("egseEnableNak2Cmd", "EGSE")
    # consistency check
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed for egseEnableNak2", "EGSE")
      return False
    # enable the ack sending
    EGSE.IF.s_serverConfiguration.egseAck2 = EGSE.IF.ENABLE_NAK
    # notify the GUI
    self.notifyGUItask("EGSE_ENABLED_NAK2")
    return True
  def egseDisableAck2Cmd(self, argv):
    """Decoded egseDisableAck2 command"""
    self.logMethod("egseDisableAck2Cmd", "EGSE")
    # consistency check
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed for egseDisableAck2", "EGSE")
      return False
    # enable the ack sending
    EGSE.IF.s_serverConfiguration.egseAck2 = EGSE.IF.DISABLE_ACK
    # notify the GUI
    self.notifyGUItask("EGSE_DISABLED_ACK2")
    return True
  # ---------------------------------------------------------------------------
  def setPacketDataCmd(self, argv, extraData):
    """Decoded setPacketData command"""
    self.logMethod("setPacketDataCmd", "SPACE")

    # consistency check
    if len(argv) != 2 and len(argv) != 4:
      LOG_WARNING("invalid parameters passed for setPacketData", "SPACE")
      return False

    # extract the arguments
    pktMnemonic = argv[1]
    if len(argv) == 2:
      params = ""
      values = ""
    else:
      params = argv[2]
      values = argv[3]
    tmStruct = extraData
    # check the packet data
    tmPacketData = SUPP.IF.s_definitions.getTMpacketInjectData(pktMnemonic, params, values, tmStruct)
    if tmPacketData == None:
      LOG_WARNING("invalid data passed for setPacketData", "SPACE")
      return False
    # initialise the packet data
    SPACE.IF.s_configuration.tmPacketData = tmPacketData
    LOG("Packet = " + SPACE.IF.s_configuration.tmPacketData.pktName, "SPACE")
    LOG("SPID = " + str(SPACE.IF.s_configuration.tmPacketData.pktSPID), "SPACE")
    LOG("Parameters and values = " + str(SPACE.IF.s_configuration.tmPacketData.parameterValuesList), "SPACE")

    # notify the GUI
    self.notifyGUItask("PACKETDATA_SET")
    return True
  # ---------------------------------------------------------------------------
  def sendPacketCmd(self, argv, extraData):
    """Decoded sendPacket command"""
    self.logMethod("sendPacketCmd", "SPACE")

    # consistency check
    if len(argv) != 1 and len(argv) != 2 and len(argv) != 4:
      LOG_WARNING("invalid parameters passed for sendPacketCmd", "SPACE")
      return False

    # extract the arguments
    if len(argv) == 1:
      if SPACE.IF.s_configuration.tmPacketData == None:
        LOG_WARNING("packet data not initialised", "SPACE")
        return False
      tmPacketData = SPACE.IF.s_configuration.tmPacketData
    else:
      pktMnemonic = argv[1]
      if len(argv) == 2:
        params = ""
        values = ""
      else:
        params = argv[2]
        values = argv[3]
      tmStruct = extraData
      # check the packet data
      tmPacketData = SUPP.IF.s_definitions.getTMpacketInjectData(pktMnemonic, params, values, tmStruct)
      if tmPacketData == None:
        LOG_WARNING("invalid data passed for sendPacketCmd", "SPACE")
        return False

    # send the packet
    try:
      SPACE.IF.s_onboardComputer.generateTMpacket(tmPacketData)
    except Exception, ex:
      LOG_WARNING("cannot send packet via connection: " + str(ex), "SPACE")
      return False
    return True
  # ---------------------------------------------------------------------------
  def enableCyclicCmd(self, argv):
    """Decoded enableCyclic command"""
    self.logMethod("enableCyclicCmd", "SPACE")

    # consistency check
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed for enableCyclic", "SPACE")
      return False

    SPACE.IF.s_onboardComputer.startCyclicTM()
    return True
  # ---------------------------------------------------------------------------
  def disableCyclicCmd(self, argv):
    """Decoded disableCyclic command"""
    self.logMethod("disableCyclic", "SPACE")

    # consistency check
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed for disableCyclic", "SPACE")
      return False

    SPACE.IF.s_onboardComputer.stopCyclicTM()
    return True
  # ---------------------------------------------------------------------------
  def obcEnableAck1Cmd(self, argv):
    """Decoded obcEnableAck1 command"""
    self.logMethod("obcEnableAck1Cmd", "SPACE")
    # consistency check
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed for obcEnableAck1", "SPACE")
      return False
    # enable the ack sending
    SPACE.IF.s_configuration.obcAck1 = SPACE.IF.ENABLE_ACK
    # notify the GUI
    self.notifyGUItask("OBC_ENABLED_ACK1")
    return True
  def obcEnableNak1Cmd(self, argv):
    """Decoded obcEnableNak1 command"""
    self.logMethod("obcEnableNak1Cmd", "SPACE")
    # consistency check
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed for obcEnableNak1", "SPACE")
      return False
    # enable the ack sending
    SPACE.IF.s_configuration.obcAck1 = SPACE.IF.ENABLE_NAK
    # notify the GUI
    self.notifyGUItask("OBC_ENABLED_NAK1")
    return True
  def obcDisableAck1Cmd(self, argv):
    """Decoded obcDisableAck1 command"""
    self.logMethod("obcDisableAck1Cmd", "SPACE")
    # consistency check
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed for obcDisableAck1", "SPACE")
      return False
    # enable the ack sending
    SPACE.IF.s_configuration.obcAck1 = SPACE.IF.DISABLE_ACK
    # notify the GUI
    self.notifyGUItask("OBC_DISABLED_ACK1")
    return True
  # ---------------------------------------------------------------------------
  def obcEnableAck2Cmd(self, argv):
    """Decoded obcEnableAck2 command"""
    self.logMethod("obcEnableAck2Cmd", "SPACE")
    # consistency check
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed for obcEnableAck2", "SPACE")
      return False
    # enable the ack sending
    SPACE.IF.s_configuration.obcAck2 = SPACE.IF.ENABLE_ACK
    # notify the GUI
    self.notifyGUItask("OBC_ENABLED_ACK2")
    return True
  def obcEnableNak2Cmd(self, argv):
    """Decoded obcEnableNak2 command"""
    self.logMethod("obcEnableNak2Cmd", "SPACE")
    # consistency check
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed for obcEnableNak2", "SPACE")
      return False
    # enable the ack sending
    SPACE.IF.s_configuration.obcAck2 = SPACE.IF.ENABLE_NAK
    # notify the GUI
    self.notifyGUItask("OBC_ENABLED_NAK2")
    return True
  def obcDisableAck2Cmd(self, argv):
    """Decoded obcDisableAck2 command"""
    self.logMethod("obcDisableAck2Cmd", "SPACE")
    # consistency check
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed for obcDisableAck2", "SPACE")
      return False
    # enable the ack sending
    SPACE.IF.s_configuration.obcAck2 = SPACE.IF.DISABLE_ACK
    # notify the GUI
    self.notifyGUItask("OBC_DISABLED_ACK2")
    return True
  # ---------------------------------------------------------------------------
  def obcEnableAck3Cmd(self, argv):
    """Decoded obcEnableAck3 command"""
    self.logMethod("obcEnableAck3Cmd", "SPACE")
    # consistency check
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed for obcEnableAck3", "SPACE")
      return False
    # enable the ack sending
    SPACE.IF.s_configuration.obcAck3 = SPACE.IF.ENABLE_ACK
    # notify the GUI
    self.notifyGUItask("OBC_ENABLED_ACK3")
    return True
  def obcEnableNak3Cmd(self, argv):
    """Decoded obcEnableNak3 command"""
    self.logMethod("obcEnableNak3Cmd", "SPACE")
    # consistency check
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed for obcEnableNak3", "SPACE")
      return False
    # enable the ack sending
    SPACE.IF.s_configuration.obcAck3 = SPACE.IF.ENABLE_NAK
    # notify the GUI
    self.notifyGUItask("OBC_ENABLED_NAK3")
    return True
  def obcDisableAck3Cmd(self, argv):
    """Decoded obcDisableAck3 command"""
    self.logMethod("obcDisableAck3Cmd", "SPACE")
    # consistency check
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed for obcDisableAck3", "SPACE")
      return False
    # enable the ack sending
    SPACE.IF.s_configuration.obcAck3 = SPACE.IF.DISABLE_ACK
    # notify the GUI
    self.notifyGUItask("OBC_DISABLED_ACK3")
    return True
  # ---------------------------------------------------------------------------
  def obcEnableAck4Cmd(self, argv):
    """Decoded obcEnableAck4 command"""
    self.logMethod("obcEnableAck4Cmd", "SPACE")
    # consistency check
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed for obcEnableAck4", "SPACE")
      return False
    # enable the ack sending
    SPACE.IF.s_configuration.obcAck4 = SPACE.IF.ENABLE_ACK
    # notify the GUI
    self.notifyGUItask("OBC_ENABLED_ACK4")
    return True
  def obcEnableNak4Cmd(self, argv):
    """Decoded obcEnableNak4 command"""
    self.logMethod("obcEnableNak4Cmd", "SPACE")
    # consistency check
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed for obcEnableNak4", "SPACE")
      return False
    # enable the ack sending
    SPACE.IF.s_configuration.obcAck4 = SPACE.IF.ENABLE_NAK
    # notify the GUI
    self.notifyGUItask("OBC_ENABLED_NAK4")
    return True
  def obcDisableAck4Cmd(self, argv):
    """Decoded obcDisableAck4 command"""
    self.logMethod("obcDisableAck4Cmd", "SPACE")
    # consistency check
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed for obcDisableAck4", "SPACE")
      return False
    # enable the ack sending
    SPACE.IF.s_configuration.obcAck4 = SPACE.IF.DISABLE_ACK
    # notify the GUI
    self.notifyGUItask("OBC_DISABLED_ACK4")
    return True
  # ---------------------------------------------------------------------------
  def sendAckCmd(self, argv):
    """Decoded sendAck command"""
    self.logMethod("sendAckCmd", "SPACE")

    # consistency check
    if len(argv) != 4:
      LOG_WARNING("invalid parameters passed for TC acknowledgement", "SPACE")
      return False

    # extract the arguments
    apid = int(argv[1])
    ssc = int(argv[2])
    subtypeStr = argv[3]
    if subtypeStr == "1":
      ackType = PUS.SERVICES.TC_ACK_ACCEPT_SUCC
    elif subtypeStr == "2":
      ackType = PUS.SERVICES.TC_ACK_ACCEPT_FAIL
    elif subtypeStr == "3":
      ackType = PUS.SERVICES.TC_ACK_EXESTA_SUCC
    elif subtypeStr == "4":
      ackType = PUS.SERVICES.TC_ACK_EXESTA_FAIL
    elif subtypeStr == "5":
      ackType = PUS.SERVICES.TC_ACK_EXEPRO_SUCC
    elif subtypeStr == "6":
      ackType = PUS.SERVICES.TC_ACK_EXEPRO_FAIL
    elif subtypeStr == "7":
      ackType = PUS.SERVICES.TC_ACK_EXECUT_SUCC
    elif subtypeStr == "8":
      ackType = PUS.SERVICES.TC_ACK_EXECUT_FAIL
    else:
      LOG_ERROR("invalid ackType for TC acknowledgement", "SPACE")
      return False
    SPACE.IF.s_onboardComputer.generateAck(apid, ssc, ackType);
    return True
  # ---------------------------------------------------------------------------
  def recordPacketsCmd(self, argv):
    """Decoded recordPackets command"""
    self.logMethod("recordPacketsCmd", "SPACE")
    # consistency check
    if SUPP.IF.s_tmRecorder.isRecording():
      LOG_WARNING("Packet recording already started", "SPACE")
      return False
    if len(argv) != 2:
      LOG_WARNING("invalid parameters passed for recordPackets", "SPACE")
      return False
    # extract the arguments
    recordFileName = argv[1]
    SUPP.IF.s_tmRecorder.startRecording(recordFileName);
    return True
  # ---------------------------------------------------------------------------
  def stopPacketRecorderCmd(self, argv):
    """Decoded stopPacketRecorder command"""
    self.logMethod("stopPacketRecorderCmd", "SPACE")
    # consistency check
    if not SUPP.IF.s_tmRecorder.isRecording():
      LOG_WARNING("Packet recording not started", "SPACE")
      return False
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed for stopPacketRecorder", "SPACE")
      return False
    SUPP.IF.s_tmRecorder.stopRecording();
    return True
  # ---------------------------------------------------------------------------
  def replayPacketsCmd(self, argv):
    """Decoded replayPackets command"""
    self.logMethod("replayPacketsCmd", "SPACE")

    # consistency check
    if len(argv) != 2:
      LOG_WARNING("invalid parameters passed for replay packets", "SPACE")
      return False

    # extract the arguments
    replayFileName = argv[1]
    SPACE.IF.s_onboardComputer.replayPackets(replayFileName);
    return True
  # ---------------------------------------------------------------------------
  def listPacketsCmd(self, argv):
    """Decoded listPackets command"""
    self.logMethod("listPacketsCmd", "SPACE")
    # consistency check
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed", "SPACE")
      return False
    # dump the packet definitions
    try:
      for tmPktDef in SUPP.IF.s_definitions.getTMpktDefs():
        LOG("TM: " + tmPktDef.pktName + " (SPID = " + str(tmPktDef.pktSPID) + ") - " + tmPktDef.pktDescr, "SPACE")
      for tcPktDef in SUPP.IF.s_definitions.getTCpktDefs():
        LOG("TC: " + tcPktDef.pktName + " (APID = " + str(tcPktDef.pktAPID) + ", TYPE = " + str(tcPktDef.pktType) + ", STPYE = " + str(tcPktDef.pktSType) + ") - " + tcPktDef.pktDescr, "SPACE")
    except Exception, ex:
      LOG_ERROR("MIB Error: " + str(ex), "SPACE")
      return False
    return True
  # ---------------------------------------------------------------------------
  def generateCmd(self, argv):
    """Decoded generate command"""
    self.logMethod("generateCmd", "SPACE")
    # consistency check
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed", "SPACE")
      return False
    # generate the testdata.sim file
    definitionFileName = SUPP.IF.s_definitions.getDefinitionFileName()
    LOG("generate to " + definitionFileName, "SPACE")
    try:
      # update the TM definitions to ensure an actual testdata.sim
      SUPP.IF.s_definitions.createDefinitions()
      LOG(definitionFileName + " generated", "SPACE")
    except Exception, ex:
      LOG_ERROR("Generation Error: " + str(ex), "SPACE")
      return False
    return True
  # ---------------------------------------------------------------------------
  def testCmd(self, argv):
    """Decoded test command"""
    self.logMethod("test", "SPACE")
    # consistency check
    if len(argv) != 2:
      LOG_WARNING("invalid parameters passed", "SPACE")
      return False
    # extract the arguments
    testMode = int(argv[1])
    if testMode == 0:
      LOG_INFO("testmode set to nominal", "SPACE")
    else:
      LOG_WARNING("testmode set to " + str(testMode), "SPACE")
    SPACE.IF.s_testMode = testMode
    return True
  # ---------------------------------------------------------------------------
  def setCCSconnected(self):
    """CCS connection established"""
    EGSE.IF.s_serverConfiguration.connected = True
    self.notifyGUItask("CCS_CONNECTED")
    SPACE.IF.s_configuration.connected = True
    self.notifyGUItask("TM_CONNECTED")
  # ---------------------------------------------------------------------------
  def setCCSdisconnected(self):
    """CCS disconnection established"""
    EGSE.IF.s_serverConfiguration.connected = False
    self.notifyGUItask("CCS_DISCONNECTED")
  # ---------------------------------------------------------------------------
  def setCCSconnected2(self):
    """CCS 2nd connection established"""
    EGSE.IF.s_serverConfiguration.connected2 = True
    self.notifyGUItask("CCS_CONNECTED2")
    SPACE.IF.s_configuration.connected = True
    self.notifyGUItask("TM_CONNECTED")
  # ---------------------------------------------------------------------------
  def setCCSdisconnected2(self):
    """CCS 2nd disconnection established"""
    EGSE.IF.s_serverConfiguration.connected2 = False
    self.notifyGUItask("CCS_DISCONNECTED2")

#############
# functions #
#############
# global shortcut functions for test commands
def help(*argv): UTIL.TASK.s_processingTask.helpCmd(("", ) + argv)
def quit(*argv): UTIL.TASK.s_processingTask.quitCmd(("", ) + argv)
def dumpConfiguration(*argv): UTIL.TASK.s_processingTask.dumpConfigurationCmd(("", ) + argv)
def setPacketData(*argv): UTIL.TASK.s_processingTask.setPacketDataCmd(("", ) + argv)
def sendPacket(*argv): UTIL.TASK.s_processingTask.sendPacketCmd(("", ) + argv)
def enableCyclic(*argv): UTIL.TASK.s_processingTask.enableCyclicCmd(("", ) + argv)
def disableCyclic(*argv): UTIL.TASK.s_processingTask.disableCyclicCmd(("", ) + argv)
def sendAck(*argv): UTIL.TASK.s_processingTask.sendAckCmd(("", ) + argv)
def recordPackets(*argv): UTIL.TASK.s_processingTask.recordPacketsCmd(("", ) + argv)
def stopPacketRecorder(*argv): UTIL.TASK.s_processingTask.stopPacketRecorderCmd(("", ) + argv)
def replayPackets(*argv): UTIL.TASK.s_processingTask.replayPacketsCmd(("", ) + argv)
def obcEnableAck1(*argv): UTIL.TASK.s_processingTask.obcEnableAck1Cmd(("", ) + argv)
def obcEnableNak1(*argv): UTIL.TASK.s_processingTask.obcEnableNak1Cmd(("", ) + argv)
def obcDisableAck1(*argv): UTIL.TASK.s_processingTask.obcDisableAck1Cmd(("", ) + argv)
def obcEnableAck2(*argv): UTIL.TASK.s_processingTask.obcEnableAck2Cmd(("", ) + argv)
def obcEnableNak2(*argv): UTIL.TASK.s_processingTask.obcEnableNak2Cmd(("", ) + argv)
def obcDisableAck2(*argv): UTIL.TASK.s_processingTask.obcDisableAck2Cmd(("", ) + argv)
def obcEnableAck3(*argv): UTIL.TASK.s_processingTask.obcEnableAck3Cmd(("", ) + argv)
def obcEnableNak3(*argv): UTIL.TASK.s_processingTask.obcEnableNak3Cmd(("", ) + argv)
def obcDisableAck3(*argv): UTIL.TASK.s_processingTask.obcDisableAck3Cmd(("", ) + argv)
def obcEnableAck4(*argv): UTIL.TASK.s_processingTask.obcEnableAck4Cmd(("", ) + argv)
def obcEnableNak4(*argv): UTIL.TASK.s_processingTask.obcEnableNak4Cmd(("", ) + argv)
def obcDisableAck4(*argv): UTIL.TASK.s_processingTask.obcDisableAck4Cmd(("", ) + argv)
def listPackets(*argv): UTIL.TASK.s_processingTask.listPacketsCmd(("", ) + argv)
def generate(*argv): UTIL.TASK.s_processingTask.generateCmd(("", ) + argv)
def testCmd(*argv): UTIL.TASK.s_processingTask.testCmd(("", ) + argv)
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
UTIL.TCO.setOBTmissionEpochStr(UTIL.SYS.s_configuration.OBT_MISSION_EPOCH_STR)
UTIL.TCO.setOBTleapSeconds(int(UTIL.SYS.s_configuration.OBT_LEAP_SECONDS))
PUS.PACKET.setTMttTimeProperties(
  UTIL.SYS.s_configuration.TM_TT_TIME_FORMAT,
  int(UTIL.SYS.s_configuration.TM_TT_TIME_BYTE_OFFSET))
PUS.SERVICES.service1_setTCackParamsProperties(
  int(UTIL.SYS.s_configuration.TC_ACK_APID_PARAM_BYTE_OFFSET),
  int(UTIL.SYS.s_configuration.TC_ACK_SSC_PARAM_BYTE_OFFSET))
EGSE.IF.s_serverConfiguration = EGSE.IF.ServerConfiguration()
SPACE.IF.s_configuration = SPACE.IF.Configuration()
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
  gui0view = SCOE.EGSEgui.GUIview(tab0)
  gui1view = SPACEUI.SPACEgui.GUIview(tab1)
  gui2view = SPACEUI.MILgui.GUIview(tab2)
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
SUPP.TMrecorder.init("SPACE")
SPACE.OBC.init(egseMode=True)
SPACE.TMGEN.init()
SPACE.TMRPLY.init()
SPACE.ASW.init()
SPACE.MIL.init()

# create the EGSE server
LOG("Open the EGSE servers")
SCOE.EGSEserver.createEGSEservers(UTIL.SYS.s_configuration.HOST)

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
