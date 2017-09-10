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
# Ground and Spacecraft simulator                                             *
#******************************************************************************
import sys, os
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import CCSDS.TIME
import GRND.IF, GRND.NCTRSDU
import LINK.IF, LINK.TMGEN, LINK.TMTC
import PUS.SERVICES
import SCOS.ENV
import SIM.TMserver, SIM.TCserver, SIM.AdminServer, SIM.GRNDgui, SIM.LINKgui
import SPACE.DEF, SPACE.IF, SPACE.OBC, SPACE.OBQ, SPACE.TMGEN, SPACE.TMRPLY
import SPACEUI.SPACEgui, SPACEUI.OBQgui
import UI.TKI
import UTIL.SYS, UTIL.TASK

#############
# constants #
#############
SYS_CONFIGURATION = [
  ["HOST", "127.0.0.1"],
  ["NCTRS_ADMIN_SERVER_PORT", "13006"],
  ["NCTRS_TC_SERVER_PORT", "13007"],
  ["NCTRS_TM_SERVER_PORT", "2502"],
  ["SPACECRAFT_ID", "758"],
  ["DEF_GROUND_STATION_ID", "10"],
  ["GROUND_STATION_NAME", "ESA G/S "],
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
  ["TC_TT_TIME_FORMAT", "CUC"],
  ["TC_TT_TIME_BYTE_OFFSET", "<<shall be passed as environment variable>>"],
  ["TC_TT_FINE_TIME_BYTE_SIZE", "2"],
  ["TC_TT_PKT_BYTE_OFFSET", "<<shall be passed as environment variable>>"],
  ["TM_CYCLIC_MNEMO", "<<shall be passed as environment variable>>"],
  ["TM_CYCLIC_PERIOD_MS", "5000"],
  ["TM_TT_TIME_FORMAT", "CUC"],
  ["TM_TT_TIME_BYTE_OFFSET", "<<shall be passed as environment variable>>"],
  ["TM_TT_FINE_TIME_BYTE_SIZE", "2"],
  ["TM_RECORD_FORMAT", "CRYOSAT"],
  ["TM_REPLAY_KEY", "SPID"],
  ["OBT_MISSION_EPOCH_STR", CCSDS.TIME.TAI_MISSION_EPOCH_STR],
  ["OBT_LEAP_SECONDS", str(CCSDS.TIME.GPS_LEAP_SECONDS_2015)],
  ["ERT_MISSION_EPOCH_STR", CCSDS.TIME.TAI_MISSION_EPOCH_STR],
  ["ERT_LEAP_SECONDS", str(CCSDS.TIME.GPS_LEAP_SECONDS_2015)],
  ["SYS_COLOR_LOG", "1"],
  ["SYS_APP_MNEMO", "SIM"],
  ["SYS_APP_NAME", "Simulator"],
  ["SYS_APP_VERSION", "1.0"]]

