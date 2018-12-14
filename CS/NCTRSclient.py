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
# NCTRS client for connection to Ground Station via NCTRS interface           *
# implements EGOS-NIS-NCTR-ICD-0002-i4r0.2 (Signed).pdf                       *
#******************************************************************************
import sys
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import GRND.IF, GRND.NCTRS
import CS.FRAMEmodel
import UTIL.TASK

###########
# classes #
###########
# =============================================================================
class TMclient(GRND.NCTRS.TMreceiver):
  """Subclass of GRND.NCTRS.TMreceiver"""
  # this client only receives NCTRS TM data units
  # ---------------------------------------------------------------------------
  def __init__(self, hostName, portNr):
    """Initialise attributes only"""
    GRND.NCTRS.TMreceiver.__init__(self)
    self.hostName = hostName
    self.portNr = portNr
  # ---------------------------------------------------------------------------
  def connectLink(self):
    """Connects TM link to NCTRS server"""
    if self.connectToServer(self.hostName, self.portNr):
      GRND.IF.s_clientConfiguration.nctrsTMconn = True
      UTIL.TASK.s_processingTask.notifyNCTRS1connected()
    else:
      LOG_ERROR("Connect TM link failed", "NCTRS")
  # ---------------------------------------------------------------------------
  def disconnectLink(self):
    """Disconnects TM link from NCTRS server"""
    self.disconnectFromServer()
    GRND.IF.s_clientConfiguration.nctrsTMconn = False
    UTIL.TASK.s_processingTask.notifyNCTRS1disconnected()
  # ---------------------------------------------------------------------------
  def notifyTMdataUnit(self, tmDu):
    """TM frame received: hook for derived classes"""
    LOG_INFO("TM frame received", "NCTRS")
    CS.FRAMEmodel.s_frameModel.receiveTMframe("")

# =============================================================================
class TCclient(GRND.NCTRS.TCsender):
  """Subclass of GRND.NCTRS.TCsender"""
  # this client sends NCTRS TC data units
  # and receives automatically TC response data units
  # ---------------------------------------------------------------------------
  def __init__(self, hostName, portNr):
    """Initialise attributes only"""
    GRND.NCTRS.TCsender.__init__(self)
    self.hostName = hostName
    self.portNr = portNr
  # ---------------------------------------------------------------------------
  def connectLink(self):
    """Connects TC link to NCTRS server"""
    if self.connectToServer(self.hostName, self.portNr):
      GRND.IF.s_clientConfiguration.nctrsTCconn = True
      UTIL.TASK.s_processingTask.notifyNCTRS2connected()
    else:
      LOG_ERROR("Connect TC link failed", "NCTRS")
  # ---------------------------------------------------------------------------
  def disconnectLink(self):
    """Disconnects TC link from NCTRS server"""
    self.disconnectFromServer()
    GRND.IF.s_clientConfiguration.nctrsTCconn = False
    UTIL.TASK.s_processingTask.notifyNCTRS2disconnected()

# =============================================================================
class AdminClient(GRND.NCTRS.AdminMessageReceiver):
  """Subclass of GRND.NCTRS.AdminMessageReceiver"""
  # this client only receives NCTRS admin message data units
  # ---------------------------------------------------------------------------
  def __init__(self, hostName, portNr):
    """Initialise attributes only"""
    GRND.NCTRS.AdminMessageReceiver.__init__(self)
    self.hostName = hostName
    self.portNr = portNr
  # ---------------------------------------------------------------------------
  def connectLink(self):
    """Connects admin message link to NCTRS server"""
    if self.connectToServer(self.hostName, self.portNr):
      GRND.IF.s_clientConfiguration.nctrsAdminConn = True
      UTIL.TASK.s_processingTask.notifyNCTRS3connected()
    else:
      LOG_ERROR("Connect admin message link failed", "NCTRS")
  # ---------------------------------------------------------------------------
  def disconnectLink(self):
    """Disconnects admin message link from NCTRS server"""
    self.disconnectFromServer()
    GRND.IF.s_clientConfiguration.nctrsAdminConn = False
    UTIL.TASK.s_processingTask.notifyNCTRS3disconnected()
  # ---------------------------------------------------------------------------
  def notifyAdminMessageDataUnit(self, messageDu):
    """Admin message response received"""
    LOG_INFO("AdminClient.notifyAdminMessageDataUnit", "NCTRS")

