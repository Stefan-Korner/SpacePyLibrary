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
# EGSE interfaces - EDEN protocol                                             *
# implements Core_EGSE_AD03_GAL_REQ_ALS_SA_R_0002_EGSE_IRD_issue2.pdf         *
#******************************************************************************
import sys
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import EGSE.EDENPDU, EGSE.IF
import UTIL.TASK, UTIL.TCP, UTIL.TIME

###########
# classes #
###########

# =============================================================================
class Server(UTIL.TCP.SingleClientServer):
  """EDEN PDU interface - SCOE side"""
  # ---------------------------------------------------------------------------
  def __init__(self, portNr):
    """Initialise attributes only"""
    modelTask = UTIL.TASK.s_processingTask
    UTIL.TCP.SingleClientServer.__init__(self, modelTask, portNr)
  # ---------------------------------------------------------------------------
  def sendPDU(self, pdu):
    """Send the PDU to CCS"""
    # this operation does not verify the contents of the PDU
    self.send(pdu.getBuffer())
  # ---------------------------------------------------------------------------
  def sendTc_eSpace(self, tcSpacePDU, telecommandEchoStatus):
    """Send a (TC_E,SPACE) PDU to the CCS"""
    if EGSE.IF.s_serverConfiguration.egseAck1 == EGSE.IF.ENABLE_ACK:
      # normal processing
      if telecommandEchoStatus == 0:
        LOG_INFO("EDEN.Server.sendTc_eSpace(OK)")
      else:
        LOG_ERROR("EDEN.Server.sendTc_eSpace(ERROR)")
    elif EGSE.IF.s_serverConfiguration.egseAck1 == EGSE.IF.ENABLE_NAK:
      LOG_WARNING("force ERROR for (TC_E,SPACE)")
      telecommandEchoStatus = 1
    else:
      LOG_WARNING("suppress (TC_E,SPACE)")
      return
    tc_eSpacePDU = EGSE.EDENPDU.TC_Espace(tcSpacePDU.buffer)
    tc_eSpacePDU.telecommandEchoStatus = telecommandEchoStatus
    self.sendPDU(tc_eSpacePDU)
  # ---------------------------------------------------------------------------
  def sendTc_eScoe(self, tcSpacePDU, telecommandEchoStatus):
    """Send a (TC_E,SCOE) PDU to the CCS"""
    if EGSE.IF.s_serverConfiguration.egseAck1 == EGSE.IF.ENABLE_ACK:
      # normal processing
      if telecommandEchoStatus == 0:
        LOG_INFO("EDEN.Server.sendTc_eScoe(OK)")
      else:
        LOG_ERROR("EDEN.Server.sendTc_eScoe(ERROR)")
    elif EGSE.IF.s_serverConfiguration.egseAck1 == EGSE.IF.ENABLE_NAK:
      LOG_WARNING("force ERROR for (TC_E,SCOE)")
      telecommandEchoStatus = 1
    else:
      LOG_WARNING("suppress (TC_E,SCOE)")
      return
    tc_eScoePDU = EGSE.EDENPDU.TC_Escoe(tcSpacePDU.buffer)
    tc_eScoePDU.telecommandEchoStatus = telecommandEchoStatus
    self.sendPDU(tc_eScoePDU)
  # ---------------------------------------------------------------------------
  def sendTc_aSpace(self, status, tcIdentificationWord):
    """Send a (TC_A,SPACE) PDU to the CCS"""
    if EGSE.IF.s_serverConfiguration.egseAck2 == EGSE.IF.ENABLE_ACK:
      # normal processing
      if status == 0:
        LOG_INFO("EDEN.Server.sendTc_aSpace(OK)")
      else:
        LOG_ERROR("EDEN.Server.sendTc_aSpace(ERROR)")
    elif EGSE.IF.s_serverConfiguration.egseAck2 == EGSE.IF.ENABLE_NAK:
      LOG_WARNING("force ERROR for (TC_A,SPACE)")
      status = 1
    else:
      LOG_WARNING("suppress (TC_A,SPACE)")
      return
    pdu = EGSE.EDENPDU.PDU()
    pdu.pduType = EGSE.EDENPDU.PDU_TYPE_TC_A
    pdu.subType = EGSE.EDENPDU.SUB_TYPE_SPACE
    pdu.field2 = status
    pdu.field3 = tcIdentificationWord
    self.sendPDU(pdu)
  # ---------------------------------------------------------------------------
  def sendTc_aScoe(self, status, tcIdentificationWord):
    """Send a (TC_A,SCOE) PDU to the CCS"""
    if EGSE.IF.s_serverConfiguration.egseAck2 == EGSE.IF.ENABLE_ACK:
      # normal processing
      if status == 0:
        LOG_INFO("EDEN.Server.sendTc_aScoe(OK)")
      else:
        LOG_ERROR("EDEN.Server.sendTc_aScoe(ERROR)")
    elif EGSE.IF.s_serverConfiguration.egseAck2 == EGSE.IF.ENABLE_NAK:
      LOG_WARNING("force ERROR for (TC_A,SCOE)")
      status = 1
    else:
      LOG_WARNING("suppress (TC_A,SCOE)")
      return
    pdu = EGSE.EDENPDU.PDU()
    pdu.pduType = EGSE.EDENPDU.PDU_TYPE_TC_A
    pdu.subType = EGSE.EDENPDU.SUB_TYPE_SCOE
    pdu.field2 = status
    pdu.field3 = tcIdentificationWord
    self.sendPDU(pdu)
  # ---------------------------------------------------------------------------
  def sendTmSpace(self, tmPacket):
    """Send a (TM,SPACE) PDU to the CCS"""
    LOG_INFO("EDEN.Server.sendTmSpace")
    tmSpacePDU = EGSE.EDENPDU.TMspace()
    tmSpacePDU.setCCSDSpacket(tmPacket)
    self.sendPDU(tmSpacePDU)
  # ---------------------------------------------------------------------------
  def sendTmScoe(self, tmPacket):
    """Send a (TM,SCOE) PDU to the CCS"""
    LOG_INFO("EDEN.Server.sendTmScoe")
    tmScoePDU = EGSE.EDENPDU.TMscoe()
    tmScoePDU.setCCSDSpacket(tmPacket)
    self.sendPDU(tmScoePDU)
  # ---------------------------------------------------------------------------
  def sendCmdAnsw(self, message):
    """Send a (CMD,ANSW) PDU to the CCS"""
    LOG_INFO("EDEN.Server.sendCmdAnsw")
    pdu = EGSE.EDENPDU.PDU()
    pdu.pduType = EGSE.EDENPDU.PDU_TYPE_CMD
    pdu.subType = EGSE.EDENPDU.SUB_TYPE_ANSW
    pdu.setDataField(message)
    self.sendPDU(pdu)
  # ---------------------------------------------------------------------------
  def receiveCallback(self, socket, stateMask):
    """Callback when the CCS has send data"""
    # read the PDU header
    pduHeader = self.recv(EGSE.EDENPDU.PDU_HEADER_BYTE_SIZE)
    if pduHeader == None:
      # failure handling was done automatically by derived logic
      return
    # consistency check
    pduHeaderLen = len(pduHeader)
    if pduHeaderLen != EGSE.EDENPDU.PDU_HEADER_BYTE_SIZE:
      LOG_ERROR("Read of PDU header failed: invalid size: " + str(pduHeaderLen))
      self.disconnectClient()
      return
    pdu = EGSE.EDENPDU.PDU(pduHeader)
    # read the data field for the PDU
    dataFieldLength = pdu.dataFieldLength
    if dataFieldLength > 0:
      dataField = self.recv(dataFieldLength)
      if dataField == None:
        # failure handling was done automatically by derived logic
        return
      # consistency check
      remainingSizeRead = len(dataField)
      if remainingSizeRead != dataFieldLength:
        LOG_ERROR("Read of remaining PDU failed: invalid remaining size: " + str(remainingSizeRead))
        self.disconnectClient()
        return
      pdu.setDataField(dataField)
    # dispatch depending on pduType and subType
    try:
      if pdu.pduType == EGSE.EDENPDU.PDU_TYPE_TC:
        if pdu.subType == EGSE.EDENPDU.SUB_TYPE_SPACE:
          # (TC,SPACE)
          LOG_INFO("EDEN.Server.receiveCallback(TC,SPACE)")
          tcSpacePDU = EGSE.EDENPDU.TCspace(pdu.buffer)
          if self.notifyTcSpace(tcSpacePDU.getCCSDSpacket()):
            # forwarding OK
            self.sendTc_eSpace(tcSpacePDU, 0)
            self.sendTc_aSpace(0, tcSpacePDU.tcIdentificationWord)
          else:
            # forwarding failed
            self.sendTc_eSpace(tcSpacePDU, 1)
            self.sendTc_aSpace(1, tcSpacePDU.tcIdentificationWord)
        elif pdu.subType == EGSE.EDENPDU.SUB_TYPE_SCOE:
          # (TC,SCOE)
          LOG_INFO("EDEN.Server.receiveCallback(TC,SCOE)")
          tcScoePDU = EGSE.EDENPDU.TCscoe(pdu.buffer)
          if self.notifyTcScoe(tcScoePDU.getCCSDSpacket()):
            # forwarding OK
            self.sendTc_eScoe(tcScoePDU, 0)
            self.sendTc_aScoe(0, tcScoePDU.tcIdentificationWord)
          else:
            # forwarding failed
            self.sendTc_eScoe(tcScoePDU, 1)
            self.sendTc_aScoe(1, tcScoePDU.tcIdentificationWord)
        else:
          LOG_ERROR("Read of PDU header failed: invalid subType: " + str(pdu.subType))
          LOG("PDU = " + str(pdu))
          self.disconnectClient()
      elif pdu.pduType == EGSE.EDENPDU.PDU_TYPE_CMD:
        if pdu.subType == EGSE.EDENPDU.SUB_TYPE_EXEC:
          # (CMD,EXEC)
          LOG_INFO("EDEN.Server.receiveCallback(CMD,EXEC)")
          self.notifyCmdExec(pdu.getDataField().tostring())
        else:
          LOG_ERROR("Read of PDU header failed: invalid subType: " + str(pdu.subType))
          LOG("PDU = " + str(pdu))
          self.disconnectClient()
      else:
        LOG_ERROR("Read of PDU header failed: invalid pduType: " + str(pdu.pduType))
        LOG("PDU = " + str(pdu))
        self.disconnectClient()
    except Exception as ex:
      LOG_ERROR("Processing of received PDU failed: " + str(ex))
      self.disconnectClient()
  # ---------------------------------------------------------------------------
  def notifyTcSpace(self, tcPacket):
    """(TC,SPACE) received: hook for derived classes"""
    LOG("notifyTcSpace: tcPacket = " + UTIL.DU.array2str(tcPacket))
    return True
  # ---------------------------------------------------------------------------
  def notifyTcScoe(self, tcPacket):
    """(TC,SCOE) received: hook for derived classes"""
    LOG("notifyTcScoe: tcPacket = " + UTIL.DU.array2str(tcPacket))
    return True
  # ---------------------------------------------------------------------------
  def notifyCmdExec(self, message):
    """(CMD,EXEC) received: hook for derived classes"""
    LOG("notifyCmdExec: message = " + message)

