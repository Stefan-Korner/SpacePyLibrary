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
import os, sys
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import UTIL.TCP, UTIL.SYS

###########################
# Initialisation sequence #
###########################
# create the TCP/IP cient
LOG("Open the TCP client")
client = UTIL.TCP.Client()
hostName = os.getenv("HOST")
if hostName == None:
  #hostName = "10.0.0.100"
  hostName = "192.168.178.46"
dataSocket = client.connectToServer(hostName, 1234)
if not dataSocket:
  sys.exit(-1)
dataSocket.send("quit\n")
dataSocket.close()
sys.exit(0)