###########
# classes #
###########
# =============================================================================
class ModelTask(UTIL.TASK.ProcessingTask):
  """The Simulator is the processing model"""
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
    elif (cmd == "I") or (cmd == "INITIALISEAD"):
      retStatus = self.initialiseADcmd(argv)
    elif (cmd == "AA") or (cmd == "GRNDENABLEACK1"):
      retStatus = self.grndEnableAck1Cmd(argv)
    elif (cmd == "NA") or (cmd == "GRNDENABLENAK1"):
      retStatus = self.grndEnableNak1Cmd(argv)
    elif (cmd == "DA") or (cmd == "GRNDDISABLEACK1"):
      retStatus = self.grndDisableAck1Cmd(argv)
    elif (cmd == "AB") or (cmd == "GRNDENABLEACK2"):
      retStatus = self.grndEnableAck2Cmd(argv)
    elif (cmd == "NB") or (cmd == "GRNDENABLENAK2"):
      retStatus = self.grndEnableNak2Cmd(argv)
    elif (cmd == "DB") or (cmd == "GRNDDISABLEACK2"):
      retStatus = self.grndDisableAck2Cmd(argv)
    elif (cmd == "RF") or (cmd == "RECORDFRAMES"):
      retStatus = self.recordFramesCmd(argv)
    elif (cmd == "SR") or (cmd == "STOPFRAMERECORDER"):
      retStatus = self.stopFrameRecorderCmd(argv)
    elif (cmd == "T") or (cmd == "SETCLCW"):
      retStatus = self.setCLCWcmd(argv)
    elif (cmd == "V") or (cmd == "ENABLECLCW"):
      retStatus = self.enableCLCWcmd(argv)
    elif (cmd == "W") or (cmd == "DISABLECLCW"):
      retStatus = self.disableCLCWcmd(argv)
    elif (cmd == "O") or (cmd == "SETLOCKOUT"):
      retStatus = self.setLockoutCmd(argv)
    elif (cmd == "R") or (cmd == "RESETLOCKOUT"):
      retStatus = self.resetLockoutCmd(argv)
    elif (cmd == "P") or (cmd == "SETPACKETDATA"):
      retStatus = self.setPacketDataCmd(argv)
    elif (cmd == "S") or (cmd == "SENDPACKET"):
      retStatus = self.sendPacketCmd(argv)
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
    elif (cmd == "RP") or (cmd == "REPLAYPACKETS"):
      retStatus = self.replayPacketsCmd(argv)
    elif (cmd == "L") or (cmd == "LISTPACKETS"):
      retStatus = self.listPacketsCmd(argv)
    elif (cmd == "G") or (cmd == "GENERATE"):
      retStatus = self.generateCmd(argv)
    elif (cmd == "A5") or (cmd == "OBQENABLEACK1"):
      retStatus = self.obqEnableAck1Cmd(argv)
    elif (cmd == "N5") or (cmd == "OBQENABLENAK1"):
      retStatus = self.obqEnableNak1Cmd(argv)
    elif (cmd == "D5") or (cmd == "OBQDISABLEACK1"):
      retStatus = self.obqDisableAck1Cmd(argv)
    elif (cmd == "A6") or (cmd == "OBQENABLEACK2"):
      retStatus = self.obqEnableAck2Cmd(argv)
    elif (cmd == "N6") or (cmd == "OBQENABLENAK2"):
      retStatus = self.obqEnableNak2Cmd(argv)
    elif (cmd == "D6") or (cmd == "OBQDISABLEACK2"):
      retStatus = self.obqDisableAck2Cmd(argv)
    elif (cmd == "A7") or (cmd == "OBQENABLEACK3"):
      retStatus = self.obqEnableAck3Cmd(argv)
    elif (cmd == "N7") or (cmd == "OBQENABLENAK3"):
      retStatus = self.obqEnableNak3Cmd(argv)
    elif (cmd == "D7") or (cmd == "OBQDISABLEACK3"):
      retStatus = self.obqDisableAck3Cmd(argv)
    elif (cmd == "A8") or (cmd == "OBQENABLEACK4"):
      retStatus = self.obqEnableAck4Cmd(argv)
    elif (cmd == "N8") or (cmd == "OBQENABLENAK4"):
      retStatus = self.obqEnableNak4Cmd(argv)
    elif (cmd == "D8") or (cmd == "OBQDISABLEACK4"):
      retStatus = self.obqDisableAck4Cmd(argv)
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
    LOG_INFO("Available ground segment commands:", "GRND")
    LOG("", "GRND")
    LOG("x  | exit ...............terminates client connection (only for TCP/IP clients)", "GRND")
    LOG("h  | help ...............provides this information", "GRND")
    LOG("q  | quit ...............terminates SIM application", "GRND")
    LOG("u  | dumpConfiguration...dumps the configuration", "GRND")
    LOG("i  | initialiseAD........initialise AD mode", "GRND")
    LOG("aa | grndEnableAck1......enables autom. sending of ACK1 for TCs", "GRND")
    LOG("na | grndEnableNak1......enables autom. sending of NAK1 for TCs", "GRND")
    LOG("da | grndDisableAck1.....disables autom. sending of ACK1 for TCs", "GRND")
    LOG("ab | grndEnableAck2......enables autom. sending of ACK2 for TCs", "GRND")
    LOG("nb | grndEnableNak2......enables autom. sending of NAK2 for TCs", "GRND")
    LOG("db | grndDisableAck2.....disables autom. sending of ACK2 for TCs", "GRND")
    LOG("rf | recordFrames <recordFile> records TM frames", "GRND")
    LOG("sr | stopFrameRecorder...stops recording of TM frames", "GRND")
    LOG_INFO("Available space link commands:", "LINK")
    LOG("", "LINK")
    LOG("x | exit ................terminates client connection (only for TCP/IP clients)", "LINK")
    LOG("h | help ................provides this information", "LINK")
    LOG("q | quit ................terminates SIM application", "LINK")
    LOG("u | dumpConfiguration....dumps the configuration", "LINK")
    LOG("t | setCLCW <value>......set the CLCW report value", "LINK")
    LOG("v | enableCLCW...........enables autom. sending of CLCW", "LINK")
    LOG("w | disableCLCW..........disables autom. sending of CLCW", "LINK")
    LOG("o | setLockout...........set lockout flag in CLCW", "LINK")
    LOG("r | resetLockout.........reset lockout flag in CLCW", "LINK")
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
    LOG("rp | replayPackets <replayFile> replays TM packets", "SPACE")
    LOG("l  | listPackets.........lists available packets", "SPACE")
    LOG("g  | generate............generates the testdata.sim file in testbin directory", "SPACE")
    LOG_INFO("Available onboard queue commands:", "OBQ")
    LOG("", "OBQ")
    LOG("x  | exit ...............terminates client connection (only for TCP/IP clients)", "OBQ")
    LOG("h  | help ...............provides this information", "OBQ")
    LOG("q  | quit ...............terminates SIM application", "OBQ")
    LOG("u  | dumpConfiguration...dumps the configuration", "OBQ")
    LOG("a5 | obqEnableAck1.......enables autom. sending of ACK1 for OBQ TCs", "OBQ")
    LOG("n5 | obqEnableNak1.......enables autom. sending of NAK1 for OBQ TCs", "OBQ")
    LOG("d5 | obqDisableAck1......disables autom. sending of ACK1 for OBQ TCs", "OBQ")
    LOG("a6 | obqEnableAck2.......enables autom. sending of ACK2 for OBQ TCs", "OBQ")
    LOG("n6 | obqEnableNak2.......enables autom. sending of NaK2 for OBQ TCs", "OBQ")
    LOG("d6 | obqDisableAck2......disables autom. sending of ACK2 for OBQ TCs", "OBQ")
    LOG("a7 | obqEnableAck3.......enables autom. sending of ACK3 for OBQ TCs", "OBQ")
    LOG("n7 | obqEnableNak3.......enables autom. sending of NAK3 for OBQ TCs", "OBQ")
    LOG("d7 | obqDisableAck3......disables autom. sending of ACK3 for OBQ TCs", "OBQ")
    LOG("a8 | obqEnableAck4.......enables autom. sending of ACK4 for OBQ TCs", "OBQ")
    LOG("n8 | obqEnableNak4.......enables autom. sending of NAK4 for OBQ TCs", "OBQ")
    LOG("d8 | obqDisableAck4......disables autom. sending of ACK4 for OBQ TCs", "OBQ")
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
    GRND.IF.s_configuration.dump()
    LINK.IF.s_configuration.dump()
    SPACE.IF.s_configuration.dump()
    return True
  # ---------------------------------------------------------------------------
  def initialiseADcmd(self, argv):
    """Decoded initialiseAD command"""
    self.logMethod("initialiseADcmd", "LINK")
    SIM.AdminServer.sendAdminMessageTC(GRND.NCTRSDU.ADMIN_MSG_TC_AD_SERVICE_AVAILABLE_FROM_GS)
    return True
  # ---------------------------------------------------------------------------
  def grndEnableAck1Cmd(self, argv):
    """Decoded grndEnableAck1 command"""
    self.logMethod("grndEnableAck1Cmd", "GRND")
    # consistency check
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed for grndEnableAck1", "GRND")
      return False
    # enable the ack sending
    GRND.IF.s_configuration.grndAck1 = GRND.IF.ENABLE_ACK
    # notify the GUI
    self.notifyGUItask("GRND_ENABLED_ACK1")
    return True
  def grndEnableNak1Cmd(self, argv):
    """Decoded grndEnableNak1 command"""
    self.logMethod("grndEnableNak1Cmd", "GRND")
    # consistency check
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed for grndEnableNak1", "GRND")
      return False
    # enable the ack sending
    GRND.IF.s_configuration.grndAck1 = GRND.IF.ENABLE_NAK
    # notify the GUI
    self.notifyGUItask("GRND_ENABLED_NAK1")
    return True
  def grndDisableAck1Cmd(self, argv):
    """Decoded grndDisableAck1 command"""
    self.logMethod("grndDisableAck1Cmd", "GRND")
    # consistency check
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed for grndDisableAck1", "GRND")
      return False
    # enable the ack sending
    GRND.IF.s_configuration.grndAck1 = GRND.IF.DISABLE_ACK
    # notify the GUI
    self.notifyGUItask("GRND_DISABLED_ACK1")
    return True
  # ---------------------------------------------------------------------------
  def grndEnableAck2Cmd(self, argv):
    """Decoded grndEnableAck2 command"""
    self.logMethod("grndEnableAck2Cmd", "GRND")
    # consistency check
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed for grndEnableAck2", "GRND")
      return False
    # enable the ack sending
    GRND.IF.s_configuration.grndAck2 = GRND.IF.ENABLE_ACK
    # notify the GUI
    self.notifyGUItask("GRND_ENABLED_ACK2")
    return True
  def grndEnableNak2Cmd(self, argv):
    """Decoded grndEnableNak2 command"""
    self.logMethod("grndEnableNak2Cmd", "GRND")
    # consistency check
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed for grndEnableNak2", "GRND")
      return False
    # enable the ack sending
    GRND.IF.s_configuration.grndAck2 = GRND.IF.ENABLE_NAK
    # notify the GUI
    self.notifyGUItask("GRND_ENABLED_NAK2")
    return True
  def grndDisableAck2Cmd(self, argv):
    """Decoded grndDisableAck2 command"""
    self.logMethod("grndDisableAck2Cmd", "GRND")
    # consistency check
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed for grndDisableAck2", "GRND")
      return False
    # enable the ack sending
    GRND.IF.s_configuration.grndAck2 = GRND.IF.DISABLE_ACK
    # notify the GUI
    self.notifyGUItask("GRND_DISABLED_ACK2")
    return True
  # ---------------------------------------------------------------------------
  def recordFramesCmd(self, argv):
    """decoded recordFrames command"""
    self.logMethod("recordFramesCmd", "GRND")
    # consistency check
    if GRND.IF.s_configuration.frameRecordFile:
      LOG_WARNING("Frame recording already started", "GRND")
      return False
    if len(argv) != 2:
      LOG_WARNING("invalid parameters passed for recordFrames", "GRND")
      return False
    # extract the arguments
    recordFileName = argv[1]
    GRND.IF.s_tmMcsLink.recordFrames(recordFileName);
    return True
  # ---------------------------------------------------------------------------
  def stopFrameRecorderCmd(self, argv):
    """decoded stopFrameRecorder command"""
    self.logMethod("stopFrameRecorderCmd", "GRND")
    # consistency check
    if not GRND.IF.s_configuration.frameRecordFile:
      LOG_WARNING("Frame recording not started", "GRND")
      return False
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed for stopFrameRecorder", "GRND")
      return False
    GRND.IF.s_tmMcsLink.stopFrameRecorder();
    return True
  # ---------------------------------------------------------------------------
  def setCLCWcmd(self, argv):
    """Decoded setCLCW command"""
    self.logMethod("setCLCWcmd", "LINK")

    # consistency check
    if len(argv) != 2:
      LOG_WARNING("invalid parameters passed for setCLCW", "LINK")
      return False

    # extract the arguments
    try:
      reportValue = int(argv[1])
    except:
      LOG_WARNING("invalid format for CLCW report value (should be 0...255)", "LINK")
      return False
    if reportValue < 0 or reportValue > 255:
      LOG_WARNING("invalid value for CLCW report value (should be 0...255)", "LINK")
      return False

    # set the CLCW sequenceNumber
    LINK.IF.s_tmFrameGenerator.setCLCWcount(reportValue)
    return True
  # ---------------------------------------------------------------------------
  def enableCLCWcmd(self, argv):
    """Decoded enableCLCW command"""
    self.logMethod("enableCLCWcmd", "LINK")
    # consistency check
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed for enableCLCW", "LINK")
      return False
    # enable the CLCW sending
    LINK.IF.s_configuration.enableCLCW = True
    # notify the GUI
    self.notifyGUItask("ENABLED_CLCW")
    return True
  # ---------------------------------------------------------------------------
  def disableCLCWcmd(self, argv):
    """Decoded disableCLCW command"""
    self.logMethod("disableCLCWcmd", "LINK")
    # consistency check
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed for disableCLCW", "LINK")
      return False
    # disable the CLCW sending
    LINK.IF.s_configuration.enableCLCW = False
    # notify the GUI
    self.notifyGUItask("DISABLED_CLCW")
    return True
  # ---------------------------------------------------------------------------
  def setLockoutCmd(self, argv):
    """Decoded setLockout command"""
    self.logMethod("setLockoutCmd", "LINK")
    # consistency check
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed for setLockoutCmd", "LINK")
      return False
    clcwDefaults = LINK.IF.CLCWdefaults()
    clcwDefaults.lockout = 1
    LINK.IF.s_tmFrameGenerator.initCLCW(clcwDefaults)
    # notify the GUI
    self.notifyGUItask("LOCKOUT_SET")
    return True
  # ---------------------------------------------------------------------------
  def resetLockoutCmd(self, argv):
    """Decoded resetLockout command"""
    self.logMethod("resetLockoutCmd", "LINK")
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed for resetLockoutCmd", "LINK")
      return False
    clcwDefaults = LINK.IF.CLCWdefaults()
    clcwDefaults.lockout = 0
    LINK.IF.s_tmFrameGenerator.initCLCW(clcwDefaults)
    # notify the GUI
    self.notifyGUItask("LOCKOUT_RESET")
    return True
  # ---------------------------------------------------------------------------
  def setPacketDataCmd(self, argv):
    """Decoded setPacketData command"""
    self.logMethod("setPacketDataCmd", "SPACE")

    # consistency check
    if len(argv) != 2 and len(argv) != 4:
      LOG_WARNING("invalid parameters passed for TM connection", "SPACE")
      return False

    # extract the arguments
    pktMnemonic = argv[1]
    if len(argv) == 2:
      params = ""
      values = ""
    else:
      params = argv[2]
      values = argv[3]
    # check the packet data
    tmPacketData = SPACE.IF.s_definitions.getTMpacketInjectData(pktMnemonic, params, values)
    if tmPacketData == None:
      LOG_WARNING("invalid data passed for TM connection", "SPACE")
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
  def sendPacketCmd(self, argv):
    """Decoded sendPacket command"""
    self.logMethod("sendPacketCmd", "SPACE")

    # consistency check
    if len(argv) != 1 and len(argv) != 2 and len(argv) != 4:
      LOG_WARNING("invalid parameters passed for TM connection", "SPACE")
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
      # check the packet data
      tmPacketData = SPACE.IF.s_definitions.getTMpacketInjectData(pktMnemonic, params, values)
      if tmPacketData == None:
        LOG_WARNING("invalid data passed for TM connection", "SPACE")
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
    # read the MIB 
    try:
      for tmPktDef in SPACE.IF.s_definitions.getTMpktDefs():
        LOG(tmPktDef.pktName + " (SPID = " + str(tmPktDef.pktSPID) + ") - " + tmPktDef.pktDescr, "SPACE")
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
    definitionFileName = SCOS.ENV.s_environment.definitionFileName()
    LOG("generate to " + definitionFileName, "SPACE")
    try:
      # update the TM definitions to ensure an actual testdata.sim
      SPACE.IF.s_definitions.createDefinitions()
      LOG(definitionFileName + " generated", "SPACE")
    except Exception, ex:
      LOG_ERROR("Generation Error: " + str(ex), "SPACE")
      return False
    return True
  # ---------------------------------------------------------------------------
  def obqEnableAck1Cmd(self, argv):
    """Decoded obqEnableAck1 command"""
    self.logMethod("obqEnableAck1Cmd", "OBQ")
    # consistency check
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed for obqEnableAck1", "OBQ")
      return False
    # enable the ack sending
    SPACE.IF.s_configuration.obqAck1 = SPACE.IF.ENABLE_ACK
    # notify the GUI
    self.notifyGUItask("OBQ_ENABLED_ACK1")
    return True
  def obqEnableNak1Cmd(self, argv):
    """Decoded obqEnableNak1 command"""
    self.logMethod("obqEnableNak1Cmd", "OBQ")
    # consistency check
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed for obqEnableNak1", "OBQ")
      return False
    # enable the ack sending
    SPACE.IF.s_configuration.obqAck1 = SPACE.IF.ENABLE_NAK
    # notify the GUI
    self.notifyGUItask("OBQ_ENABLED_NAK1")
    return True
  def obqDisableAck1Cmd(self, argv):
    """Decoded obqDisableAck1 command"""
    self.logMethod("obqDisableAck1Cmd", "OBQ")
    # consistency check
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed for obqDisableAck1", "OBQ")
      return False
    # enable the ack sending
    SPACE.IF.s_configuration.obqAck1 = SPACE.IF.DISABLE_ACK
    # notify the GUI
    self.notifyGUItask("OBQ_DISABLED_ACK1")
    return True
  # ---------------------------------------------------------------------------
  def obqEnableAck2Cmd(self, argv):
    """Decoded obqEnableAck2 command"""
    self.logMethod("obqEnableAck2Cmd", "OBQ")
    # consistency check
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed for obqEnableAck2", "OBQ")
      return False
    # enable the ack sending
    SPACE.IF.s_configuration.obqAck2 = SPACE.IF.ENABLE_ACK
    # notify the GUI
    self.notifyGUItask("OBQ_ENABLED_ACK2")
    return True
  def obqEnableNak2Cmd(self, argv):
    """Decoded obqEnableNak2 command"""
    self.logMethod("obqEnableNak2Cmd", "OBQ")
    # consistency check
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed for obqEnableNak2", "OBQ")
      return False
    # enable the ack sending
    SPACE.IF.s_configuration.obqAck2 = SPACE.IF.ENABLE_NAK
    # notify the GUI
    self.notifyGUItask("OBQ_ENABLED_NAK2")
    return True
  def obqDisableAck2Cmd(self, argv):
    """Decoded obqDisableAck2 command"""
    self.logMethod("obqDisableAck2Cmd", "OBQ")
    # consistency check
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed for obqDisableAck2", "OBQ")
      return False
    # enable the ack sending
    SPACE.IF.s_configuration.obqAck2 = SPACE.IF.DISABLE_ACK
    # notify the GUI
    self.notifyGUItask("OBQ_DISABLED_ACK2")
    return True
  # ---------------------------------------------------------------------------
  def obqEnableAck3Cmd(self, argv):
    """Decoded obqEnableAck3 command"""
    self.logMethod("obqEnableAck3Cmd", "OBQ")
    # consistency check
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed for obqEnableAck3", "OBQ")
      return False
    # enable the ack sending
    SPACE.IF.s_configuration.obqAck3 = SPACE.IF.ENABLE_ACK
    # notify the GUI
    self.notifyGUItask("OBQ_ENABLED_ACK3")
    return True
  def obqEnableNak3Cmd(self, argv):
    """Decoded obqEnableNak3 command"""
    self.logMethod("obqEnableNak3Cmd", "OBQ")
    # consistency check
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed for obqEnableNak3", "OBQ")
      return False
    # enable the ack sending
    SPACE.IF.s_configuration.obqAck3 = SPACE.IF.ENABLE_NAK
    # notify the GUI
    self.notifyGUItask("OBQ_ENABLED_NAK3")
    return True
  def obqDisableAck3Cmd(self, argv):
    """Decoded obqDisableAck3 command"""
    self.logMethod("obqDisableAck3Cmd", "OBQ")
    # consistency check
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed for obqDisableAck3", "OBQ")
      return False
    # enable the ack sending
    SPACE.IF.s_configuration.obqAck3 = SPACE.IF.DISABLE_ACK
    # notify the GUI
    self.notifyGUItask("OBQ_DISABLED_ACK3")
    return True
  # ---------------------------------------------------------------------------
  def obqEnableAck4Cmd(self, argv):
    """Decoded obqEnableAck4 command"""
    self.logMethod("obqEnableAck4Cmd", "OBQ")
    # consistency check
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed for obqEnableAck4", "OBQ")
      return False
    # enable the ack sending
    SPACE.IF.s_configuration.obqAck4 = SPACE.IF.ENABLE_ACK
    # notify the GUI
    self.notifyGUItask("OBQ_ENABLED_ACK4")
    return True
  def obqEnableNak4Cmd(self, argv):
    """Decoded obqEnableNak4 command"""
    self.logMethod("obqEnableNak4Cmd", "OBQ")
    # consistency check
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed for obqEnableNak4", "OBQ")
      return False
    # enable the ack sending
    SPACE.IF.s_configuration.obqAck4 = SPACE.IF.ENABLE_NAK
    # notify the GUI
    self.notifyGUItask("OBQ_ENABLED_NAK4")
    return True
  def obqDisableAck4Cmd(self, argv):
    """Decoded obqDisableAck4 command"""
    self.logMethod("obqDisableAck4Cmd", "OBQ")
    # consistency check
    if len(argv) != 1:
      LOG_WARNING("invalid parameters passed for obqDisableAck4", "OBQ")
      return False
    # enable the ack sending
    SPACE.IF.s_configuration.obqAck4 = SPACE.IF.DISABLE_ACK
    # notify the GUI
    self.notifyGUItask("OBQ_DISABLED_ACK4")
    return True
  # ---------------------------------------------------------------------------
  def setTMconnected(self):
    """TM connection established"""
    GRND.IF.s_configuration.nctrsTMconn = True
    SPACE.IF.s_configuration.connected = True
    self.notifyGUItask("TM_CONNECTED")
  # ---------------------------------------------------------------------------
  def setTCconnected(self):
    """TC connection established"""
    GRND.IF.s_configuration.nctrsTCconn = True
    self.notifyGUItask("TC_CONNECTED")
  # ---------------------------------------------------------------------------
  def setAdminConnected(self):
    """Admin notification connection established"""
    GRND.IF.s_configuration.nctrsAdminConn = True
    self.notifyGUItask("ADMIN_CONNECTED")

