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
# Space Simulation - Space Interface                                          *
#******************************************************************************
import string
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import CCSDS.DU, CCSDS.PACKET
import UTIL.DU, UTIL.SYS

#############
# constants #
#############
ENABLE_ACK = 0
ENABLE_NAK = 1
DISABLE_ACK = 2
ACK_STRS = ["ENABLE_ACK", "ENABLE_NAK", "DISABLE_ACK"]
RPLY_PKT = 0     # replay file TM packet entry
RPLY_RAWPKT = 1  # replay file raw TM packet entry
RPLY_SLEEP = 2   # replay file sleep entry
RPLY_OBT = 3     # replay file onboard time entry
RPLY_ERT = 4     # replay file earth reception time entry
MIL_BUS_PF = 0   # MIL Platform Bus
MIL_BUS_PL = 1   # MIL Payload Bus

###########
# classes #
###########
# =============================================================================
class Configuration(object):
  """Configuration"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """Initialise the connection relevant informations"""
    self.connected = False
    self.tmPacketData = None
    self.sendCyclic = False
    self.cyclicPeriodMs = int(UTIL.SYS.s_configuration.TM_CYCLIC_PERIOD_MS)
    self.obcAck1 = ENABLE_ACK
    self.obcAck2 = ENABLE_ACK
    self.obcAck3 = ENABLE_ACK
    self.obcAck4 = ENABLE_ACK
    self.obqAck1 = ENABLE_ACK
    self.obqAck2 = ENABLE_ACK
    self.obqAck3 = ENABLE_ACK
    self.obqAck4 = ENABLE_ACK
  # ---------------------------------------------------------------------------
  def dump(self):
    """Dumps the status of the configuration attributes"""
    LOG_INFO("Space segment configuration", "SPACE")
    LOG("Connected = " + str(self.connected), "SPACE")
    if self.tmPacketData == None:
      LOG("No packet defined", "SPACE")
    else:
      LOG("Packet = " + self.tmPacketData.pktName, "SPACE")
      LOG("SPID = " + str(self.tmPacketData.pktSPID), "SPACE")
      LOG("Parameters and values = " + str(self.tmPacketData.parameterValuesList), "SPACE")
    LOG("Send cyclic TM = " + str(self.sendCyclic), "SPACE")
    LOG("TC Ack 1 = " + ACK_STRS[self.obcAck1], "SPACE")
    LOG("TC Ack 2 = " + ACK_STRS[self.obcAck2], "SPACE")
    LOG("TC Ack 3 = " + ACK_STRS[self.obcAck3], "SPACE")
    LOG("TC Ack 4 = " + ACK_STRS[self.obcAck4], "SPACE")
    LOG_INFO("Onboard queue configuration", "OBQ")
    LOG("TC Ack 1 = " + ACK_STRS[self.obqAck1], "OBQ")
    LOG("TC Ack 2 = " + ACK_STRS[self.obqAck2], "OBQ")
    LOG("TC Ack 3 = " + ACK_STRS[self.obqAck3], "OBQ")
    LOG("TC Ack 4 = " + ACK_STRS[self.obqAck4], "OBQ")

##############
# interfaces #
##############
# =============================================================================
class OnboardComputer(object):
  """Interface of the onboard computer"""
  # ---------------------------------------------------------------------------
  def pushTCpacket(self, tcPacketDu):
    """consumes a telecommand packet from the uplink"""
    # shall return True for successful processing, otherwise False
    return True
  # ---------------------------------------------------------------------------
  def processTCpacket(self, tcPacketDu, ack1, ack2, ack3, ack4):
    """processes a telecommand packet"""
    # shall return True for successful processing, otherwise False
    return True
  # ---------------------------------------------------------------------------
  def generateEmptyTMpacket(self, pktMnemonic):
    """generates an empty TM packet (all parameters are zero)"""
    # shall return True for successful processing, otherwise False
    return True
  # ---------------------------------------------------------------------------
  def generateEmptyTMpacketBySPID(self, spid):
    """generates an empty TM packet (all parameters are zero)"""
    # shall return True for successful processing, otherwise False
    return True
  # ---------------------------------------------------------------------------
  def generateTMpacket(self, tmPacketData, obtUTC=None, ertUTC=None):
    """generates a TM packet"""
    # shall return True for successful processing, otherwise False
    return True
  # ---------------------------------------------------------------------------
  def generateAcksFromTCpacket(self, tcPacketDu, ack1, ack2, ack3, ack4):
    """generates TC acknowledgements according to PUS service 1"""
    # shall return True for successful processing, otherwise False
    return True
  # ---------------------------------------------------------------------------
  def generateAck(self, tcAPID, tcSSC, ackType):
    """generates a TC acknowledgement according to PUS service 1"""
    # shall return True for successful processing, otherwise False
    return True
  # ---------------------------------------------------------------------------
  def pushTMpacket(self, tmPacketDu, ertUTC):
    """sends TM packet DU to CCS or downlink"""
    # shall return True for successful processing, otherwise False
    return True
  # ---------------------------------------------------------------------------
  def replayPackets(self, replayFileName):
    """sends TM packet from a replay file"""
    pass
  # ---------------------------------------------------------------------------
  def startCyclicTM(self):
    """start sending of cyclic TM"""
    pass
  # ---------------------------------------------------------------------------
  def stopCyclicTM(self):
    """stops sending of cyclic TM"""
    pass

# =============================================================================
class OnboardQueue(object):
  """Interface of the onboard queue"""
  # ---------------------------------------------------------------------------
  def getQueue(self):
    """returns the onboard queue"""
    pass
  # ---------------------------------------------------------------------------
  def pushMngPacket(self, tcPacketDu):
    """consumes a management telecommand packet"""
    pass
  # ---------------------------------------------------------------------------
  def pushExecPacket(self, tcPacketDu):
    """consumes a telecommand packet that shall be executed immediately"""

# =============================================================================
class ApplicationSoftware(object):
  """Interface of the spacecraft's application software"""
  # ---------------------------------------------------------------------------
  def processTCpacket(self, tcPacketDu):
    """processes a telecommand C&C packet from the CCS"""
    # shall return True for successful processing, otherwise False
    return True
  # ---------------------------------------------------------------------------
  # shall be overloaded in derived classes
  def getBcPfAPID(self):
    pass
  def getBcPlAPID(self):
    pass
  def getRtPfAPID(self):
    pass
  def getRtPlAPID(self):
    pass
  # ---------------------------------------------------------------------------
  def notifyMILdatablockAcquisition(self, rtAddress, dataBlock):
    """The BC has received on the MIL Bus a data block from a RT"""
    pass
  # ---------------------------------------------------------------------------
  def notifyMILdatablockDistribution(self, rtAddress, dataBlock):
    """The mRT has received on the MIL Bus a data block from the BC"""
    pass

