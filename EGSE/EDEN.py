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
# EGSE interfaces - EDEN protocol                                             *
#******************************************************************************
import sys
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import EGSE.EDENPDU
import UTIL.TASK, UTIL.TCP, UTIL.TIME

###########
# classes #
###########

# =============================================================================
class Server(UTIL.TCP.SingleClientReceivingServer):
  """EDEN PDU interface - SCOE side"""
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
  def sendCmdAnsw(self, message):
    """Send a (CMD,ANSW) PDU to the CCS"""
    pdu = EGSE.EDENPDU.PDU()
    pdu.pduType = EGSE.EDENPDU.PDU_TYPE_CMD
    pdu.subType = EGSE.EDENPDU.SUB_TYPE_ANSW
    pdu.setDataField(message)
    self.sendPDU(pdu)
  # ---------------------------------------------------------------------------
  def receiveCallback(self, socket, stateMask):
    """Callback when the CCS has send data"""
    # read the PDU header from the data socket
    try:
      pduHeader = self.dataSocket.recv(EGSE.EDENPDU.PDU_HEADER_BYTE_SIZE);
    except Exception, ex:
      self.disconnectClient()
      self.notifyConnectionClosed(str(ex))
      return
    # consistency check
    pduHeaderLen = len(pduHeader)
    if pduHeaderLen == 0:
      self.disconnectClient()
      self.notifyConnectionClosed("")
      return
    if pduHeaderLen != EGSE.EDENPDU.PDU_HEADER_BYTE_SIZE:
      LOG_ERROR("Read of PDU header failed: invalid size: " + str(pduHeaderLen))
      self.disconnectClient()
      self.notifyConnectionClosed("invalid data")
      return
    pdu = EGSE.EDENPDU.PDU(pduHeader)
    # consistency check
    dataFieldLength = pdu.dataFieldLength
    if dataFieldLength <= 0:
      LOG_ERROR("Read of PDU header failed: invalid data field size: " + str(dataFieldLength))
      self.disconnectClient()
      self.notifyConnectionClosed("invalid data")
      return
    # read the data field for the PDU from the data socket
    try:
      dataField = self.dataSocket.recv(dataFieldLength);
    except Exception, ex:
      LOG_ERROR("Read of remaining PDU failed: " + str(ex))
      self.disconnectClient()
      self.notifyConnectionClosed("invalid data")
      return
    # consistency check
    remainingSizeRead = len(dataField)
    if remainingSizeRead != dataFieldLength:
      LOG_ERROR("Read of remaining PDU failed: invalid remaining size: " + str(remainingSizeRead))
      self.disconnectClient()
      self.notifyConnectionClosed("invalid data")
      return
    pdu.setDataField(dataField)
    try:
      if pdu.pduType == EGSE.EDENPDU.PDU_TYPE_TC:
        if pdu.subType == EGSE.EDENPDU.SUB_TYPE_SPACE:
          # (TC,SPACE)
          self.notifyTcSpace(pdu.getDataField())
        elif pdu.subType == EGSE.EDENPDU.SUB_TYPE_SCOE:
          # (TC,SCOE)
          self.notifyTcScoe(pdu.getDataField())
        else:
          LOG_ERROR("Read of PDU header failed: invalid subType: " + str(pdu.subType))
          LOG_INFO("PDU = " + str(pdu))
          self.disconnectClient()
          self.notifyConnectionClosed("invalid data")
      elif pdu.pduType == EGSE.EDENPDU.PDU_TYPE_CMD:
        if pdu.subType == EGSE.EDENPDU.SUB_TYPE_EXEC:
          # (CMD,EXEC)
          self.notifyCmdExec(pdu.getDataField().tostring())
        else:
          LOG_ERROR("Read of PDU header failed: invalid subType: " + str(pdu.subType))
          LOG_INFO("PDU = " + str(pdu))
          self.disconnectClient()
          self.notifyConnectionClosed("invalid data")
      else:
        LOG_ERROR("Read of PDU header failed: invalid pduType: " + str(pdu.pduType))
        LOG_INFO("PDU = " + str(pdu))
        self.disconnectClient()
        self.notifyConnectionClosed("invalid data")
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
  # ---------------------------------------------------------------------------
  def notifyTcScoe(self, tcPacket):
    """(TC,SCOE) received: hook for derived classes"""
    LOG_INFO("notifyTcScoe: tcPacket = " + UTIL.DU.array2str(tcPacket))
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
  """EDEN PDU interface - CCS side"""
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
    pdu = EGSE.EDENPDU.PDU()
    pdu.pduType = EGSE.EDENPDU.PDU_TYPE_TC
    pdu.subType = EGSE.EDENPDU.SUB_TYPE_SPACE
    pdu.setDataField(tcPacket)
    self.sendPDU(pdu)
  # ---------------------------------------------------------------------------
  def sendTcScoe(self, tcPacket):
    """Send a (TC,SCOE) PDU to the SCOE"""
    pdu = EGSE.EDENPDU.PDU()
    pdu.pduType = EGSE.EDENPDU.PDU_TYPE_TC
    pdu.subType = EGSE.EDENPDU.SUB_TYPE_SCOE
    pdu.setDataField(tcPacket)
    self.sendPDU(pdu)
  # ---------------------------------------------------------------------------
  def sendCmdExec(self, tcPacket):
    """Send a (CMD,EXEC) PDU to the SCOE"""
    pdu = EGSE.EDENPDU.PDU()
    pdu.pduType = EGSE.EDENPDU.PDU_TYPE_CMD
    pdu.subType = EGSE.EDENPDU.SUB_TYPE_EXEC
    pdu.setDataField(tcPacket)
    self.sendPDU(pdu)
  # ---------------------------------------------------------------------------
  def receiveCallback(self, socket, stateMask):
    """Callback when the SCOE has send data"""
    # read the PDU header from the data socket
    try:
      pduHeader = self.dataSocket.recv(EGSE.EDENPDU.PDU_HEADER_BYTE_SIZE);
    except Exception, ex:
      self.disconnectFromServer()
      self.notifyConnectionClosed(str(ex))
      return
    # consistency check
    pduHeaderLen = len(pduHeader)
    if pduHeaderLen == 0:
      # client termination
      self.disconnectFromServer()
      self.notifyConnectionClosed("")
      return
    if pduHeaderLen != EGSE.EDENPDU.PDU_HEADER_BYTE_SIZE:
      LOG_ERROR("Read of PDU header failed: invalid size: " + str(pduHeaderLen))
      self.disconnectFromServer()
      self.notifyConnectionClosed("invalid data")
      return
    pdu = EGSE.EDENPDU.PDU(pduHeader)
    # consistency check
    dataFieldLength = pdu.dataFieldLength
    if dataFieldLength <= 0:
      LOG_ERROR("Read of PDU header failed: invalid data field size: " + str(dataFieldLength))
      self.disconnectFromServer()
      self.notifyConnectionClosed("invalid data")
      return
    # read the data field for the PDU from the data socket
    try:
      dataField = self.dataSocket.recv(dataFieldLength);
    except Exception, ex:
      LOG_ERROR("Read of remaining PDU failed: " + str(ex))
      self.disconnectFromServer()
      self.notifyConnectionClosed("invalid data")
      return
    # consistency check
    remainingSizeRead = len(dataField)
    if remainingSizeRead != dataFieldLength:
      LOG_ERROR("Read of remaining PDU failed: invalid remaining size: " + str(remainingSizeRead))
      self.disconnectFromServer()
      self.notifyConnectionClosed("invalid data")
      return
    pdu.setDataField(dataField)
    try:
      if pdu.pduType == EGSE.EDENPDU.PDU_TYPE_CMD:
        if pdu.subType == EGSE.EDENPDU.SUB_TYPE_ANSW:
          # (CMD,ANSW)
          self.notifyCmdAnsw(pdu.getDataField().tostring())
        else:
          LOG_ERROR("Read of PDU header failed: invalid subType: " + str(pdu.subType))
          LOG_INFO("PDU = " + str(pdu))
          self.disconnectClient()
          self.notifyConnectionClosed("invalid data")
      else:
        LOG_ERROR("Read of PDU header failed: invalid pduType: " + str(pdu.pduType))
        LOG_INFO("PDU = " + str(pdu))
        self.disconnectClient()
        self.notifyConnectionClosed("invalid data")
    except Exception, ex:
      LOG_ERROR("Processing of received PDU failed: " + str(ex))
  # ---------------------------------------------------------------------------
  def notifyConnectionClosed(self, details):
    """Connection closed by server"""
    LOG_WARNING("Connection closed by SCOE: " + details)
  # ---------------------------------------------------------------------------
  def notifyCmdAnsw(self, message):
    """(CMD,ANSW) received: hook for derived classes"""
    LOG_INFO("notifyCmdAnsw: message = " + message)
