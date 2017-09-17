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
import CCSDS.PACKET
import EGSE.CNCPDU
import UTIL.TASK, UTIL.TCP, UTIL.TIME

###########
# classes #
###########

# =============================================================================
class TCserver(UTIL.TCP.SingleClientReceivingServer):
  """CNC TC interface - SCOE side"""
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
  def sendCNCpacket(self, cncTMpacketDU):
    """Send a CnC TM packet to the CCS"""
    # this operation does not verify the contents of the cncTMpacketDU
    self.dataSocket.send(cncTMpacketDU.getBufferString())
  # ---------------------------------------------------------------------------
  def sendCNCackNak(self, cncTCpacketDU):
    """Send a CnC ACK or NAK as response to a CnC TC packet to the CCS"""
    # format the response message according to the cncTCpacketDU
    # note: this violates the resposibility of the CCSDS packet processing
    #       because this should be done in the SPACE module
    # TODO: the recent implementation does not consider specific CnC messages
    #       but simply appends the message to the ACK/NAK token
    if EGSE.IF.s_configuration.egseAck2 == EGSE.IF.ENABLE_ACK:
      # normal processing
      if okStatus:
        LOG_INFO("CNC.TCserver.sendCNCackNak(ACK)")
      else:
        LOG_ERROR("CNC.TCserver.sendCNCackNak(NAK)")
    elif EGSE.IF.s_configuration.egseAck2 == EGSE.IF.ENABLE_NAK:
      LOG_WARNING("force CnC NAK")
      okStatus = False
    else:
      LOG_WARNING("suppress CNC ACK/NAK")
      return
    apid = cncTCpacketDU.applicationProcessId
    ssc = cncTCpacketDU.sequenceControlCount
    cncMessage = cncTCpacketDU.getCNCmessage()
    if okStatus:
      responseMessage = "ACK " + cncMessage
    else:
      responseMessage = "NAK " + cncMessage
    responseDU = EGSE.CNCPDU.TMpacket()
    responseDU.applicationProcessId = apid
    responseDU.sequenceControlCount = ssc
    responseDU.segmentationFlags = CCSDS.PACKET.UNSEGMENTED
    responseDU.setCNCmessage(responseMessage)
    self.sendCNCpacket(responseDU)
  # ---------------------------------------------------------------------------
  def sendNAK(self, cncTCpacketDU):
    """Send a NAK as response to a CnC TC packet to the CCS"""
    # format the response message according to the cncTCpacketDU
    # note: this violates the resposibility of the CCSDS packet processing
    #       because this should be done in the SPACE module
    # TODO: the recent implementation does not consider specific Cnc messages
    #       but simply appends the message to the NAK token
    apid = cncTCpacketDU.applicationProcessId
    ssc = cncTCpacketDU.sequenceControlCount
    nakMessage = "NAK " + cncTCpacketDU.getCNCmessage()
    responseDU = EGSE.CNCPDU.TMpacket()
    responseDU.applicationProcessId = apid
    responseDU.sequenceControlCount = ssc
    responseDU.segmentationFlags = CCSDS.PACKET.UNSEGMENTED
    responseDU.setCNCmessage(nakMessage)
    self.sendCNCpacket(responseDU)
  # ---------------------------------------------------------------------------
  def receiveCallback(self, socket, stateMask):
    """Callback when the CCS has send data"""
    # read the packet header from the data socket
    try:
      packetHeader = self.dataSocket.recv(CCSDS.PACKET.PRIMARY_HEADER_BYTE_SIZE);
    except Exception, ex:
      self.disconnectClient()
      self.notifyConnectionClosed(str(ex))
      return
    # consistency check
    packetHeaderLen = len(packetHeader)
    if packetHeaderLen == 0:
      self.disconnectClient()
      self.notifyConnectionClosed("empty data read")
      return
    if packetHeaderLen != CCSDS.PACKET.PRIMARY_HEADER_BYTE_SIZE:
      LOG_ERROR("Read of CnC header failed: invalid size: " + str(pduHeaderLen))
      return
    packetVersionNumber = packetHeader[0] >> 5
    if packetVersionNumber == EGSE.CNCPDU.VERSION_NUMBER:
      LOG_INFO("CNC.TCserver.receiveCallback(CnC command)")
      tcPacketDU = EGSE.CNCPDU.TCpacket(packetHeader)
    else:
      LOG_INFO("CNC.TCserver.receiveCallback(CCSDS telecommand)")
      tcPacketDU = CCSDS.PACKET.TCpacket(packetHeader)
    # read the data field for the packet from the data socket
    dataFieldLength = tcPacketDU.packetLength + 1
    try:
      dataField = self.dataSocket.recv(dataFieldLength);
    except Exception, ex:
      LOG_ERROR("Read of packet dataField failed: " + str(ex))
      return
    # consistency check
    remainingSizeRead = len(dataField)
    if remainingSizeRead != dataFieldLength:
      LOG_ERROR("Read of remaining packet failed: invalid remaining size: " + str(remainingSizeRead))
      return
    tcPacketDU.setDataField(dataField)
    # dispatch the CnC command
    try:
      LOG_INFO("CNC.TCserver.receiveCallback(CnC command)")
      okStatus = self.notifyCNCcommand(tcPacketDU)
      self.sendCNCackNak(tcPacketDU, okStatus)
    except Exception, ex:
      LOG_ERROR("Processing of received CnC command failed: " + str(ex))
  # ---------------------------------------------------------------------------
  def notifyConnectionClosed(self, details):
    """TC connection closed by client"""
    LOG_WARNING("TC connection closed by CCS: " + details)
  # ---------------------------------------------------------------------------
  def notifyCNCcommand(self, cncTCpacketDU):
    """CnC command received: hook for derived classes"""
    LOG_INFO("notifyCNCcommand: tcPacket = " + UTIL.DU.array2str(cncTCpacketDU.getBufferString()))
    LOG_INFO("message = " + cncTCpacketDU.getCNCmessage())
    return True
  # ---------------------------------------------------------------------------
  def clientAccepted(self):
    """hook for derived classes"""
    pass

