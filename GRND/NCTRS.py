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
# Ground Simulation - NCTRS Module                                            *
# implements EGOS-NIS-NCTR-ICD-0002-i4r0.2 (Signed).pdf                       *
#******************************************************************************
import socket, sys
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import GRND.IF, GRND.NCTRSDU
import UTIL.SYS, UTIL.TASK, UTIL.TCO, UTIL.TCP, UTIL.TIME

#############
# constants #
#############
SOCKET_TYPE = type(socket.socket())

####################
# global variables #
####################
s_tmDUtype = None

###########
# classes #
###########
# =============================================================================
class TMreceiver(UTIL.TCP.Client):
  """NCTRS telemetry receiver interface - MCS side"""
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
    LOG_ERROR("TMreceiver.recvError: " + errorMessage, "NCTRS")
    # default implementation: disconnect from server
    self.disconnectFromServer()
  # ---------------------------------------------------------------------------
  def sendError(self, errorMessage):
    """
    Send bytes from the data socket has failed,
    overloaded from UTIL.TCP.Client
    """
    LOG_ERROR("TMreceiver.sendError: " + errorMessage, "NCTRS")
    # default implementation: disconnect from server
    self.disconnectFromServer()
  # ---------------------------------------------------------------------------
  def receiveCallback(self, socket, stateMask):
    """Callback when NCTRS has send data"""
    # read the TM data unit
    try:
      # note: automatic failure handling of derived method
      #       UTIL.TCP.Client.recvError() cannot be used here,
      #       because the derived method UTIL.TCP.Client.recv()
      #       cannot be used by readNCTRSframe()
      tmDu = readNCTRSframe(self.dataSocket)
    except Exception as ex:
      # explicit failure handling
      self.recvError(str(ex))
      return
    self.notifyTMdataUnit(tmDu)
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
class TMsender(UTIL.TCP.SingleClientServer):
  """NCTRS telemetry sender interface - NCTRS side"""
  # ---------------------------------------------------------------------------
  def __init__(self, portNr, nctrsTMfields):
    """Initialise attributes only"""
    modelTask = UTIL.TASK.s_processingTask
    UTIL.TCP.SingleClientServer.__init__(self, modelTask, portNr)
    self.nctrsTMfields = nctrsTMfields
  # ---------------------------------------------------------------------------
  def sendTmDataUnit(self, tmDu):
    """Send the TM data unit to the TM receiver"""
    # ensure a correct size attribute
    tmDu.packetSize = len(tmDu)
    # this operation does not verify the contents of the DU
    self.send(tmDu.getBuffer())
  # ---------------------------------------------------------------------------
  def sendFrame(self, tmFrame):
    """Send the TM frame to the TM receiver"""
    ertTime = UTIL.TCO.correlateToERTmissionEpoch(UTIL.TIME.getActualTime())
    tmDu = createTMdataUnit()
    tmDu.setFrame(tmFrame)
    tmDu.spacecraftId = self.nctrsTMfields.spacecraftId
    tmDu.dataStreamType = self.nctrsTMfields.dataStreamType
    tmDu.virtualChannelId = self.nctrsTMfields.virtualChannelId
    tmDu.routeId = self.nctrsTMfields.routeId
    tmDu.earthReceptionTime = ertTime
    tmDu.sequenceFlag = self.nctrsTMfields.sequenceFlag
    tmDu.qualityFlag = self.nctrsTMfields.qualityFlag
    self.sendTmDataUnit(tmDu)
  # ---------------------------------------------------------------------------
  def receiveCallback(self, socket, stateMask):
    """Callback when the MCS has closed the connection"""
    # preform a dummy recv to force connection handling
    self.recv(1)

