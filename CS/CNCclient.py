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
# CNC client for connection to SCOE                                           *
# implements CAIT-03474-ASTR_issue_3_EGSE_IRD.pdf                             *
#******************************************************************************
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import CCSDS.PACKET
import EGSE.CNC, EGSE.IF
import MC.IF
import PUS.PACKET
import UTIL.TASK

###########
# classes #
###########
# =============================================================================
class TCclient(EGSE.CNC.TCclient):
  """Subclass of EGSE.CNC.TCclient"""
  # this client sends CnC commands
  # and receives automatically ACK/NAK CnC responses
  # ---------------------------------------------------------------------------
  def __init__(self):
    """Initialise attributes only"""
    EGSE.CNC.TCclient.__init__(self)
  # ---------------------------------------------------------------------------
  def connected(self):
    """hook for derived classes"""
    LOG_INFO("TCclient.connected", "CNC")
    EGSE.IF.s_cncClientConfiguration.connected = True
    UTIL.TASK.s_processingTask.notifyCNCconnected()
  # ---------------------------------------------------------------------------
  def disconnected(self):
    """hook for derived classes"""
    LOG_WARNING("TCclient.disconnected", "CNC")
    EGSE.IF.s_cncClientConfiguration.connected = False
    UTIL.TASK.s_processingTask.notifyCNCdisconnected()
  # ---------------------------------------------------------------------------
  def pushTCpacket(self, tcPacketDu):
    """Consumes a telecommand packet"""
    # the CCSDS TC packet is not checked but directly send
    self.sendCNCpacket(tcPacketDu.getBuffer())
  # ---------------------------------------------------------------------------
  def notifyCNCresponse(self, cncAckNakDU):
    """CnC response received: overloaded from EGSE.CNC.TCclient"""
    LOG_INFO("notifyCNCresponse: message = " + cncAckNakDU.getCNCmessage(), "CNC")
    MC.IF.s_tmModel.pushTMpacket(cncAckNakDU, None)
  # ---------------------------------------------------------------------------
  def notifyCCSDSresponse(self, tcAckNakDU):
    """TC response received: overloaded from EGSE.CNC.TCclient"""
    LOG_INFO("notifyCCSDSresponse: status = " + tcAckNakDU.getStatus(), "CNC")
    MC.IF.s_tmModel.pushTMpacket(tcAckNakDU, None)

# =============================================================================
class TMclient(EGSE.CNC.TMclient):
  """Subclass of EGSE.CNC.TMclient"""
  # this client only receives CCSDS TM packets
  # ---------------------------------------------------------------------------
  def __init__(self):
    """Initialise attributes only"""
    EGSE.CNC.TMclient.__init__(self)
  # ---------------------------------------------------------------------------
  def connected(self):
    """hook for derived classes"""
    LOG_INFO("TMclient.connected", "CNC")
    EGSE.IF.s_cncClientConfiguration.connected2 = True
    UTIL.TASK.s_processingTask.notifyCNC2connected()
  # ---------------------------------------------------------------------------
  def disconnected(self):
    """hook for derived classes"""
    LOG_WARNING("TMclient.disconnected", "CNC")
    EGSE.IF.s_cncClientConfiguration.connected2 = False
    UTIL.TASK.s_processingTask.notifyCNC2disconnected()
  # ---------------------------------------------------------------------------
  def notifyTMpacket(self, tmPacket):
    """TM packet received: overloaded from EGSE.CNC.TMclient"""
    if PUS.PACKET.isPUSpacket(tmPacket):
      # PUS packet
      tmPacketDu = PUS.PACKET.TMpacket(tmPacket)
      LOG_INFO("PUS TM packet extracted", "CNC")
    else:
      # CCSDS packet
      tmPacketDu = CCSDS.PACKET.TMpacket(tmPacket)
      LOG_INFO("CCSDS TM packet extracted", "CNC")
    MC.IF.s_tmModel.pushTMpacket(tmPacketDu, None)

####################
# global variables #
####################
# CNC clients are singletons
s_client = None
s_client2 = None

#############
# functions #
#############
# functions to encapsulate access to s_client and s_client2
# -----------------------------------------------------------------------------
def createClients():
  """create the EGSE clients"""
  global s_client, s_client2
  cncHost = EGSE.IF.s_cncClientConfiguration.cncHost
  if cncHost == "":
    LOG_INFO("no CNC connection configured", "CNC")
    return
  s_client = TCclient()
  s_client2 = TMclient()
# -----------------------------------------------------------------------------
def connectCNC():
  """Connect CNC TC link"""
  LOG_INFO("Connect CNC TC link", "CNC")
  cncHost = EGSE.IF.s_cncClientConfiguration.cncHost
  cncPort = EGSE.IF.s_cncClientConfiguration.cncPort
  if cncHost == "" or cncPort == "-1":
    LOG_ERROR("no CNC TC link configured", "CNC")
    return
  if not s_client.connectToServer(cncHost, int(cncPort)):
    LOG_ERROR("Connect TC link failed", "CNC")
# -----------------------------------------------------------------------------
def disconnectCNC():
  """Disonnect CNC TC link"""
  LOG_INFO("Disonnect CNC TC link", "CNC")
  cncHost = EGSE.IF.s_cncClientConfiguration.cncHost
  cncPort = EGSE.IF.s_cncClientConfiguration.cncPort
  if cncHost == "" or cncPort == "-1":
    LOG_ERROR("no CNC TC link configured", "CNC")
    return
  s_client.disconnectFromServer()
# -----------------------------------------------------------------------------
def connectCNC2():
  """Connect CNC TM link"""
  LOG_INFO("Connect CNC TM link", "CNC")
  cncHost = EGSE.IF.s_cncClientConfiguration.cncHost
  cncPort2 = EGSE.IF.s_cncClientConfiguration.cncPort2
  if cncHost == "" or cncPort2 == "-1":
    LOG_ERROR("no CNC TM link configured", "CNC")
    return
  if not s_client2.connectToServer(cncHost, int(cncPort2)):
    LOG_ERROR("Connect TM link failed", "CNC")
# -----------------------------------------------------------------------------
def disconnectCNC2():
  """Disonnect CNC TM link"""
  LOG_INFO("Disonnect CNC TM link", "CNC")
  cncHost = EGSE.IF.s_cncClientConfiguration.cncHost
  cncPort2 = EGSE.IF.s_cncClientConfiguration.cncPort2
  if cncHost == "" or cncPort2 == "-1":
    LOG_ERROR("no CNC TM link configured", "CNC")
    return
  s_client2.disconnectFromServer()
