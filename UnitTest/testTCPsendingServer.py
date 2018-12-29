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
# Unit Tests                                                                  *
#******************************************************************************
import sys
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import UTIL.SYS, UTIL.TASK, UTIL.TCP

#############
# constants #
#############
MAXBYTESREAD = 256

###########
# classes #
###########
# =============================================================================
class TCPsendingServer(UTIL.TCP.SingleClientReceivingServer):
  """Subclass of UTIL.TCP.SingleClientReceivingServer"""
  # ---------------------------------------------------------------------------
  def __init__(self, portNr):
    modelTask = UTIL.TASK.s_processingTask
    UTIL.TCP.SingleClientReceivingServer.__init__(self, modelTask, portNr)
  # ---------------------------------------------------------------------------
  def accepted(self, clientSocket):
    """Overloaded from SingleClientReceivingServer"""
    UTIL.TCP.SingleClientReceivingServer.accepted(self, clientSocket)
    self.dataSocket.send("connected\n")
    # prepare a timer that calls the after method one second ago
    UTIL.TASK.s_processingTask.createTimeHandler(1000, self.after)
  # ---------------------------------------------------------------------------
  def receiveCallback(self, socket, stateMask):
    """Callback when data are received"""
    LOG("*** TCPsendingServer.receiveCallback ***")
    try:
      data = self.dataSocket.recv(MAXBYTESREAD)
    except Exception as ex:
      # read failed
      LOG_ERROR("Read failed: " + str(ex))
    if len(data) == 0:
      LOG_ERROR("invalid data read, len(data) = " + str(len(data)))
      LOG("client will be dis-connected...")
      self.disconnectClient()
    else:
      LOG("data read, len(data) = " + str(len(data)))
      LOG("data = " + data.decode("ascii"))      
  # ---------------------------------------------------------------------------
  def after(self):
    """Called from a timer 1 second after connect"""
    LOG("*** after ***")
    self.dataSocket.send("quit\n")

#############
# functions #
#############
# -----------------------------------------------------------------------------
def initConfiguration():
  """initialise the system configuration"""
  UTIL.SYS.s_configuration.setDefaults([
    ["HOST", "127.0.0.1"],
    ["SERVER_PORT", "1234"]])
# -----------------------------------------------------------------------------
def createServer():
  """create the TCP server"""
  server = TCPsendingServer(portNr=int(UTIL.SYS.s_configuration.SERVER_PORT))
  if not server.openConnectPort(UTIL.SYS.s_configuration.HOST):
    sys.exit(-1)

########
# main #
########
if __name__ == "__main__":
  # initialise the system configuration
  initConfiguration()
  # initialise the console handler
  consoleHandler = UTIL.TASK.ConsoleHandler()
  # initialise the model
  modelTask = UTIL.TASK.ProcessingTask(isParent=True)
  # register the console handler
  modelTask.registerConsoleHandler(consoleHandler)
  # create the TCP server
  LOG("Open the TCP server")
  createServer()
  # start the tasks
  LOG("start modelTask...")
  modelTask.start()
