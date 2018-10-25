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
# Spacecraft Application Software                                             *
#******************************************************************************
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import PUS.PACKET, PUS.SERVICES
import SPACE.IF
import UTIL.DU, UTIL.SYS

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

# EUCLID Power SCOEs
BS_Initialize = 0x0302
BS_SetLocal = 0x0314
BS_SetRemote = 0x0315
BS_LockInstruments = 0x0312
BS_UnlockInstruments = 0x0313
BS_SetOnline = 0x0307
BS_SetOffline = 0x0306
BS_SelfTest = 0x0311
FTH_Initialize = 0x0403
FTH_EnableGUI = 0x0435
FTH_DisableGUI = 0x0436
FTH_SetOnline = 0x0405
FTH_SetOffline = 0x0406
FTH_SelfTest = 0x0410
FTH_ConfigNEA = 0x0411
FTH_ConfigNEA_NEA_ID_BYTE_OFFSET = 14
FTH_ConfigNEA_NEA_ID_BYTE_SIZE = 64
FTH_ConfigNEA_A_LO_BYTE_OFFSET = 78
FTH_ConfigNEA_A_LO_BYTE_SIZE = 4
FTH_ConfigNEA_A_HI_min_BYTE_OFFSET = 82
FTH_ConfigNEA_A_HI_min_BYTE_SIZE = 4
FTH_ConfigNEA_A_HI_max_BYTE_OFFSET = 86
FTH_ConfigNEA_A_HI_max_BYTE_SIZE = 4
FTH_ConfigNEA_Tmin_BYTE_OFFSET = 90
FTH_ConfigNEA_Tmin_BYTE_SIZE = 1
FTH_ConfigNEA_Tmax_BYTE_OFFSET = 91
FTH_ConfigNEA_Tmax_BYTE_SIZE = 1
FTH_ConfigNEA_NEA_TYPE_BYTE_OFFSET = 92
FTH_ConfigNEA_NEA_TYPE_BYTE_SIZE = 64
FTH_SelectNEA = 0x0434
FTH_SelectNEA_NEA_ID_BYTE_OFFSET = 14
FTH_SelectNEA_NEA_ID_BYTE_SIZE = 64
FTH_SelectNEA_NEA_TYPE_BYTE_OFFSET = 78
FTH_SelectNEA_NEA_TYPE_BYTE_SIZE = 64
FTH_SelectNEA_select_BYTE_OFFSET = 142
FTH_SelectNEA_select_BYTE_SIZE = 1
FTH_NEA_Mask_BYTE_SIZE = 128
FTH_NEA_Pulse_BYTE_SIZE = 128
LPS_Initialize = 0x0022
LPS_SetLocal = 0x0041
LPS_SetRemote = 0x0042
LPS_LockInstruments = 0x0039
LPS_UnlockInstruments = 0x0040
LPS_SetOnLine = 0x0016
LPS_SetOffLine = 0x0017
LPS_SelfTest = 0x0035
SAS_Initialize = 0x0210
SAS_SetLocal = 0x0233
SAS_SetRemote = 0x0234
SAS_LockInstruments = 0x0229
SAS_UnlockInstruments = 0x0230
SAS_SetOnline = 0x0206
SAS_SetOffline = 0x0208
SAS_SelfTest = 0x0225
# Commanding Mode
EPWR_CMD_LOCAL = "0"
EPWR_CMD_REMOTE = "1"
# Operation Mode
EPWR_OP_OFFLINE = "0"
EPWR_OP_OFFLINE2 = "4"
EPWR_OP_ONLINE = "8"
EPWR_OP_ONLINE2 = "15"
EPWR_OP_FTH_ONLINE = "1"
EPWR_BS_OP = "CHSTAT1"
EPWR_FTH_OP = "ONOFF"
EPWR_LPS_OP_Section1P = "CHSTAT1"
EPWR_LPS_OP_Section1S = "CHSTAT2"
EPWR_LPS_OP_Section2P = "CHSTAT3"
EPWR_LPS_OP_Section2S = "CHSTAT4"
EPWR_LPS_OP_Section3P = "CHSTAT5"
EPWR_LPS_OP_Section3S = "CHSTAT6"
EPWR_SAS_OP_Section1 = "CHSTATSA1"
EPWR_SAS_OP_Section2 = "CHSTATSA2"
EPWR_SAS_OP_Section3 = "CHSTATSA3"
EPWR_SAS_OP_Section4 = "CHSTATSA4"
EPWR_SAS_OP_Section5 = "CHSTATSA5"
EPWR_SAS_OP_Section6 = "CHSTATSA6"
EPWR_SAS_OP_Section7 = "CHSTATSA7"
EPWR_SAS_OP_Section8 = "CHSTATSA8"
EPWR_SAS_OP_Section9 = "CHSTATSA9"
EPWR_SAS_OP_Section10 = "CHSTATSA10"
EPWR_SAS_OP_Section11 = "CHSTATSA11"
EPWR_SAS_OP_Section12 = "CHSTATSA12"
EPWR_SAS_OP_Section13 = "CHSTATSA13"
EPWR_SAS_OP_Section14 = "CHSTATSA14"
EPWR_SAS_OP_Section15 = "CHSTATSA15"
# SCOE Running
EPWR_SRUN_LPSN = "0,1"
EPWR_SRUN_LPSR = "1,1"
EPWR_SRUN_SAS = "0,0"
EPWR_SRUN_PARAMS = "ONOFF11,ONOFF12"

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
    LOG_INFO("ApplicationSoftwareImpl.processTCpacket(" + str(apid) + ")", "SPACE")
    # packet is a PUS Function Management command
    if tcPacketDu.serviceType == PUS.SERVICES.TC_FKT_TYPE:
      if tcPacketDu.serviceSubType == PUS.SERVICES.TC_FKT_PERFORM_FUNCTION:
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

