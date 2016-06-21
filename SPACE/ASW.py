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

#############
# constants #
#############
# MIL Bus Controller
BC_Identify_FID = 0x4E21
BC_SelfTest_FID = 0x4E22
BC_GetSelfTestReport_FID = 0x4E23
BC_Reset_FID = 0x4E24
BC_Configure_FID = 0x4E25
BC_ConfigureFrame_FID = 0x4E26
BC_AddInterrogation_FID = 0x4E27
BC_Discover_FID = 0x4E28
E5013_SETUP_DIST_DATABLOCK_FID = 0x4E2D
BC_Start_FID = 0x4E2E
BC_Stop_FID = 0x4E2F
BC_ForceFrameSwitch_FID = 0x4E29
BC_Send_FID = 0x4E30
BC_SetData_FID = 0x4E31
BC_ForceBusSwitch_FID = 0x4E32
BC_InjectError_FID = 0x4E33
BC_ClearError_FID = 0x4E34
E5013_BC_ACTIVATE_FID = 0x4E35
E5013_BC_DEACTIVATE_FID = 0x4E36
E5013_DTD_FID = 0x4E39

# MIL Bus Remote Terminal
RT_Identify_FID = 0x4E3E
RT_SelfTest_FID = 0x4E3F
RT_GetSelfTestReport_FID = 0x4E40
RT_Configure_FID = 0x4E41
RT_AddResponse_FID = 0x4E42
RT_Reset_FID = 0x4E43
RT_SAEnable_FID = 0x4E44
E5013_SETUP_ACQU_DATABLOCK_FID = 0x4E2A
RT_Start_FID = 0x4E45
RT_Stop_FID = 0x4E46
RT_InjectError_FID = 0x4E47
RT_ClearError_FID = 0x4E48
E5013_RT_ACTIVATE_FID = 0x4E49
E5013_RT_DEACTIVATE_FID = 0x4E4A
E5013_ATR_FID = 0x4E4B

###########
# classes #
###########
# =============================================================================
class ApplicationSoftwareImpl(SPACE.IF.ApplicationSoftware):
  """Implementation of the spacecraft's application software"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """Initialise attributes only"""
    self.tcFunctionIdBytePos = \
      int(UTIL.SYS.s_configuration.TC_FKT_ID_BYTE_OFFSET)
    self.tcFunctionIdByteSize = \
      int(UTIL.SYS.s_configuration.TC_FKT_ID_BYTE_SIZE)
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
        apid = tcPacketDu.applicationProcessId
        tcFunctionId = tcPacketDu.getUnsigned(
          self.tcFunctionIdBytePos, self.tcFunctionIdByteSize)
        LOG("tcFunctionId = " + str(tcFunctionId), "SPACE")
        if apid == 1920 and SPACE.IF.s_milBusController != None:
          if tcFunctionId == BC_Identify_FID:
            return SPACE.IF.s_milBusController.identify()
          elif tcFunctionId == BC_SelfTest_FID:
            return SPACE.IF.s_milBusController.selfTest()
          elif tcFunctionId == BC_GetSelfTestReport_FID:
            return SPACE.IF.s_milBusController.getSelfTestReport()
          elif tcFunctionId == BC_Reset_FID:
            return SPACE.IF.s_milBusController.reset()
          elif tcFunctionId == BC_Configure_FID:
            return SPACE.IF.s_milBusController.configure()
          elif tcFunctionId == BC_ConfigureFrame_FID:
            return SPACE.IF.s_milBusController.configureFrame()
          elif tcFunctionId == BC_AddInterrogation_FID:
            return SPACE.IF.s_milBusController.addInterrogation()
          elif tcFunctionId == BC_Discover_FID:
            return SPACE.IF.s_milBusController.discover()
          elif tcFunctionId == E5013_SETUP_DIST_DATABLOCK_FID:
            return SPACE.IF.s_milBusController.setupDistDatablock()
          elif tcFunctionId == BC_Start_FID:
            return SPACE.IF.s_milBusController.start()
          elif tcFunctionId == BC_Stop_FID:
            return SPACE.IF.s_milBusController.stop()
          elif tcFunctionId == BC_ForceFrameSwitch_FID:
            return SPACE.IF.s_milBusController.forceFrameSwitch()
          elif tcFunctionId == BC_Send_FID:
            return SPACE.IF.s_milBusController.send()
          elif tcFunctionId == BC_SetData_FID:
            return SPACE.IF.s_milBusController.setData()
          elif tcFunctionId == BC_ForceBusSwitch_FID:
            return SPACE.IF.s_milBusController.forceBusSwitch()
          elif tcFunctionId == BC_InjectError_FID:
            return SPACE.IF.s_milBusController.injectError()
          elif tcFunctionId == BC_ClearError_FID:
            return SPACE.IF.s_milBusController.clearError()
          elif tcFunctionId == E5013_BC_ACTIVATE_FID:
            return SPACE.IF.s_milBusController.activate()
          elif tcFunctionId == E5013_BC_DEACTIVATE_FID:
            return SPACE.IF.s_milBusController.deactivate()
          elif tcFunctionId == E5013_DTD_FID:
            return SPACE.IF.s_milBusController.dtd()
        elif apid == 1922 and SPACE.IF.s_milBusRemoteTerminals != None:
          if tcFunctionId == RT_Identify_FID:
            return SPACE.IF.s_milBusRemoteTerminals.identify()
          elif tcFunctionId == RT_SelfTest_FID:
            return SPACE.IF.s_milBusRemoteTerminals.selfTest()
          elif tcFunctionId == RT_GetSelfTestReport_FID:
            return SPACE.IF.s_milBusRemoteTerminals.getSelfTestReport()
          elif tcFunctionId == RT_Configure_FID:
            return SPACE.IF.s_milBusRemoteTerminals.configure()
          elif tcFunctionId == RT_AddResponse_FID:
            return SPACE.IF.s_milBusRemoteTerminals.addResponse()
          elif tcFunctionId == RT_Reset_FID:
            return SPACE.IF.s_milBusRemoteTerminals.reset()
          elif tcFunctionId == RT_SAEnable_FID:
            return SPACE.IF.s_milBusRemoteTerminals.saEnable()
          elif tcFunctionId == E5013_SETUP_ACQU_DATABLOCK_FID:
            return SPACE.IF.s_milBusRemoteTerminals.setupAcquDatablock()
          elif tcFunctionId == RT_Start_FID:
            return SPACE.IF.s_milBusRemoteTerminals.start()
          elif tcFunctionId == RT_Stop_FID:
            return SPACE.IF.s_milBusRemoteTerminals.stop()
          elif tcFunctionId == RT_InjectError_FID:
            return SPACE.IF.s_milBusRemoteTerminals.injectError()
          elif tcFunctionId == RT_ClearError_FID:
            return SPACE.IF.s_milBusRemoteTerminals.clearError()
          elif tcFunctionId == E5013_RT_ACTIVATE_FID:
            return SPACE.IF.s_milBusRemoteTerminals.activate()
          elif tcFunctionId == E5013_RT_DEACTIVATE_FID:
            return SPACE.IF.s_milBusRemoteTerminals.deactivate()
          elif tcFunctionId == E5013_ATR_FID:
            return SPACE.IF.s_milBusRemoteTerminals.atr()
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
