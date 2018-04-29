#******************************************************************************
# (C) 2014, Stefan Korner, Austria                                            *
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
# Space Simulation - Onboard Computer                                         *
#******************************************************************************
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import CCSDS.PACKET
import EGSE.IF
import LINK.IF
import PUS.PACKET, PUS.SERVICES
import SPACE.IF
import UTIL.SYS, UTIL.TASK, UTIL.TIME

###########
# classes #
###########
# =============================================================================
class OnboardComputerImpl(SPACE.IF.OnboardComputer):
  """Interface of the onboard computer"""
  # ---------------------------------------------------------------------------
  def __init__(self, egseMode):
    """Initialise attributes only"""
    self.egseMode = egseMode
    self.replayOBT = None
    self.replayERT = None
  # ---------------------------------------------------------------------------
  def pushTCpacket(self, tcPacketDu):
    """
    consumes a telecommand packet from the uplink:
    implementation of SPACE.IF.OnboardComputer.pushTCpacket
    """
    LOG_INFO("pushTCpacket", "SPACE")
    LOG("APID =    " + str(tcPacketDu.applicationProcessId), "SPACE")
    LOG("SSC =     " + str(tcPacketDu.sequenceControlCount), "SPACE")
    if tcPacketDu.dataFieldHeaderFlag == 1:
      # CCSDS packet is a PUS packet
      object.__setattr__(tcPacketDu, "attributeMap2", PUS.PACKET.TC_PACKET_DATAFIELD_HEADER_ATTRIBUTES)
      LOG("TYPE =    " + str(tcPacketDu.serviceType), "SPACE")
      LOG("SUBTYPE = " + str(tcPacketDu.serviceSubType), "SPACE")
      # the existence of a CRC for PUS packets is mission dependant
      # for SCOS-2000 compatibility we expect a CRC
      if not tcPacketDu.checkChecksum():
        LOG_ERROR("invalid TC packet CRC", "SPACE")
        return False
    else:
      LOG("non-PUS packet", "SPACE")
      LOG("tcPacketDu = " + str(tcPacketDu), "SPACE")
    # further processing of the TC packet (e.g. reply telemetry)
    return self.processTCpacket(tcPacketDu,
                                SPACE.IF.s_configuration.obcAck1,
                                SPACE.IF.s_configuration.obcAck2,
                                SPACE.IF.s_configuration.obcAck3,
                                SPACE.IF.s_configuration.obcAck4)
  # ---------------------------------------------------------------------------
  def processTCpacket(self, tcPacketDu, ack1, ack2, ack3, ack4):
    """
    processes a telecommand packet:
    implementation of SPACE.IF.OnboardComputer.processTCpacket
    """
    LOG_INFO("processTCpacket", "SPACE")
    LOG("APID =    " + str(tcPacketDu.applicationProcessId), "SPACE")
    LOG("SSC =     " + str(tcPacketDu.sequenceControlCount), "SPACE")
    ok = True
    if tcPacketDu.dataFieldHeaderFlag == 1:
      # CCSDS packet is a PUS packet
      object.__setattr__(tcPacketDu, "attributeMap2", PUS.PACKET.TC_PACKET_DATAFIELD_HEADER_ATTRIBUTES)
      LOG("TYPE =    " + str(tcPacketDu.serviceType), "SPACE")
      LOG("SUBTYPE = " + str(tcPacketDu.serviceSubType), "SPACE")
      # special handling if the packet is a PUS OBQ management command
      if tcPacketDu.serviceType == PUS.SERVICES.TC_OBQ_TYPE:
        if SPACE.IF.s_onboardQueue == None:
          LOG_ERROR("No OBQ implementation for OBQ management command", "SPACE")
          ok = False
        else:
          SPACE.IF.s_onboardQueue.processTCpacket(tcPacketDu)
      # delegate other services to the spacecraft application software
      elif SPACE.IF.s_applicationSoftware != None:
        ok = SPACE.IF.s_applicationSoftware.processTCpacket(tcPacketDu)
      # send TC acknowledgements
      if ok:
        ok &= self.generateAcksFromTCpacket(tcPacketDu, ack1, ack2, ack3, ack4)
    else:
      LOG("non-PUS packet", "SPACE")
      LOG("tcPacketDu = " + str(tcPacketDu), "SPACE")
    return ok
  # ---------------------------------------------------------------------------
  def generateEmptyTMpacket(self, pktMnemonic):
    """
    generates an empty TM packet (all parameters are zero):
    implementation of SPACE.IF.OnboardComputer.generateTMpacket
    """
    params = ""
    values = ""
    tmPacketData = SPACE.IF.s_definitions.getTMpacketInjectData(pktMnemonic,
                                                                params,
                                                                values)
    # check the TM packet data
    if tmPacketData == None:
      LOG_ERROR("TM packet creation failed for " + pktMnemonic, "SPACE")
      return False
    # send the TM packet
    return self.generateTMpacket(tmPacketData)
  # ---------------------------------------------------------------------------
  def generateEmptyTMpacketBySPID(self, spid):
    """
    generates an empty TM packet (all parameters are zero):
    implementation of SPACE.IF.OnboardComputer.generateEmptyTMpacketBySPID
    """
    params = ""
    values = ""
    tmPacketData = SPACE.IF.s_definitions.getTMpacketInjectDataBySPID(spid,
                                                                      params,
                                                                      values)

    # check the TM packet data
    if tmPacketData == None:
      LOG_ERROR("TM packet creation failed for SPID " + str(spid), "SPACE")
      return False
    # send the TM packet
    return self.generateTMpacket(tmPacketData)
  # ---------------------------------------------------------------------------
  def generateTMpacket(self, tmPacketData, obtUTC=None, ertUTC=None):
    """
    generates a TM packet:
    implementation of SPACE.IF.OnboardComputer.generateTMpacket
    """
    # create the TM packet
    spid = tmPacketData.pktSPID
    paramValues = tmPacketData.parameterValuesList
    dataField = tmPacketData.dataField
    segmentationFlags = tmPacketData.segmentationFlags
    tmPacketDu = SPACE.IF.s_tmPacketGenerator.getTMpacket(spid,
                                                          paramValues,
                                                          dataField,
                                                          segmentationFlags,
                                                          obtUTC)
    if tmPacketDu.dataFieldHeaderFlag:
      LOG("PUS Packet:" + UTIL.DU.array2str(tmPacketDu.getBufferString()[0:min(16,len(tmPacketDu))]), "SPACE")
    else:
      LOG("CCSDS Packet:" + UTIL.DU.array2str(tmPacketDu.getBufferString()[0:min(16,len(tmPacketDu))]), "SPACE")
    if tmPacketDu == None:
      LOG_ERROR("packet creation failed: SPID = " + str(spid), "SPACE")
      return False
    # send the TM packet
    return self.pushTMpacket(tmPacketDu, ertUTC)
  # ---------------------------------------------------------------------------
  def generateAcksFromTCpacket(self, tcPacketDu, ack1, ack2, ack3, ack4):
    """
    generates a TC acknowledgements according to PUS service 1:
    implementation of SPACE.IF.OnboardComputer.generateAcksFromTCpacket
    """
    ok = True
    tcAPID =  str(tcPacketDu.applicationProcessId)
    tcSSC = str(tcPacketDu.sequenceControlCount)
    if ack1 == SPACE.IF.ENABLE_ACK:
      LOG_INFO("generate ACK1 (TC_ACK_ACCEPT_SUCC)", "SPACE")
      ok &= self.generateAck(tcAPID, tcSSC, PUS.SERVICES.TC_ACK_ACCEPT_SUCC)
    elif ack1 == SPACE.IF.ENABLE_NAK:
      LOG_ERROR("generate NAK1 (TC_ACK_ACCEPT_FAIL)", "SPACE")
      ok &= self.generateAck(tcAPID, tcSSC, PUS.SERVICES.TC_ACK_ACCEPT_FAIL)
    else:
      LOG_WARNING("suppress ACK1 (TC_ACK_ACCEPT_SUCC)", "SPACE")
    if ack2 == SPACE.IF.ENABLE_ACK:
      LOG_INFO("generate ACK2 (TC_ACK_EXESTA_SUCC)", "SPACE")
      ok &= self.generateAck(tcAPID, tcSSC, PUS.SERVICES.TC_ACK_EXESTA_SUCC)
    elif ack2 == SPACE.IF.ENABLE_NAK:
      LOG_ERROR("generate NAK2 (TC_ACK_EXESTA_FAIL)", "SPACE")
      ok &= self.generateAck(tcAPID, tcSSC, PUS.SERVICES.TC_ACK_EXESTA_FAIL)
    else:
      LOG_WARNING("suppress ACK2 (TC_ACK_EXESTA_SUCC)", "SPACE")
    if ack3 == SPACE.IF.ENABLE_ACK:
      LOG_INFO("generate ACK3 (TC_ACK_EXEPRO_SUCC)", "SPACE")
      ok &= self.generateAck(tcAPID, tcSSC, PUS.SERVICES.TC_ACK_EXEPRO_SUCC)
    elif ack3 == SPACE.IF.ENABLE_NAK:
      LOG_ERROR("generate NAK3 (TC_ACK_EXEPRO_FAIL)", "SPACE")
      ok &= self.generateAck(tcAPID, tcSSC, PUS.SERVICES.TC_ACK_EXEPRO_FAIL)
    else:
      LOG_WARNING("suppress ACK3 (TC_ACK_EXEPRO_SUCC)", "SPACE")
    if ack4 == SPACE.IF.ENABLE_ACK:
      LOG_INFO("generate ACK4 (TC_ACK_EXECUT_SUCC)", "SPACE")
      ok &= self.generateAck(tcAPID, tcSSC, PUS.SERVICES.TC_ACK_EXECUT_SUCC)
    elif ack4 == SPACE.IF.ENABLE_NAK:
      LOG_ERROR("generate NAK4 (TC_ACK_EXECUT_FAIL)", "SPACE")
      ok &= self.generateAck(tcAPID, tcSSC, PUS.SERVICES.TC_ACK_EXECUT_FAIL)
    else:
      LOG_WARNING("suppress ACK4 (TC_ACK_EXECUT_SUCC)", "SPACE")
    return ok
  # ---------------------------------------------------------------------------
  def generateAck(self, tcAPID, tcSSC, ackType):
    """
    generates a TC acknowledgement according to PUS service 1
    implementation of SPACE.IF.OnboardComputer.generateAck
    """
    if not SPACE.IF.s_configuration.connected:
      LOG_WARNING("cannot send ACK/NAK because TM link is not active", "SPACE")
      return False
    if ackType == PUS.SERVICES.TC_ACK_ACCEPT_SUCC:
      pktMnemo = UTIL.SYS.s_configuration.TC_ACK_ACCEPT_SUCC_MNEMO
    elif ackType == PUS.SERVICES.TC_ACK_ACCEPT_FAIL:
      pktMnemo = UTIL.SYS.s_configuration.TC_ACK_ACCEPT_FAIL_MNEMO
    elif ackType == PUS.SERVICES.TC_ACK_EXESTA_SUCC:
      pktMnemo = UTIL.SYS.s_configuration.TC_ACK_EXESTA_SUCC_MNEMO
    elif ackType == PUS.SERVICES.TC_ACK_EXESTA_FAIL:
      pktMnemo = UTIL.SYS.s_configuration.TC_ACK_EXESTA_FAIL_MNEMO
    elif ackType == PUS.SERVICES.TC_ACK_EXEPRO_SUCC:
      pktMnemo = UTIL.SYS.s_configuration.TC_ACK_EXEPRO_SUCC_MNEMO
    elif ackType == PUS.SERVICES.TC_ACK_EXEPRO_FAIL:
      pktMnemo = UTIL.SYS.s_configuration.TC_ACK_EXEPRO_FAIL_MNEMO
    elif ackType == PUS.SERVICES.TC_ACK_EXECUT_SUCC:
      pktMnemo = UTIL.SYS.s_configuration.TC_ACK_EXECUT_SUCC_MNEMO
    elif ackType == PUS.SERVICES.TC_ACK_EXECUT_FAIL:
      pktMnemo = UTIL.SYS.s_configuration.TC_ACK_EXECUT_FAIL_MNEMO
    else:
      LOG_ERROR("invalid ackType for TC acknowledgement: " + str(ackType), "SPACE")
      return False
    if pktMnemo == "None":
      LOG("no telemetry packet defined for acknowledgement(" + str(ackType) + ")", "SPACE")
      return True
    # create the TM packet
    params =  "PUS_TYPE1_APID,PUS_TYPE1_SSC"
    values =  str(tcAPID)
    values += ","
    values += str(tcSSC)
    tmPacketData = SPACE.IF.s_definitions.getTMpacketInjectData(pktMnemo,
                                                                params,
                                                                values)
    # check the TM packet
    if tmPacketData == None:
      LOG_ERROR("packet creation failed for this acknowledgement: " + str(ackType), "SPACE")
      return False
    # send the TM packet
    return self.generateTMpacket(tmPacketData)
  # ---------------------------------------------------------------------------
  def pushTMpacket(self, tmPacketDu, ertUTC):
    """
    sends TM packet DU to CCS or downlink
    implementation of SPACE.IF.OnboardComputer.pushTMpacket
    """
    if self.egseMode:
      EGSE.IF.s_ccsLink.pushTMpacket(tmPacketDu)
    else:
      LINK.IF.s_packetLink.pushTMpacket(tmPacketDu, ertUTC)
    return True
  # ---------------------------------------------------------------------------
  def replayPackets(self, replayFileName):
    """
    sends TM packet from a replay file
    implementation of SPACE.IF.OnboardComputer.replayPackets
    """
    self.replayOBT = None
    self.replayERT = None
    if SPACE.IF.s_tmPacketReplayer.readReplayFile(replayFileName):
      # notify the GUI
      UTIL.TASK.s_processingTask.notifyGUItask("UPDATE_REPLAY")
      # start replay with sending of the first TM packet
      self.sendReplayPacket()
  # ---------------------------------------------------------------------------
  def sendReplayPacket(self):
    """timer triggered"""
    nextItem = SPACE.IF.s_tmPacketReplayer.getNextItem()
    while nextItem != None:
      itemType = nextItem[0]
      if itemType == SPACE.IF.RPLY_PKT:
        # TM packet
        tmPacketData = nextItem[1]
        pktMnemo = tmPacketData.pktName
        spid = tmPacketData.pktSPID
        if tmPacketData.segmentationFlags == CCSDS.PACKET.FIRST_SEGMENT:
          LOG("firstSegment " + pktMnemo + ", SPID=" + str(spid), "SPACE")
        elif tmPacketData.segmentationFlags == CCSDS.PACKET.CONTINUATION_SEGMENT:
          LOG("continuationSegment " + pktMnemo + ", SPID=" + str(spid), "SPACE")
        elif tmPacketData.segmentationFlags == CCSDS.PACKET.LAST_SEGMENT:
          LOG("lastSegment " + pktMnemo + ", SPID=" + str(spid), "SPACE")
        else:
          LOG("sendPacket " + pktMnemo + ", SPID=" + str(spid), "SPACE")
        # send the TM packet
        self.generateTMpacket(tmPacketData, self.replayOBT, self.replayERT)
      elif itemType == SPACE.IF.RPLY_RAWPKT:
        # TM raw packet
        rawPkt = nextItem[1]
        tmPacketDu = CCSDS.PACKET.TMpacket(rawPkt)
        LOG("sendRawPacket APID=" + str(tmPacketDu.applicationProcessId) +
            ", SSC=" + str(tmPacketDu.sequenceControlCount), "SPACE")
        # send the TM packet
        self.pushTMpacket(tmPacketDu, self.replayERT)
      elif itemType == SPACE.IF.RPLY_SLEEP:
        # sleep
        sleepValue = nextItem[1]
        LOG("sleep(" + str(sleepValue) + ")", "SPACE")
        UTIL.TASK.s_processingTask.createTimeHandler(sleepValue,
                                                     self.sendReplayPacket)
        # notify the GUI
        UTIL.TASK.s_processingTask.notifyGUItask("UPDATE_REPLAY")
        return
      elif itemType == SPACE.IF.RPLY_OBT:
        # onboard time
        self.replayOBT = nextItem[1]
        LOG("obt(" + UTIL.TIME.getASDtimeStr(self.replayOBT) + ")", "SPACE")
        # notify the GUI
        UTIL.TASK.s_processingTask.notifyGUItask("UPDATE_REPLAY")
      else:
        # earth reception time
        self.replayERT = nextItem[1]
        LOG("ert(" + UTIL.TIME.getASDtimeStr(self.replayERT) + ")", "SPACE")
        # notify the GUI
        UTIL.TASK.s_processingTask.notifyGUItask("UPDATE_REPLAY")
      nextItem = SPACE.IF.s_tmPacketReplayer.getNextItem()
    # cyclic sending terminated
    LOG_WARNING("replay finished", "SPACE")
    # notify the GUI
    UTIL.TASK.s_processingTask.notifyGUItask("UPDATE_REPLAY")
  # ---------------------------------------------------------------------------
  def startCyclicTM(self):
    """
    start sending of cyclic:
    implementation of SPACE.IF.OnboardComputer.startCyclicTM
    """
    # enable the cyclic sending
    SPACE.IF.s_configuration.sendCyclic = True
    self.sendCyclicCallback()
    # notify the GUI
    UTIL.TASK.s_processingTask.notifyGUItask("ENABLED_CYCLIC")
  # ---------------------------------------------------------------------------
  def stopCyclicTM(self):
    """
    stops sending of cyclic:
    implementation of SPACE.IF.OnboardComputer.stopCyclicTM
    """
    # disable the cyclic sending
    SPACE.IF.s_configuration.sendCyclic = False
    # notify the GUI
    UTIL.TASK.s_processingTask.notifyGUItask("DISABLED_CYCLIC")
  # ---------------------------------------------------------------------------
  def sendCyclicCallback(self):
    """timer triggered"""
    if not SPACE.IF.s_configuration.sendCyclic:
      # cyclic sending terminated
      return
    UTIL.TASK.s_processingTask.createTimeHandler(SPACE.IF.s_configuration.cyclicPeriodMs,
                                                 self.sendCyclicCallback)
    pktMnemo = UTIL.SYS.s_configuration.TM_CYCLIC_MNEMO
    LOG("sendCyclic(" + pktMnemo + ")", "SPACE")
    # create the TM packet
    params = ""
    values = ""
    tmPacketData = SPACE.IF.s_definitions.getTMpacketInjectData(pktMnemo,
                                                                params,
                                                                values)
    # check the TM packet
    if tmPacketData == None:
      LOG_ERROR("packet creation failed for cyclic TM", "SPACE")
      return
    # send the TM packet
    self.generateTMpacket(tmPacketData)

#############
# functions #
#############
def init(egseMode):
  # initialise singleton(s)
  SPACE.IF.s_onboardComputer = OnboardComputerImpl(egseMode)