#############
# functions #
#############
# global shortcut functions for test commands
def help(*argv): UTIL.TASK.s_processingTask.helpCmd(("", ) + argv)
def quit(*argv): UTIL.TASK.s_processingTask.quitCmd(("", ) + argv)
def dumpConfiguration(*argv): UTIL.TASK.s_processingTask.dumpConfigurationCmd(("", ) + argv)
def initialiseAD(*argv): UTIL.TASK.s_processingTask.initialiseADcmd(("", ) + argv)
def grndEnableAck1(*argv): UTIL.TASK.s_processingTask.grndEnableAck1Cmd(("", ) + argv)
def grndEnableNak1(*argv): UTIL.TASK.s_processingTask.grndEnableNak1Cmd(("", ) + argv)
def grndDisableAck1(*argv): UTIL.TASK.s_processingTask.grndDisableAck1Cmd(("", ) + argv)
def grndEnableAck2(*argv): UTIL.TASK.s_processingTask.grndEnableAck2Cmd(("", ) + argv)
def grndEnableNak2(*argv): UTIL.TASK.s_processingTask.grndEnableNak2Cmd(("", ) + argv)
def grndDisableAck2(*argv): UTIL.TASK.s_processingTask.grndDisableAck2Cmd(("", ) + argv)
def recordFrames(*argv): UTIL.TASK.s_processingTask.recordFramesCmd(("", ) + argv)
def stopFrameRecorder(*argv): UTIL.TASK.s_processingTask.stopFrameRecorderCmd(("", ) + argv)
def setCLCW(*argv): UTIL.TASK.s_processingTask.setCLCWcmd(("", ) + argv)
def enableCLCW(*argv): UTIL.TASK.s_processingTask.enableCLCWcmd(("", ) + argv)
def disableCLCW(*argv): UTIL.TASK.s_processingTask.disableCLCWcmd(("", ) + argv)
def setLockout(*argv): UTIL.TASK.s_processingTask.setLockoutCmd(("", ) + argv)
def resetLockout(*argv): UTIL.TASK.s_processingTask.resetLockoutCmd(("", ) + argv)
def setPacketData(*argv): UTIL.TASK.s_processingTask.setPacketDataCmd(("", ) + argv)
def sendPacket(*argv): UTIL.TASK.s_processingTask.sendPacketCmd(("", ) + argv)
def enableCyclic(*argv): UTIL.TASK.s_processingTask.enableCyclicCmd(("", ) + argv)
def disableCyclic(*argv): UTIL.TASK.s_processingTask.disableCyclicCmd(("", ) + argv)
def sendAck(*argv): UTIL.TASK.s_processingTask.sendAckCmd(("", ) + argv)
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
def obqEnableAck1(*argv): UTIL.TASK.s_processingTask.obqEnableAck1Cmd(("", ) + argv)
def obqEnableNak1(*argv): UTIL.TASK.s_processingTask.obqEnableNak1Cmd(("", ) + argv)
def obqDisableAck1(*argv): UTIL.TASK.s_processingTask.obqDisableAck1Cmd(("", ) + argv)
def obqEnableAck2(*argv): UTIL.TASK.s_processingTask.obqEnableAck2Cmd(("", ) + argv)
def obqEnableNak2(*argv): UTIL.TASK.s_processingTask.obqEnableNak2Cmd(("", ) + argv)
def obqDisableAck2(*argv): UTIL.TASK.s_processingTask.obqDisableAck2Cmd(("", ) + argv)
def obqEnableAck3(*argv): UTIL.TASK.s_processingTask.obqEnableAck3Cmd(("", ) + argv)
def obqEnableNak3(*argv): UTIL.TASK.s_processingTask.obqEnableNak3Cmd(("", ) + argv)
def obqDisableAck3(*argv): UTIL.TASK.s_processingTask.obqDisableAck3Cmd(("", ) + argv)
def obqEnableAck4(*argv): UTIL.TASK.s_processingTask.obqEnableAck4Cmd(("", ) + argv)
def obqEnableNak4(*argv): UTIL.TASK.s_processingTask.obqEnableNak4Cmd(("", ) + argv)
def obqDisableAck4(*argv): UTIL.TASK.s_processingTask.obqDisableAck4Cmd(("", ) + argv)
# -----------------------------------------------------------------------------
def printUsage(launchScriptName):
  """Prints the possible commandline options of the test driver"""
  print ""
  print "usage:"
  print "------"
  print ""
  print launchScriptName
  print "\t[ -i | -interpreter | -c | -cmdprompt | -bg | -background ]"
  print "\t[ -n | -nogui ] [ -p <port> | -port <port> ]"
  print "\t[ -l <logfile> | -logfile <logfile> ] [ -h | -help ]"
  print ""

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
CCSDS.TIME.setOBTmissionEpochStr(UTIL.SYS.s_configuration.OBT_MISSION_EPOCH_STR)
CCSDS.TIME.setOBTleapSeconds(int(UTIL.SYS.s_configuration.OBT_LEAP_SECONDS))
CCSDS.TIME.setERTmissionEpochStr(UTIL.SYS.s_configuration.ERT_MISSION_EPOCH_STR)
CCSDS.TIME.setERTleapSeconds(int(UTIL.SYS.s_configuration.ERT_LEAP_SECONDS))
GRND.IF.s_configuration = GRND.IF.Configuration()
LINK.IF.s_configuration = LINK.IF.Configuration()
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
  win0 = UI.TKI.createWindow()
  win1 = UI.TKI.createWindow()
  win2 = UI.TKI.createWindow()
  win3 = UI.TKI.createWindow()
  gui0view = SIM.GRNDgui.GUIview(win0)
  gui1view = SIM.LINKgui.GUIview(win1)
  gui2view = SPACEUI.SPACEgui.GUIview(win2)
  gui3view = SPACEUI.OBQgui.GUIview(win3)
  UI.TKI.finaliseGUIcreation()
