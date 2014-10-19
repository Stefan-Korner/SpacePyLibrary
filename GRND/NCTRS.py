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
# Ground Simulation - NCTRS Module                                            *
#******************************************************************************
import sys
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import GRND.IF, GRND.NCTRSDU
import UTIL.TASK, UTIL.TCP, UTIL.TIME

###########
# classes #
###########
# =============================================================================
class TMreceiver(UTIL.TCP.SingleServerReceivingClient):
  """NCTRS telemetry receiver interface - SCOS side"""
  # connectToServer and disconnectFromServer are inherited
  # and must be handled in a proper way from the application
  # ---------------------------------------------------------------------------
  def __init__(self):
    """Initialise attributes only"""
    modelTask = UTIL.TASK.s_processingTask
    UTIL.TCP.SingleServerReceivingClient.__init__(self, modelTask)
  # ---------------------------------------------------------------------------
  def receiveCallback(self, socket, stateMask):
    """Callback when NCTRS has send data"""
    # read the TM data unit header from the data socket
    try:
      tmDuHeader = self.dataSocket.recv(GRND.NCTRSDU.TM_DU_HEADER_BYTE_SIZE);
    except Exception, ex:
      self.disconnectFromServer()
      self.notifyConnectionClosed(str(ex))
      return
    # consistency check
    tmDuHeaderLen = len(tmDuHeader)
    if tmDuHeaderLen == 0:
      # client termination
      self.disconnectFromServer()
      self.notifyConnectionClosed("")
      return
    if tmDuHeaderLen != GRND.NCTRSDU.TM_DU_HEADER_BYTE_SIZE:
      LOG_ERROR("Read of TM DU header failed: invalid size: " + str(tmDuHeaderLen))
      self.disconnectFromServer()
      self.notifyConnectionClosed("invalid data")
      return
    tmDu = GRND.NCTRSDU.TMdataUnit(tmDuHeader)
    # consistency check
    packetSize = tmDu.packetSize
    remainingSizeExpected = packetSize - GRND.NCTRSDU.TM_DU_HEADER_BYTE_SIZE
    if remainingSizeExpected <= 0:
      LOG_ERROR("Read of TM DU header failed: invalid packet size field: " + str(remainingSizeExpected))
      self.disconnectFromServer()
      self.notifyConnectionClosed("invalid data")
      return
    # read the remaining bytes for the TM data unit
    # from the data socket
    try:
      tmRemaining = self.dataSocket.recv(remainingSizeExpected);
    except Exception, ex:
      LOG_ERROR("Read of remaining TM DU failed: " + str(ex))
      self.disconnectFromServer()
      self.notifyConnectionClosed("invalid data")
      return
    # consistency check
    remainingSizeRead = len(tmRemaining)
    if remainingSizeRead != remainingSizeExpected:
      LOG_ERROR("Read of remaining TM DU failed: invalid remaining size: " + str(remainingSizeRead))
      self.disconnectFromServer()
      self.notifyConnectionClosed("invalid data")
      return
    # TM frame
    tmDu.append(tmRemaining)
    self.notifyTMdataUnit(tmDu)
  # ---------------------------------------------------------------------------
  def notifyConnectionClosed(self, details):
    """Connection closed by server"""
    LOG_WARNING("Connection closed by TMserver: " + details)
  # ---------------------------------------------------------------------------
  def notifyTMdataUnit(self, tmDu):
    """TM frame received: hook for derived classes"""
    pass
  # ---------------------------------------------------------------------------
  def notifyError(self, errorMessage, data):
    """error notification: hook for derived classes"""
    pass