# =============================================================================
class TMpacketGenerator(object):
  """Interface of the generator for telemetry packets"""
  # ---------------------------------------------------------------------------
  def getIdlePacket(self, packetSize):
    """
    creates an idle packet for filling space in a parent container
    (e.g. a CCSDS TM frame)
    """
    pass
  # ---------------------------------------------------------------------------
  def getTMpacket(self,
                  spid,
                  parameterValues,
                  tmStruct,
                  dataField=None,
                  segmentationFlags=CCSDS.PACKET.UNSEGMENTED,
                  obtTimeStamp=None,
                  reuse=True):
    """creates a CCSDS TM packet with optional parameter values"""
    pass

# =============================================================================
class TMpacketReplayer(object):
  """Interface of the replayer for telemetry packets"""
  # ---------------------------------------------------------------------------
  def readReplayFile(self, replayFileName):
    """
    reads TM packets and directives from a replay file
    """
    pass
  # ---------------------------------------------------------------------------
  def getItems(self):
    """returns items from the replay list"""
    pass
  # ---------------------------------------------------------------------------
  def getNextItem(self):
    """returns next item from the replay list or None"""
    pass

# =============================================================================
class MILbus(object):
  """Interface of the MIL Bus"""
  # ---------------------------------------------------------------------------
  def bcWriteSubAddress(self, rtAddress, subAddress, data):
    """Bus Controller: writes data to a sub-address"""
    pass
  # ---------------------------------------------------------------------------
  def bcReadSubAddress(self, rtAddress, subAddress):
    """Bus Controller: reads data from a sub-address"""
    pass
  # ---------------------------------------------------------------------------
  def bcDatablockDistribtionRequest(self, rtAddress, dataBlock):
    """Bus Controller: initiate a datablock distribution"""
    pass
  # ---------------------------------------------------------------------------
  def rtWriteSubAddress(self, rtAddress, subAddress, data):
    """Remote Terminal: writes data to a sub-address"""
    pass
  # ---------------------------------------------------------------------------
  def rtReadSubAddress(self, rtAddress, subAddress):
    """Remote Terminal: reads data from a sub-address"""
    pass
  # ---------------------------------------------------------------------------
  def rtDatablockAcquisitionRequest(self, rtAddress, dataBlock):
    """Remote Terminal: initiate a datablock acquisition"""
    pass

