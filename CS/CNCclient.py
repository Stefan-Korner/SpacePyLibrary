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
# implements implements CAIT-03474-ASTR_issue_3_EGSE_IRD.pdf                  *
#******************************************************************************
import sys
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import CCSDS.PACKET
import EGSE.CNC, EGSE.IF
import MC.IF
import UTIL.SYS, UTIL.TASK

###########
# classes #
###########
# =============================================================================
class TCclient(EGSE.CNC.TCclient):
  """Subclass of EGSE.CNC.TCclient"""
  # this client sends CnC commands
  # and receives automatically ACK/NAK CnC responses
  # ---------------------------------------------------------------------------
  def __init__(self, hostName, portNr):
    """Initialise attributes only"""
    EGSE.CNC.TCclient.__init__(self)
    self.hostName = hostName
    self.portNr = portNr
  # ---------------------------------------------------------------------------
  def connectTClink(self):
    """Connects TC link to server (e.g. SCOE)"""
    if self.connectToServer(self.hostName, self.portNr):
      EGSE.IF.s_cncClientConfiguration.connected = True
      UTIL.TASK.s_processingTask.notifyCNCconnected()
    else:
      LOG_ERROR("Connect TC link failed", "CNC")
  # ---------------------------------------------------------------------------
  def disconnectTClink(self):
    """Disconnects TC link from server (e.g. SCOE)"""
    self.disconnectFromServer()
    EGSE.IF.s_cncClientConfiguration.connected = False
    UTIL.TASK.s_processingTask.notifyCNCdisconnected()
  # ---------------------------------------------------------------------------
  def notifyCNCresponse(self, cncTMpacketDU):
    """CnC response received: overloaded from EGSE.CNC.TCclient"""
    LOG_INFO("notifyCNCresponse: message = " + cncTMpacketDU.getCNCmessage(), "CNC")
    MC.IF.s_tmModel.pushTMpacket(cncTMpacketDU, None)

# =============================================================================
class TMclient(EGSE.CNC.TMclient):
  """Subclass of EGSE.CNC.TMclient"""
  # this client only receives CCSDS TM packets
  # ---------------------------------------------------------------------------
  def __init__(self, hostName, portNr):
    """Initialise attributes only"""
    EGSE.CNC.TMclient.__init__(self)
    self.hostName = hostName
    self.portNr = portNr
  # ---------------------------------------------------------------------------
  def connectTMlink(self):
    """Connects TM link to server (e.g. SCOE)"""
    if self.connectToServer(self.hostName, self.portNr):
      EGSE.IF.s_cncClientConfiguration.connected2 = True
      UTIL.TASK.s_processingTask.notifyCNC2connected()
    else:
      LOG_ERROR("Connect TM link failed", "CNC")
  # ---------------------------------------------------------------------------
  def disconnectTMlink(self):
    """Disconnects TM link from server (e.g. SCOE)"""
    self.disconnectFromServer()
    EGSE.IF.s_cncClientConfiguration.connected2 = False
    UTIL.TASK.s_processingTask.notifyCNC2disconnected()
  # ---------------------------------------------------------------------------
  def notifyTMpacket(self, tmPacket):
    """TM packet received: overloaded from EGSE.CNC.TMclient"""
    LOG_INFO("notifyTMpacket", "CNC")
    tmPacketDu = CCSDS.PACKET.TMpacket(tmPacket)
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
  cncPort = int(EGSE.IF.s_cncClientConfiguration.cncPort)
  s_client = TCclient(cncHost, cncPort)
  cncPort2 = int(EGSE.IF.s_cncClientConfiguration.cncPort2)
  s_client2 = TMclient(cncHost, cncPort2)
# -----------------------------------------------------------------------------
def connectCNC():
  """Connect CNC TC link"""
  LOG_INFO("Connect CNC TC link", "CNC")
  if EGSE.IF.s_cncClientConfiguration.cncHost == "" or \
     EGSE.IF.s_cncClientConfiguration.cncPort == "-1":
    LOG_ERROR("no CNC TC link configured", "CNC")
    return
  s_client.connectTClink()
# -----------------------------------------------------------------------------
def disconnectCNC():
  """Disonnect CNC TC link"""
  LOG_INFO("Disonnect CNC TC link", "CNC")
  if EGSE.IF.s_cncClientConfiguration.cncHost == "" or \
     EGSE.IF.s_cncClientConfiguration.cncPort == "-1":
    LOG_ERROR("no CNC TC link configured", "CNC")
    return
  s_client.disconnectTClink()
# -----------------------------------------------------------------------------
def connectCNC2():
  """Connect CNC TM link"""
  LOG_INFO("Connect CNC TM link", "CNC")
  if EGSE.IF.s_cncClientConfiguration.cncHost == "" or \
     EGSE.IF.s_cncClientConfiguration.cncPort2 == "-1":
    LOG_ERROR("no CNC TM link configured", "CNC")
    return
  s_client2.connectTMlink()
# -----------------------------------------------------------------------------
def disconnectCNC2():
  """Disonnect CNC TM link"""
  LOG_INFO("Disonnect CNC TM link", "CNC")
  if EGSE.IF.s_cncClientConfiguration.cncHost == "" or \
     EGSE.IF.s_cncClientConfiguration.cncPort2 == "-1":
    LOG_ERROR("no CNC TM link configured", "CNC")
    return
  s_client2.disconnectTMlink()