# =============================================================================
class TCreceiver(UTIL.TCP.SingleClientServer):
  """NCTRS telecommand receiver interface - NCTRS side"""
  # ---------------------------------------------------------------------------
  def __init__(self, portNr, groundstationId):
    """Initialise attributes only"""
    modelTask = UTIL.TASK.s_processingTask
    UTIL.TCP.SingleClientServer.__init__(self, modelTask, portNr)
    self.groundstationId = groundstationId
  # ---------------------------------------------------------------------------
  def sendTcDataUnit(self, tcDu):
    """Send the TC data unit to the TC sender"""
    # ensure a correct size attribute
    tcDu.packetSize = len(tcDu)
    # this operation does not verify the contents of the DU
    self.send(tcDu.getBuffer())
  # ---------------------------------------------------------------------------
  def receiveCallback(self, socket, stateMask):
    """Callback when the MCS has send data"""
    # read the TC data unit header
    tcDuHeader = self.recv(GRND.NCTRSDU.TC_DU_HEADER_BYTE_SIZE)
    if tcDuHeader == None:
      # failure handling was done automatically by derived logic
      return
    # consistency check
    tcDuHeaderLen = len(tcDuHeader)
    if tcDuHeaderLen != GRND.NCTRSDU.TC_DU_HEADER_BYTE_SIZE:
      LOG_ERROR("Read of TC DU header failed: invalid size: " + str(tcDuHeaderLen))
      self.disconnectClient()
      return
    tcDu = GRND.NCTRSDU.TCdataUnit(tcDuHeader)
    # consistency check
    packetSize = tcDu.packetSize
    remainingSizeExpected = packetSize - GRND.NCTRSDU.TC_DU_HEADER_BYTE_SIZE
    if remainingSizeExpected <= 0:
      LOG_ERROR("Read of TC DU header failed: invalid packet size field: " + str(remainingSizeExpected))
      self.disconnectClient()
      return
    # read the remaining bytes for the TC data unit
    tcRemaining = self.recv(remainingSizeExpected)
    if tcRemaining == None:
      # failure handling was done automatically by derived logic
      return
    # consistency check
    remainingSizeRead = len(tcRemaining)
    if remainingSizeRead != remainingSizeExpected:
      LOG_ERROR("Read of remaining TC DU failed: invalid remaining size: " + str(remainingSizeRead))
      self.disconnectClient()
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
    except Exception as ex:
      LOG_ERROR("Processing of received data unit failed: " + str(ex))
      self.disconnectClient()
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
    except Exception as ex:
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
    except Exception as ex:
      self.notifyError("CLTU extraction failed", ex)
      return
    self.notifyCltu(cltu)
  # ---------------------------------------------------------------------------
  def notifyTCdirectivesDataUnit(self, tcDirDu):
    """COP1 directive received"""
    LOG_ERROR("TCreceiver.notifyTCdirectivesDataUnit not implemented")
    sys.exit(-1)
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
    ertTime = UTIL.TCO.correlateToERTmissionEpoch(UTIL.TIME.getActualTime())
    tcRespDu = requestDataUnit.createResponseDataUnit()
    tcRespDu.time = ertTime
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
class TCsender(UTIL.TCP.Client):
  """NCTRS telecommand sender interface - SCOS side"""
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
    LOG_ERROR("TCsender.recvError: " + errorMessage, "NCTRS")
    # default implementation: disconnect from server
    self.disconnectFromServer()
  # ---------------------------------------------------------------------------
  def sendError(self, errorMessage):
    """
    Send bytes from the data socket has failed,
    overloaded from UTIL.TCP.Client
    """
    LOG_ERROR("TCsender.sendError: " + errorMessage, "NCTRS")
    # default implementation: disconnect from server
    self.disconnectFromServer()
  # ---------------------------------------------------------------------------
  def sendTcDataUnit(self, tcDu):
    """Send the TC data unit to the TC receiver"""
    # ensure a correct size attribute
    tcDu.packetSize = len(tcDu)
    # this operation does not verify the contents of the DU
    self.send(tcDu.getBuffer())
  # ---------------------------------------------------------------------------
  def sendTCpacket(self, packetData):
    """Send the TC packet to the TC receiver"""
    packetDu = GRND.NCTRSDU.TCpacketDataUnit()
    packetDu.setTCpacket(packetData)
    self.sendTcDataUnit(packetDu)
  # ---------------------------------------------------------------------------
  def sendCltu(self, cltu):
    """Send the CLTU to the TC receiver"""
    cltuDu = GRND.NCTRSDU.TCcltuDataUnit()
    cltuDu.setCltu(cltu)
    self.sendTcDataUnit(cltuDu)
  # ---------------------------------------------------------------------------
  def receiveCallback(self, socket, stateMask):
    """Callback when NCTRS has send data"""
    # read the TC data unit header
    tcDuHeader = self.recv(GRND.NCTRSDU.TC_DU_HEADER_BYTE_SIZE)
    if tcDuHeader == None:
      # failure handling was done automatically by derived logic
      return
    # consistency check
    tcDuHeaderLen = len(tcDuHeader)
    if tcDuHeaderLen != GRND.NCTRSDU.TC_DU_HEADER_BYTE_SIZE:
      LOG_ERROR("Read of TC DU header failed: invalid size: " + str(tcDuHeaderLen), "NCTRS")
      self.disconnectFromServer()
      return
    tcDu = GRND.NCTRSDU.TCdataUnit(tcDuHeader)
    # consistency check
    packetSize = tcDu.packetSize
    remainingSizeExpected = packetSize - GRND.NCTRSDU.TC_DU_HEADER_BYTE_SIZE
    if remainingSizeExpected <= 0:
      LOG_ERROR("Read of TC DU header failed: invalid packet size field: " + str(remainingSizeExpected), "NCTRS")
      self.disconnectFromServer()
      return
    # read the remaining bytes for the TC data unit
    tcRemaining = self.recv(remainingSizeExpected)
    if tcRemaining == None:
      # failure handling was done automatically by derived logic
      return
    # consistency check
    remainingSizeRead = len(tcRemaining)
    if remainingSizeRead != remainingSizeExpected:
      LOG_ERROR("Read of remaining TC DU failed: invalid remaining size: " + str(remainingSizeRead), "NCTRS")
      self.disconnectFromServer()
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
      LOG_ERROR("Read of TC DU header failed: invalid dataUnitType: " + str(dataUnitType), "NCTRS")
      self.disconnectFromServer()
  # ---------------------------------------------------------------------------
  def notifyTCpacketResponseDataUnit(self, tcPktRespDu):
    """AD packet / BD segment response received"""
    LOG_ERROR("TCsender.notifyTCpacketResponseDataUnit not implemented", "NCTRS")
    sys.exit(-1)
  # ---------------------------------------------------------------------------
  def notifyTCcltuResponseDataUnit(self, tcCltuRespDu):
    """CLTU response received"""
    LOG_ERROR("TCsender.notifyTCcltuResponseDataUnit not implemented", "NCTRS")
    sys.exit(-1)
  # ---------------------------------------------------------------------------
  def notifyTClinkStatusDataUnit(self, tcLinkStatDu):
    """Link status received"""
    LOG_ERROR("TCsender.notifyTClinkStatusDataUnit not implemented", "NCTRS")
    sys.exit(-1)

