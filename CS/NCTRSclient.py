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
  def __init__(self):
    """Initialise attributes only"""
    GRND.NCTRS.TMreceiver.__init__(self)
  # ---------------------------------------------------------------------------
  def connected(self):
    """hook for derived classes"""
    LOG_INFO("TMclient.connected", "NCTRS")
    GRND.IF.s_clientConfiguration.nctrsTMconn = True
    UTIL.TASK.s_processingTask.notifyNCTRS1connected()
  # ---------------------------------------------------------------------------
  def disconnected(self):
    """hook for derived classes"""
    LOG_WARNING("TMclient.disconnected", "NCTRS")
    GRND.IF.s_clientConfiguration.nctrsTMconn = False
    UTIL.TASK.s_processingTask.notifyNCTRS1disconnected()
  # ---------------------------------------------------------------------------
  def notifyTMdataUnit(self, tmDu):
    """TM frame received"""
    # overloaded from GRND.NCTRS.TMreceiver
    LOG_INFO("TM frame received", "NCTRS")
    # extract the TM frame from the NCTRS data unit
    # and send it to the frame processing
    frame = tmDu.getFrame()
    CS.FRAMEmodel.s_frameModel.receiveTMframe(frame)

# =============================================================================
class TCclient(GRND.NCTRS.TCsender):
  """Subclass of GRND.NCTRS.TCsender"""
  # this client sends NCTRS TC data units
  # and receives automatically TC response data units
  # ---------------------------------------------------------------------------
  def __init__(self):
    """Initialise attributes only"""
    GRND.NCTRS.TCsender.__init__(self)
  # ---------------------------------------------------------------------------
  def connected(self):
    """hook for derived classes"""
    LOG_INFO("TCclient.connected", "NCTRS")
    GRND.IF.s_clientConfiguration.nctrsTCconn = True
    UTIL.TASK.s_processingTask.notifyNCTRS2connected()
  # ---------------------------------------------------------------------------
  def disconnected(self):
    """hook for derived classes"""
    LOG_WARNING("TCclient.disconnected", "NCTRS")
    GRND.IF.s_clientConfiguration.nctrsTCconn = False
    UTIL.TASK.s_processingTask.notifyNCTRS2disconnected()
  # ---------------------------------------------------------------------------
  def notifyTCpacketResponseDataUnit(self, tcPktRespDu):
    """AD packet / BD segment response received"""
    # overloaded from GRND.NCTRS.TCsender
    LOG_INFO("TCsender.notifyTCpacketResponseDataUnit", "NCTRS")
  # ---------------------------------------------------------------------------
  def notifyTCcltuResponseDataUnit(self, tcCltuRespDu):
    """CLTU response received"""
    # overloaded from GRND.NCTRS.TCsender
    LOG_INFO("TCsender.notifyTCcltuResponseDataUnit", "NCTRS")
  # ---------------------------------------------------------------------------
  def notifyTClinkStatusDataUnit(self, tcLinkStatDu):
    """Link status received"""
    # overloaded from GRND.NCTRS.TCsender
    LOG_INFO("TCsender.notifyTClinkStatusDataUnit", "NCTRS")

# =============================================================================
class AdminClient(GRND.NCTRS.AdminMessageReceiver):
  """Subclass of GRND.NCTRS.AdminMessageReceiver"""
  # this client only receives NCTRS admin message data units
  # ---------------------------------------------------------------------------
  def __init__(self):
    """Initialise attributes only"""
    GRND.NCTRS.AdminMessageReceiver.__init__(self)
  # ---------------------------------------------------------------------------
  def connected(self):
    """hook for derived classes"""
    LOG_INFO("AdminClient.connected", "NCTRS")
    GRND.IF.s_clientConfiguration.nctrsAdminConn = True
    UTIL.TASK.s_processingTask.notifyNCTRS3connected()
  # ---------------------------------------------------------------------------
  def disconnected(self):
    """hook for derived classes"""
    LOG_WARNING("AdminClient.disconnected", "NCTRS")
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
  s_tmClient = TMclient()
  s_tcClient = TCclient()
  s_adminClient = AdminClient()
