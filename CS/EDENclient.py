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
import sys
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import EGSE.EDEN, EGSE.IF
import UTIL.SYS

###########
# classes #
###########
# =============================================================================
class Client(EGSE.EDEN.Client):
  """Subclass of EGSE.EDEN.Client"""
  # this client sends CCSDS TC packets and received CCSDS TM packets
  # ---------------------------------------------------------------------------
  def __init__(self, hostName, portNr):
    """Initialise attributes only"""
    EGSE.EDEN.Client.__init__(self)
    self.hostName = hostName
    self.portNr = portNr

# =============================================================================
class Client2(EGSE.EDEN.Client):
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
    # no EDEN connection configured
    LOG_INFO
  edenPort = int(EGSE.IF.s_edenClientConfiguration.edenPort)
  s_client = Client(edenHost, edenPort)
  edenPort2 = int(EGSE.IF.s_edenClientConfiguration.edenPort2)
  if edenPort2 > 0:
    # there is a second EDEN connection configured
    s_client2 = Client2(edenHost, edenPort2)