# =============================================================================
class EUCLIDpowerFEEsim_BS(ApplicationSoftwareImpl):
  """Implementation of the EUCLID BS Power Frontend Simulation"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """Initialise attributes only"""
    ApplicationSoftwareImpl.__init__(self)
    self.commandingMode = EPWR_CMD_LOCAL
    self.operationMode = EPWR_OP_OFFLINE
  # ---------------------------------------------------------------------------
  def processTCpacket(self, tcPacketDu):
    """
    processes a telecommand C&C packet from the CCS
    implementation of SPACE.IF.ApplicationSoftware.processTCpacket
    """
    apid = tcPacketDu.applicationProcessId
    LOG_INFO("EUCLIDpowerFEEsim_BS.processTCpacket(" + str(apid) + ")", "SPACE")
    # packet is a PUS Function Management command
    if tcPacketDu.serviceType == PUS.SERVICES.TC_FKT_TYPE:
      if tcPacketDu.serviceSubType == PUS.SERVICES.TC_FKT_PERFORM_FUNCTION:
        tcFunctionId = tcPacketDu.getUnsigned(
          self.tcFunctionIdBytePos, self.tcFunctionIdByteSize)
        LOG("tcFunctionId = " + str(tcFunctionId), "SPACE")
        if tcFunctionId == BS_Initialize:
          LOG_INFO("*** BS_Initialize ***", "SPACE")
          LOG("push HKTM", "SPACE")
          return self.sendBS_Monitor()
        elif tcFunctionId == BS_SetLocal:
          LOG_INFO("*** BS_SetLocal ***", "SPACE")
          LOG("set the SCOE into the LOCAL commanding mode", "SPACE")
          self.commandingMode = EPWR_CMD_LOCAL
        elif tcFunctionId == BS_SetRemote:
          LOG_INFO("*** BS_SetRemote ***", "SPACE")
          LOG("set the SCOE into the REMOTE commanding mode", "SPACE")
          self.commandingMode = EPWR_CMD_REMOTE
        elif tcFunctionId == BS_LockInstruments:
          LOG_INFO("*** BS_LockInstruments ***", "SPACE")
          LOG("not used for simulation", "SPACE")
        elif tcFunctionId == BS_UnlockInstruments:
          LOG_INFO("*** BS_UnlockInstruments ***", "SPACE")
          LOG("not used for simulation", "SPACE")
        elif tcFunctionId == BS_SetOnline:
          LOG_INFO("*** BS_SetOnline ***", "SPACE")
          LOG("set the SCOE into the ONLINE operation mode", "SPACE")
          self.operationMode = EPWR_OP_ONLINE
          return self.sendBS_Monitor()
        elif tcFunctionId == BS_SetOffline:
          LOG_INFO("*** BS_SetOffline ***", "SPACE")
          LOG("set the SCOE into the OFFLINE operation mode", "SPACE")
          self.operationMode = EPWR_OP_OFFLINE
          return self.sendBS_Monitor()
        elif tcFunctionId == BS_SelfTest:
          LOG_INFO("*** BS_SelfTest ***", "SPACE")
          # the SELFTEST is only allowed in OFFLINE mode
          if self.operationMode == EPWR_OP_ONLINE:
            LOG_ERROR("SELFTEST not allowed when system is ONLINE", "SPACE")
            return False
        else:
          # unexpected Function ID
          LOG_WARNING("no simulation for Function ID " + str(tcFunctionId) + " implemented", "SPACE")
        return True
    LOG_WARNING("TC ignored by simulation", "SPACE")
    return True
  # ---------------------------------------------------------------------------
  def sendBS_Monitor(self):
    """sends the LPS_Monitor TM packet to CCS"""
    pktMnemonic = "BS_Monitor"
    params = EPWR_BS_OP
    values = self.operationMode
    tmPacketData = SPACE.IF.s_definitions.getTMpacketInjectData(pktMnemonic,
                                                                params,
                                                                values)
    # check the TM packet data
    if tmPacketData == None:
      LOG_ERROR("TM packet creation failed for " + pktMnemonic, "SPACE")
      return False
    # send the TM packet
    return SPACE.IF.s_onboardComputer.generateTMpacket(tmPacketData)

# =============================================================================
class EUCLIDpowerFEEsim_FTH(ApplicationSoftwareImpl):
  """Implementation of the EUCLID FTH Power Frontend Simulation"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """Initialise attributes only"""
    ApplicationSoftwareImpl.__init__(self)
    self.commandingMode = EPWR_CMD_LOCAL
    self.operationMode = EPWR_OP_OFFLINE
  # ---------------------------------------------------------------------------
  def processTCpacket(self, tcPacketDu):
    """
    processes a telecommand C&C packet from the CCS
    implementation of SPACE.IF.ApplicationSoftware.processTCpacket
    """
    apid = tcPacketDu.applicationProcessId
    LOG_INFO("EUCLIDpowerFEEsim_BS.processTCpacket(" + str(apid) + ")", "SPACE")
    # packet is a PUS Function Management command
    if tcPacketDu.serviceType == PUS.SERVICES.TC_FKT_TYPE:
      if tcPacketDu.serviceSubType == PUS.SERVICES.TC_FKT_PERFORM_FUNCTION:
        tcFunctionId = tcPacketDu.getUnsigned(
          self.tcFunctionIdBytePos, self.tcFunctionIdByteSize)
        LOG("tcFunctionId = " + str(tcFunctionId), "SPACE")
        if tcFunctionId == FTH_Initialize:
          LOG_INFO("*** FTH_Initialize ***", "SPACE")
          LOG("push HKTM", "SPACE")
          return self.sendFTH_MonitorProUST()
        elif tcFunctionId == FTH_EnableGUI:
          LOG_INFO("*** FTH_EnableGUI ***", "SPACE")
          LOG("set the SCOE into the REMOTE commanding mode", "SPACE")
          self.commandingMode = EPWR_CMD_REMOTE
        elif tcFunctionId == FTH_DisableGUI:
          LOG_INFO("*** FTH_DisableGUI ***", "SPACE")
          LOG("set the SCOE into the LOCAL commanding mode", "SPACE")
          self.commandingMode = EPWR_CMD_LOCAL
        elif tcFunctionId == FTH_SetOnline:
          LOG_INFO("*** FTH_SetOnline ***", "SPACE")
          LOG("set the SCOE into the ONLINE operation mode", "SPACE")
          self.operationMode = EPWR_OP_FTH_ONLINE
          return self.sendFTH_MonitorProUST()
        elif tcFunctionId == FTH_SetOffline:
          LOG_INFO("*** FTH_SetOffline ***", "SPACE")
          LOG("set the SCOE into the OFFLINE operation mode", "SPACE")
          self.operationMode = EPWR_OP_OFFLINE
          return self.sendFTH_MonitorProUST()
        elif tcFunctionId == FTH_SelfTest:
          LOG_INFO("*** FTH_SelfTest ***", "SPACE")
          # the SELFTEST is only allowed in OFFLINE mode
          if self.operationMode == EPWR_OP_FTH_ONLINE:
            LOG_ERROR("SELFTEST not allowed when system is ONLINE", "SPACE")
            return False
        elif tcFunctionId == FTH_ConfigNEA:
          LOG_INFO("*** FTH_ConfigNEA ***", "SPACE")
          pNEA_ID = tcPacketDu.getString(
            FTH_ConfigNEA_NEA_ID_BYTE_OFFSET, FTH_ConfigNEA_NEA_ID_BYTE_SIZE).rstrip('\0')
          pA_LO = tcPacketDu.getUnsigned(
            FTH_ConfigNEA_A_LO_BYTE_OFFSET, FTH_ConfigNEA_A_LO_BYTE_SIZE)
          pA_LO = UTIL.DU.unsigned2signed(pA_LO, FTH_ConfigNEA_A_LO_BYTE_SIZE) / 1000000.0
          pA_HI_min = tcPacketDu.getUnsigned(
            FTH_ConfigNEA_A_HI_min_BYTE_OFFSET, FTH_ConfigNEA_A_HI_min_BYTE_SIZE)
          pA_HI_min = UTIL.DU.unsigned2signed(pA_HI_min, FTH_ConfigNEA_A_HI_min_BYTE_SIZE) / 1000000.0
          pA_HI_max = tcPacketDu.getUnsigned(
            FTH_ConfigNEA_A_HI_max_BYTE_OFFSET, FTH_ConfigNEA_A_HI_max_BYTE_SIZE)
          pA_HI_max = UTIL.DU.unsigned2signed(pA_HI_max, FTH_ConfigNEA_A_HI_max_BYTE_SIZE) / 1000000.0
          pA_Tmin = tcPacketDu.getUnsigned(
            FTH_ConfigNEA_Tmin_BYTE_OFFSET, FTH_ConfigNEA_Tmin_BYTE_SIZE)
          pA_Tmax = tcPacketDu.getUnsigned(
            FTH_ConfigNEA_Tmax_BYTE_OFFSET, FTH_ConfigNEA_Tmax_BYTE_SIZE)
          pNEA_TYPE = tcPacketDu.getString(
            FTH_ConfigNEA_NEA_TYPE_BYTE_OFFSET, FTH_ConfigNEA_NEA_TYPE_BYTE_SIZE).rstrip('\0')
          LOG_INFO("pNEA_ID = " + pNEA_ID, "SPACE")
          LOG_INFO("pA_LO = " + str(pA_LO), "SPACE")
          LOG_INFO("pA_HI_min = " + str(pA_HI_min), "SPACE")
          LOG_INFO("pA_HI_max = " + str(pA_HI_max), "SPACE")
          LOG_INFO("pA_Tmin = " + str(pA_Tmin), "SPACE")
          LOG_INFO("pA_Tmax = " + str(pA_Tmax), "SPACE")
          LOG_INFO("pNEA_TYPE = " + pNEA_TYPE, "SPACE")
          neaMask = str(str(pA_LO) + "," + str(pA_HI_min) + "," + str(pA_HI_max) + "," + str(pA_Tmin) + ".0," + str(pA_Tmax) + ".0")
          if pNEA_ID == "NEA1" and pNEA_TYPE == "N":
            paramName = "NEA_MASK_1N"
          elif pNEA_ID == "NEA1" and pNEA_TYPE == "R":
            paramName = "NEA_MASK_1R"
          elif pNEA_ID == "NEA2" and pNEA_TYPE == "N":
            paramName = "NEA_MASK_2N"
          elif pNEA_ID == "NEA2" and pNEA_TYPE == "R":
            paramName = "NEA_MASK_2R"
          elif pNEA_ID == "NEA3" and pNEA_TYPE == "N":
            paramName = "NEA_MASK_3N"
          elif pNEA_ID == "NEA3" and pNEA_TYPE == "R":
            paramName = "NEA_MASK_3R"
          else:
            # unexpected NEA_Mask identifiers
            LOG_WARNING("invalid NEA_ID " + pNEA_ID + " or NEA_TYPE " + pNEA_TYPE, "SPACE")
            return False
          return self.sendFTH_MonitorProUST_withStringParam(paramName, neaMask, FTH_NEA_Mask_BYTE_SIZE)
        elif tcFunctionId == FTH_SelectNEA:
          LOG_INFO("*** FTH_SelectNEA ***", "SPACE")
          pNEA_ID = tcPacketDu.getString(
            FTH_SelectNEA_NEA_ID_BYTE_OFFSET, FTH_SelectNEA_NEA_ID_BYTE_SIZE).rstrip('\0')
          pNEA_TYPE = tcPacketDu.getString(
            FTH_SelectNEA_NEA_TYPE_BYTE_OFFSET, FTH_SelectNEA_NEA_TYPE_BYTE_SIZE).rstrip('\0')
          pSelect = tcPacketDu.getUnsigned(
            FTH_SelectNEA_select_BYTE_OFFSET, FTH_SelectNEA_select_BYTE_SIZE)
          LOG_INFO("pNEA_ID = " + pNEA_ID, "SPACE")
          LOG_INFO("pNEA_TYPE = " + pNEA_TYPE, "SPACE")
          LOG_INFO("pSelect = " + str(pSelect), "SPACE")
          if pSelect == 1:
            neaPulse = "0,0.0,0.0,None,Selected"
          else:
            neaPulse = "0,0.0,0.0,None,Unselected"
          if pNEA_ID == "NEA1" and pNEA_TYPE == "N":
            paramName = "NEA_PULSE_1N"
          elif pNEA_ID == "NEA1" and pNEA_TYPE == "R":
            paramName = "NEA_PULSE_1R"
          elif pNEA_ID == "NEA2" and pNEA_TYPE == "N":
            paramName = "NEA_PULSE_2N"
          elif pNEA_ID == "NEA2" and pNEA_TYPE == "R":
            paramName = "NEA_PULSE_2R"
          elif pNEA_ID == "NEA3" and pNEA_TYPE == "N":
            paramName = "NEA_PULSE_3N"
          elif pNEA_ID == "NEA3" and pNEA_TYPE == "R":
            paramName = "NEA_PULSE_3R"
          else:
            # unexpected NEA_Pulse identifiers
            LOG_WARNING("invalid NEA_ID " + pNEA_ID + " or NEA_TYPE " + pNEA_TYPE, "SPACE")
            return False
          return self.sendFTH_MonitorProUST_withStringParam(paramName, neaPulse, FTH_NEA_Pulse_BYTE_SIZE)
        else:
          # unexpected Function ID
          LOG_WARNING("no simulation for Function ID " + str(tcFunctionId) + " implemented", "SPACE")
        return True
    LOG_WARNING("TC ignored by simulation", "SPACE")
    return True
  # ---------------------------------------------------------------------------
  def sendFTH_MonitorProUST(self):
    """sends the FTH_MonitorProUST TM packet to CCS"""
    pktMnemonic = "FTH_MonitorProUST"
    params = EPWR_FTH_OP
    values = self.operationMode
    tmPacketData = SPACE.IF.s_definitions.getTMpacketInjectData(pktMnemonic,
                                                                params,
                                                                values)
    # check the TM packet data
    if tmPacketData == None:
      LOG_ERROR("TM packet creation failed for " + pktMnemonic, "SPACE")
      return False
    # send the TM packet
    return SPACE.IF.s_onboardComputer.generateTMpacket(tmPacketData)
  # ---------------------------------------------------------------------------
  def sendFTH_MonitorProUST_withStringParam(self, paramName, paramValue, paramSize):
    """sends the FTH_MonitorProUST TM packet to CCS"""
    pktMnemonic = "FTH_MonitorProUST"
    params = ""
    values = ""
    tmPacketData = SPACE.IF.s_definitions.getTMpacketInjectData(pktMnemonic,
                                                                params,
                                                                values)
    # check the TM packet data
    if tmPacketData == None:
      LOG_ERROR("TM packet creation failed for " + pktMnemonic, "SPACE")
      return False
    # force the correct parameter size and add the parameter
    paramValue = (paramValue + (' ' * paramSize))[0:paramSize]
    tmPacketData.parameterValuesList.append([paramName,paramValue])
    # send the TM packet
    return SPACE.IF.s_onboardComputer.generateTMpacket(tmPacketData)

# =============================================================================
class EUCLIDpowerFEEsim_LPS_SAS(ApplicationSoftwareImpl):
  """Implementation of the EUCLID LPS/SAS Power Frontend Simulation"""
  # ---------------------------------------------------------------------------
  def __init__(self, isNominal):
    """Initialise attributes only"""
    ApplicationSoftwareImpl.__init__(self)
    self.isNominal = isNominal
    self.commandingMode = EPWR_CMD_LOCAL
    self.lpsOperationMode = EPWR_OP_OFFLINE
    self.sasOperationMode = EPWR_OP_OFFLINE
    self.scoeRunning = EPWR_SRUN_SAS
  # ---------------------------------------------------------------------------
  def processTCpacket(self, tcPacketDu):
    """
    processes a telecommand C&C packet from the CCS
    implementation of SPACE.IF.ApplicationSoftware.processTCpacket
    """
    apid = tcPacketDu.applicationProcessId
    LOG_INFO("EUCLIDpowerFEEsim_LPS_SAS.processTCpacket(" + str(apid) + ")", "SPACE")
    # packet is a PUS Function Management command
    if tcPacketDu.serviceType == PUS.SERVICES.TC_FKT_TYPE:
      if tcPacketDu.serviceSubType == PUS.SERVICES.TC_FKT_PERFORM_FUNCTION:
        tcFunctionId = tcPacketDu.getUnsigned(
          self.tcFunctionIdBytePos, self.tcFunctionIdByteSize)
        LOG("tcFunctionId = " + str(tcFunctionId), "SPACE")
        if tcFunctionId == LPS_Initialize:
          LOG_INFO("*** LPS_Initialize ***", "SPACE")
          LOG("set the SCOE into the LPSN running mode", "SPACE")
          if self.isNominal:
            self.scoeRunning = EPWR_SRUN_LPSN
          else:
            self.scoeRunning = EPWR_SRUN_LPSR
          return self.sendLPS_Monitor()
        elif tcFunctionId == LPS_SetLocal:
          LOG_INFO("*** LPS_SetLocal ***", "SPACE")
          LOG("set the SCOE into the LOCAL commanding mode", "SPACE")
          self.commandingMode = EPWR_CMD_LOCAL
        elif tcFunctionId == LPS_SetRemote:
          LOG_INFO("*** LPS_SetRemote ***", "SPACE")
          LOG("set the SCOE into the REMOTE commanding mode", "SPACE")
          self.commandingMode = EPWR_CMD_REMOTE
        elif tcFunctionId == LPS_LockInstruments:
          LOG_INFO("*** LPS_LockInstruments ***", "SPACE")
          LOG("not used for simulation", "SPACE")
        elif tcFunctionId == LPS_UnlockInstruments:
          LOG_INFO("*** LPS_UnlockInstruments ***", "SPACE")
          LOG("not used for simulation", "SPACE")
        elif tcFunctionId == LPS_SetOnLine:
          LOG_INFO("*** LPS_SetOnLine ***", "SPACE")
          LOG("set the SCOE into the ONLINE operation mode", "SPACE")
          self.lpsOperationMode = EPWR_OP_ONLINE
          return self.sendLPS_Monitor()
        elif tcFunctionId == LPS_SetOffLine:
          LOG_INFO("*** LPS_SetOffLine ***", "SPACE")
          LOG("set the SCOE into the OFFLINE operation mode", "SPACE")
          self.lpsOperationMode = EPWR_OP_OFFLINE
          return self.sendLPS_Monitor()
        elif tcFunctionId == LPS_SelfTest:
          LOG_INFO("*** LPS_SelfTest ***", "SPACE")
        elif tcFunctionId == SAS_Initialize:
          LOG_INFO("*** SAS_Initialize ***", "SPACE")
          LOG("set the SCOE into the SAS running mode", "SPACE")
          self.scoeRunning = EPWR_SRUN_SAS
          return self.sendLPS_Monitor()
        elif tcFunctionId == SAS_SetLocal:
          LOG_INFO("*** SAS_SetLocal ***", "SPACE")
          self.commandingMode = EPWR_CMD_LOCAL
        elif tcFunctionId == SAS_SetRemote:
          LOG_INFO("*** SAS_SetRemote ***", "SPACE")
          self.commandingMode = EPWR_CMD_REMOTE
        elif tcFunctionId == SAS_LockInstruments:
          LOG_INFO("*** SAS_LockInstruments ***", "SPACE")
          LOG("not used for simulation", "SPACE")
        elif tcFunctionId == SAS_UnlockInstruments:
          LOG_INFO("*** SAS_UnlockInstruments ***", "SPACE")
          LOG("not used for simulation", "SPACE")
        elif tcFunctionId == SAS_SetOnline:
          LOG_INFO("*** SAS_SetOnline ***", "SPACE")
          LOG("set the SCOE into the OFFLINE operation mode", "SPACE")
          self.sasOperationMode = EPWR_OP_ONLINE
          return self.sendSAS_Monitor()
        elif tcFunctionId == SAS_SetOffline:
          LOG_INFO("*** SAS_SetOffline ***", "SPACE")
          self.sasOperationMode = EPWR_OP_OFFLINE
          return self.sendSAS_Monitor()
        elif tcFunctionId == SAS_SelfTest:
          LOG_INFO("*** SAS_SelfTest ***", "SPACE")
        else:
          # unexpected Function ID
          LOG_WARNING("no simulation for Function ID " + str(tcFunctionId) + " implemented", "SPACE")
        return True
    LOG_WARNING("TC ignored by simulation", "SPACE")
    return True
  # ---------------------------------------------------------------------------
  def sendLPS_Monitor(self):
    """sends the LPS_Monitor TM packet to CCS"""
    pktMnemonic = "LPS_Monitor"
    params = EPWR_SRUN_PARAMS + "," + \
             EPWR_LPS_OP_Section1P + "," + \
             EPWR_LPS_OP_Section1S + "," + \
             EPWR_LPS_OP_Section2P + "," + \
             EPWR_LPS_OP_Section2S + "," + \
             EPWR_LPS_OP_Section3P + "," + \
             EPWR_LPS_OP_Section3S
    values = self.scoeRunning + "," + \
             self.lpsOperationMode + "," + \
             self.lpsOperationMode + "," + \
             self.lpsOperationMode + "," + \
             self.lpsOperationMode + "," + \
             self.lpsOperationMode + "," + \
             self.lpsOperationMode
    tmPacketData = SPACE.IF.s_definitions.getTMpacketInjectData(pktMnemonic,
                                                                params,
                                                                values)
    # check the TM packet data
    if tmPacketData == None:
      LOG_ERROR("TM packet creation failed for " + pktMnemonic, "SPACE")
      return False
    # send the TM packet
    return SPACE.IF.s_onboardComputer.generateTMpacket(tmPacketData)
  # ---------------------------------------------------------------------------
  def sendSAS_Monitor(self):
    """sends the SAS_Monitor TM packet to CCS"""
    pktMnemonic = "SAS_Monitor"
    params = EPWR_SAS_OP_Section1 + "," + \
             EPWR_SAS_OP_Section2 + "," + \
             EPWR_SAS_OP_Section3 + "," + \
             EPWR_SAS_OP_Section4 + "," + \
             EPWR_SAS_OP_Section5 + "," + \
             EPWR_SAS_OP_Section6 + "," + \
             EPWR_SAS_OP_Section7 + "," + \
             EPWR_SAS_OP_Section8 + "," + \
             EPWR_SAS_OP_Section9 + "," + \
             EPWR_SAS_OP_Section10 + "," + \
             EPWR_SAS_OP_Section11 + "," + \
             EPWR_SAS_OP_Section12 + "," + \
             EPWR_SAS_OP_Section13 + "," + \
             EPWR_SAS_OP_Section14 + "," + \
             EPWR_SAS_OP_Section15
    values = self.sasOperationMode + "," + \
             self.sasOperationMode + "," + \
             self.sasOperationMode + "," + \
             self.sasOperationMode + "," + \
             self.sasOperationMode + "," + \
             self.sasOperationMode + "," + \
             self.sasOperationMode + "," + \
             self.sasOperationMode + "," + \
             self.sasOperationMode + "," + \
             self.sasOperationMode + "," + \
             self.sasOperationMode + "," + \
             self.sasOperationMode + "," + \
             self.sasOperationMode + "," + \
             self.sasOperationMode + "," + \
             self.sasOperationMode
    tmPacketData = SPACE.IF.s_definitions.getTMpacketInjectData(pktMnemonic,
                                                                params,
                                                                values)
    # check the TM packet data
    if tmPacketData == None:
      LOG_ERROR("TM packet creation failed for " + pktMnemonic, "SPACE")
      return False
    # send the TM packet
    return SPACE.IF.s_onboardComputer.generateTMpacket(tmPacketData)

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
  elif mission == "EUCLID_BS":
    SPACE.IF.s_applicationSoftware = EUCLIDpowerFEEsim_BS()
  elif mission == "EUCLID_FTH":
    SPACE.IF.s_applicationSoftware = EUCLIDpowerFEEsim_FTH()
  elif mission == "EUCLID_LPSN":
    SPACE.IF.s_applicationSoftware = EUCLIDpowerFEEsim_LPS_SAS(True)
  elif mission == "EUCLID_LPSR":
    SPACE.IF.s_applicationSoftware = EUCLIDpowerFEEsim_LPS_SAS(False)
  else:
    LOG_ERROR("No ASW implementation for mission " + mission + " present", "SPACE")