# =============================================================================
class AdminMessageSender(UTIL.TCP.SingleClientServer):
  """NCTRS admin message sender interface - NCTRS side"""
  # ---------------------------------------------------------------------------
  def __init__(self, portNr, groundstationName):
    """Initialise attributes only"""
    modelTask = UTIL.TASK.s_processingTask
    UTIL.TCP.SingleClientServer.__init__(self, modelTask, portNr)
    self.groundstationName = groundstationName
  # ---------------------------------------------------------------------------
  def sendAdminMessageDataUnit(self, messageDu):
    """Send the admin message data unit to the admin message receiver"""
    # ensure a correct size attribute
    messageDu.packetSize = len(messageDu)
    # this operation does not verify the contents of the DU
    self.send(messageDu.getBuffer())
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
    # preform a dummy recv to force connection handling
    self.recv(1)
  # ---------------------------------------------------------------------------
  def notifyError(self, errorMessage, data):
    """error notification: hook for derived classes"""
    pass

# =============================================================================
class AdminMessageReceiver(UTIL.TCP.Client):
  """NCTRS admin message receiver interface - MCS side"""
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
    LOG_ERROR("AdminMessageReceiver.recvError: " + errorMessage, "NCTRS")
    # default implementation: disconnect from server
    self.disconnectFromServer()
  # ---------------------------------------------------------------------------
  def sendError(self, errorMessage):
    """
    Send bytes from the data socket has failed,
    overloaded from UTIL.TCP.Client
    """
    LOG_ERROR("AdminMessageReceiver.sendError: " + errorMessage, "NCTRS")
    # default implementation: disconnect from server
    self.disconnectFromServer()
  # ---------------------------------------------------------------------------
  def receiveCallback(self, socket, stateMask):
    """Callback when NCTRS has send data"""
    # read the admin message unit header
    messageHeader = self.recv(GRND.NCTRSDU.MESSAGE_HEADER_BYTE_SIZE)
    if messageHeader == None:
      # failure handling was done automatically by derived logic
      return
    # consistency check
    messageHeaderLen = len(messageHeader)
    if messageHeaderLen != GRND.NCTRSDU.MESSAGE_HEADER_BYTE_SIZE:
      LOG_ERROR("Read of admin message DU header failed: invalid size: " + str(messageHeaderLen), "NCTRS")
      self.disconnectFromServer()
      return
    messageDu = GRND.NCTRSDU.AdminMessageDataUnit(messageHeader)
    # consistency check
    packetSize = messageDu.packetSize
    remainingSizeExpected = packetSize - GRND.NCTRSDU.MESSAGE_HEADER_BYTE_SIZE
    if remainingSizeExpected <= 0:
      LOG_ERROR("Read of admin message DU header failed: invalid packet size field: " + str(remainingSizeExpected), "NCTRS")
      self.disconnectFromServer()
      return
    # read the remaining bytes for the TC data unit
    messageRemaining = self.recv(remainingSizeExpected)
    if messageRemaining == None:
      # failure handling was done automatically by derived logic
      return
    # consistency check
    remainingSizeRead = len(messageRemaining)
    if remainingSizeRead != remainingSizeExpected:
      LOG_ERROR("Read of remaining admin message DU failed: invalid remaining size: " + str(remainingSizeRead), "NCTRS")
      self.disconnectFromServer()
      return
    # set the message
    messageDu.setMessage(messageRemaining)
    self.notifyAdminMessageDataUnit(messageDu)
  # ---------------------------------------------------------------------------
  def notifyAdminMessageDataUnit(self, messageDu):
    """Admin message response received"""
    LOG_ERROR("AdminMessageReceiver.messageDu not implemented", "NCTRS")
    sys.exit(-1)

