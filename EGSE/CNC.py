#******************************************************************************
# (C) 2017, Stefan Korner, Austria                                            *
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
# EGSE interfaces - CnC protocol                                              *
# implements CAIT-03474-ASTR_issue_3_EGSE_IRD.pdf                             *
#******************************************************************************
import sys
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import EGSE.CNCPDU
import UTIL.TASK, UTIL.TCP, UTIL.TIME

###########
# classes #
###########

# =============================================================================
class Server(UTIL.TCP.SingleClientReceivingServer):
  """CNC PDU interface - SCOE side"""
  # ---------------------------------------------------------------------------
  def __init__(self, portNr):
    """Initialise attributes only"""
    modelTask = UTIL.TASK.s_processingTask
    UTIL.TCP.SingleClientReceivingServer.__init__(self, modelTask, portNr)
  # ---------------------------------------------------------------------------
  def accepted(self, clientSocket):
    """Overloaded from SingleClientReceivingServer"""
    UTIL.TCP.SingleClientReceivingServer.accepted(self, clientSocket)
    self.clientAccepted()
  # ---------------------------------------------------------------------------
  def sendPDU(self, pdu):
    """Send the PDU to CCS"""
    # this operation does not verify the contents of the PDU
    self.dataSocket.send(pdu.getBufferString())
  # ---------------------------------------------------------------------------
  def sendTc_aSpace(self, status, tcIdentificationWord):
    """Send a (TC_A,SPACE) PDU to the CCS"""
    if status == 0:
      LOG_INFO("CNC.Server.sendTc_aSpace(OK)")
    else:
      LOG_ERROR("CNC.Server.sendTc_aSpace(ERROR)")
    pdu = EGSE.CNCPDU.PDU()
    pdu.pduType = EGSE.CNCPDU.PDU_TYPE_TC_A
    pdu.subType = EGSE.CNCPDU.SUB_TYPE_SPACE
    pdu.field2 = status
    pdu.field3 = tcIdentificationWord
    self.sendPDU(pdu)
  # ---------------------------------------------------------------------------
  def sendTc_aScoe(self, status, tcIdentificationWord):
    """Send a (TC_A,SCOE) PDU to the CCS"""
    if status == 0:
      LOG_INFO("CNC.Server.sendTc_aScoe(OK)")
    else:
      LOG_ERROR("CNC.Server.sendTc_aScoe(ERROR)")
    pdu = EGSE.CNCPDU.PDU()
    pdu.pduType = EGSE.CNCPDU.PDU_TYPE_TC_A
    pdu.subType = EGSE.CNCPDU.SUB_TYPE_SCOE
    pdu.field2 = status
    pdu.field3 = tcIdentificationWord
    self.sendPDU(pdu)
  # ---------------------------------------------------------------------------
  def sendTc_eSpace(self, tcSpacePDU, telecommandEchoStatus):
    """Send a (TC_E,SPACE) PDU to the CCS"""
    if telecommandEchoStatus == 0:
      LOG_INFO("CNC.Server.sendTc_eSpace(OK)")
    else:
      LOG_ERROR("CNC.Server.sendTc_eSpace(ERROR)")
    tc_eSpacePDU = EGSE.CNCPDU.TC_Espace(tcSpacePDU.buffer)
    tc_eSpacePDU.telecommandEchoStatus = telecommandEchoStatus
    self.sendPDU(tc_eSpacePDU)
  # ---------------------------------------------------------------------------
  def sendTc_eScoe(self, tcSpacePDU, telecommandEchoStatus):
    """Send a (TC_E,SCOE) PDU to the CCS"""
    if telecommandEchoStatus == 0:
      LOG_INFO("CNC.Server.sendTc_eScoe(OK)")
    else:
      LOG_ERROR("CNC.Server.sendTc_eScoe(ERROR)")
    tc_eScoePDU = EGSE.CNCPDU.TC_Escoe(tcSpacePDU.buffer)
    tc_eScoePDU.telecommandEchoStatus = telecommandEchoStatus
    self.sendPDU(tc_eScoePDU)
  # ---------------------------------------------------------------------------
  def sendTmSpace(self, tmPacket):
    """Send a (TM,SPACE) PDU to the CCS"""
    LOG_INFO("CNC.Server.sendTmSpace")
    tmSpacePDU = EGSE.CNCPDU.TMspace()
    tmSpacePDU.setCCSDSpacket(tmPacket)
    self.sendPDU(tmSpacePDU)
  # ---------------------------------------------------------------------------
  def sendTmScoe(self, tmPacket):
    """Send a (TM,SCOE) PDU to the CCS"""
    LOG_INFO("CNC.Server.sendTmScoe")
    tmScoePDU = EGSE.CNCPDU.TMscoe()
    tmScoePDU.setCCSDSpacket(tmPacket)
    self.sendPDU(tmScoePDU)
  # ---------------------------------------------------------------------------
  def sendCmdAnsw(self, message):
    """Send a (CMD,ANSW) PDU to the CCS"""
    LOG_INFO("CNC.Server.sendCmdAnsw")
    pdu = EGSE.CNCPDU.PDU()
    pdu.pduType = EGSE.CNCPDU.PDU_TYPE_CMD
    pdu.subType = EGSE.CNCPDU.SUB_TYPE_ANSW
    pdu.setDataField(message)
    self.sendPDU(pdu)
  # ---------------------------------------------------------------------------
  def receiveCallback(self, socket, stateMask):
    """Callback when the CCS has send data"""
    # read the PDU header from the data socket
    try:
      pduHeader = self.dataSocket.recv(EGSE.CNCPDU.PDU_HEADER_BYTE_SIZE);
    except Exception, ex:
      self.disconnectClient()
      self.notifyConnectionClosed(str(ex))
      return
    # consistency check
    pduHeaderLen = len(pduHeader)
    if pduHeaderLen == 0:
      self.disconnectClient()
      self.notifyConnectionClosed("empty data read")
      return
    if pduHeaderLen != EGSE.CNCPDU.PDU_HEADER_BYTE_SIZE:
      LOG_ERROR("Read of PDU header failed: invalid size: " + str(pduHeaderLen))
      return
    pdu = EGSE.CNCPDU.PDU(pduHeader)
    # read the data field for the PDU from the data socket
    dataFieldLength = pdu.dataFieldLength
    if dataFieldLength > 0:
      try:
        dataField = self.dataSocket.recv(dataFieldLength);
      except Exception, ex:
        LOG_ERROR("Read of PDU dataField failed: " + str(ex))
        return
      # consistency check
      remainingSizeRead = len(dataField)
      if remainingSizeRead != dataFieldLength:
        LOG_ERROR("Read of remaining PDU failed: invalid remaining size: " + str(remainingSizeRead))
        return
      pdu.setDataField(dataField)
    # dispatch depending on pduType and subType
    try:
      if pdu.pduType == EGSE.CNCPDU.PDU_TYPE_TC:
        if pdu.subType == EGSE.CNCPDU.SUB_TYPE_SPACE:
          # (TC,SPACE)
          LOG_INFO("CNC.Server.receiveCallback(TC,SPACE)")
          tcSpacePDU = EGSE.CNCPDU.TCspace(pdu.buffer)
          if self.notifyTcSpace(tcSpacePDU.getCCSDSpacket()):
            # forwarding OK
            self.sendTc_aSpace(0, tcSpacePDU.tcIdentificationWord)
            self.sendTc_eSpace(tcSpacePDU, 0)
          else:
            # forwarding failed
            self.sendTc_aSpace(1, tcSpacePDU.tcIdentificationWord)
            self.sendTc_eSpace(tcSpacePDU, 1)
        elif pdu.subType == EGSE.CNCPDU.SUB_TYPE_SCOE:
          # (TC,SCOE)
          LOG_INFO("CNC.Server.receiveCallback(TC,SCOE)")
          tcScoePDU = EGSE.CNCPDU.TCscoe(pdu.buffer)
          if self.notifyTcScoe(tcScoePDU.getCCSDSpacket()):
            # forwarding OK
            self.sendTc_aScoe(0, tcScoePDU.tcIdentificationWord)
            self.sendTc_eScoe(tcScoePDU, 0)
          else:
            # forwarding failed
            self.sendTc_aScoe(1, tcScoePDU.tcIdentificationWord)
            self.sendTc_eScoe(tcScoePDU, 1)
        else:
          LOG_ERROR("Read of PDU header failed: invalid subType: " + str(pdu.subType))
          LOG_INFO("PDU = " + str(pdu))
      elif pdu.pduType == EGSE.CNCPDU.PDU_TYPE_CMD:
        if pdu.subType == EGSE.CNCPDU.SUB_TYPE_EXEC:
          # (CMD,EXEC)
          LOG_INFO("CNC.Server.receiveCallback(CMD,EXEC)")
          self.notifyCmdExec(pdu.getDataField().tostring())
        else:
          LOG_ERROR("Read of PDU header failed: invalid subType: " + str(pdu.subType))
          LOG_INFO("PDU = " + str(pdu))
      else:
        LOG_ERROR("Read of PDU header failed: invalid pduType: " + str(pdu.pduType))
        LOG_INFO("PDU = " + str(pdu))
    except Exception, ex:
      LOG_ERROR("Processing of received PDU failed: " + str(ex))
  # ---------------------------------------------------------------------------
  def notifyConnectionClosed(self, details):
    """Connection closed by client"""
    LOG_WARNING("Connection closed by CCS: " + details)
  # ---------------------------------------------------------------------------
  def notifyTcSpace(self, tcPacket):
    """(TC,SPACE) received: hook for derived classes"""
    LOG_INFO("notifyTcSpace: tcPacket = " + UTIL.DU.array2str(tcPacket))
    return True
  # ---------------------------------------------------------------------------
  def notifyTcScoe(self, tcPacket):
    """(TC,SCOE) received: hook for derived classes"""
    LOG_INFO("notifyTcScoe: tcPacket = " + UTIL.DU.array2str(tcPacket))
    return True
  # ---------------------------------------------------------------------------
  def notifyCmdExec(self, message):
    """(CMD,EXEC) received: hook for derived classes"""
    LOG_INFO("notifyCmdExec: message = " + message)
  # ---------------------------------------------------------------------------
  def clientAccepted(self):
    """hook for derived classes"""
    pass

