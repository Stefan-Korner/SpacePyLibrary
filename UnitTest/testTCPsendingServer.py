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
# Unit Tests                                                                  *
#******************************************************************************
import sys
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import UTIL.TCP, UTIL.SYS

###########
# classes #
###########
# =============================================================================
class TCPsendingServer(UTIL.TCP.Server):
  """Subclass of UTIL.TCP.Server"""
  # ---------------------------------------------------------------------------
  def __init__(self, eventLoop, portNr):
    UTIL.TCP.Server.__init__(self, eventLoop, portNr)
    self.clientSocket = None
  # ---------------------------------------------------------------------------
  def accepted(self, clientSocket):
    """Client has connected"""
    LOG("*** accepted ***")
    self.clientSocket = clientSocket
    self.clientSocket.send("connected\n")
    # prepare a timer that calls the after method one second ago
    UTIL.SYS.s_eventLoop.createtimehandler(1000, self.after)
  # ---------------------------------------------------------------------------
  def after(self):
    """Called from a timer 1 second after connect"""
    LOG("*** after ***")
    self.clientSocket.send("quit\n")

###########################
# Initialisation sequence #
###########################
# register a console handler for termination
consoleHandler = UTIL.SYS.ConsoleHandler()
# create the TCP/IP sender
LOG("Open the TCP server")
server = TCPsendingServer(UTIL.SYS.s_eventLoop, portNr=1234)
if not server.openConnectPort():
  sys.exit(-1)
# start the event loop
LOG("Start the event loop...")
UTIL.SYS.s_eventLoop.start()
sys.exit(0)
