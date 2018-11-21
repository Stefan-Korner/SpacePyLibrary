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
class CNCtcServer(EGSE.CNC.TCserver):
  """Subclass of EGSE.CNC.TCserver"""
  # this server receives CnC commands
  # and sends automatically ACK/NAK CnC responses
  # ---------------------------------------------------------------------------
  def __init__(self, portNr):
    """Initialise attributes only"""
    EGSE.CNC.TCserver.__init__(self, portNr)
  # ---------------------------------------------------------------------------
  def clientAccepted(self):
    """Overloaded from EGSE.CNC.TCserver"""
    LOG_INFO("CCS client accepted", "EGSE")
    # notify the status change
    UTIL.TASK.s_processingTask.setCCSconnected()
  # ---------------------------------------------------------------------------
  def notifyError(self, errorMessage, data):
    """error notification"""
    LOG_ERROR(errorMessage)
    try:
      LOG(str(data))
    except Exception as ex:
      LOG_WARNING("data passed to notifyError are invalid: " + str(ex))
  # ---------------------------------------------------------------------------
  def notifyCNCcommand(self, cncCommandDU):
    """CnC command received: overloaded from EGSE.CNC.TCServer"""
    return SPACE.IF.s_onboardComputer.pushTCpacket(cncCommandDU)
  # ---------------------------------------------------------------------------
  def notifyCCSDScommand(self, ccsdsTCpacketDU):
    """CCSDS telecommand received: overloaded from EGSE.CNC.TCServer"""
    return SPACE.IF.s_onboardComputer.pushTCpacket(ccsdsTCpacketDU)

# =============================================================================
class CNCtmServer(EGSE.CNC.TMserver, EGSE.IF.CCSlink):
  """Subclass of EGSE.CNC.TMserver"""
  # this server only sends CCSDS TM packets
  # ---------------------------------------------------------------------------
  def __init__(self, portNr):
    """Initialise attributes only"""
    EGSE.CNC.TMserver.__init__(self, portNr)
  # ---------------------------------------------------------------------------
  def clientAccepted(self):
    """Overloaded from EGSE.CNC.TMserver"""
    LOG_INFO("CCS client accepted", "EGSE")
    # notify the status change
    UTIL.TASK.s_processingTask.setCCSconnected2()
  # ---------------------------------------------------------------------------
  def pushTMpacket(self, tmPacketDu):
    """
    consumes a telemetry packet:
    implementation of EGSE.IF.CCSlink.pushTMpacket
    """
    # the CCSDS TM packet is not checked but directly send
    self.sendTMpacket(tmPacketDu.getBufferString())
  # ---------------------------------------------------------------------------
  def notifyError(self, errorMessage, data):
    """error notification"""
    LOG_ERROR(errorMessage)
    try:
      LOG(str(data))
    except Exception as ex:
      LOG_WARNING("data passed to notifyError are invalid: " + str(ex))

# =============================================================================
class EDENserver(EGSE.EDEN.Server, EGSE.IF.CCSlink):
  """Subclass of EGSE.EDEN.Server"""
  # this server receives CCSDS TC packets and sends CCSDS TM packets
  # ---------------------------------------------------------------------------
  def __init__(self, portNr):
    """Initialise attributes only"""
    EGSE.EDEN.Server.__init__(self, portNr)
  # ---------------------------------------------------------------------------
  def clientAccepted(self):
    """Overloaded from EGSE.EDEN.Server"""
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
    self.sendTmSpace(tmPacketDu.getBufferString())
  # ---------------------------------------------------------------------------
  def notifyError(self, errorMessage, data):
    """error notification"""
    LOG_ERROR(errorMessage)
    try:
      LOG(str(data))
    except Exception as ex:
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
  """Subclass of EGSE.EDEN.Server"""
  # this server only receives TC packets (for simulating a 2nd server endpoint)
  # ---------------------------------------------------------------------------
  def __init__(self, portNr):
    """Initialise attributes only"""
    EGSE.EDEN.Server.__init__(self, portNr)
  # ---------------------------------------------------------------------------
  def clientAccepted(self):
    """Overloaded from EGSE.EDEN.Server"""
    LOG_INFO("CCS client accepted", "EGSE")
    # notify the status change
    UTIL.TASK.s_processingTask.setCCSconnected2()
  # ---------------------------------------------------------------------------
  def notifyError(self, errorMessage, data):
    """error notification"""
    LOG_ERROR(errorMessage)
    try:
      LOG(str(data))
    except Exception as ex:
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
# EGSE servers are singletons
s_server = None
s_server2 = None

#############
# functions #
#############
# functions to encapsulate access to s_server and s_server2
# -----------------------------------------------------------------------------
def createEGSEservers(hostName=None):
  """create the EGSE server"""
  global s_server, s_server2
  egseProtocol = UTIL.SYS.s_configuration.EGSE_PROTOCOL
  if egseProtocol == "CNC":
    s_server = CNCtcServer(portNr=int(UTIL.SYS.s_configuration.CCS_SERVER_PORT))
  elif egseProtocol == "EDEN":
    s_server = EDENserver(portNr=int(UTIL.SYS.s_configuration.CCS_SERVER_PORT))
  else:
    LOG_ERROR("invalid EGSE_PROTOCOL defined")
    sys.exit(-1)
  if not s_server.openConnectPort(hostName):
    sys.exit(-1)
  serverPort2 = int(UTIL.SYS.s_configuration.CCS_SERVER_PORT2)
  if serverPort2 > 0:
    # there is a second server port configured
    if egseProtocol == "CNC":
      s_server2 = CNCtmServer(portNr=serverPort2)
    elif egseProtocol == "EDEN":
      s_server2 = EDENserver2(portNr=serverPort2)
    if not s_server2.openConnectPort(hostName):
      sys.exit(-1)
  else:
    if egseProtocol == "CNC":
      LOG_ERROR("CNC protocol requires 2 server ports (TC + TM) configured")
      sys.exit(-1)
  # the link where TM is sent to CCS
  if egseProtocol == "CNC":
    EGSE.IF.s_ccsLink = s_server2
  elif egseProtocol == "EDEN":
    EGSE.IF.s_ccsLink = s_server