# =============================================================================
class Client(UTIL.TCP.SingleServerReceivingClient):
  """CNC PDU interface - CCS side"""
  # connectToServer and disconnectFromServer are inherited
  # and must be handled in a proper way from the application
  # ---------------------------------------------------------------------------
  def __init__(self):
    """Initialise attributes only"""
    modelTask = UTIL.TASK.s_processingTask
    UTIL.TCP.SingleServerReceivingClient.__init__(self, modelTask)
  # ---------------------------------------------------------------------------
  def sendPDU(self, pdu):
    """Send the PDU to the SCOE"""
    # this operation does not verify the contents of the DU
    self.dataSocket.send(pdu.getBufferString())
  # ---------------------------------------------------------------------------
  def sendTcSpace(self, tcPacket):
    """Send a (TC,SPACE) PDU to the SCOE"""
    LOG_INFO("CNC.Client.sendTcSpace")
    tcSpacePDU = EGSE.CNCPDU.TCspace()
    tcSpacePDU.setCCSDSpacket(tcPacket)
    self.sendPDU(tcSpacePDU)
  # ---------------------------------------------------------------------------
  def sendTcScoe(self, tcPacket):
    """Send a (TC,SCOE) PDU to the SCOE"""
    LOG_INFO("CNC.Client.sendTcScoe")
    tcScoePDU = EGSE.CNCPDU.TCscoe()
    tcScoePDU.setCCSDSpacket(tcPacket)
    self.sendPDU(tcScoePDU)
  # ---------------------------------------------------------------------------
  def sendCmdExec(self, tcPacket):
    """Send a (CMD,EXEC) PDU to the SCOE"""
    LOG_INFO("CNC.Client.sendCmdExec")
    pdu = EGSE.CNCPDU.PDU()
    pdu.pduType = EGSE.CNCPDU.PDU_TYPE_CMD
    pdu.subType = EGSE.CNCPDU.SUB_TYPE_EXEC
    pdu.setDataField(tcPacket)
    self.sendPDU(pdu)
  # ---------------------------------------------------------------------------
  def receiveCallback(self, socket, stateMask):
    """Callback when the SCOE has send data"""
    # read the PDU header from the data socket
    try:
      pduHeader = self.dataSocket.recv(EGSE.CNCPDU.PDU_HEADER_BYTE_SIZE);
    except Exception, ex:
      self.disconnectFromServer()
      self.notifyConnectionClosed(str(ex))
      return
    # consistency check
    pduHeaderLen = len(pduHeader)
    if pduHeaderLen == 0:
      # client termination
      self.disconnectFromServer()
      self.notifyConnectionClosed("empty data read")
      return
    if pduHeaderLen != EGSE.CNCPDU.PDU_HEADER_BYTE_SIZE:
      LOG_ERROR("Read of PDU header failed: invalid size: " + str(pduHeaderLen))
      return
    pdu = EGSE.CNCPDU.PDU(pduHeader)
    # read the data field for the PDU from the data socket
    dataFieldLength = pdu.dataFieldLength
    if dataFieldLength > 0:
      try:
        dataField = self.dataSocket.recv(dataFieldLength);
      except Exception, ex:
        LOG_ERROR("Read of PDU dataField failed: " + str(ex))
        return
      # consistency check
      remainingSizeRead = len(dataField)
      if remainingSizeRead != dataFieldLength:
        LOG_ERROR("Read of remaining PDU failed: invalid remaining size: " + str(remainingSizeRead))
        return
      pdu.setDataField(dataField)
    # dispatch depending on pduType and subType
    try:
      if pdu.pduType == EGSE.CNCPDU.PDU_TYPE_TC_A:
        if pdu.subType == EGSE.CNCPDU.SUB_TYPE_SPACE:
          # (TC_A,SPACE)
          LOG_INFO("CNC.Client.receiveCallback(TC_A,SPACE)")
          self.notifyTc_aSpace(pdu.field2, pdu.field3)
        elif pdu.subType == EGSE.CNCPDU.SUB_TYPE_SCOE:
          # (TC_A,SCOE)
          LOG_INFO("CNC.Client.receiveCallback(TC_A,SCOE)")
          self.notifyTc_aScoe(pdu.field2, pdu.field3)
        else:
          LOG_ERROR("Read of PDU header failed: invalid subType: " + str(pdu.subType))
          LOG_INFO("PDU = " + str(pdu))
      elif pdu.pduType == EGSE.CNCPDU.PDU_TYPE_TC_E:
        if pdu.subType == EGSE.CNCPDU.SUB_TYPE_SPACE:
          # (TC_E,SPACE)
          LOG_INFO("CNC.Client.receiveCallback(TC_E,SPACE)")
          tc_eSpacePDU = EGSE.CNCPDU.TC_Espace(pdu.buffer)
          self.notifyTc_eSpace(tc_eSpacePDU.getCCSDSpacket())
        elif pdu.subType == EGSE.CNCPDU.SUB_TYPE_SCOE:
          # (TC_E,SCOE)
          LOG_INFO("CNC.Client.receiveCallback(TC_E,SCOE)")
          tc_eScoePDU = EGSE.CNCPDU.TC_Escoe(pdu.buffer)
          self.notifyTc_eScoe(tc_eScoePDU.getCCSDSpacket())
        else:
          LOG_ERROR("Read of PDU header failed: invalid subType: " + str(pdu.subType))
          LOG_INFO("PDU = " + str(pdu))
      elif pdu.pduType == EGSE.CNCPDU.PDU_TYPE_TM:
        if pdu.subType == EGSE.CNCPDU.SUB_TYPE_SPACE:
          # (TM,SPACE)
          LOG_INFO("CNC.Client.receiveCallback(TM,SPACE)")
          tmSpacePDU = EGSE.CNCPDU.TMspace(pdu.buffer)
          self.notifyTmSpace(tmSpacePDU.getCCSDSpacket())
        elif pdu.subType == EGSE.CNCPDU.SUB_TYPE_SCOE:
          # (TM,SCOE)
          LOG_INFO("CNC.Client.receiveCallback(TM,SCOE)")
          tmScoePDU = EGSE.CNCPDU.TMscoe(pdu.buffer)
          self.notifyTmScoe(tmScoePDU.getCCSDSpacket())
        else:
          LOG_ERROR("Read of PDU header failed: invalid subType: " + str(pdu.subType))
          LOG_INFO("PDU = " + str(pdu))
      elif pdu.pduType == EGSE.CNCPDU.PDU_TYPE_CMD:
        if pdu.subType == EGSE.CNCPDU.SUB_TYPE_ANSW:
          # (CMD,ANSW)
          LOG_INFO("CNC.Client.receiveCallback(CMD,ANSW)")
          self.notifyCmdAnsw(pdu.getDataField().tostring())
        else:
          LOG_ERROR("Read of PDU header failed: invalid subType: " + str(pdu.subType))
          LOG_INFO("PDU = " + str(pdu))
      else:
        LOG_ERROR("Read of PDU header failed: invalid pduType: " + str(pdu.pduType))
        LOG_INFO("PDU = " + str(pdu))
    except Exception, ex:
      LOG_ERROR("Processing of received PDU failed: " + str(ex))
  # ---------------------------------------------------------------------------
  def notifyConnectionClosed(self, details):
    """Connection closed by server"""
    LOG_WARNING("Connection closed by SCOE: " + details)
  # ---------------------------------------------------------------------------
  def notifyTc_aSpace(self, status, tcIdentificationWord):
    """(TC_A,SPACE) received: hook for derived classes"""
    LOG_INFO("notifyTc_aSpace: status = " + str(status) + ", tcIdentificationWord = " + str(tcIdentificationWord))
  # ---------------------------------------------------------------------------
  def notifyTc_aScoe(self, status, tcIdentificationWord):
    """(TC_A,SCOE) received: hook for derived classes"""
    LOG_INFO("notifyTc_aScoe: status = " + str(status) + ", tcIdentificationWord = " + str(tcIdentificationWord))
  # ---------------------------------------------------------------------------
  def notifyTc_eSpace(self, tcPacket):
    """(TC_E,SPACE) received: hook for derived classes"""
    LOG_INFO("notifyTc_eSpace: tcPacket = " + UTIL.DU.array2str(tcPacket))
  # ---------------------------------------------------------------------------
  def notifyTc_eScoe(self, tcPacket):
    """(TC_E,SCOE) received: hook for derived classes"""
    LOG_INFO("notifyTc_eScoe: tcPacket = " + UTIL.DU.array2str(tcPacket))
  # ---------------------------------------------------------------------------
  def notifyTmSpace(self, tmPacket):
    """(TM,SPACE) received: hook for derived classes"""
    LOG_INFO("notifyTmSpace: tmPacket = " + UTIL.DU.array2str(tmPacket))
  # ---------------------------------------------------------------------------
  def notifyTmScoe(self, tmPacket):
    """(TM,SCOE) received: hook for derived classes"""
    LOG_INFO("notifyTmScoe: tmPacket = " + UTIL.DU.array2str(tmPacket))
  # ---------------------------------------------------------------------------
  def notifyCmdAnsw(self, message):
    """(CMD,ANSW) received: hook for derived classes"""
    LOG_INFO("notifyCmdAnsw: message = " + message)
