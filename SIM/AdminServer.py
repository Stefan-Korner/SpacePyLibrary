#******************************************************************************
# (C) 2014, Stefan Korner, Austria                                            *
#                                                                             *
# The Space Python Library is free software; you can redistribute it and/or   *
# modify it under the terms of the GNU Lesser General Public License as       *
# published by the Free Software Foundation; either version 2.1 of the        *
# License, or (at your option) any later version.                             *
#                                                                             *
# The Space C++ Library is distributed in the hope that it will be useful,    *
# but WITHOUT ANY WARRANTY; without even the implied warranty of              *
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser     *
# General Public License for more details.                                    *
#******************************************************************************
# NCTRS admin message server                                                  *
#******************************************************************************
import sys
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import GRND.NCTRS
import UTIL.SYS, UTIL.TASK

###########
# classes #
###########
# =============================================================================
class AdminSender(GRND.NCTRS.AdminMessageSender):
  """Subclass of GRND.NCTRS.AdminMessageSender"""
  def __init__(self, portNr, groundstationName):
    """Initialise attributes only"""
    GRND.NCTRS.AdminMessageSender.__init__(self, portNr, groundstationName)
  # ---------------------------------------------------------------------------
  def clientAccepted(self):
    """Overloaded from GRND.NCTRS.AdminMessageSender"""
    LOG_INFO("NCTRS admin message receiver (client) accepted", "GRND")
    # notify the status change
    UTIL.TASK.s_processingTask.setTCconnected()
    # establish TC link
    self.sendAdminMessageTC(GRND.NCTRSDU.ADMIN_MSG_TC_LINK_ESTABLISHED_TO_GS)
  # ---------------------------------------------------------------------------
  def notifyError(self, errorMessage, data):
    """error notification"""
    LOG_ERROR(errorMessage)
    try:
      LOG(str(data))
    except Exception, ex:
      LOG_WARNING("data passed to notifyError are invalid: " + str(ex))

####################
# global variables #
####################
# NCTRS admin message sender is a singleton
s_adminSender = None

#############
# functions #
#############
# functions to encapsulate access to s_adminSender
# -----------------------------------------------------------------------------
def createAdminSender():
  """create the NCTRS admin message sender"""
  global s_adminSender
  s_adminSender = AdminSender(
    portNr=int(UTIL.SYS.s_configuration.NCTRS_ADMIN_SERVER_PORT),
    groundstationName=UTIL.SYS.s_configuration.GROUND_STATION_NAME)
  if not s_adminSender.openConnectPort():
    sys.exit(-1)
# -----------------------------------------------------------------------------
def sendAdminMessageTC(eventId, adCounter=0, vcId=0, mapId=0):
  """Send the TC admin message data unit"""
  global s_adminSender
  if s_adminSender == None:
    LOG_ERROR("No NCTRS admin message sender available", "GRND")
  else:
    s_adminSender.sendAdminMessageTC(eventId, adCounter, vcId, mapId)
