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
# supports one of the following EGSE_PROTOCOLs for CCS connection:            *
# - CNC:  implements CAIT-03474-ASTR_issue_3_EGSE_IRD.pdf                     *
# - EDEN: implements Core_EGSE_AD03_GAL_REQ_ALS_SA_R_0002_EGSE_IRD_issue2.pdf *
#******************************************************************************
import sys
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import CCSDS.PACKET
import EGSE.CNC, EGSE.EDEN, EGSE.IF
import SPACE.IF
import UTIL.SYS, UTIL.TASK

###########
# classes #
###########
# =============================================================================
class CNCserver(EGSE.CNC.Server, EGSE.IF.CCSlink):
  """Subclass of GRND.NCTRS.TCreceiver"""
  # this server only receives TC packets and sends TM packets
  # ---------------------------------------------------------------------------
  def __init__(self, portNr):
    """Initialise attributes only"""
    EGSE.CNC.Server.__init__(self, portNr)
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
    """(TC,SPACE) received: overloaded from EGSE.CNC.Server"""
    tcPacketDu = CCSDS.PACKET.TCpacket(tcPacket)
    return SPACE.IF.s_onboardComputer.pushTCpacket(tcPacketDu)
  # ---------------------------------------------------------------------------
  def notifyTcScoe(self, tcPacket):
    """(TC,SCOE) received: overloaded from EGSE.CNC.Server"""
    tcPacketDu = CCSDS.PACKET.TCpacket(tcPacket)
    return SPACE.IF.s_onboardComputer.pushTCpacket(tcPacketDu)
  # ---------------------------------------------------------------------------
  def notifyCmdExec(self, message):
    """(CMD,EXEC) received: overloaded from EGSE.CNC.Server"""
    LOG_INFO("notifyCmdExec: message = " + message)
    self.sendCmdAnsw("this is a (CMD,ANSW) message")

# =============================================================================
class CNCserver2(EGSE.CNC.Server):
  """Subclass of GRND.NCTRS.TCreceiver"""
  # this server only receives TC packets
  # ---------------------------------------------------------------------------
  def __init__(self, portNr):
    """Initialise attributes only"""
    EGSE.CNC.Server.__init__(self, portNr)
  # ---------------------------------------------------------------------------
  def clientAccepted(self):
    """Overloaded from GRND.NCTRS.TCreceiver"""
    LOG_INFO("CCS client accepted", "EGSE")
    # notify the status change
    UTIL.TASK.s_processingTask.setCCSconnected2()
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
    """(TC,SPACE) received: overloaded from EGSE.CNC.Server"""
    tcPacketDu = CCSDS.PACKET.TCpacket(tcPacket)
    return SPACE.IF.s_onboardComputer.pushTCpacket(tcPacketDu)
  # ---------------------------------------------------------------------------
  def notifyTcScoe(self, tcPacket):
    """(TC,SCOE) received: overloaded from EGSE.CNC.Server"""
    tcPacketDu = CCSDS.PACKET.TCpacket(tcPacket)
    return SPACE.IF.s_onboardComputer.pushTCpacket(tcPacketDu)
  # ---------------------------------------------------------------------------
  def notifyCmdExec(self, message):
    """(CMD,EXEC) received: overloaded from EGSE.CNC.Server"""
    LOG_INFO("notifyCmdExec: message = " + message)
    self.sendCmdAnsw("this is a (CMD,ANSW) message")

# =============================================================================
class EDENserver(EGSE.EDEN.Server, EGSE.IF.CCSlink):
  """Subclass of GRND.NCTRS.TCreceiver"""
  # this server only receives TC packets and sends TM packets
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
    return SPACE.IF.s_onboardComputer.pushTCpacket(tcPacketDu)
  # ---------------------------------------------------------------------------
  def notifyTcScoe(self, tcPacket):
    """(TC,SCOE) received: overloaded from EGSE.EDEN.Server"""
    tcPacketDu = CCSDS.PACKET.TCpacket(tcPacket)
    return SPACE.IF.s_onboardComputer.pushTCpacket(tcPacketDu)
  # ---------------------------------------------------------------------------
  def notifyCmdExec(self, message):
    """(CMD,EXEC) received: overloaded from EGSE.EDEN.Server"""
    LOG_INFO("notifyCmdExec: message = " + message)
    self.sendCmdAnsw("this is a (CMD,ANSW) message")

# =============================================================================
class EDENserver2(EGSE.EDEN.Server):
  """Subclass of GRND.NCTRS.TCreceiver"""
  # this server only receives TC packets
  # ---------------------------------------------------------------------------
  def __init__(self, portNr):
    """Initialise attributes only"""
    EGSE.EDEN.Server.__init__(self, portNr)
  # ---------------------------------------------------------------------------
  def clientAccepted(self):
    """Overloaded from GRND.NCTRS.TCreceiver"""
    LOG_INFO("CCS client accepted", "EGSE")
    # notify the status change
    UTIL.TASK.s_processingTask.setCCSconnected2()
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
    return SPACE.IF.s_onboardComputer.pushTCpacket(tcPacketDu)
  # ---------------------------------------------------------------------------
  def notifyTcScoe(self, tcPacket):
    """(TC,SCOE) received: overloaded from EGSE.EDEN.Server"""
    tcPacketDu = CCSDS.PACKET.TCpacket(tcPacket)
    return SPACE.IF.s_onboardComputer.pushTCpacket(tcPacketDu)
  # ---------------------------------------------------------------------------
  def notifyCmdExec(self, message):
    """(CMD,EXEC) received: overloaded from EGSE.EDEN.Server"""
    LOG_INFO("notifyCmdExec: message = " + message)
    self.sendCmdAnsw("this is a (CMD,ANSW) message")

####################
# global variables #
####################
# EGSE server is a singleton
s_server = None
s_server2 = None

#############
# functions #
#############
# functions to encapsulate access to s_server
# -----------------------------------------------------------------------------
def createEGSEserver(hostName=None):
  """create the EGSE server"""
  global s_server, s_server2
  egseProtocol = UTIL.SYS.s_configuration.EGSE_PROTOCOL
  if egseProtocol == "CNC":
    s_server = CNCserver(portNr=int(UTIL.SYS.s_configuration.CCS_SERVER_PORT))
  elif egseProtocol == "EDEN":
    s_server = EDENserver(portNr=int(UTIL.SYS.s_configuration.CCS_SERVER_PORT))
  else:
    LOG_ERROR("invalid EGSE_PROTOCOL defined")
    sys.exit(-1)
  if not s_server.openConnectPort(hostName):
    sys.exit(-1)
  serverPort2 = int(UTIL.SYS.s_configuration.CCS_SERVER_PORT2)
  if serverPort2 == 0:
    if egseProtocol == "CNC":
      LOG_ERROR("CNC protocol requires 2 server ports configured")
      sys.exit(-1)
  else:
    # there is a second server port configured
    if egseProtocol == "CNC":
      s_server2 = CNCserver2(portNr=serverPort2)
      EGSE.IF.s_ccsLink = s_server2
    elif egseProtocol == "EDEN":
      s_server2 = EDENserver2(portNr=serverPort2)
    if not s_server2.openConnectPort(hostName):
      sys.exit(-1)
  # the link where TM is sent to CCS
  if egseProtocol == "CNC":
    EGSE.IF.s_ccsLink = s_server2
  elif egseProtocol == "EDEN":
    EGSE.IF.s_ccsLink = s_server