# =============================================================================
class TCclient(UTIL.TCP.SingleServerReceivingClient):
  """CNC TC interface - CCS side"""
  # connectToServer and disconnectFromServer are inherited
  # and must be handled in a proper way from the application
  # ---------------------------------------------------------------------------
  def __init__(self):
    """Initialise attributes only"""
    modelTask = UTIL.TASK.s_processingTask
    UTIL.TCP.SingleServerReceivingClient.__init__(self, modelTask)
  # ---------------------------------------------------------------------------
  def sendCNCpacket(self, cncTCpacketDU):
    """Send a CnC TC packet to the SCOE"""
    # this operation does not verify the contents of the cncTCpacketDU
    self.dataSocket.send(cncTCpacketDU.getBufferString())
  # ---------------------------------------------------------------------------
  def receiveCallback(self, socket, stateMask):
    """Callback when the SCOE has send data"""
    # read the packet header from the data socket
    try:
      packetHeader = self.dataSocket.recv(CCSDS.PACKET.PRIMARY_HEADER_BYTE_SIZE);
    except Exception, ex:
      self.disconnectFromServer()
      self.notifyConnectionClosed(str(ex))
      return
    # consistency check
    packetHeaderLen = len(packetHeader)
    if packetHeaderLen == 0:
      # client termination
      self.disconnectFromServer()
      self.notifyConnectionClosed("empty data read")
      return
    if packetHeaderLen != CCSDS.PACKET.PRIMARY_HEADER_BYTE_SIZE:
      LOG_ERROR("Read of CnC header failed: invalid size: " + str(pduHeaderLen))
      return
    cncTMpacketDU = EGSE.CNCPDU.TMpacket(packetHeader)
    # read the data field for the packet from the data socket
    dataFieldLength = cncTMpacketDU.packetLength + 1
    try:
      dataField = self.dataSocket.recv(dataFieldLength);
    except Exception, ex:
      LOG_ERROR("Read of packet dataField failed: " + str(ex))
      return
    # consistency check
    remainingSizeRead = len(dataField)
    if remainingSizeRead != dataFieldLength:
      LOG_ERROR("Read of remaining packet failed: invalid remaining size: " + str(remainingSizeRead))
      return
    cncTMpacketDU.setCNCmessage(dataField)
    # dispatch the CnC response
    try:
      LOG_INFO("CNC.TCclient.receiveCallback(CnC response)")
      self.notifyCNCresponse(cncTMpacketDU)
    except Exception, ex:
      LOG_ERROR("Processing of received CnC response failed: " + str(ex))
  # ---------------------------------------------------------------------------
  def notifyConnectionClosed(self, details):
    """Connection closed by server"""
    LOG_WARNING("Connection closed by SCOE: " + details)
  # ---------------------------------------------------------------------------
  def notifyCNCresponse(self, cncTMpacketDU):
    """CnC response received: hook for derived classes"""
    LOG_INFO("notifyCNCresponse: cncTMpacketDU = " + UTIL.DU.array2str(cncTMpacketDU.getBufferString()))
    LOG_INFO("message = " + cncTMpacketDU.getCNCmessage())
    return True

