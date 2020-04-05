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
# EDEN client for connection to SCOE                                          *
# implements Core_EGSE_AD03_GAL_REQ_ALS_SA_R_0002_EGSE_IRD_issue2.pdf         *
#******************************************************************************
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import CCSDS.PACKET
import EGSE.EDEN, EGSE.IF
import MC.IF
import PUS.PACKET
import UTIL.TASK

###########
# classes #
###########
# =============================================================================
class Client(EGSE.EDEN.Client):
  """Subclass of EGSE.EDEN.Client"""
  # this client sends CCSDS TC packets and received CCSDS TM packets
  # ---------------------------------------------------------------------------
  def __init__(self):
    """Initialise attributes only"""
    EGSE.EDEN.Client.__init__(self)
  # ---------------------------------------------------------------------------
  def connected(self):
    """hook for derived classes"""
    LOG_INFO("Client.connected", "EDEN")
    EGSE.IF.s_edenClientConfiguration.connected = True
    UTIL.TASK.s_processingTask.notifyEDENconnected()
  # ---------------------------------------------------------------------------
  def disconnected(self):
    """hook for derived classes"""
    LOG_WARNING("Client.disconnected", "EDEN")
    EGSE.IF.s_edenClientConfiguration.connected = False
    UTIL.TASK.s_processingTask.notifyEDENdisconnected()
  # ---------------------------------------------------------------------------
  def pushTcSpace(self, tcPacketDu):
    """Consumes a telecommand packet"""
    # the CCSDS TC packet is not checked but directly send
    self.sendTcScoe(tcPacketDu.getBuffer())
  # ---------------------------------------------------------------------------
  def pushTcScoe(self, tcPacketDu):
    """Consumes a telecommand packet"""
    # the CCSDS TC packet is not checked but directly send
    self.sendTcScoe(tcPacketDu.getBuffer())
  # ---------------------------------------------------------------------------
  def notifyTmSpace(self, tmPacket):
    """(TM,SPACE) received: overloaded from EGSE.EDEN.Client"""
    if PUS.PACKET.isPUSpacket(tmPacket):
      # PUS packet
      tmPacketDu = PUS.PACKET.TMpacket(tmPacket)
      LOG_INFO("PUS TM/SPACE packet extracted", "EDEN")
    else:
      # CCSDS packet
      tmPacketDu = CCSDS.PACKET.TMpacket(tmPacket)
      LOG_INFO("CCSDS TM/SPACE packet extracted", "EDEN")
    MC.IF.s_tmModel.pushTMpacket(tmPacketDu, None)
  # ---------------------------------------------------------------------------
  def notifyTmScoe(self, tmPacket):
    """(TM,SCOE) received: overloaded from EGSE.EDEN.Client"""
    if PUS.PACKET.isPUSpacket(tmPacket):
      # PUS packet
      tmPacketDu = PUS.PACKET.TMpacket(tmPacket)
      LOG_INFO("PUS TM/SCOE packet extracted", "EDEN")
    else:
      # CCSDS packet
      tmPacketDu = CCSDS.PACKET.TMpacket(tmPacket)
      LOG_INFO("CCSDS TM/SCOE packet extracted", "EDEN")
    MC.IF.s_tmModel.pushTMpacket(tmPacketDu, None)

