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
# MIL Bus general

# MIL Bus Controller
BC_PF_APID = 1920
BC_PL_APID = 1921

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
RT_PF_APID = 1922
RT_PL_APID = 1923

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
        if apid == BC_PF_APID and SPACE.IF.s_milBusController != None:
          if tcFunctionId == BC_Identify_FID:
            if SPACE.IF.s_milBusController.identify(SPACE.IF.MIL_BUS_PF):
              # BC_Identity_PF
              return SPACE.IF.s_onboardComputer.generateEmptyTMpacket("YD2TMPK00001")
            return False
          elif tcFunctionId == BC_SelfTest_FID:
            if SPACE.IF.s_milBusController.selfTest(SPACE.IF.MIL_BUS_PF):
              # BC_SelfTestResponse_PF
              return SPACE.IF.s_onboardComputer.generateEmptyTMpacket("YD2TMPK00002")
            return False
          elif tcFunctionId == BC_GetSelfTestReport_FID:
            if SPACE.IF.s_milBusController.getSelfTestReport(SPACE.IF.MIL_BUS_PF):
              # BC_SelfTestReport_PF
              return SPACE.IF.s_onboardComputer.generateEmptyTMpacket("YD2TMPK00003")
            return False
          elif tcFunctionId == BC_Reset_FID:
            if SPACE.IF.s_milBusController.reset(SPACE.IF.MIL_BUS_PF):
              # BC_ResetResponse_PF
              return SPACE.IF.s_onboardComputer.generateEmptyTMpacket("YD2TMPK00004")
            return False
          elif tcFunctionId == BC_Configure_FID:
            return SPACE.IF.s_milBusController.configure(SPACE.IF.MIL_BUS_PF)
          elif tcFunctionId == BC_ConfigureFrame_FID:
            return SPACE.IF.s_milBusController.configureFrame(SPACE.IF.MIL_BUS_PF)
          elif tcFunctionId == BC_AddInterrogation_FID:
            return SPACE.IF.s_milBusController.addInterrogation(SPACE.IF.MIL_BUS_PF)
          elif tcFunctionId == BC_Discover_FID:
            return SPACE.IF.s_milBusController.discover(SPACE.IF.MIL_BUS_PF)
          elif tcFunctionId == E5013_SETUP_DIST_DATABLOCK_FID:
            return SPACE.IF.s_milBusController.setupDistDatablock(SPACE.IF.MIL_BUS_PF)
          elif tcFunctionId == BC_Start_FID:
            return SPACE.IF.s_milBusController.start(SPACE.IF.MIL_BUS_PF)
          elif tcFunctionId == BC_Stop_FID:
            return SPACE.IF.s_milBusController.stop(SPACE.IF.MIL_BUS_PF)
          elif tcFunctionId == BC_ForceFrameSwitch_FID:
            return SPACE.IF.s_milBusController.forceFrameSwitch(SPACE.IF.MIL_BUS_PF)
          elif tcFunctionId == BC_Send_FID:
            return SPACE.IF.s_milBusController.send(SPACE.IF.MIL_BUS_PF)
          elif tcFunctionId == BC_SetData_FID:
            return SPACE.IF.s_milBusController.setData(SPACE.IF.MIL_BUS_PF)
          elif tcFunctionId == BC_ForceBusSwitch_FID:
            return SPACE.IF.s_milBusController.forceBusSwitch(SPACE.IF.MIL_BUS_PF)
          elif tcFunctionId == BC_InjectError_FID:
            return SPACE.IF.s_milBusController.injectError(SPACE.IF.MIL_BUS_PF)
          elif tcFunctionId == BC_ClearError_FID:
            return SPACE.IF.s_milBusController.clearError(SPACE.IF.MIL_BUS_PF)
          elif tcFunctionId == E5013_BC_ACTIVATE_FID:
            return SPACE.IF.s_milBusController.activate(SPACE.IF.MIL_BUS_PF)
          elif tcFunctionId == E5013_BC_DEACTIVATE_FID:
            return SPACE.IF.s_milBusController.deactivate(SPACE.IF.MIL_BUS_PF)
          elif tcFunctionId == E5013_DTD_FID:
            return SPACE.IF.s_milBusController.dtd(SPACE.IF.MIL_BUS_PF)
        elif apid == RT_PF_APID and SPACE.IF.s_milBusRemoteTerminals != None:
          if tcFunctionId == RT_Identify_FID:
            if SPACE.IF.s_milBusRemoteTerminals.identify(SPACE.IF.MIL_BUS_PF):
              # RT_Identity_PF
              return SPACE.IF.s_onboardComputer.generateEmptyTMpacket("YD2TMPK00030")
            return False
          elif tcFunctionId == RT_SelfTest_FID:
            if SPACE.IF.s_milBusRemoteTerminals.selfTest(SPACE.IF.MIL_BUS_PF):
              # RT_SelfTestResponse_PF
              return SPACE.IF.s_onboardComputer.generateEmptyTMpacket("YD2TMPK00031")
            return False
          elif tcFunctionId == RT_GetSelfTestReport_FID:
            if SPACE.IF.s_milBusRemoteTerminals.getSelfTestReport(SPACE.IF.MIL_BUS_PF):
              # RT_SelfTestReport_PF
              return SPACE.IF.s_onboardComputer.generateEmptyTMpacket("YD2TMPK00032")
            return False
          elif tcFunctionId == RT_Configure_FID:
            return SPACE.IF.s_milBusRemoteTerminals.configure(SPACE.IF.MIL_BUS_PF)
          elif tcFunctionId == RT_AddResponse_FID:
            return SPACE.IF.s_milBusRemoteTerminals.addResponse(SPACE.IF.MIL_BUS_PF)
          elif tcFunctionId == RT_Reset_FID:
            if SPACE.IF.s_milBusRemoteTerminals.reset(SPACE.IF.MIL_BUS_PF):
              # RT_ResetResponse_PF
              return SPACE.IF.s_onboardComputer.generateEmptyTMpacket("YD2TMPK00035")
            return False
          elif tcFunctionId == RT_SAEnable_FID:
            return SPACE.IF.s_milBusRemoteTerminals.saEnable(SPACE.IF.MIL_BUS_PF)
          elif tcFunctionId == E5013_SETUP_ACQU_DATABLOCK_FID:
            return SPACE.IF.s_milBusRemoteTerminals.setupAcquDatablock(SPACE.IF.MIL_BUS_PF)
          elif tcFunctionId == RT_Start_FID:
            return SPACE.IF.s_milBusRemoteTerminals.start(SPACE.IF.MIL_BUS_PF)
          elif tcFunctionId == RT_Stop_FID:
            return SPACE.IF.s_milBusRemoteTerminals.stop(SPACE.IF.MIL_BUS_PF)
          elif tcFunctionId == RT_InjectError_FID:
            return SPACE.IF.s_milBusRemoteTerminals.injectError(SPACE.IF.MIL_BUS_PF)
          elif tcFunctionId == RT_ClearError_FID:
            return SPACE.IF.s_milBusRemoteTerminals.clearError(SPACE.IF.MIL_BUS_PF)
          elif tcFunctionId == E5013_RT_ACTIVATE_FID:
            return SPACE.IF.s_milBusRemoteTerminals.activate(SPACE.IF.MIL_BUS_PF)
          elif tcFunctionId == E5013_RT_DEACTIVATE_FID:
            return SPACE.IF.s_milBusRemoteTerminals.deactivate(SPACE.IF.MIL_BUS_PF)
          elif tcFunctionId == E5013_ATR_FID:
            return SPACE.IF.s_milBusRemoteTerminals.atr(SPACE.IF.MIL_BUS_PF)
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