# =============================================================================
class TMserver(UTIL.TCP.Server):
  """CNC TM interface - SCOE side"""
  # ---------------------------------------------------------------------------
  def __init__(self, portNr):
    """Initialise attributes only"""
    modelTask = UTIL.TASK.s_processingTask
    UTIL.TCP.Server.__init__(self, modelTask, portNr)
    self.clientSocket = None
  # ---------------------------------------------------------------------------
  def accepted(self, clientSocket):
    """Overloaded from SingleClientReceivingServer"""
    self.clientSocket = clientSocket
    self.clientAccepted()
  # ---------------------------------------------------------------------------
  def sendTMpacket(self, tmPacket):
    """Send a CCSDS TM packet to the CCS"""
    # this operation does not verify the contents of the tmPacket
    self.clientSocket.send(tmPacket)
  # ---------------------------------------------------------------------------
  def notifyConnectionClosed(self, details):
    """TM connection closed by client"""
    LOG_WARNING("TM connection closed by CCS: " + details)
  # ---------------------------------------------------------------------------
  def clientAccepted(self):
    """hook for derived classes"""
    pass

# =============================================================================
class TMclient(UTIL.TCP.SingleServerReceivingClient):
  """CNC TM interface - CCS side"""
  # connectToServer and disconnectFromServer are inherited
  # and must be handled in a proper way from the application
  # ---------------------------------------------------------------------------
  def __init__(self):
    """Initialise attributes only"""
    modelTask = UTIL.TASK.s_processingTask
    UTIL.TCP.SingleServerReceivingClient.__init__(self, modelTask)
  # ---------------------------------------------------------------------------
  def receiveCallback(self, socket, stateMask):
    """Callback when the SCOE has send data"""
    # read the packet header from the data socket
    try:
      packetHeader = self.dataSocket.recv(CCSDS.PACKET.PRIMARY_HEADER_BYTE_SIZE);
    except Exception, ex:
      self.disconnectFromServer()
      self.notifyConnectionClosed(str(ex))
      return
    # consistency check
    packetHeaderLen = len(packetHeader)
    if packetHeaderLen == 0:
      # client termination
      self.disconnectFromServer()
      self.notifyConnectionClosed("empty data read")
      return
    if packetHeaderLen != CCSDS.PACKET.PRIMARY_HEADER_BYTE_SIZE:
      LOG_ERROR("Read of CCSDS packet header failed: invalid size: " + str(pduHeaderLen))
      return
    ccsdsTMpacketDU = CCSDS.PACKET.TMpacket(packetHeader)
    # read the data field for the packet from the data socket
    dataFieldLength = ccsdsTMpacketDU.packetLength + 1
    try:
      dataField = self.dataSocket.recv(dataFieldLength);
    except Exception, ex:
      LOG_ERROR("Read of packet dataField failed: " + str(ex))
      return
    # consistency check
    remainingSizeRead = len(dataField)
    if remainingSizeRead != dataFieldLength:
      LOG_ERROR("Read of remaining packet failed: invalid remaining size: " + str(remainingSizeRead))
      return
    ccsdsTMpacketDU.append(dataField)
    # dispatch the CCSDS tm packet
    try:
      LOG_INFO("CNC.TMclient.receiveCallback(TM packet)")
      self.notifyTMpacket(ccsdsTMpacketDU.getBufferString())
    except Exception, ex:
      LOG_ERROR("Processing of received TM packet failed: " + str(ex))
  # ---------------------------------------------------------------------------
  def notifyConnectionClosed(self, details):
    """Connection closed by server"""
    LOG_WARNING("Connection closed by TMserver: " + details)
  # ---------------------------------------------------------------------------
  def notifyTMpacket(self, tmPacket):
    """TM packet received: hook for derived classes"""
    LOG_INFO("notifyTMpacket: tmPacket = " + UTIL.DU.array2str(tmPacket))
  # ---------------------------------------------------------------------------
  def notifyError(self, errorMessage, data):
    """error notification: hook for derived classes"""
    pass