# =============================================================================
class Client2(EGSE.EDEN.Client):
  """Subclass of EGSE.EDEN.Client"""
  # this client is used for simulating a 2nd client endpoint
  # ---------------------------------------------------------------------------
  def __init__(self):
    """Initialise attributes only"""
    EGSE.EDEN.Client.__init__(self)
  # ---------------------------------------------------------------------------
  def connected(self):
    """hook for derived classes"""
    LOG_INFO("Client2.connected", "EDEN")
    EGSE.IF.s_edenClientConfiguration.connected2 = True
    UTIL.TASK.s_processingTask.notifyEDEN2connected()
  # ---------------------------------------------------------------------------
  def disconnected(self):
    """hook for derived classes"""
    LOG_WARNING("Client2.disconnected", "EDEN")
    EGSE.IF.s_edenClientConfiguration.connected2 = False
    UTIL.TASK.s_processingTask.notifyEDEN2disconnected()
  # ---------------------------------------------------------------------------
  def pushTcSpace(self, tcPacketDu):
    """Consumes a telecommand packet"""
    # the CCSDS TC packet is not checked but directly send
    self.sendTcScoe(tcPacketDu.getBuffer())
  # ---------------------------------------------------------------------------
  def pushTcScoe(self, tcPacketDu):
    """Consumes a telecommand packet"""
    # the CCSDS TC packet is not checked but directly send
    self.sendTcScoe(tcPacketDu.getBuffer())
  # ---------------------------------------------------------------------------
  def notifyTmSpace(self, tmPacket):
    """(TM,SPACE) received: overloaded from EGSE.EDEN.Client"""
    tmPacketDu = CCSDS.PACKET.TMpacket(tmPacket)
    MC.IF.s_tmModel.pushTMpacket(tmPacketDu, None)
  # ---------------------------------------------------------------------------
  def notifyTmScoe(self, tmPacket):
    """(TM,SCOE) received: overloaded from EGSE.EDEN.Client"""
    tmPacketDu = CCSDS.PACKET.TMpacket(tmPacket)
    MC.IF.s_tmModel.pushTMpacket(tmPacketDu, None)

####################
# global variables #
####################
# EDEN clients are singletons
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
  edenHost = EGSE.IF.s_edenClientConfiguration.edenHost
  if edenHost == "":
    LOG_INFO("no EDEN connection configured", "EDEN")
    return
  s_client = Client()
  edenPort2 = EGSE.IF.s_edenClientConfiguration.edenPort2
  if edenPort2 != "-1":
    # there is a second EDEN connection configured
    s_client2 = Client2()
# -----------------------------------------------------------------------------
def connectEDEN():
  """Connect EDEN link 1"""
  LOG_INFO("Connect EDEN link 1", "EDEN")
  edenHost = EGSE.IF.s_edenClientConfiguration.edenHost
  edenPort = int(EGSE.IF.s_edenClientConfiguration.edenPort)
  if edenHost == "" or edenPort == "-1":
    LOG_ERROR("no EDEN link 1 configured", "EDEN")
    return
  if not s_client.connectToServer(edenHost, int(edenPort)):
    LOG_ERROR("Connect link 1 failed", "EDEN")
# -----------------------------------------------------------------------------
def disconnectEDEN():
  """Disonnect EDEN link 1"""
  LOG_INFO("Disonnect EDEN link 1", "EDEN")
  edenHost = EGSE.IF.s_edenClientConfiguration.edenHost
  edenPort = EGSE.IF.s_edenClientConfiguration.edenPort
  if edenHost == "" or edenPort == "-1":
    LOG_ERROR("no EDEN TC link 1 configured", "EDEN")
    return
  s_client.disconnectFromServer()
# -----------------------------------------------------------------------------
def connectEDEN2():
  """Connect EDEN link 2"""
  LOG_INFO("Connect EDEN link 2", "EDEN")
  edenHost = EGSE.IF.s_edenClientConfiguration.edenHost
  edenPort2 = EGSE.IF.s_edenClientConfiguration.edenPort2
  if edenHost == "" or edenPort2 == "-1":
    LOG_ERROR("no EDEN link 2 configured", "EDEN")
    return
  if not s_client2.connectToServer(edenHost, int(edenPort2)):
    LOG_ERROR("Connect link 2 failed", "EDEN")
# -----------------------------------------------------------------------------
def disconnectEDEN2():
  """Disonnect EDEN link 2"""
  LOG_INFO("Disonnect EDEN link 2", "EDEN")
  edenHost = EGSE.IF.s_edenClientConfiguration.edenHost
  edenPort2 = EGSE.IF.s_edenClientConfiguration.edenPort2
  if edenHost == "" or edenPort2 == "-1":
    LOG_ERROR("no EDEN link 2 configured", "EDEN")
    return
  s_client2.disconnectFromServer()