# =============================================================================
class Client(UTIL.TCP.Client):
  """EDEN PDU interface - CCS side"""
  # connectToServer and disconnectFromServer are inherited
  # and must be handled in a proper way from the application
  # ---------------------------------------------------------------------------
  def __init__(self):
    """Initialise attributes only"""
    modelTask = UTIL.TASK.s_processingTask
    UTIL.TCP.Client.__init__(self, modelTask)
  # ---------------------------------------------------------------------------
  def recvError(self, errorMessage):
    """
    Read bytes from the data socket has failed,
    overloaded from UTIL.TCP.Client
    """
    LOG_ERROR("Client.recvError: " + errorMessage, "EDEN")
    # default implementation: disconnect from server
    self.disconnectFromServer()
  # ---------------------------------------------------------------------------
  def sendError(self, errorMessage):
    """
    Send bytes from the data socket has failed,
    overloaded from UTIL.TCP.Client
    """
    LOG_ERROR("Client.sendError: " + errorMessage, "EDEN")
    # default implementation: disconnect from server
    self.disconnectFromServer()
  # ---------------------------------------------------------------------------
  def sendPDU(self, pdu):
    """Send the PDU to the SCOE"""
    # this operation does not verify the contents of the DU
    self.send(pdu.getBuffer())
  # ---------------------------------------------------------------------------
  def sendTcSpace(self, tcPacket):
    """Send a (TC,SPACE) PDU to the SCOE"""
    LOG_INFO("EDEN.Client.sendTcSpace", "EDEN")
    tcSpacePDU = EGSE.EDENPDU.TCspace()
    tcSpacePDU.setCCSDSpacket(tcPacket)
    self.sendPDU(tcSpacePDU)
  # ---------------------------------------------------------------------------
  def sendTcScoe(self, tcPacket):
    """Send a (TC,SCOE) PDU to the SCOE"""
    LOG_INFO("EDEN.Client.sendTcScoe", "EDEN")
    tcScoePDU = EGSE.EDENPDU.TCscoe()
    tcScoePDU.setCCSDSpacket(tcPacket)
    self.sendPDU(tcScoePDU)
  # ---------------------------------------------------------------------------
  def sendCmdExec(self, tcPacket):
    """Send a (CMD,EXEC) PDU to the SCOE"""
    LOG_INFO("EDEN.Client.sendCmdExec", "EDEN")
    pdu = EGSE.EDENPDU.PDU()
    pdu.pduType = EGSE.EDENPDU.PDU_TYPE_CMD
    pdu.subType = EGSE.EDENPDU.SUB_TYPE_EXEC
    pdu.setDataField(tcPacket)
    self.sendPDU(pdu)
  # ---------------------------------------------------------------------------
  def receiveCallback(self, socket, stateMask):
    """Callback when the SCOE has send data"""
    # read the PDU header
    pduHeader = self.recv(EGSE.EDENPDU.PDU_HEADER_BYTE_SIZE)
    if pduHeader == None:
      # failure handling was done automatically by derived logic
      return
    # consistency check
    pduHeaderLen = len(pduHeader)
    if pduHeaderLen != EGSE.EDENPDU.PDU_HEADER_BYTE_SIZE:
      LOG_ERROR("Read of PDU header failed: invalid size: " + str(pduHeaderLen), "EDEN")
      self.disconnectFromServer()
      return
    pdu = EGSE.EDENPDU.PDU(pduHeader)
    # read the data field for the PDU
    dataFieldLength = pdu.dataFieldLength
    if dataFieldLength > 0:
      dataField = self.recv(dataFieldLength)
      if dataField == None:
        # failure handling was done automatically by derived logic
        return
      # consistency check
      remainingSizeRead = len(dataField)
      if remainingSizeRead != dataFieldLength:
        LOG_ERROR("Read of remaining PDU failed: invalid remaining size: " + str(remainingSizeRead), "EDEN")
        self.disconnectFromServer()
        return
      pdu.setDataField(dataField)
    # dispatch depending on pduType and subType
    try:
      if pdu.pduType == EGSE.EDENPDU.PDU_TYPE_TC_A:
        if pdu.subType == EGSE.EDENPDU.SUB_TYPE_SPACE:
          # (TC_A,SPACE)
          LOG_INFO("EDEN.Client.receiveCallback(TC_A,SPACE)", "EDEN")
          self.notifyTc_aSpace(pdu.field2, pdu.field3)
        elif pdu.subType == EGSE.EDENPDU.SUB_TYPE_SCOE:
          # (TC_A,SCOE)
          LOG_INFO("EDEN.Client.receiveCallback(TC_A,SCOE)", "EDEN")
          self.notifyTc_aScoe(pdu.field2, pdu.field3)
        else:
          LOG_ERROR("Read of PDU header failed: invalid subType: " + str(pdu.subType), "EDEN")
          LOG("PDU = " + str(pdu), "EDEN")
          self.disconnectFromServer()
      elif pdu.pduType == EGSE.EDENPDU.PDU_TYPE_TC_E:
        if pdu.subType == EGSE.EDENPDU.SUB_TYPE_SPACE:
          # (TC_E,SPACE)
          LOG_INFO("EDEN.Client.receiveCallback(TC_E,SPACE)", "EDEN")
          tc_eSpacePDU = EGSE.EDENPDU.TC_Espace(pdu.buffer)
          self.notifyTc_eSpace(tc_eSpacePDU.getCCSDSpacket())
        elif pdu.subType == EGSE.EDENPDU.SUB_TYPE_SCOE:
          # (TC_E,SCOE)
          LOG_INFO("EDEN.Client.receiveCallback(TC_E,SCOE)", "EDEN")
          tc_eScoePDU = EGSE.EDENPDU.TC_Escoe(pdu.buffer)
          self.notifyTc_eScoe(tc_eScoePDU.getCCSDSpacket())
        else:
          LOG_ERROR("Read of PDU header failed: invalid subType: " + str(pdu.subType), "EDEN")
          LOG("PDU = " + str(pdu))
          self.disconnectFromServer()
      elif pdu.pduType == EGSE.EDENPDU.PDU_TYPE_TM:
        if pdu.subType == EGSE.EDENPDU.SUB_TYPE_SPACE:
          # (TM,SPACE)
          LOG_INFO("EDEN.Client.receiveCallback(TM,SPACE)", "EDEN")
          tmSpacePDU = EGSE.EDENPDU.TMspace(pdu.buffer)
          self.notifyTmSpace(tmSpacePDU.getCCSDSpacket())
        elif pdu.subType == EGSE.EDENPDU.SUB_TYPE_SCOE:
          # (TM,SCOE)
          LOG_INFO("EDEN.Client.receiveCallback(TM,SCOE)", "EDEN")
          tmScoePDU = EGSE.EDENPDU.TMscoe(pdu.buffer)
          self.notifyTmScoe(tmScoePDU.getCCSDSpacket())
        else:
          LOG_ERROR("Read of PDU header failed: invalid subType: " + str(pdu.subType), "EDEN")
          LOG("PDU = " + str(pdu), "EDEN")
          self.disconnectFromServer()
      elif pdu.pduType == EGSE.EDENPDU.PDU_TYPE_CMD:
        if pdu.subType == EGSE.EDENPDU.SUB_TYPE_ANSW:
          # (CMD,ANSW)
          LOG_INFO("EDEN.Client.receiveCallback(CMD,ANSW)", "EDEN")
          self.notifyCmdAnsw(pdu.getDataField().tostring())
        else:
          LOG_ERROR("Read of PDU header failed: invalid subType: " + str(pdu.subType), "EDEN")
          LOG("PDU = " + str(pdu), "EDEN")
          self.disconnectFromServer()
      else:
        LOG_ERROR("Read of PDU header failed: invalid pduType: " + str(pdu.pduType), "EDEN")
        LOG("PDU = " + str(pdu), "EDEN")
        self.disconnectFromServer()
    except Exception as ex:
      LOG_ERROR("Processing of received PDU failed: " + str(ex), "EDEN")
      self.disconnectFromServer()
  # ---------------------------------------------------------------------------
  def notifyTc_aSpace(self, status, tcIdentificationWord):
    """(TC_A,SPACE) received: hook for derived classes"""
    LOG("notifyTc_aSpace: status = " + str(status) + ", tcIdentificationWord = " + str(tcIdentificationWord), "EDEN")
  # ---------------------------------------------------------------------------
  def notifyTc_aScoe(self, status, tcIdentificationWord):
    """(TC_A,SCOE) received: hook for derived classes"""
    LOG("notifyTc_aScoe: status = " + str(status) + ", tcIdentificationWord = " + str(tcIdentificationWord), "EDEN")
  # ---------------------------------------------------------------------------
  def notifyTc_eSpace(self, tcPacket):
    """(TC_E,SPACE) received: hook for derived classes"""
    LOG("notifyTc_eSpace: tcPacket = " + UTIL.DU.array2str(tcPacket), "EDEN")
  # ---------------------------------------------------------------------------
  def notifyTc_eScoe(self, tcPacket):
    """(TC_E,SCOE) received: hook for derived classes"""
    LOG("notifyTc_eScoe: tcPacket = " + UTIL.DU.array2str(tcPacket), "EDEN")
  # ---------------------------------------------------------------------------
  def notifyTmSpace(self, tmPacket):
    """(TM,SPACE) received: hook for derived classes"""
    LOG("notifyTmSpace: tmPacket = " + UTIL.DU.array2str(tmPacket), "EDEN")
  # ---------------------------------------------------------------------------
  def notifyTmScoe(self, tmPacket):
    """(TM,SCOE) received: hook for derived classes"""
    LOG("notifyTmScoe: tmPacket = " + UTIL.DU.array2str(tmPacket), "EDEN")
  # ---------------------------------------------------------------------------
  def notifyCmdAnsw(self, message):
    """(CMD,ANSW) received: hook for derived classes"""
    LOG("notifyCmdAnsw: message = " + message, "EDEN")
