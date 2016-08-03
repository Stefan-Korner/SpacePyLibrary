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
MTG_BC_PF_APID = 1920
MTG_BC_PL_APID = 1921
S4_BC_PF_APID = 1537
S4_BC_PL_APID = 1539

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
MTG_RT_PF_APID = 1922
MTG_RT_PL_APID = 1923
S4_RT_PF_APID = 1538
S4_RT_PL_APID = 1540

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
  # shall be overloaded in derived classes
  def sendBC_Identity(self, bus):
    pass
  def sendBC_SelfTestResponse(self, bus, errorId):
    pass
  def sendBC_SelfTestReport(self, bus):
    pass
  def sendBC_ResetResponse(self, bus):
    pass
  def sendRT_Identity(self, bus):
    pass
  def sendRT_SelfTestResponse(self, bus, errorId):
    pass
  def sendRT_SelfTestReport(self, bus):
    pass
  def sendRT_ResetResponse(self, bus):
    pass
  # ---------------------------------------------------------------------------
  def processTCpacket(self, tcPacketDu):
    """
    processes a telecommand C&C packet from the CCS
    implementation of SPACE.IF.ApplicationSoftware.processTCpacket
    """
    apid = tcPacketDu.applicationProcessId
    LOG_INFO("ApplicationSoftwareImpl.processTCpacke(" + str(apid) + ")t", "SPACE")
    # packet is a PUS Function Management command
    if tcPacketDu.serviceType == PUS.SERVICES.TC_FKT_TYPE:
      if tcPacketDu.serviceSubType == PUS.SERVICES.TC_FKT_PERFORM_FUNCITON:
        tcFunctionId = tcPacketDu.getUnsigned(
          self.tcFunctionIdBytePos, self.tcFunctionIdByteSize)
        LOG("tcFunctionId = " + str(tcFunctionId), "SPACE")
        forwardToBc = False
        forwardToRt = False
        if apid == self.getBcPfAPID():
          forwardToBc = True
          bus = SPACE.IF.MIL_BUS_PF
        elif apid == self.getBcPlAPID():
          forwardToBc = True
          bus = SPACE.IF.MIL_BUS_PL
        elif apid == self.getRtPfAPID():
          forwardToRt = True
          bus = SPACE.IF.MIL_BUS_PF
        elif apid == self.getRtPlAPID():
          forwardToRt = True
          bus = SPACE.IF.MIL_BUS_PL
        else:
          # unexpected APID
          return False
        if forwardToBc and SPACE.IF.s_milBusController != None:
          if tcFunctionId == BC_Identify_FID:
            if SPACE.IF.s_milBusController.identify(bus):
              return self.sendBC_Identity(bus)
            return False
          elif tcFunctionId == BC_SelfTest_FID:
            errorId = 1
            if SPACE.IF.s_milBusController.selfTest(bus):
              errorId = 0
            return self.sendBC_SelfTestResponse(bus, errorId)
          elif tcFunctionId == BC_GetSelfTestReport_FID:
            if SPACE.IF.s_milBusController.getSelfTestReport(bus):
              return self.sendBC_SelfTestReport(bus)
            return False
          elif tcFunctionId == BC_Reset_FID:
            if SPACE.IF.s_milBusController.reset(bus):
              return self.sendBC_ResetResponse(bus)
            return False
          elif tcFunctionId == BC_Configure_FID:
            return SPACE.IF.s_milBusController.configure(bus)
          elif tcFunctionId == BC_ConfigureFrame_FID:
            return SPACE.IF.s_milBusController.configureFrame(bus)
          elif tcFunctionId == BC_AddInterrogation_FID:
            return SPACE.IF.s_milBusController.addInterrogation(bus)
          elif tcFunctionId == BC_Discover_FID:
            return SPACE.IF.s_milBusController.discover(bus)
          elif tcFunctionId == E5013_SETUP_DIST_DATABLOCK_FID:
            return SPACE.IF.s_milBusController.setupDistDatablock(bus)
          elif tcFunctionId == BC_Start_FID:
            return SPACE.IF.s_milBusController.start(bus)
          elif tcFunctionId == BC_Stop_FID:
            return SPACE.IF.s_milBusController.stop(bus)
          elif tcFunctionId == BC_ForceFrameSwitch_FID:
            return SPACE.IF.s_milBusController.forceFrameSwitch(bus)
          elif tcFunctionId == BC_Send_FID:
            return SPACE.IF.s_milBusController.send(bus)
          elif tcFunctionId == BC_SetData_FID:
            return SPACE.IF.s_milBusController.setData(bus)
          elif tcFunctionId == BC_ForceBusSwitch_FID:
            return SPACE.IF.s_milBusController.forceBusSwitch(bus)
          elif tcFunctionId == BC_InjectError_FID:
            return SPACE.IF.s_milBusController.injectError(bus)
          elif tcFunctionId == BC_ClearError_FID:
            return SPACE.IF.s_milBusController.clearError(bus)
          elif tcFunctionId == E5013_BC_ACTIVATE_FID:
            return SPACE.IF.s_milBusController.activate(bus)
          elif tcFunctionId == E5013_BC_DEACTIVATE_FID:
            return SPACE.IF.s_milBusController.deactivate(bus)
          elif tcFunctionId == E5013_DTD_FID:
            return SPACE.IF.s_milBusController.dtd(bus)
        elif forwardToRt and SPACE.IF.s_milBusRemoteTerminals != None:
          if tcFunctionId == RT_Identify_FID:
            if SPACE.IF.s_milBusRemoteTerminals.identify(bus):
              return self.sendRT_Identity(bus)
            return False
          elif tcFunctionId == RT_SelfTest_FID:
            errorId = 1
            if SPACE.IF.s_milBusRemoteTerminals.selfTest(bus):
              errorId = 0
            return self.sendRT_SelfTestResponse(bus, errorId)
          elif tcFunctionId == RT_GetSelfTestReport_FID:
            if SPACE.IF.s_milBusRemoteTerminals.getSelfTestReport(bus):
              return self.sendRT_SelfTestReport(bus)
            return False
          elif tcFunctionId == RT_Configure_FID:
            return SPACE.IF.s_milBusRemoteTerminals.configure(bus)
          elif tcFunctionId == RT_AddResponse_FID:
            return SPACE.IF.s_milBusRemoteTerminals.addResponse(bus)
          elif tcFunctionId == RT_Reset_FID:
            if SPACE.IF.s_milBusRemoteTerminals.reset(bus):
              return self.sendRT_ResetResponse(bus)
            return False
          elif tcFunctionId == RT_SAEnable_FID:
            return SPACE.IF.s_milBusRemoteTerminals.saEnable(bus)
          elif tcFunctionId == E5013_SETUP_ACQU_DATABLOCK_FID:
            return SPACE.IF.s_milBusRemoteTerminals.setupAcquDatablock(bus)
          elif tcFunctionId == RT_Start_FID:
            return SPACE.IF.s_milBusRemoteTerminals.start(bus)
          elif tcFunctionId == RT_Stop_FID:
            return SPACE.IF.s_milBusRemoteTerminals.stop(bus)
          elif tcFunctionId == RT_InjectError_FID:
            return SPACE.IF.s_milBusRemoteTerminals.injectError(bus)
          elif tcFunctionId == RT_ClearError_FID:
            return SPACE.IF.s_milBusRemoteTerminals.clearError(bus)
          elif tcFunctionId == E5013_RT_ACTIVATE_FID:
            return SPACE.IF.s_milBusRemoteTerminals.activate(bus)
          elif tcFunctionId == E5013_RT_DEACTIVATE_FID:
            return SPACE.IF.s_milBusRemoteTerminals.deactivate(bus)
          elif tcFunctionId == E5013_ATR_FID:
            return SPACE.IF.s_milBusRemoteTerminals.atr(bus)
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