# =============================================================================
class NCTRStmFields(object):
  """Helper class that contains static initialization attributes"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """Initialise attributes with default values"""
    self.spacecraftId = 0
    self.dataStreamType = 0
    self.virtualChannelId = 0
    self.routeId = 0
    self.sequenceFlag = 0
    self.qualityFlag = 0

# =============================================================================
class TMsender(UTIL.TCP.Server):
  """NCTRS telemetry sender interface - NCTRS side"""
  # ---------------------------------------------------------------------------
  def __init__(self, portNr, nctrsTMfields):
    """Initialise attributes only"""
    modelTask = UTIL.TASK.s_processingTask
    UTIL.TCP.Server.__init__(self, modelTask, portNr)
    self.clientSocket = None
    self.nctrsTMfields = nctrsTMfields
  # ---------------------------------------------------------------------------
  def accepted(self, clientSocket):
    """Overloaded from SingleClientReceivingServer"""
    self.clientSocket = clientSocket
    self.clientAccepted()
  # ---------------------------------------------------------------------------
  def sendTmDataUnit(self, tmDu):
    """Send the TM data unit to the TM receiver"""
    # ensure a correct size attribute
    tmDu.packetSize = len(tmDu)
    # this operation does not verify the contents of the DU
    self.clientSocket.send(tmDu.getBufferString())
  # ---------------------------------------------------------------------------
  def sendFrame(self, tmFrame):
    """Send the TM frame to the TM receiver"""
    actualCCSDStimeDU = UTIL.TIME.getCCSDStimeDU(UTIL.TIME.getActualTime())
    tmDu = GRND.NCTRSDU.TMdataUnit()
    tmDu.setFrame(tmFrame)
    tmDu.spacecraftId = self.nctrsTMfields.spacecraftId
    tmDu.dataStreamType = self.nctrsTMfields.dataStreamType
    tmDu.virtualChannelId = self.nctrsTMfields.virtualChannelId
    tmDu.routeId = self.nctrsTMfields.routeId
    tmDu.earthReceptionTime = actualCCSDStimeDU.getBufferString()
    tmDu.sequenceFlag = self.nctrsTMfields.sequenceFlag
    tmDu.qualityFlag = self.nctrsTMfields.qualityFlag
    self.sendTmDataUnit(tmDu)
  # ---------------------------------------------------------------------------
  def clientAccepted(self):
    """hook for derived classes"""
    pass

# =============================================================================
class TCreceiver(UTIL.TCP.SingleClientReceivingServer):
  """NCTRS telecommand receiver interface - NCTRS side"""
  # ---------------------------------------------------------------------------
  def __init__(self, portNr, groundstationId):
    """Initialise attributes only"""
    modelTask = UTIL.TASK.s_processingTask
    UTIL.TCP.SingleClientReceivingServer.__init__(self, modelTask, portNr)
    self.groundstationId = groundstationId
  # ---------------------------------------------------------------------------
  def accepted(self, clientSocket):
    """Overloaded from SingleClientReceivingServer"""
    UTIL.TCP.SingleClientReceivingServer.accepted(self, clientSocket)
    self.clientAccepted()
  # ---------------------------------------------------------------------------
  def sendTcDataUnit(self, tcDu):
    """Send the TC data unit to the TC sender"""
    # ensure a correct size attribute
    tcDu.packetSize = len(tcDu)
    # this operation does not verify the contents of the DU
    self.dataSocket.send(tcDu.getBufferString())
  # ---------------------------------------------------------------------------
  def receiveCallback(self, socket, stateMask):
    """Callback when the MCS has send data"""
    # read the TC data unit header from the data socket
    try:
      tcDuHeader = self.dataSocket.recv(GRND.NCTRSDU.TC_DU_HEADER_BYTE_SIZE);
    except Exception, ex:
      self.disconnectClient()
      self.notifyConnectionClosed(str(ex))
      return
    # consistency check
    tcDuHeaderLen = len(tcDuHeader)
    if tcDuHeaderLen == 0:
      self.disconnectClient()
      self.notifyConnectionClosed("")
      return
    if tcDuHeaderLen != GRND.NCTRSDU.TC_DU_HEADER_BYTE_SIZE:
      LOG_ERROR("Read of TC DU header failed: invalid size: " + str(tcDuHeaderLen))
      self.disconnectClient()
      self.notifyConnectionClosed("invalid data")
      return
    tcDu = GRND.NCTRSDU.TCdataUnit(tcDuHeader)
    # consistency check
    packetSize = tcDu.packetSize
    remainingSizeExpected = packetSize - GRND.NCTRSDU.TC_DU_HEADER_BYTE_SIZE
    if remainingSizeExpected <= 0:
      LOG_ERROR("Read of TC DU header failed: invalid packet size field: " + str(remainingSizeExpected))
      self.disconnectClient()
      self.notifyConnectionClosed("invalid data")
      return
    # read the remaining bytes for the TC data unit
    # from the data socket
    try:
      tcRemaining = self.dataSocket.recv(remainingSizeExpected);
    except Exception, ex:
      LOG_ERROR("Read of remaining TC DU failed: " + str(ex))
      self.disconnectClient()
      self.notifyConnectionClosed("invalid data")
      return
    # consistency check
    remainingSizeRead = len(tcRemaining)
    if remainingSizeRead != remainingSizeExpected:
      LOG_ERROR("Read of remaining TC DU failed: invalid remaining size: " + str(remainingSizeRead))
      self.disconnectClient()
      self.notifyConnectionClosed("invalid data")
      return
    dataUnitType = tcDu.dataUnitType
    try:
      if dataUnitType == GRND.NCTRSDU.TC_PACKET_HEADER_DU_TYPE:
        # AD packet / BD segment
        tcDu.append(tcRemaining, GRND.NCTRSDU.TC_PACKET_HEADER_ATTRIBUTES)
        self.notifyTCpacketDataUnit(tcDu)
      elif dataUnitType == GRND.NCTRSDU.TC_CLTU_HEADER_DU_TYPE:
        # CLTU
        tcDu.append(tcRemaining, GRND.NCTRSDU.TC_CLTU_HEADER_ATTRIBUTES)
        self.notifyTCcltuDataUnit(tcDu)
      elif dataUnitType == GRND.NCTRSDU.TC_DIRECTIVES_DU_TYPE:
        # COP1 directive
        tcDu.append(tcRemaining, GRND.NCTRSDU.TC_DIRECTIVES_ATTRIBUTES)
        self.notifyTCdirectivesDataUnit(tcDu)
      else:
        LOG_ERROR("Read of TC DU header failed: invalid dataUnitType: " + str(dataUnitType))
        self.disconnectClient()
        self.notifyConnectionClosed("invalid data")
    except Exception, ex:
      LOG_ERROR("Processing of received data unit failed: " + str(ex))
  # ---------------------------------------------------------------------------
  def notifyConnectionClosed(self, details):
    """Connection closed by client"""
    LOG_WARNING("Connection closed by TCclient: " + details)
  # ---------------------------------------------------------------------------
  def notifyTCpacketDataUnit(self, tcPktDu):
    """AD packet / BD segment received"""
    # send UV ACCEPT confirmation
    if GRND.IF.s_configuration.grndAck1 == GRND.IF.ENABLE_ACK:
      LOG_INFO("generate ACK1 (TC_ACK_UV_ACCEPT_CONFIRM)")
      self.sendResponseDataUnit(tcPktDu,
                                GRND.NCTRSDU.TC_ACK_UV_ACCEPT_CONFIRM)
    elif GRND.IF.s_configuration.grndAck1 == GRND.IF.ENABLE_NAK:
      LOG_WARNING("generate NAK1 (TC_ACK_UV_ACCEPT_FAILURE)")
      self.sendResponseDataUnit(tcPktDu,
                                GRND.NCTRSDU.TC_ACK_UV_ACCEPT_FAILURE)
    else:
      LOG_WARNING("suppress ACK1 (TC_ACK_UV_ACCEPT_CONFIRM)")
    # send UV TRANSMIT confirmation
    if GRND.IF.s_configuration.grndAck2 == GRND.IF.ENABLE_ACK:
      LOG_INFO("generate ACK2 (TC_ACK_UV_TRANSMIT_CONFIRM)")
      self.sendResponseDataUnit(tcPktDu,
                                GRND.NCTRSDU.TC_ACK_UV_TRANSMIT_CONFIRM)
    elif GRND.IF.s_configuration.grndAck2 == GRND.IF.ENABLE_NAK:
      LOG_ERROR("generate NAK2 (TC_ACK_UV_TRANSMIT_FAILURE)")
      self.sendResponseDataUnit(tcPktDu,
                                GRND.NCTRSDU.TC_ACK_UV_TRANSMIT_FAILURE)
    else:
      LOG_WARNING("suppress ACK2 (TC_ACK_UV_TRANSMIT_CONFIRM)")
    # send UV TRANSFER confirmation
    # this verification stage does not provide ENABLE/DISABLE
    LOG_INFO("generate ACK3 (TC_ACK_UV_TRANSFER_CONFIRM)")
    self.sendResponseDataUnit(tcPktDu,
                              GRND.NCTRSDU.TC_ACK_UV_TRANSFER_CONFIRM)
    # extract the TC packet from the NCTRS TC packet data unit
    try:
      packetData = tcPktDu.getTCpacket()
    except Exception, ex:
      self.notifyError("TC packet extraction failed", ex)
      return
    self.notifyTCpacket(packetData)
  # ---------------------------------------------------------------------------
  def notifyTCcltuDataUnit(self, tcCltuDu):
    """CLTU received"""
    # send UV ACCEPT confirmation
    if GRND.IF.s_configuration.grndAck1 == GRND.IF.ENABLE_ACK:
      LOG_INFO("generate ACK1 (TC_ACK_UV_ACCEPT_CONFIRM)")
      self.sendResponseDataUnit(tcCltuDu,
                                GRND.NCTRSDU.TC_ACK_UV_ACCEPT_CONFIRM)
    elif GRND.IF.s_configuration.grndAck1 == GRND.IF.ENABLE_NAK:
      LOG_WARNING("generate NAK1 (TC_ACK_UV_ACCEPT_FAILURE)")
      self.sendResponseDataUnit(tcCltuDu,
                                GRND.NCTRSDU.TC_ACK_UV_ACCEPT_FAILURE)
    else:
      LOG_WARNING("suppress ACK1 (TC_ACK_UV_ACCEPT_CONFIRM)")
    # send UV TRANSMIT confirmation
    if GRND.IF.s_configuration.grndAck2 == GRND.IF.ENABLE_ACK:
      LOG_INFO("generate ACK2 (TC_ACK_UV_TRANSMIT_CONFIRM)")
      self.sendResponseDataUnit(tcCltuDu,
                                GRND.NCTRSDU.TC_ACK_UV_TRANSMIT_CONFIRM)
    elif GRND.IF.s_configuration.grndAck2 == GRND.IF.ENABLE_NAK:
      LOG_ERROR("generate NAK2 (TC_ACK_UV_TRANSMIT_FAILURE)")
      self.sendResponseDataUnit(tcCltuDu,
                                GRND.NCTRSDU.TC_ACK_UV_TRANSMIT_FAILURE)
    else:
      LOG_WARNING("suppress ACK2 (TC_ACK_UV_TRANSMIT_CONFIRM)")
    # extract the CLTU from the NCTRS CLTU data unit
    try:
      cltu = tcCltuDu.getCltu()
    except Exception, ex:
      self.notifyError("CLTU extraction failed", ex)
      return
    self.notifyCltu(cltu)
  # ---------------------------------------------------------------------------
  def notifyTCdirectivesDataUnit(self, tcDirDu):
    """COP1 directive received"""
    LOG_ERROR("TCreceiver.notifyTCdirectivesDataUnit not implemented")
    sys.exit(-1)
  # ---------------------------------------------------------------------------
  def clientAccepted(self):
    """hook for derived classes"""
    pass
  # ---------------------------------------------------------------------------
  def notifyError(self, errorMessage, data):
    """error notification: hook for derived classes"""
    pass
  # ---------------------------------------------------------------------------
  def notifyTCpacket(self, packetData):
    """TC packet received: hook for derived classes"""
    pass
  # ---------------------------------------------------------------------------
  def notifyCltu(self, cltu):
    """CLTU received: hook for derived classes"""
    pass
  # ---------------------------------------------------------------------------
  def sendResponseDataUnit(self, requestDataUnit, acknowledgement):
    """sends a response data unit from a request data unit"""
    actualCCSDStimeDU = UTIL.TIME.getCCSDStimeDU(UTIL.TIME.getActualTime())
    tcRespDu = requestDataUnit.createResponseDataUnit()
    tcRespDu.time = actualCCSDStimeDU.getBufferString()
    tcRespDu.serviceType = requestDataUnit.serviceType
    tcRespDu.groundstationId = self.groundstationId
    tcRespDu.sequenceCounter = requestDataUnit.tcId
    tcRespDu.acknowledgement = acknowledgement
    tcRespDu.reason = 0
    tcRespDu.spaceInQueue = 0
    tcRespDu.nextADcounter = 0
    tcRespDu.lastCLCW = [0, 0, 0, 0]
    self.sendTcDataUnit(tcRespDu)

# =============================================================================
class TCsender(UTIL.TCP.SingleServerReceivingClient):
  """NCTRS telecommand sender interface - SCOS side"""
  # connectToServer and disconnectFromServer are inherited
  # and must be handled in a proper way from the application
  # ---------------------------------------------------------------------------
  def __init__(self):
    """Initialise attributes only"""
    modelTask = UTIL.TASK.s_processingTask
    UTIL.TCP.SingleServerReceivingClient.__init__(self, modelTask)
  # ---------------------------------------------------------------------------
  def sendTcDataUnit(self, tcDu):
    """Send the TC data unit to the TC receiver"""
    # ensure a correct size attribute
    tcDu.packetSize = len(tcDu)
    # this operation does not verify the contents of the DU
    self.dataSocket.send(tcDu.getBufferString())
  # ---------------------------------------------------------------------------
  def receiveCallback(self, socket, stateMask):
    """Callback when NCTRS has send data"""
    # read the TC data unit header from the data socket
    try:
      tcDuHeader = self.dataSocket.recv(GRND.NCTRSDU.TC_DU_HEADER_BYTE_SIZE);
    except Exception, ex:
      self.disconnectFromServer()
      self.notifyConnectionClosed(str(ex))
      return
    # consistency check
    tcDuHeaderLen = len(tcDuHeader)
    if tcDuHeaderLen == 0:
      # client termination
      self.disconnectFromServer()
      self.notifyConnectionClosed("")
      return
    if tcDuHeaderLen != GRND.NCTRSDU.TC_DU_HEADER_BYTE_SIZE:
      LOG_ERROR("Read of TC DU header failed: invalid size: " + str(tcDuHeaderLen))
      self.disconnectFromServer()
      self.notifyConnectionClosed("invalid data")
      return
    tcDu = GRND.NCTRSDU.TCdataUnit(tcDuHeader)
    # consistency check
    packetSize = tcDu.packetSize
    remainingSizeExpected = packetSize - GRND.NCTRSDU.TC_DU_HEADER_BYTE_SIZE
    if remainingSizeExpected <= 0:
      LOG_ERROR("Read of TC DU header failed: invalid packet size field: " + str(remainingSizeExpected))
      self.disconnectFromServer()
      self.notifyConnectionClosed("invalid data")
      return
    # read the remaining bytes for the TC data unit
    # from the data socket
    try:
      tcRemaining = self.dataSocket.recv(remainingSizeExpected);
    except Exception, ex:
      LOG_ERROR("Read of remaining TC DU failed: " + str(ex))
      self.disconnectFromServer()
      self.notifyConnectionClosed("invalid data")
      return
    # consistency check
    remainingSizeRead = len(tcRemaining)
    if remainingSizeRead != remainingSizeExpected:
      LOG_ERROR("Read of remaining TC DU failed: invalid remaining size: " + str(remainingSizeRead))
      self.disconnectFromServer()
      self.notifyConnectionClosed("invalid data")
      return
    dataUnitType = tcDu.dataUnitType
    if dataUnitType == GRND.NCTRSDU.TC_PACKET_RESPONSE_DU_TYPE:
      # AD packet / BD segment response
      tcDu.append(tcRemaining, GRND.NCTRSDU.TC_PACKET_RESPONSE_ATTRIBUTES)
      self.notifyTCpacketResponseDataUnit(tcDu)
    elif dataUnitType == GRND.NCTRSDU.TC_CLTU_RESPONSE_DU_TYPE:
      # CLTU response
      tcDu.append(tcRemaining, GRND.NCTRSDU.TC_CLTU_RESPONSE_ATTRIBUTES)
      self.notifyTCcltuResponseDataUnit(tcDu)
    elif dataUnitType == GRND.NCTRSDU.TC_LINK_STATUS_DU_TYPE:
      # Link status
      tcDu.append(tcRemaining, GRND.NCTRSDU.TC_LINK_STATUS_ATTRIBUTES)
      self.notifyTClinkStatusDataUnit(tcDu)
    else:
      LOG_ERROR("Read of TC DU header failed: invalid dataUnitType: " + str(dataUnitType))
      self.disconnectFromServer()
      self.notifyConnectionClosed("invalid data")
  # ---------------------------------------------------------------------------
  def notifyConnectionClosed(self, details):
    """Connection closed by server"""
    LOG_WARNING("Connection closed by TCserver: " + details)
  # ---------------------------------------------------------------------------
  def notifyTCpacketResponseDataUnit(self, tcPktRespDu):
    """AD packet / BD segment response received"""
    LOG_ERROR("TCsender.notifyTCpacketResponseDataUnit not implemented")
    sys.exit(-1)
  # ---------------------------------------------------------------------------
  def notifyTCcltuResponseDataUnit(self, tcCltuRespDu):
    """CLTU response received"""
    LOG_ERROR("TCsender.notifyTCcltuResponseDataUnit not implemented")
    sys.exit(-1)
  # ---------------------------------------------------------------------------
  def notifyTClinkStatusDataUnit(self, tcLinkStatDu):
    """Link status received"""
    LOG_ERROR("TCsender.notifyTClinkStatusDataUnit not implemented")
    sys.exit(-1)

# =============================================================================
class AdminMessageSender(UTIL.TCP.SingleClientReceivingServer):
  """NCTRS admin message sender interface - NCTRS side"""
  # ---------------------------------------------------------------------------
  def __init__(self, portNr, groundstationName):
    """Initialise attributes only"""
    modelTask = UTIL.TASK.s_processingTask
    UTIL.TCP.SingleClientReceivingServer.__init__(self, modelTask, portNr)
    self.groundstationName = groundstationName
  # ---------------------------------------------------------------------------
  def accepted(self, clientSocket):
    """Overloaded from SingleClientReceivingServer"""
    UTIL.TCP.SingleClientReceivingServer.accepted(self, clientSocket)
    self.clientAccepted()
  # ---------------------------------------------------------------------------
  def sendAdminMessageDataUnit(self, messageDu):
    """Send the admin message data unit to the admin message receiver"""
    # ensure a correct size attribute
    messageDu.packetSize = len(messageDu)
    # this operation does not verify the contents of the DU
    self.dataSocket.send(messageDu.getBufferString())
  # ---------------------------------------------------------------------------
  def sendAdminMessageTM(self, eventId):
    """Send the TM admin message data unit"""
    messageDu = GRND.NCTRSDU.AdminMessageDataUnit()
    messageDu.set(GRND.NCTRSDU.ADMIN_MSG_TM, eventId)
    self.sendAdminMessageDataUnit(messageDu)
  # ---------------------------------------------------------------------------
  def sendAdminMessageTC(self, eventId, adCounter=0, vcId=0, mapId=0):
    """Send the TC admin message data unit"""
    messageDu = GRND.NCTRSDU.AdminMessageDataUnit()
    messageDu.set(GRND.NCTRSDU.ADMIN_MSG_TC,
                  eventId,
                  groundstationName=self.groundstationName,
                  adCounter=adCounter,
                  vcId=vcId,
                  mapId=mapId)
    self.sendAdminMessageDataUnit(messageDu)
  # ---------------------------------------------------------------------------
  def receiveCallback(self, socket, stateMask):
    """Callback when the MCS has send data"""
    LOG_ERROR("Admin message receiver has send data (unexpected)")
    self.disconnectClient()
    self.notifyConnectionClosed("-")
  # ---------------------------------------------------------------------------
  def notifyConnectionClosed(self, details):
    """Connection closed by client"""
    LOG_WARNING("Connection closed by admin message client: " + details)
  # ---------------------------------------------------------------------------
  def clientAccepted(self):
    """hook for derived classes"""
    pass
  # ---------------------------------------------------------------------------
  def notifyError(self, errorMessage, data):
    """error notification: hook for derived classes"""
    pass

# =============================================================================
class AdminMessageReceiver(UTIL.TCP.SingleServerReceivingClient):
  """NCTRS admin message receiver interface - SCOS side"""
  # connectToServer and disconnectFromServer are inherited
  # and must be handled in a proper way from the application
  # ---------------------------------------------------------------------------
  def __init__(self):
    """Initialise attributes only"""
    modelTask = UTIL.TASK.s_processingTask
    UTIL.TCP.SingleServerReceivingClient.__init__(self, modelTask)
  # ---------------------------------------------------------------------------
  def receiveCallback(self, socket, stateMask):
    """Callback when NCTRS has send data"""
    # read the admin message unit header from the data socket
    try:
      messageHeader = self.dataSocket.recv(GRND.NCTRSDU.MESSAGE_HEADER_BYTE_SIZE);
    except Exception, ex:
      self.disconnectFromServer()
      self.notifyConnectionClosed(str(ex))
      return
    # consistency check
    messageHeaderLen = len(messageHeader)
    if messageHeaderLen == 0:
      # client termination
      self.disconnectFromServer()
      self.notifyConnectionClosed("")
      return
    if messageHeaderLen != GRND.NCTRSDU.MESSAGE_HEADER_BYTE_SIZE:
      LOG_ERROR("Read of admin message DU header failed: invalid size: " + str(messageHeaderLen))
      self.disconnectFromServer()
      self.notifyConnectionClosed("invalid data")
      return
    messageDu = GRND.NCTRSDU.AdminMessageDataUnit(messageHeader)
    # consistency check
    packetSize = messageDu.packetSize
    remainingSizeExpected = packetSize - GRND.NCTRSDU.MESSAGE_HEADER_BYTE_SIZE
    if remainingSizeExpected <= 0:
      LOG_ERROR("Read of admin message DU header failed: invalid packet size field: " + str(remainingSizeExpected))
      self.disconnectFromServer()
      self.notifyConnectionClosed("invalid data")
      return
    # read the remaining bytes for the TC data unit
    # from the data socket
    try:
      messageRemaining = self.dataSocket.recv(remainingSizeExpected);
    except Exception, ex:
      LOG_ERROR("Read of remaining admin message DU failed: " + str(ex))
      self.disconnectFromServer()
      self.notifyConnectionClosed("invalid data")
      return
    # consistency check
    remainingSizeRead = len(messageRemaining)
    if remainingSizeRead != remainingSizeExpected:
      LOG_ERROR("Read of remaining admin message DU failed: invalid remaining size: " + str(remainingSizeRead))
      self.disconnectFromServer()
      self.notifyConnectionClosed("invalid data")
      return
    # set the message
    messageDu.setMessage(messageRemaining)
    self.notifyAdminMessageDataUnit(messageDu)
  # ---------------------------------------------------------------------------
  def notifyConnectionClosed(self, details):
    """Connection closed by server"""
    LOG_WARNING("Connection closed by TCserver: " + details)
  # ---------------------------------------------------------------------------
  def notifyAdminMessageDataUnit(self, messageDu):
    """Admin message response received"""
    LOG_ERROR("AdminMessageReceiver.messageDu not implemented")
    sys.exit(-1)
