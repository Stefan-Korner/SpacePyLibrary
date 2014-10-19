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
# SCOE reference implementation: uses EDEN interface for CCS connection       *
#******************************************************************************
import sys, os
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import EGSE.EDEN
import SCOE.EGSEserver, SCOE.EGSEgui
import UI.TKI
import UTIL.SYS, UTIL.TASK

#############
# constants #
#############
SYS_CONFIGURATION = [
  ["HOST", "192.168.1.100"],
  ["EDEN_SERVER_PORT", "48569"],
  ["SYS_COLOR_LOG", "1"],
  ["SYS_APP_MNEMO", "SCOE"],
  ["SYS_APP_NAME", "Special Checkout Equipment"],
  ["SYS_APP_VERSION", "1.0"]]

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
    EGSE.IF.s_configuration.dump()
    return True
  # ---------------------------------------------------------------------------
  def setCCSconnected(self):
    """CCS connection established"""
    EGSE.IF.s_configuration.connected = True
    #SPACE.IF.s_configuration.connected = True
    self.notifyGUItask("CCS_CONNECTED")

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
print "*** sys.argv =", sys.argv
if sys.argv[0] == "":
  interpreter = True
  sys.argv = os.getenv("ARGS").split()
  launchScriptName = sys.argv[0]
else:
  interpreter = False
  launchScriptName = sys.argv[1]
# initialise the system configuration
UTIL.SYS.s_configuration.setDefaults(SYS_CONFIGURATION)
#UTIL.TIME.setMissionEpochStr(UTIL.SYS.s_configuration.TCO_MISSION_EPOCH_STR)
EGSE.IF.s_configuration = EGSE.IF.Configuration()
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
  gui0view = SCOE.EGSEgui.GUIview(win0)
  UI.TKI.finaliseGUIcreation()
else:
  modelTask = ModelTask(isParent=True)
# register the TCP/IP server socket for remote control
if requestHandler.portNr != 0:
  print "register connect port..."
  if not requestHandler.openConnectPort():
    sys.exit(-1)
  connectSocket = requestHandler.connectSocket
  modelTask.createFileHandler(connectSocket, requestHandler.tcpConnectCallback)
# register the requestHandler as console handler if requested
if cmdPrompt:
  print "register console handler..."
  modelTask.registerConsoleHandler(requestHandler)

# initialise singletons
#TODO

# create the EGSE server
LOG("Open the EGSE server")
SCOE.EGSEserver.createEGSEserver()

# load the definition data
#TODO

# start the tasks
print "start modelTask..."
modelTask.start()
if guiMode:
  print "start guiTask..."
  guiTask.start()
  print "guiTask terminated"
  modelTask.join()
print "modelTask terminated"
