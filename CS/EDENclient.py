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
# EGSE client for connection to SCOE                                          *
# supports one of the following EGSE_PROTOCOLs for SCOE connection:           *
# - CNC:  implements CAIT-03474-ASTR_issue_3_EGSE_IRD.pdf                     *
# - EDEN: implements Core_EGSE_AD03_GAL_REQ_ALS_SA_R_0002_EGSE_IRD_issue2.pdf *
#******************************************************************************
import sys
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import EGSE.CNC, EGSE.EDEN, EGSE.IF
import UTIL.SYS

###########
# classes #
###########
# =============================================================================
class CNCtcClient(EGSE.CNC.TCclient):
  """Subclass of EGSE.CNC.TCclient"""
  # this client sends CnC commands
  # and receives automatically ACK/NAK CnC responses
  # ---------------------------------------------------------------------------
  def __init__(self, hostName, portNr):
    """Initialise attributes only"""
    EGSE.CNC.TCclient.__init__(self)
    self.hostName = hostName
    self.portNr = portNr

# =============================================================================
class CNCtmClient(EGSE.CNC.TMclient):
  """Subclass of EGSE.CNC.TMclient"""
  # this client only receives CCSDS TM packets
  # ---------------------------------------------------------------------------
  def __init__(self, hostName, portNr):
    """Initialise attributes only"""
    EGSE.CNC.TMclient.__init__(self)
    self.hostName = hostName
    self.portNr = portNr

# =============================================================================
class EDENclient(EGSE.EDEN.Client):
  """Subclass of EGSE.EDEN.Client"""
  # this client sends CCSDS TC packets and received CCSDS TM packets
  # ---------------------------------------------------------------------------
  def __init__(self, hostName, portNr):
    """Initialise attributes only"""
    EGSE.EDEN.Client.__init__(self)
    self.hostName = hostName
    self.portNr = portNr

# =============================================================================
class EDENclient(EGSE.EDEN.Client):
  """Subclass of EGSE.EDEN.Client"""
  # this client is used for simulating a 2nd client endpoint
  # ---------------------------------------------------------------------------
  def __init__(self, hostName, portNr):
    """Initialise attributes only"""
    EGSE.EDEN.Client.__init__(self)
    self.hostName = hostName
    self.portNr = portNr

####################
# global variables #
####################
# EGSE clients are singletons
s_client = None
s_client2 = None

#############
# functions #
#############
# functions to encapsulate access to s_client and s_client2
# -----------------------------------------------------------------------------
def createEGSEclients(hostName=None):
  """create the EGSE clients"""
  global s_client, s_client2
  egseProtocol = UTIL.SYS.s_configuration.EGSE_PROTOCOL
  if egseProtocol == "CNC":
    s_client = CNCtcClient(hostName, portNr=int(UTIL.SYS.s_configuration.SCOE_SERVER_PORT))
  elif egseProtocol == "EDEN":
    s_client = EDENclient(hostName, portNr=int(UTIL.SYS.s_configuration.SCOE_SERVER_PORT))
  else:
    LOG_ERROR("invalid EGSE_PROTOCOL defined")
    sys.exit(-1)
  serverPort2 = int(UTIL.SYS.s_configuration.SCOE_SERVER_PORT2)
  if serverPort2 > 0:
    # there is a second server port configured
    if egseProtocol == "CNC":
      s_client2 = CNCtmClient(hostName, portNr=serverPort2)
    elif egseProtocol == "EDEN":
      s_client2 = EDENclient2(hostName, portNr=serverPort2)
  else:
    if egseProtocol == "CNC":
      LOG_ERROR("CNC protocol requires 2 server ports (TC + TM) configured")
      sys.exit(-1)
