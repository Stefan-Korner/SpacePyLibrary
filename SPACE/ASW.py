#******************************************************************************
# (C) 2016, Stefan Korner, Austria                                            *
#                                                                             *
# The Space Python Library is free software; you can redistribute it and/or   *
# modify it under the terms of the GNU Lesser General Public License as       *
# published by the Free Software Foundation; either version 2.1 of the        *
# License, or (at your option) any later version.                             *
#                                                                             *
# The Space Python Library is distributed in the hope that it will be useful, *
# but WITHOUT ANY WARRANTY; without even the implied warranty of              *
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser     *
# General Public License for more details.                                    *
#******************************************************************************
# Spacecraft Application Software                                             *
#******************************************************************************
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import PUS.PACKET, PUS.SERVICES
import SPACE.IF
import UTIL.SYS

###########
# classes #
###########

# =============================================================================
class ApplicationSoftwareImpl(SPACE.IF.ApplicationSoftware):
  """Implementation of the spacecraft's application software"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """Initialise attributes only"""
    self.tcFunctionIdBytePos = UTIL.SYS.s_configuration.TC_FKT_ID_BYTE_OFFSET
    self.tcFunctionIdByteSize = UTIL.SYS.s_configuration.TC_FKT_ID_BYTE_SIZE
  # ---------------------------------------------------------------------------
  def processTCpacket(self, tcPacketDu):
    """
    processes a telecommand C&C packet from the CCS
    implementation of SPACE.IF.ApplicationSoftware.processTCpacket
    """
    LOG_INFO("ApplicationSoftwareImpl.processTCpacket", "SPACE")
    # packet is a PUS Function Management command
    if tcPacketDu.serviceType == PUS.SERVICES.TC_FKT_TYPE:
      if tcPacketDu.serviceSubType == PUS.SERVICES.TC_FKT_PERFORM_FUNCITON:
#******************************************************************************
# faked processing begin
#******************************************************************************
        apid = tcPacketDu.applicationProcessId
        if apid == 1920:
          if SPACE.IF.s_milBusController != None:
            return SPACE.IF.s_milBusController.processTCpacket(tcPacketDu)
        elif apid == 1922:
          if SPACE.IF.s_milBusRemoteTerminals != None:
            return SPACE.IF.s_milBusRemoteTerminals.processTCpacket(tcPacketDu)
#******************************************************************************
# faked processing end
#******************************************************************************
        tcFunctionId = tcPacketDu.getUnsigned(
          self.tcFunctionIdBytePos, self.tcFunctionIdByteSize)
        LOG("tcFunctionId = " + str(tcFunctionId), "SPACE")
    return True
  # ---------------------------------------------------------------------------
  def notifyMILdatablockAcquisition(self, rtAddress, dataBlock):
    """
    The BC has received on the MIL Bus a data block from a RT
    """
    LOG_INFO("ApplicationSoftwareImpl.notifyMILdatablockAcquisition(" + str(rtAddress) + ")", "SPACE")
  # ---------------------------------------------------------------------------
  def notifyMILdatablockDistribution(self, rtAddress, dataBlock):
    """
    The mRT has received on the MIL Bus a data block from the BC
    """
    LOG_INFO("ApplicationSoftwareImpl.notifyMILdatablockDistribution(" + str(rtAddress) + ")", "SPACE")

#############
# functions #
#############
def init():
  # initialise singleton(s)
  SPACE.IF.s_applicatonSoftware = ApplicationSoftwareImpl()