#############
# functions #
#############
# -----------------------------------------------------------------------------
def getTMdataUnitType():
  """returns the NCTRS TM data unit type according to NCTRS_TM_DU_VERSION"""
  global s_tmDUtype
  if s_tmDUtype == None:
    nctrsTMversion = UTIL.SYS.s_configuration.NCTRS_TM_DU_VERSION
    if nctrsTMversion == "V0":
      s_tmDUtype = GRND.NCTRSDU.TM_V0_ERT_FORMAT
    elif nctrsTMversion == "V1_CDS1":
      s_tmDUtype = GRND.NCTRSDU.TM_V1_CDS1_ERT_FORMAT
    elif nctrsTMversion == "V1_CDS2":
      s_tmDUtype = GRND.NCTRSDU.TM_V1_CDS2_ERT_FORMAT
    elif nctrsTMversion == "V1_CDS3":
      s_tmDUtype = GRND.NCTRSDU.TM_V1_CDS3_ERT_FORMAT
    else:
      LOG_ERROR("Invalid NCTRS_TM_DU_VERSION " + nctrsTMversion, "NCTRS")
      sys.exit(-1)
  return s_tmDUtype
# -----------------------------------------------------------------------------
def createTMdataUnit(binaryString=None):
  """creates a NCTRS TM data unit according to the NCTRS_TM_DU_VERSION"""
  tmDUtype = getTMdataUnitType()
  if s_tmDUtype == GRND.NCTRSDU.TM_V0_ERT_FORMAT:
    return GRND.NCTRSDU.TMdataUnitV0(binaryString)
  elif s_tmDUtype == GRND.NCTRSDU.TM_V1_CDS1_ERT_FORMAT:
    return GRND.NCTRSDU.TMdataUnitV1CDS1(binaryString)
  elif s_tmDUtype == GRND.NCTRSDU.TM_V1_CDS2_ERT_FORMAT:
    return GRND.NCTRSDU.TMdataUnitV1CDS2(binaryString)
  elif s_tmDUtype == GRND.NCTRSDU.TM_V1_CDS3_ERT_FORMAT:
    return GRND.NCTRSDU.TMdataUnitV1CDS3(binaryString)
  LOG_ERROR("Invalid s_tmDUtype " + str(s_tmDUtype), "NCTRS")
  sys.exit(-1)
