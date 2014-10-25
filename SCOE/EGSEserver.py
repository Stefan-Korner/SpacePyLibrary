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
# EGSE server for connection to CCS                                           *
#******************************************************************************
import sys
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import CCSDS.PACKET
import EGSE.EDEN, EGSE.IF
import SPACE.IF
import UTIL.SYS, UTIL.TASK

###########
# classes #
###########
# =============================================================================
class Server(EGSE.EDEN.Server, EGSE.IF.CCSlink):
  """Subclass of GRND.NCTRS.TCreceiver"""
  # ---------------------------------------------------------------------------
  def __init__(self, portNr):
    """Initialise attributes only"""
    EGSE.EDEN.Server.__init__(self, portNr)
  # ---------------------------------------------------------------------------
  def clientAccepted(self):
    """Overloaded from GRND.NCTRS.TCreceiver"""
    LOG_INFO("CCS client accepted", "EGSE")
    # notify the status change
    UTIL.TASK.s_processingTask.setCCSconnected()
  # ---------------------------------------------------------------------------
  def pushTMpacket(self, tmPacketDu):
    """
    consumes a telemetry packet:
    implementation of EGSE.IF.CCSlink.pushTMpacket
    """
    # we expect a SPACE packet and not a SCOE packet
    self.sendTmSpace(tmPacketDu.buffer)
  # ---------------------------------------------------------------------------
  def notifyError(self, errorMessage, data):
    """error notification"""
    LOG_ERROR(errorMessage)
    try:
      LOG(str(data))
    except Exception, ex:
      LOG_WARNING("data passed to notifyError are invalid: " + str(ex))
  # ---------------------------------------------------------------------------
  def notifyTcSpace(self, tcPacket):
    """(TC,SPACE) received: overloaded from EGSE.EDEN.Server"""
    tcPacketDu = CCSDS.PACKET.TCpacket(tcPacket)
    SPACE.IF.s_onboardComputer.pushTCpacket(tcPacketDu)
    return True
  # ---------------------------------------------------------------------------
  def notifyTcScoe(self, tcPacket):
    """(TC,SCOE) received: overloaded from EGSE.EDEN.Server"""
    tcPacketDu = CCSDS.PACKET.TCpacket(tcPacket)
    SPACE.IF.s_onboardComputer.pushTCpacket(tcPacketDu)
    return True

####################
# global variables #
####################
# EGSE server is a singleton
s_server = None

#############
# functions #
#############
# functions to encapsulate access to s_server
# -----------------------------------------------------------------------------
def createEGSEserver():
  """create the EGSE server"""
  global s_server
  s_server = Server(portNr=int(UTIL.SYS.s_configuration.EDEN_SERVER_PORT))
  EGSE.IF.s_ccsLink = s_server
  if not s_server.openConnectPort(UTIL.SYS.s_configuration.HOST):
    sys.exit(-1)
