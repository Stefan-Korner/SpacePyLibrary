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
import EGSE.CNC, EGSE.IF
import UTIL.SYS

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
    # no CNC connection configured
    LOG_INFO
  cncPort = int(EGSE.IF.s_cncClientConfiguration.cncPort)
  s_client = TCclient(cncHost, cncPort)
  cncPort2 = int(EGSE.IF.s_cncClientConfiguration.cncPort2)
  s_client2 = TMclient(cncHost, cncPort2)