# -----------------------------------------------------------------------------
def connectNCTRS1():
  """Connect NCTRS TM link"""
  LOG_INFO("Connect NCTRS TM link", "NCTRS")
  nctrsHost = GRND.IF.s_clientConfiguration.nctrsHost
  nctrsTMport = GRND.IF.s_clientConfiguration.nctrsTMport
  if nctrsHost == "" or nctrsTMport == "-1":
    LOG_ERROR("no NCTRS TM link configured", "NCTRS")
    return
  if not s_tmClient.connectToServer(nctrsHost, int(nctrsTMport)):
    LOG_ERROR("Connect TM link failed", "NCTRS")
# -----------------------------------------------------------------------------
def disconnectNCTRS1():
  """Disonnect NCTRS TM link"""
  LOG_INFO("Disonnect NCTRS TM link", "NCTRS")
  nctrsHost = GRND.IF.s_clientConfiguration.nctrsHost
  nctrsTMport = GRND.IF.s_clientConfiguration.nctrsTMport
  if nctrsHost == "" or nctrsTMport == "-1":
    LOG_ERROR("no NCTRS TM link configured", "NCTRS")
    return
  s_tmClient.disconnectFromServer()
# -----------------------------------------------------------------------------
def connectNCTRS2():
  """Connect NCTRS TC link"""
  LOG_INFO("Connect NCTRS TC link", "NCTRS")
  nctrsHost = GRND.IF.s_clientConfiguration.nctrsHost
  nctrsTCport = GRND.IF.s_clientConfiguration.nctrsTCport
  if nctrsHost == "" or nctrsTCport == "-1":
    LOG_ERROR("no NCTRS TC link configured", "NCTRS")
    return
  if not s_tcClient.connectToServer(nctrsHost, int(nctrsTCport)):
    LOG_ERROR("Connect TC link failed", "NCTRS")
# -----------------------------------------------------------------------------
def disconnectNCTRS2():
  """Disonnect NCTRS TC link"""
  LOG_INFO("Disonnect NCTRS TC link", "NCTRS")
  nctrsHost = GRND.IF.s_clientConfiguration.nctrsHost
  nctrsTCport = GRND.IF.s_clientConfiguration.nctrsTCport
  if nctrsHost == "" or nctrsTCport == "-1":
    LOG_ERROR("no NCTRS TC link configured", "NCTRS")
    return
  s_tcClient.disconnectFromServer()
# -----------------------------------------------------------------------------
def connectNCTRS3():
  """Connect NCTRS Admin link"""
  LOG_INFO("Connect NCTRS Admin link", "NCTRS")
  nctrsHost = GRND.IF.s_clientConfiguration.nctrsHost
  nctrsAdminPort = GRND.IF.s_clientConfiguration.nctrsAdminPort
  if nctrsHost == "" or nctrsAdminPort == "-1":
    LOG_ERROR("no NCTRS Admin link configured", "NCTRS")
    return
  if not s_adminClient.connectToServer(nctrsHost, int(nctrsAdminPort)):
    LOG_ERROR("Connect admin message link failed", "NCTRS")
# -----------------------------------------------------------------------------
def disconnectNCTRS3():
  """Disonnect NCTRS Admin link"""
  LOG_INFO("Disonnect NCTRS Admin link", "NCTRS")
  nctrsHost = GRND.IF.s_clientConfiguration.nctrsHost
  nctrsAdminPort = GRND.IF.s_clientConfiguration.nctrsAdminPort
  if nctrsHost == "" or nctrsAdminPort == "-1":
    LOG_ERROR("no NCTRS Admin link configured", "NCTRS")
    return
  s_adminClient.disconnectFromServer()
