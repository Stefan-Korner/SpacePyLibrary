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
# NCTRS TC server                                                             *
#******************************************************************************
import sys
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import CCSDS.PACKET
import GRND.NCTRS
import LINK.IF
import PUS.SERVICES
import SPACE.OBC, SPACE.TMGEN
import UTIL.SYS, UTIL.TASK

###########
# classes #
###########
# =============================================================================
class NCTRStcReceiver(GRND.NCTRS.TCreceiver):
  """Subclass of GRND.NCTRS.TCreceiver"""
  # ---------------------------------------------------------------------------
  def __init__(self, portNr, groundstationId):
    """Initialise attributes only"""
    GRND.NCTRS.TCreceiver.__init__(self, portNr, groundstationId)
  # ---------------------------------------------------------------------------
  def clientAccepted(self):
    """Overloaded from GRND.NCTRS.TCreceiver"""
    LOG_INFO("NCTRS TC sender (client) accepted", "GRND")
    # notify the status change
    UTIL.TASK.s_processingTask.setAdminConnected()
  # ---------------------------------------------------------------------------
  def notifyTCpacketDataUnit(self, tcPktDu):
    """AD packet / BD segment received"""
    LOG_INFO("notifyTCpacketDataUnit", "GNRD")
    LOG("tcPktDu = " + str(tcPktDu), "GNRD")
    GRND.NCTRS.TCreceiver.notifyTCpacketDataUnit(self, tcPktDu)
  # ---------------------------------------------------------------------------
  def notifyTCcltuDataUnit(self, tcCltuDu):
    """CLTU received"""
    LOG_INFO("notifyTCcltuDataUnit", "GNRD")
    GRND.NCTRS.TCreceiver.notifyTCcltuDataUnit(self, tcCltuDu)
  # ---------------------------------------------------------------------------
  def notifyTCdirectivesDataUnit(self, tcDirDu):
    """COP1 directive received"""
    LOG_INFO("notifyTCdirectivesDataUnit", "GNRD")
    LOG("tcDirDu = " + str(tcDirDu), "GNRD")
  # ---------------------------------------------------------------------------
  def notifyError(self, errorMessage, data):
    """error notification"""
    LOG_ERROR(errorMessage)
    try:
      LOG(str(data))
    except Exception as ex:
      LOG_WARNING("data passed to notifyError are invalid: " + str(ex))
  # ---------------------------------------------------------------------------
  def notifyTCpacket(self, packetData):
    """TC packet received"""
    # delegate the packet processing from GROUND to SPACE
    tcPacketDu = CCSDS.PACKET.TCpacket(packetData)
    SPACE.IF.s_onboardComputer.pushTCpacket(tcPacketDu)
  # ---------------------------------------------------------------------------
  def notifyCltu(self, cltu):
    """CLTU received"""
    # delegate the CLTU processing from GROUND to SPACE
    LINK.IF.s_spaceLink.pushTCcltu(cltu)

####################
# global variables #
####################
# NCTRS TC receiver is a singleton
s_tcReceiver = None

#############
# functions #
#############
# functions to encapsulate access to s_tcReceiver
# -----------------------------------------------------------------------------
def createTCreceiver(hostName=None):
  """create the NCTRS TC receiver"""
  global s_tcReceiver
  s_tcReceiver = NCTRStcReceiver(
    portNr=int(UTIL.SYS.s_configuration.NCTRS_TC_SERVER_PORT),
    groundstationId=int(UTIL.SYS.s_configuration.DEF_GROUND_STATION_ID))
  if not s_tcReceiver.openConnectPort(hostName):
    sys.exit(-1)