# =============================================================================
class MILbusController(object):
  """Interface of the MIL Bus Controller"""
  # ---------------------------------------------------------------------------
  # external methods that are invoked via telecommands,
  # shall return True for successful processing, otherwise False
  def identify(self, bus):
    return True
  def selfTest(self, bus):
    return True
  def getSelfTestReport(self, bus):
    return True
  def reset(self, bus):
    return True
  def configure(self, bus):
    return True
  def configureFrame(self, bus):
    return True
  def addInterrogation(self, bus):
    return True
  def discover(self, bus):
    return True
  def setupDistDatablock(self, bus):
    return True
  def start(self, bus):
    return True
  def stop(self, bus):
    return True
  def forceFrameSwitch(self, bus):
    return True
  def send(self, bus):
    return True
  def setData(self, bus):
    return True
  def forceBusSwitch(self, bus):
    return True
  def injectError(self, bus):
    return True
  def clearError(self, bus):
    return True
  def activate(self, bus):
    return True
  def deactivate(self, bus):
    return True
  def dtd(self, bus):
    return True
  # ---------------------------------------------------------------------------
  def notifyWriteSubAddress(self, rtAddress, subAddress, data):
    """A Remote Terminal has writen data to a sub-address"""
    pass
  # ---------------------------------------------------------------------------
  def notifyDatablockAcquisition(self, rtAddress, dataBlock):
    """A Remote Terminal has performed a datablock acquisition"""
    pass

# =============================================================================
class MILbusRemoteTerminals(object):
  """Interface of the MIL Bus Remote Terminals"""
  # ---------------------------------------------------------------------------
  # external methods that are invoked via telecommands,
  # shall return True for successful processing, otherwise False
  def identify(self, bus):
    return True
  def selfTest(self, bus):
    return True
  def getSelfTestReport(self, bus):
    return True
  def configure(self, bus):
    return True
  def addResponse(self, bus):
    return True
  def reset(self, bus):
    return True
  def saEnable(self, bus):
    return True
  def setupAcquDatablock(self, bus):
    return True
  def start(self, bus):
    return True
  def stop(self, bus):
    return True
  def injectError(self, bus):
    return True
  def clearError(self, bus):
    return True
  def activate(self, bus):
    return True
  def deactivate(self, bus):
    return True
  def atr(self, bus):
    return True
  # ---------------------------------------------------------------------------
  def notifyWriteSubAddress(self, rtAddress, subAddress, data):
    """The Bus Controller has writen data to a sub-address"""
    pass
  # ---------------------------------------------------------------------------
  def notifyDatablockDistribution(self, rtAddress, dataBlock):
    """The Bus Controller has performed a datablock distribution"""
    pass

####################
# global variables #
####################
# to force behaviour for testing
s_testMode = 0
# configuration is a singleton
s_configuration = None
# onboard computer is a singleton
s_onboardComputer = None
# onboard queue is a singleton
s_onboardQueue = None
# application software is a singleton
s_applicationSoftware = None
# telemetry packet generator is a singleton
s_tmPacketGenerator = None
# telemetry packet replayer is a singelton
s_tmPacketReplayer = None
# MIL Bus is a singelton
s_milBus = None
# MIL Bus Controller is a singelton
s_milBusController = None
# MIL Bus Remote Terminals is a singelton
s_milBusRemoteTerminals = None