####################
# global variables #
####################
# NCTRS clients are singletons
s_tmClient = None
s_tcClient = None
s_adminClient = None

#############
# functions #
#############
# functions to encapsulate access to s_tmClient, s_tcClient, s_adminClient
# -----------------------------------------------------------------------------
def createClients():
  """create the NCTRS clients"""
  global s_tmClient, s_tcClient, s_adminClient
  nctrsHost = GRND.IF.s_clientConfiguration.nctrsHost
  if nctrsHost == "":
    LOG_INFO("no NCTRS connection configured", "NCTRS")
    return
  nctrsTMport = int(GRND.IF.s_clientConfiguration.nctrsTMport)
  s_tmClient = TMclient(nctrsHost, nctrsTMport)
  nctrsTCport = int(GRND.IF.s_clientConfiguration.nctrsTCport)
  s_tcClient = TCclient(nctrsHost, nctrsTCport)
  nctrsAdminPort = int(GRND.IF.s_clientConfiguration.nctrsAdminPort)
  s_adminClient = AdminClient(nctrsHost, nctrsAdminPort)
# -----------------------------------------------------------------------------
def connectNCTRS1():
  """Connect NCTRS TM link"""
  LOG_INFO("Connect NCTRS TM link", "NCTRS")
  if GRND.IF.s_clientConfiguration.nctrsHost == "" or \
     GRND.IF.s_clientConfiguration.nctrsTMport == "-1":
    LOG_ERROR("no NCTRS TM link configured", "NCTRS")
    return
  s_tmClient.connectLink()
# -----------------------------------------------------------------------------
def disconnectNCTRS1():
  """Disonnect NCTRS TM link"""
  LOG_INFO("Disonnect NCTRS TM link", "NCTRS")
  if GRND.IF.s_clientConfiguration.nctrsHost == "" or \
     GRND.IF.s_clientConfiguration.nctrsTMport == "-1":
    LOG_ERROR("no NCTRS TM link configured", "NCTRS")
    return
  s_tmClient.disconnectLink()
# -----------------------------------------------------------------------------
def connectNCTRS2():
  """Connect NCTRS TC link"""
  LOG_INFO("Connect NCTRS TC link", "NCTRS")
  if GRND.IF.s_clientConfiguration.nctrsHost == "" or \
     GRND.IF.s_clientConfiguration.nctrsTCport == "-1":
    LOG_ERROR("no NCTRS TC link configured", "NCTRS")
    return
  s_tcClient.connectLink()
# -----------------------------------------------------------------------------
def disconnectNCTRS2():
  """Disonnect NCTRS TC link"""
  LOG_INFO("Disonnect NCTRS TC link", "NCTRS")
  if GRND.IF.s_clientConfiguration.nctrsHost == "" or \
     GRND.IF.s_clientConfiguration.nctrsTCport == "-1":
    LOG_ERROR("no NCTRS TC link configured", "NCTRS")
    return
  s_tcClient.disconnectLink()
# -----------------------------------------------------------------------------
def connectNCTRS3():
  """Connect NCTRS Admin link"""
  LOG_INFO("Connect NCTRS Admin link", "NCTRS")
  if GRND.IF.s_clientConfiguration.nctrsHost == "" or \
     GRND.IF.s_clientConfiguration.nctrsAdminPort == "-1":
    LOG_ERROR("no NCTRS Admin link configured", "NCTRS")
    return
  s_adminClient.connectLink()
# -----------------------------------------------------------------------------
def disconnectNCTRS3():
  """Disonnect NCTRS Admin link"""
  LOG_INFO("Disonnect NCTRS Admin link", "NCTRS")
  if GRND.IF.s_clientConfiguration.nctrsHost == "" or \
     GRND.IF.s_clientConfiguration.nctrsAdminPort == "-1":
    LOG_ERROR("no NCTRS Admin link configured", "NCTRS")
    return
  s_adminClient.disconnectLink()