# =============================================================================
class MTGapplicationSoftwareImpl(ApplicationSoftwareImpl):
  """Implementation of the MTG spacecraft's application software"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """Initialise attributes only"""
    ApplicationSoftwareImpl.__init__(self)
  # ---------------------------------------------------------------------------
  def getBcPfAPID(self):
    """implementation of SPACE.IF.ApplicationSoftware.getBcPfAPID"""
    return MTG_BC_PF_APID
  # ---------------------------------------------------------------------------
  def getBcPlAPID(self):
    """implementation of SPACE.IF.ApplicationSoftware.getBcPfAPID"""
    return MTG_BC_PL_APID
  # ---------------------------------------------------------------------------
  def getRtPfAPID(self):
    """implementation of SPACE.IF.ApplicationSoftware.getBcPfAPID"""
    return MTG_RT_PF_APID
  # ---------------------------------------------------------------------------
  def getRtPlAPID(self):
    """implementation of SPACE.IF.ApplicationSoftware.getBcPfAPID"""
    return MTG_RT_PL_APID
  # ---------------------------------------------------------------------------
  def sendBC_Identity(self, bus):
    """implementation of ApplicationSoftwareImpl.sendBC_Identity"""
    if bus == SPACE.IF.MIL_BUS_PF:
      return SPACE.IF.s_onboardComputer.generateEmptyTMpacket("YD2TMPK00001")
    else:
      return SPACE.IF.s_onboardComputer.generateEmptyTMpacket("YD2TMPK00501")
  # ---------------------------------------------------------------------------
  def sendBC_SelfTestResponse(self, bus, errorId):
    """implementation of ApplicationSoftwareImpl.sendBC_SelfTestResponse"""
    if bus == SPACE.IF.MIL_BUS_PF:
      pktMnemonic = "YD2TMPK00002"
      parErrorId = "ZD2M182X"
    else:
      pktMnemonic = "YD2TMPK00502"
      parErrorId = "ZD2M682X"
    tmPacketData = SPACE.IF.s_definitions.getTMpacketInjectData(pktMnemonic,
      parErrorId, str(errorId))
    # check the TM packet data
    if tmPacketData == None:
      LOG_ERROR("TM packet creation failed for " + pktMnemonic, "SPACE")
      return False
    # send the TM packet
    return SPACE.IF.s_onboardComputer.generateTMpacket(tmPacketData)
  # ---------------------------------------------------------------------------
  def sendBC_SelfTestReport(self, bus):
    """implementation of ApplicationSoftwareImpl.sendBC_SelfTestReport"""
    if bus == SPACE.IF.MIL_BUS_PF:
      return SPACE.IF.s_onboardComputer.generateEmptyTMpacket("YD2TMPK00003")
    else:
      return SPACE.IF.s_onboardComputer.generateEmptyTMpacket("YD2TMPK00503")
  # ---------------------------------------------------------------------------
  def sendBC_ResetResponse(self, bus):
    """implementation of ApplicationSoftwareImpl.sendBC_ResetResponse"""
    if bus == SPACE.IF.MIL_BUS_PF:
      return SPACE.IF.s_onboardComputer.generateEmptyTMpacket("YD2TMPK00004")
    else:
      return SPACE.IF.s_onboardComputer.generateEmptyTMpacket("YD2TMPK00504")
  # ---------------------------------------------------------------------------
  def sendRT_Identity(self, bus):
    """implementation of ApplicationSoftwareImpl.sendRT_Identity"""
    if bus == SPACE.IF.MIL_BUS_PF:
      return SPACE.IF.s_onboardComputer.generateEmptyTMpacket("YD2TMPK00030")
    else:
      return SPACE.IF.s_onboardComputer.generateEmptyTMpacket("YD2TMPK00530")
  # ---------------------------------------------------------------------------
  def sendRT_SelfTestResponse(self, bus, errorId):
    """implementation of ApplicationSoftwareImpl.sendRT_SelfTestResponse"""
    if bus == SPACE.IF.MIL_BUS_PF:
      pktMnemonic = "YD2TMPK00031"
      parErrorId = "ZD2M198X"
    else:
      pktMnemonic = "YD2TMPK00531"
      parErrorId = "ZD2M698X"
    tmPacketData = SPACE.IF.s_definitions.getTMpacketInjectData(pktMnemonic,
      parErrorId, str(errorId))
    # check the TM packet data
    if tmPacketData == None:
      LOG_ERROR("TM packet creation failed for " + pktMnemonic, "SPACE")
      return False
    # send the TM packet
    return SPACE.IF.s_onboardComputer.generateTMpacket(tmPacketData)
  # ---------------------------------------------------------------------------
  def sendRT_SelfTestReport(self, bus):
    """implementation of ApplicationSoftwareImpl.sendRT_SelfTestReport"""
    if bus == SPACE.IF.MIL_BUS_PF:
      return SPACE.IF.s_onboardComputer.generateEmptyTMpacket("YD2TMPK00032")
    else:
      return SPACE.IF.s_onboardComputer.generateEmptyTMpacket("YD2TMPK00532")
  # ---------------------------------------------------------------------------
  def sendRT_ResetResponse(self, bus):
    """implementation of ApplicationSoftwareImpl.sendRT_ResetResponse"""
    if bus == SPACE.IF.MIL_BUS_PF:
      return SPACE.IF.s_onboardComputer.generateEmptyTMpacket("YD2TMPK00035")
    else:
      return SPACE.IF.s_onboardComputer.generateEmptyTMpacket("YD2TMPK00535")

# =============================================================================
class S4applicationSoftwareImpl(ApplicationSoftwareImpl):
  """Implementation of the Sentinel 4 spacecraft's application software"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """Initialise attributes only"""
    ApplicationSoftwareImpl.__init__(self)
  # ---------------------------------------------------------------------------
  def getBcPfAPID(self):
    """implementation of SPACE.IF.ApplicationSoftware.getBcPfAPID"""
    return S4_BC_PF_APID
  # ---------------------------------------------------------------------------
  def getBcPlAPID(self):
    """implementation of SPACE.IF.ApplicationSoftware.getBcPfAPID"""
    return S4_BC_PL_APID
  # ---------------------------------------------------------------------------
  def getRtPfAPID(self):
    """implementation of SPACE.IF.ApplicationSoftware.getBcPfAPID"""
    return S4_RT_PF_APID
  # ---------------------------------------------------------------------------
  def getRtPlAPID(self):
    """implementation of SPACE.IF.ApplicationSoftware.getBcPfAPID"""
    return S4_RT_PL_APID
  # ---------------------------------------------------------------------------
  def sendBC_Identity(self, bus):
    """implementation of ApplicationSoftwareImpl.sendBC_Identity"""
    if bus == SPACE.IF.MIL_BUS_PF:
      return SPACE.IF.s_onboardComputer.generateEmptyTMpacket("XPSTMPK10101")
    else:
      return SPACE.IF.s_onboardComputer.generateEmptyTMpacket("XPSTMPK10601")
  # ---------------------------------------------------------------------------
  def sendBC_SelfTestResponse(self, bus, errorId):
    """implementation of ApplicationSoftwareImpl.sendBC_SelfTestResponse"""
    if bus == SPACE.IF.MIL_BUS_PF:
      pktMnemonic = "XPSTMPK10102"
      parErrorId = "XPSM100X"
    else:
      pktMnemonic = "XPSTMPK10602"
      parErrorId = "XPSM600X"
    tmPacketData = SPACE.IF.s_definitions.getTMpacketInjectData(pktMnemonic,
      parErrorId, str(errorId))
    # check the TM packet data
    if tmPacketData == None:
      LOG_ERROR("TM packet creation failed for " + pktMnemonic, "SPACE")
      return False
    # send the TM packet
    return SPACE.IF.s_onboardComputer.generateTMpacket(tmPacketData)
  # ---------------------------------------------------------------------------
  def sendBC_SelfTestReport(self, bus):
    """implementation of ApplicationSoftwareImpl.sendBC_SelfTestReport"""
    if bus == SPACE.IF.MIL_BUS_PF:
      return SPACE.IF.s_onboardComputer.generateEmptyTMpacket("XPSTMPK10103")
    else:
      return SPACE.IF.s_onboardComputer.generateEmptyTMpacket("XPSTMPK10603")
  # ---------------------------------------------------------------------------
  def sendBC_ResetResponse(self, bus):
    """implementation of ApplicationSoftwareImpl.sendBC_ResetResponse"""
    if bus == SPACE.IF.MIL_BUS_PF:
      return SPACE.IF.s_onboardComputer.generateEmptyTMpacket("XPSTMPK10104")
    else:
      return SPACE.IF.s_onboardComputer.generateEmptyTMpacket("XPSTMPK10604")
  # ---------------------------------------------------------------------------
  def sendRT_Identity(self, bus):
    """implementation of ApplicationSoftwareImpl.sendRT_Identity"""
    if bus == SPACE.IF.MIL_BUS_PF:
      return SPACE.IF.s_onboardComputer.generateEmptyTMpacket("XPSTMPK10130")
    else:
      return SPACE.IF.s_onboardComputer.generateEmptyTMpacket("XPSTMPK10630")
  # ---------------------------------------------------------------------------
  def sendRT_SelfTestResponse(self, bus, errorId):
    """implementation of ApplicationSoftwareImpl.sendRT_SelfTestResponse"""
    if bus == SPACE.IF.MIL_BUS_PF:
      pktMnemonic = "XPSTMPK10131"
      parErrorId = "XPSM184X"
    else:
      pktMnemonic = "XPSTMPK10631"
      parErrorId = "XPSM684X"
    tmPacketData = SPACE.IF.s_definitions.getTMpacketInjectData(pktMnemonic,
      parErrorId, str(errorId))
    # check the TM packet data
    if tmPacketData == None:
      LOG_ERROR("TM packet creation failed for " + pktMnemonic, "SPACE")
      return False
    # send the TM packet
    return SPACE.IF.s_onboardComputer.generateTMpacket(tmPacketData)
  # ---------------------------------------------------------------------------
  def sendRT_SelfTestReport(self, bus):
    """implementation of ApplicationSoftwareImpl.sendRT_SelfTestReport"""
    if bus == SPACE.IF.MIL_BUS_PF:
      return SPACE.IF.s_onboardComputer.generateEmptyTMpacket("XPSTMPK10132")
    else:
      return SPACE.IF.s_onboardComputer.generateEmptyTMpacket("XPSTMPK10632")
  # ---------------------------------------------------------------------------
  def sendRT_ResetResponse(self, bus):
    """implementation of ApplicationSoftwareImpl.sendRT_ResetResponse"""
    if bus == SPACE.IF.MIL_BUS_PF:
      return SPACE.IF.s_onboardComputer.generateEmptyTMpacket("XPSTMPK10135")
    else:
      return SPACE.IF.s_onboardComputer.generateEmptyTMpacket("XPSTMPK10635")

#############
# functions #
#############
def init():
  # initialise singleton(s)
  mission = UTIL.SYS.s_configuration.ASW_MISSION
  if mission == "MTG":
    SPACE.IF.s_applicationSoftware = MTGapplicationSoftwareImpl()
  elif mission == "S4":
    SPACE.IF.s_applicationSoftware = S4applicationSoftwareImpl()
  else:
    LOG_ERROR("No ASW implementation for mission " + mission + " present", "SPACE")