# -----------------------------------------------------------------------------
def readNCTRStmFrameHeader(fd):
  """creates a NCTRS TM data unit according to the NCTRS_TM_DU_VERSION"""
  # the function raises an exception when the read fails
  tmDUtype = getTMdataUnitType()
  if s_tmDUtype == GRND.NCTRSDU.TM_V0_ERT_FORMAT:
    tmDuHeaderByteSize =  GRND.NCTRSDU.TM_DU_V0_HEADER_BYTE_SIZE
  elif s_tmDUtype == GRND.NCTRSDU.TM_V1_CDS1_ERT_FORMAT:
    tmDuHeaderByteSize =  GRND.NCTRSDU.TM_DU_V1_CDS1_HEADER_BYTE_SIZE
  elif s_tmDUtype == GRND.NCTRSDU.TM_V1_CDS2_ERT_FORMAT:
    tmDuHeaderByteSize =  GRND.NCTRSDU.TM_DU_V1_CDS2_HEADER_BYTE_SIZE
  elif s_tmDUtype == GRND.NCTRSDU.TM_V1_CDS3_ERT_FORMAT:
    tmDuHeaderByteSize =  GRND.NCTRSDU.TM_DU_V1_CDS3_HEADER_BYTE_SIZE
  else:
    raise Error("Invalid s_tmDUtype " + str(s_tmDUtype))
  # read the TM data unit header
  if type(fd) == SOCKET_TYPE:
    tmDuHeader = fd.recv(tmDuHeaderByteSize)
  else:
    tmDuHeader = fd.read(tmDuHeaderByteSize)
  # consistency check
  tmDuHeaderLen = len(tmDuHeader)
  if tmDuHeaderLen == 0:
    if type(fd) == SOCKET_TYPE:
      raise Error("empty data read")
    else:
      # end of file
      raise Error("")
  if tmDuHeaderLen != tmDuHeaderByteSize:
    raise Error("Read of TM DU header failed: invalid size: " + str(tmDuHeaderLen))
  return tmDuHeader
# -----------------------------------------------------------------------------
def readNCTRSframe(fd):
  """reads one NCTRS frame from fd, raise execption when there is an error"""
  # read the TM data unit header
  try:
    tmDuHeader = readNCTRStmFrameHeader(fd)
  except Exception as ex:
    raise Error(str(ex))
  tmDu = createTMdataUnit(tmDuHeader)
  # consistency check
  packetSize = tmDu.packetSize
  remainingSizeExpected = packetSize - len(tmDuHeader)
  if remainingSizeExpected <= 0:
    raise Error("Read of TM DU header failed: invalid packet size field: " + str(remainingSizeExpected))
  # read the remaining bytes for the TM data unit
  try:
    if type(fd) == SOCKET_TYPE:
      tmRemaining = fd.recv(remainingSizeExpected)
    else:
      tmRemaining = fd.read(remainingSizeExpected)
  except Exception as ex:
    raise Error("Read of remaining TM DU failed: " + str(ex))
  # consistency check
  remainingSizeRead = len(tmRemaining)
  if remainingSizeRead != remainingSizeExpected:
    raise Error("Read of remaining TM DU failed: invalid remaining size: " + str(remainingSizeRead))
  # TM frame
  tmDu.append(tmRemaining)
  return tmDu