else:
  modelTask = ModelTask(isParent=True)
# register the TCP/IP server socket for remote control
if requestHandler.portNr != 0:
  print "register connect port..."
  if not requestHandler.openConnectPort(UTIL.SYS.s_configuration.HOST):
    sys.exit(-1)
  connectSocket = requestHandler.connectSocket
  modelTask.createFileHandler(connectSocket, requestHandler.tcpConnectCallback)
# register the requestHandler as console handler if requested
if cmdPrompt:
  print "register console handler..."
  modelTask.registerConsoleHandler(requestHandler)

# initialise singletons
SPACE.DEF.init()
SPACE.OBC.init(egseMode=False)
SPACE.OBQ.init()
SPACE.TMGEN.init()
SPACE.TMRPLY.init()
LINK.TMTC.init()
LINK.TMGEN.init()

# create the NCTRS servers
LOG("Open the NCTRS TM sender (server)")
SIM.TMserver.createTMsender(UTIL.SYS.s_configuration.HOST)
LOG("Open the NCTRS TC receiver (server)")
SIM.TCserver.createTCreceiver(UTIL.SYS.s_configuration.HOST)
LOG("Open the NCTRS admin message sender (server)")
SIM.AdminServer.createAdminSender(UTIL.SYS.s_configuration.HOST)

# load the definition data
print "load definition data (take some time) ..."
SPACE.IF.s_definitions.initDefinitions()
print "definition data loaded"

# start the tasks
print "start modelTask..."
modelTask.start()
if guiMode:
  print "start guiTask..."
  guiTask.start()
  print "guiTask terminated"
  modelTask.join()
print "modelTask terminated"
