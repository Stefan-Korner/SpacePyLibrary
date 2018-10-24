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
# MIL Bus Simulation                                                          *
#******************************************************************************
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import SPACE.IF
import UTIL.TASK

#############
# constants #
#############

# test modes
NOMINAL = 0
SELFTEST_BC_ERROR = 1
SELFTEST_RT_ERROR = 2
SELFTEST_BC_RT_ERROR = 3

###########
# classes #
###########

# =============================================================================
class MILbusImpl(SPACE.IF.MILbus):
  """Implementation of the MIL Bus"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """Initialise attributes only"""
    pass
  # ---------------------------------------------------------------------------
  def bcWriteSubAddress(self, rtAddress, subAddress, data):
    """
    Bus Controller: writes data to a sub-address
    implementation of SPACE.IF.MILbus.bcWriteSubAddress
    """
    pass
  # ---------------------------------------------------------------------------
  def bcReadSubAddress(self, rtAddress, subAddress):
    """
    Bus Controller: reads data from a sub-address
    implementation of SPACE.IF.MILbus.bcReadSubAddress
    """
    pass
  # ---------------------------------------------------------------------------
  def bcDatablockDistribtionRequest(self, rtAddress, dataBlock):
    """
    Bus Controller: initiate a datablock distribution
    implementation of SPACE.IF.MILbus.bcDatablockDistribtionRequest
    """
    LOG_INFO("MILbusImpl.bcDatablockDistribtionRequest(" + str(rtAddress) + ")", "MIL")
    UTIL.TASK.s_processingTask.notifyGUItask("RT " + str(rtAddress) + " DDB " + dataBlock)
    rts = SPACE.IF.s_milBusRemoteTerminals
    rts.notifyDatablockDistribution(rtAddress, dataBlock)
  # ---------------------------------------------------------------------------
  def rtWriteSubAddress(self, rtAddress, subAddress, data):
    """
    Remote Terminal: writes data to a sub-address
    implementation of SPACE.IF.MILbus.rtWriteSubAddress
    """
    pass
  # ---------------------------------------------------------------------------
  def rtReadSubAddress(self, rtAddress, subAddress):
    """
    Remote Terminal: reads data from a sub-address
    implementation of SPACE.IF.MILbus.rtReadSubAddress
    """
    pass
  # ---------------------------------------------------------------------------
  def rtDatablockAcquisitionRequest(self, rtAddress, dataBlock):
    """
    Remote Terminal: initiate a datablock acquisition
    implementation of SPACE.IF.MILbus.rtDatablockAcquisitionRequest
    """
    LOG_INFO("MILbusImpl.rtDatablockAcquisitionRequest(" + str(rtAddress) + ")", "MIL")
    UTIL.TASK.s_processingTask.notifyGUItask("RT " + str(rtAddress) + " ADB " + dataBlock)
    bc = SPACE.IF.s_milBusController
    bc.notifyDatablockAcquisition(rtAddress, dataBlock)

# =============================================================================
class MILbusControllerImpl(SPACE.IF.MILbusController):
  """Implementation of the MIL Bus Controller"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """Initialise attributes only"""
    pass
  # ---------------------------------------------------------------------------
  # external methods that are invoked via telecommands,
  # implementation of SPACE.IF.MILbusController
  def identify(self, bus):
    LOG_INFO("MILbusControllerImpl.identify", "MIL")
    return True
  def selfTest(self, bus):
    LOG_INFO("MILbusControllerImpl.selfTest", "MIL")
    if SPACE.IF.s_testMode == SELFTEST_BC_ERROR or \
       SPACE.IF.s_testMode == SELFTEST_BC_RT_ERROR:
      LOG_WARNING("inject error", "MIL")
      return False
    return True
  def getSelfTestReport(self, bus):
    LOG_INFO("MILbusControllerImpl.getSelfTestReport", "MIL")
    return True
  def reset(self, bus):
    LOG_INFO("MILbusControllerImpl.reset", "MIL")
    return True
  def configure(self, bus):
    LOG_INFO("MILbusControllerImpl.configure", "MIL")
    return True
  def configureFrame(self, bus):
    LOG_INFO("MILbusControllerImpl.configureFrame", "MIL")
    return True
  def addInterrogation(self, bus):
    LOG_INFO("MILbusControllerImpl.addInterrogation", "MIL")
    return True
  def discover(self, bus):
    LOG_INFO("MILbusControllerImpl.discover", "MIL")
    return True
  def setupDistDatablock(self, bus):
    LOG_INFO("MILbusControllerImpl.setupDistDatablock", "MIL")
    return True
  def start(self, bus):
    LOG_INFO("MILbusControllerImpl.start", "MIL")
    return True
  def stop(self, bus):
    LOG_INFO("MILbusControllerImpl.stop", "MIL")
    return True
  def forceFrameSwitch(self, bus):
    LOG_INFO("MILbusControllerImpl.forceFrameSwitch", "MIL")
    return True
  def send(self, bus):
    LOG_INFO("MILbusControllerImpl.send", "MIL")
    return True
  def setData(self, bus):
    LOG_INFO("MILbusControllerImpl.setData", "MIL")
    return True
  def forceBusSwitch(self, bus):
    LOG_INFO("MILbusControllerImpl.forceBusSwitch", "MIL")
    return True
  def injectError(self, bus):
    LOG_INFO("MILbusControllerImpl.injectError", "MIL")
    return True
  def clearError(self, bus):
    LOG_INFO("MILbusControllerImpl.clearError", "MIL")
    return True
  def activate(self, bus):
    LOG_INFO("MILbusControllerImpl.activate", "MIL")
    return True
  def deactivate(self, bus):
    LOG_INFO("MILbusControllerImpl.deactivate", "MIL")
    return True
  def dtd(self, bus):
    LOG_INFO("MILbusControllerImpl.dtd", "MIL")
    return True
  # SPACE.IF.s_milBus.bcDatablockDistribtionRequest(0, "***BC***")
  # ---------------------------------------------------------------------------
  def notifyWriteSubAddress(self, rtAddress, subAddress, data):
    """
    A Remote Terminal has writen data to a sub-address
    implementation of SPACE.IF.MILbusController.notifyWriteSubAddress
    """
    pass
  # ---------------------------------------------------------------------------
  def notifyDatablockAcquisition(self, rtAddress, dataBlock):
    """
    A Remote Terminal has performed a datablock acquisition
    implementation of SPACE.IF.MILbusController.notifyDatablockAcquisition
    """
    LOG_INFO("MILbusControllerImpl.notifyDatablockAcquisition(" + str(rtAddress) + ")", "MIL")
    asw = SPACE.IF.s_applicationSoftware
    asw.notifyMILdatablockAcquisition(rtAddress, dataBlock)

# =============================================================================
class MILbusRemoteTerminalsImpl(SPACE.IF.MILbusRemoteTerminals):
  """Implementation of the MIL Bus Remote Terminals"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """Initialise attributes only"""
    pass
  # ---------------------------------------------------------------------------
  # external methods that are invoked via telecommands,
  # implementation of SPACE.IF.MILbusRemoteTerminals
  def identify(self, bus):
    LOG_INFO("MILbusRemoteTerminalsImpl.identify", "MIL")
    return True
  def selfTest(self, bus):
    LOG_INFO("MILbusRemoteTerminalsImpl.selfTest", "MIL")
    if SPACE.IF.s_testMode == SELFTEST_RT_ERROR or \
       SPACE.IF.s_testMode == SELFTEST_BC_RT_ERROR:
      LOG_WARNING("inject error", "MIL")
      return False
    return True
  def getSelfTestReport(self, bus):
    LOG_INFO("MILbusRemoteTerminalsImpl.getSelfTestReport", "MIL")
    return True
  def configure(self, bus):
    LOG_INFO("MILbusRemoteTerminalsImpl.configure", "MIL")
    return True
  def addResponse(self, bus):
    LOG_INFO("MILbusRemoteTerminalsImpl.addResponse", "MIL")
    return True
  def reset(self, bus):
    LOG_INFO("MILbusRemoteTerminalsImpl.reset", "MIL")
    return True
  def saEnable(self, bus):
    LOG_INFO("MILbusRemoteTerminalsImpl.saEnable", "MIL")
    return True
  def setupAcquDatablock(self, bus):
    LOG_INFO("MILbusRemoteTerminalsImpl.setupAcquDatablock", "MIL")
    return True
  def start(self, bus):
    LOG_INFO("MILbusRemoteTerminalsImpl.start", "MIL")
    return True
  def stop(self, bus):
    LOG_INFO("MILbusRemoteTerminalsImpl.stop", "MIL")
    return True
  def injectError(self, bus):
    LOG_INFO("MILbusRemoteTerminalsImpl.injectError", "MIL")
    return True
  def clearError(self, bus):
    LOG_INFO("MILbusRemoteTerminalsImpl.clearError", "MIL")
    return True
  def activate(self, bus):
    LOG_INFO("MILbusRemoteTerminalsImpl.activate", "MIL")
    return True
  def deactivate(self, bus):
    LOG_INFO("MILbusRemoteTerminalsImpl.deactivate", "MIL")
    return True
  def atr(self, bus):
    LOG_INFO("MILbusRemoteTerminalsImpl.atr", "MIL")
    return True
  # SPACE.IF.s_milBus.rtDatablockAcquisitionRequest(1, "***RT***")
  # ---------------------------------------------------------------------------
  def notifyWriteSubAddress(self, rtAddress, subAddress, data):
    """
    The Bus Controller has writen data to a sub-address
    implementation of SPACE.IF.MILbusRemoteTerminals.notifyWriteSubAddress
    """
    pass
  # ---------------------------------------------------------------------------
  def notifyDatablockDistribution(self, rtAddress, dataBlock):
    """
    The Bus Controller has performed a datablock distribution
    implementation of SPACE.IF.MILbusRemoteTerminals.notifyDatablockDistribution
    """
    LOG_INFO("MILbusRemoteTerminalsImpl.notifyDatablockDistribution(" + str(rtAddress) + ")", "MIL")
    asw = SPACE.IF.s_applicationSoftware
    asw.notifyMILdatablockDistribution(rtAddress, dataBlock)

#############
# functions #
#############
def init():
  # initialise singleton(s)
  SPACE.IF.s_milBus = MILbusImpl()
  SPACE.IF.s_milBusController = MILbusControllerImpl()
  SPACE.IF.s_milBusRemoteTerminals = MILbusRemoteTerminalsImpl()
