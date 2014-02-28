#******************************************************************************
# (C) 2014, Stefan Korner, Austria                                            *
#                                                                             *
# The Space Python Library is free software; you can redistribute it and/or   *
# modify it under the terms of the GNU Lesser General Public License as       *
# published by the Free Software Foundation; either version 2.1 of the        *
# License, or (at your option) any later version.                             *
#                                                                             *
# The Space C++ Library is distributed in the hope that it will be useful,    *
# but WITHOUT ANY WARRANTY; without even the implied warranty of              *
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser     *
# General Public License for more details.                                    *
#******************************************************************************
# Ground Simulation - NCTRS Data Units Module                                 *
#******************************************************************************
from UTIL.DU import BITS, BYTES, UNSIGNED, BinaryUnit

#############
# constants #
#############
# =============================================================================
# the attribute dictionaries contain for each data unit attribute:
# - key: attribute name
# - value: fieldOffset, fieldLength, fieldType
# -----------------------------------------------------------------------------
TM_DU_HEADER_BYTE_SIZE = 20
TM_DU_ATTRIBUTES = {
  "packetSize":           ( 0, 4, UNSIGNED),
  "spacecraftId":         ( 4, 2, UNSIGNED),
  "dataStreamType":       ( 6, 1, UNSIGNED),
  "virtualChannelId":     ( 7, 1, UNSIGNED),
  "routeId":              ( 8, 2, UNSIGNED),
  "earthReceptionTime":   (10, 8, BYTES),
  "sequenceFlag":         (18, 1, UNSIGNED),
  "qualityFlag":          (19, 1, UNSIGNED)}
# -----------------------------------------------------------------------------
TC_DU_HEADER_BYTE_SIZE = 8
TC_DU_HEADER_ATTRIBUTES = {
  "packetSize":           ( 0, 4, UNSIGNED),
  "dataUnitType":         ( 4, 2, UNSIGNED),
  "spacecraftId":         ( 6, 2, UNSIGNED)}
# -----------------------------------------------------------------------------
TC_PACKET_HEADER_DU_TYPE = 0
TC_PACKET_HEADER_BYTE_SIZE = 7
TC_PACKET_HEADER_ATTRIBUTES = {
  "serviceType":          ( 0, 1, UNSIGNED),
  "tcId":                 ( 1, 4, UNSIGNED),
  "virtualChannelId":     ( 5, 1, UNSIGNED),
  "mapId":                ( 6, 1, UNSIGNED)}
# -----------------------------------------------------------------------------
TC_CLTU_HEADER_DU_TYPE = 7
TC_CLTU_HEADER_BYTE_SIZE = 39
TC_CLTU_HEADER_ATTRIBUTES = {
  "serviceType":          ( 0, 1, UNSIGNED),
  "tcId":                 ( 1, 4, UNSIGNED),
  "virtualChannelId":     ( 5, 1, UNSIGNED),
  "mapId":                ( 6, 1, UNSIGNED),
  "aggregationFlag":      ( 7, 4, UNSIGNED),
  "earliestProdTimeFlag": (11, 4, UNSIGNED),
  "earliestProdTime":     (15, 8, BYTES),
  "latestProdTimeFlag":   (23, 4, UNSIGNED),
  "latestProdTime":       (27, 8, BYTES),
  "delay":                (35, 4, UNSIGNED)}
# -----------------------------------------------------------------------------
TC_DIRECTIVES_DU_TYPE = 4
TC_DIRECTIVES_BYTE_SIZE = 10
TC_DIRECTIVES_ATTRIBUTES = {
  "directiveType":        ( 0, 1, UNSIGNED),
  "directiveId":          ( 1, 4, UNSIGNED),
  "virtualChannelId":     ( 5, 1, UNSIGNED),
  "parameter":            ( 6, 4, UNSIGNED)}
# -----------------------------------------------------------------------------
TC_PACKET_RESPONSE_DU_TYPE = 1
TC_PACKET_RESPONSE_BYTE_SIZE = 26
TC_PACKET_RESPONSE_ATTRIBUTES = {
  "time":                 ( 0, 8, BYTES),
  "serviceType":          ( 8, 1, UNSIGNED),
  "groundstationId":      ( 9, 2, UNSIGNED),
  "sequenceCounter":      (11, 4, UNSIGNED),
  "acknowledgement":      (15, 1, UNSIGNED),
  "reason":               (16, 1, UNSIGNED),
  "spaceInQueue":         (17, 1, UNSIGNED),
  "nextADcounter":        (18, 4, UNSIGNED),
  "lastCLCW":             (22, 4, BYTES)}
# -----------------------------------------------------------------------------
TC_CLTU_RESPONSE_DU_TYPE = 8
TC_CLTU_RESPONSE_BYTE_SIZE = 26
TC_CLTU_RESPONSE_ATTRIBUTES = {
  "time":                 ( 0, 8, BYTES),
  "serviceType":          ( 8, 1, UNSIGNED),
  "groundstationId":      ( 9, 2, UNSIGNED),
  "sequenceCounter":      (11, 4, UNSIGNED),
  "acknowledgement":      (15, 1, UNSIGNED),
  "reason":               (16, 1, UNSIGNED),
  "spaceInQueue":         (17, 1, UNSIGNED),
  "nextADcounter":        (18, 4, UNSIGNED),
  "lastCLCW":             (22, 4, BYTES)}
# -----------------------------------------------------------------------------
TC_LINK_STATUS_DU_TYPE = 3
TC_LINK_STATUS_BYTE_SIZE = 26
TC_LINK_STATUS_ATTRIBUTES = {
  "connectionStatus":     ( 0, 1, UNSIGNED),
  "groundstationName":    ( 1, 7, BYTES)}
# -----------------------------------------------------------------------------
MESSAGE_HEADER_BYTE_SIZE = 20
MESSAGE_HEADER_ATTRIBUTES = {
  "packetSize":           ( 0, 4, UNSIGNED),
  "time":                 ( 4, 8, BYTES),
  "messageType":          (12, 2, UNSIGNED),
  "severity":             (14, 2, UNSIGNED),
  "eventId":              (16, 4, UNSIGNED)}

# =============================================================================
# constant values of attributes:
# -----------------------------------------------------------------------------
# possible values for
# - TCpacketResponseDataUnit.acknowledgement
# - TCcltuResponseDataUnit.acknowledgement
TC_ACK_UV_ACCEPT_CONFIRM =   0
TC_ACK_UV_ACCEPT_FAILURE =   3
TC_ACK_UV_TRANSMIT_CONFIRM = 1
TC_ACK_UV_TRANSMIT_FAILURE = 4
TC_ACK_UV_TRANSFER_CONFIRM = 2
TC_ACK_UV_TRANSFER_FAILURE = 5
# -----------------------------------------------------------------------------
# possible values for
# - AdminMessageDataUnit.messageType
ADMIN_MSG_TM = 0
ADMIN_MSG_TC = 1
# - AdminMessageDataUnit.severity
ADMIN_MSG_INFO =  0
ADMIN_MSG_WARN =  1
ADMIN_MSG_ALARM = 2
# - AdminMessageDataUnit.eventId
ADMIN_MSG_TM_LINK_FLOW =                      1
ADMIN_MSG_TM_LINK_NOFLOW =                    2
ADMIN_MSG_TC_LINK_ESTABLISHED_TO_GS =         1
ADMIN_MSG_TC_LINK_CLOSED_TO_GS =              3
ADMIN_MSG_TC_LINK_ABORTED_TO_GS =             4
ADMIN_MSG_TC_LINK_ABORTED_FROM_GS =           5
ADMIN_MSG_TC_AD_SERVICE_AVAILABLE_FROM_GS =   6
ADMIN_MSG_TC_AD_SERVICE_FAILE_IN_GS =         7
ADMIN_MSG_TC_AD_SERVICE_TERMINATED_IN_GS =    9
ADMIN_MSG_TC_AD_SERVICE_WILL_TERM_IN_GS_BD = 13
ADMIN_MSG_TC_AD_SERVICE_WILL_TERM_IN_GS =    14
ADMIN_MSG_TC_ALL_SERVICES_WILL_TERM_IN_GS =  15
# -----------------------------------------------------------------------------
# format strings for
# - AdminMessageDataUnit.messageType parameters
TM_PAR_CHANNEL =               "%9s"
TM_PAR_DATA_TYPE =             "%4s"
TM_PAR_GS_EQUIPMENT_NAME =     "%8s"
TM_PAR_CONNECTION_REASON =    "%25s"
TM_PAR_STATUS =               "%10s"
TM_PAR_END_OF_DATA_REASON =   "%18s"
TC_PAR_COUNTER =              "%10s"
TC_PAR_REJECT_REASON =        "%13s"
TC_PAR_SERVICE =              "%12s"
TC_PAR_CMD_CONDITION_NOT_OK = "%14s"
TC_PAR_CMD_CONDITION_OK =     "%14s"
TC_PAR_GS_EQUIPMENT_NAME =     "%8s"
TC_PAR_AS_STOP_REASON =       "%15s"
TC_PAR_MAPID =                 "%2s"
TC_PAR_VCID =                  "%2s"
TC_PAR_SEGMENT_STATUS =        "%1s"
TC_PAR_CONNECTION_REASON =    "%17s"
TC_PAR_TCE_CODE =              "%3s"
TC_PAR_AD_FAILURE_REASON =    "%18s"

###########
# classes #
###########
# =============================================================================
class TMdataUnit(BinaryUnit):
  """NCTRS telemetry data unit"""
  # ---------------------------------------------------------------------------
  def __init__(self, binaryString=None):
    """default constructor: initialise with header size"""
    # note: correct packetSize is not forced!
    emptyData = (binaryString == None)
    if emptyData:
      binaryString = "\0" * TM_DU_HEADER_BYTE_SIZE
    BinaryUnit.__init__(self,
                        binaryString,
                        TM_DU_HEADER_BYTE_SIZE,
                        TM_DU_ATTRIBUTES)
  # ---------------------------------------------------------------------------
  def getFrame(self):
    """returns the CLTU"""
    # the packetSize must contain the correct size
    headerByteSize = TM_DU_HEADER_BYTE_SIZE
    return self.getBytes(headerByteSize, self.packetSize - headerByteSize)
  # ---------------------------------------------------------------------------
  def setFrame(self, frame):
    """set the CLTU and the packetSize"""
    self.setLen(TM_DU_HEADER_BYTE_SIZE)
    self.append(frame)
    self.packetSize = len(self)

# =============================================================================
class TCdataUnit(BinaryUnit):
  """NCTRS telecommand data unit"""
  # ---------------------------------------------------------------------------
  def __init__(self, binaryString=None):
    """default constructor: initialise with header size"""
    # note: correct packetSize is not forced!
    emptyData = (binaryString == None)
    if emptyData:
      binaryString = "\0" * TC_DU_HEADER_BYTE_SIZE
    BinaryUnit.__init__(self,
                        binaryString,
                        TC_DU_HEADER_BYTE_SIZE,
                        TC_DU_HEADER_ATTRIBUTES)
  # ---------------------------------------------------------------------------
  def createResponseDataUnit(self):
    """creates a corresponding ResponseDataUnit"""
    if self.dataUnitType == TC_PACKET_HEADER_DU_TYPE:
      retVal = TCpacketResponseDataUnit()
    elif self.dataUnitType == TC_CLTU_HEADER_DU_TYPE:
      retVal = TCcltuResponseDataUnit()
    else:
      raise AttributeError("createResponseDataUnit() only possible for TCpacketDataUnit or TCcltuDataUnit")
    # common attributes for TC PACKET and TC CLTU response
    retVal.spacecraftId = self.spacecraftId
    return retVal
  # ---------------------------------------------------------------------------
  def getTCpacket(self):
    """returns the TC packet"""
    if self.dataUnitType != TC_PACKET_HEADER_DU_TYPE:
      raise AttributeError("getTCpacket() only possible for TCpacketDataUnit")
    # the packetSize must contain the correct size
    headerByteSize = TC_DU_HEADER_BYTE_SIZE + TC_PACKET_HEADER_BYTE_SIZE
    return self.getBytes(headerByteSize, self.packetSize - headerByteSize)
  # ---------------------------------------------------------------------------
  def setTCpacket(self, packetData):
    """set the TC packet and the packetSize"""
    if self.dataUnitType != TC_PACKET_HEADER_DU_TYPE:
      raise AttributeError("setTCpacket() only possible for TCpacketDataUnit")
    self.setLen(TC_DU_HEADER_BYTE_SIZE + TC_PACKET_HEADER_BYTE_SIZE)
    self.append(packetData)
    self.packetSize = len(self)
  # ---------------------------------------------------------------------------
  def getCltu(self):
    """returns the CLTU"""
    if self.dataUnitType != TC_CLTU_HEADER_DU_TYPE:
      raise AttributeError("getCltu() only possible for TCcltuDataUnit")
    # the packetSize must contain the correct size
    headerByteSize = TC_DU_HEADER_BYTE_SIZE + TC_CLTU_HEADER_BYTE_SIZE
    return self.getBytes(headerByteSize, self.packetSize - headerByteSize)
  # ---------------------------------------------------------------------------
  def setCltu(self, cltu):
    """set the CLTU and the packetSize"""
    if self.dataUnitType != TC_CLTU_HEADER_DU_TYPE:
      raise AttributeError("setCltu() only possible for TCcltuDataUnit")
    self.setLen(TC_DU_HEADER_BYTE_SIZE + TC_CLTU_HEADER_BYTE_SIZE)
    self.append(cltu)
    self.packetSize = len(self)

# =============================================================================
class TCpacketDataUnit(TCdataUnit):
  """NCTRS telecommand packet data unit"""
  # ---------------------------------------------------------------------------
  def __init__(self, binaryString=None):
    """default constructor: initialise with header size"""
    emptyData = (binaryString == None)
    if emptyData:
      binaryString = "\0" * (TC_DU_HEADER_BYTE_SIZE +
                             TC_PACKET_HEADER_BYTE_SIZE)
    BinaryUnit.__init__(self,
                        binaryString,
                        TC_DU_HEADER_BYTE_SIZE,
                        TC_DU_HEADER_ATTRIBUTES,
                        TC_PACKET_HEADER_ATTRIBUTES)
    if emptyData:
      # AD packet / BD segment
      self.dataUnitType = TC_PACKET_HEADER_DU_TYPE
      self.packetSize = len(self)

# =============================================================================
class TCcltuDataUnit(TCdataUnit):
  """NCTRS telecommand CLTU data unit"""
  # ---------------------------------------------------------------------------
  def __init__(self, binaryString=None):
    """default constructor: initialise with header size"""
    emptyData = (binaryString == None)
    if emptyData:
      binaryString = "\0" * (TC_DU_HEADER_BYTE_SIZE +
                             TC_CLTU_HEADER_BYTE_SIZE)
    BinaryUnit.__init__(self,
                        binaryString,
                        TC_DU_HEADER_BYTE_SIZE,
                        TC_DU_HEADER_ATTRIBUTES,
                        TC_CLTU_HEADER_ATTRIBUTES)
    if emptyData:
      # CLTU
      self.dataUnitType = TC_CLTU_HEADER_DU_TYPE
      self.packetSize = len(self)

# =============================================================================
class TCdirectivesDataUnit(TCdataUnit):
  """NCTRS telecommand directives data unit"""
  # ---------------------------------------------------------------------------
  def __init__(self, binaryString=None):
    """default constructor: initialise with header size"""
    emptyData = (binaryString == None)
    if emptyData:
      binaryString = "\0" * (TC_DU_HEADER_BYTE_SIZE +
                             TC_DIRECTIVES_BYTE_SIZE)
    BinaryUnit.__init__(self,
                        binaryString,
                        TC_DU_HEADER_BYTE_SIZE,
                        TC_DU_HEADER_ATTRIBUTES,
                        TC_DIRECTIVES_ATTRIBUTES)
    if emptyData:
      # COP1 directive
      self.dataUnitType = TC_DIRECTIVES_DU_TYPE
      self.packetSize = len(self)

# =============================================================================
class TCpacketResponseDataUnit(TCdataUnit):
  """NCTRS telecommand packet response data unit"""
  # ---------------------------------------------------------------------------
  def __init__(self, binaryString=None):
    """default constructor: initialise with header size"""
    emptyData = (binaryString == None)
    if emptyData:
      binaryString = "\0" * (TC_DU_HEADER_BYTE_SIZE +
                             TC_PACKET_RESPONSE_BYTE_SIZE)
    BinaryUnit.__init__(self,
                        binaryString,
                        TC_DU_HEADER_BYTE_SIZE,
                        TC_DU_HEADER_ATTRIBUTES,
                        TC_PACKET_RESPONSE_ATTRIBUTES)
    if emptyData:
      # AD packet / BD segment response
      self.dataUnitType = TC_PACKET_RESPONSE_DU_TYPE
      self.packetSize = len(self)

# =============================================================================
class TCcltuResponseDataUnit(TCdataUnit):
  """NCTRS telecommand CLTU response data unit"""
  # ---------------------------------------------------------------------------
  def __init__(self, binaryString=None):
    """default constructor: initialise with header size"""
    emptyData = (binaryString == None)
    if emptyData:
      binaryString = "\0" * (TC_DU_HEADER_BYTE_SIZE +
                             TC_CLTU_RESPONSE_BYTE_SIZE)
    BinaryUnit.__init__(self,
                        binaryString,
                        TC_DU_HEADER_BYTE_SIZE,
                        TC_DU_HEADER_ATTRIBUTES,
                        TC_CLTU_RESPONSE_ATTRIBUTES)
    if emptyData:
      # CLTU response
      self.dataUnitType = TC_CLTU_RESPONSE_DU_TYPE
      self.packetSize = len(self)

# =============================================================================
class TClinkStatusDataUnit(TCdataUnit):
  """NCTRS link status data unit"""
  # ---------------------------------------------------------------------------
  def __init__(self, binaryString=None):
    """default constructor: initialise with header size"""
    emptyData = (binaryString == None)
    if emptyData:
      binaryString = "\0" * (TC_DU_HEADER_BYTE_SIZE +
                             TC_LINK_STATUS_BYTE_SIZE)
    BinaryUnit.__init__(self,
                        binaryString,
                        TC_DU_HEADER_BYTE_SIZE,
                        TC_DU_HEADER_ATTRIBUTES,
                        TC_LINK_STATUS_ATTRIBUTES)
    if emptyData:
      # Link status
      self.dataUnitType = TC_LINK_STATUS_DU_TYPE
      self.packetSize = len(self)

# =============================================================================
class AdminMessageDataUnit(BinaryUnit):
  """NCTRS admin message data unit"""
  # ---------------------------------------------------------------------------
  def __init__(self, binaryString=None):
    """default constructor: initialise with header size"""
    # note: correct packetSize is not forced!
    emptyData = (binaryString == None)
    if emptyData:
      binaryString = "\0" * MESSAGE_HEADER_BYTE_SIZE
    BinaryUnit.__init__(self,
                        binaryString,
                        MESSAGE_HEADER_BYTE_SIZE,
                        MESSAGE_HEADER_ATTRIBUTES)
  # ---------------------------------------------------------------------------
  def getMessage(self):
    """returns the admin message"""
    # the packetSize must contain the correct size
    headerByteSize = MESSAGE_HEADER_BYTE_SIZE
    return self.getBytes(headerByteSize, self.packetSize - headerByteSize).tostring()
  # ---------------------------------------------------------------------------
  def setMessage(self, message):
    """set the admin message and the packetSize"""
    self.setLen(MESSAGE_HEADER_BYTE_SIZE)
    self.append(message)
    self.packetSize = len(self)
  # ---------------------------------------------------------------------------
  def set(self, 
          messageType,
          eventId,
          groundstationName=None,
          adCounter=0,
          vcId=0,
          mapId=0):
    """set all attributes of the admin message"""
    self.messageType = messageType
    self.eventId = eventId
    if messageType == ADMIN_MSG_TM:
      if eventId == ADMIN_MSG_TM_LINK_FLOW:
        self.severity = ADMIN_MSG_INFO
        self.setMessage("Set TM link status to TM FLOW" +
                        "\0")
      elif eventId == ADMIN_MSG_TM_LINK_NOFLOW:
        self.severity = ADMIN_MSG_WARN
        self.setMessage("Set TM link status to NO TM FLOW" +
                        "\0")
      else:
        raise AttributeError("unexpected eventId for ADMIN_MSG_TM")
    elif messageType == ADMIN_MSG_TC:
      if eventId == ADMIN_MSG_TC_LINK_ESTABLISHED_TO_GS:
        self.severity = ADMIN_MSG_INFO
        self.setMessage("Established TC link to " +
                        (TC_PAR_GS_EQUIPMENT_NAME % groundstationName) +
                        ":seq.count=" +
                        (TC_PAR_COUNTER % adCounter) +
                        "\0")
      elif eventId == ADMIN_MSG_TC_LINK_CLOSED_TO_GS:
        self.severity = ADMIN_MSG_WARN
        self.setMessage("Closed TC link to " +
                        (TC_PAR_GS_EQUIPMENT_NAME % groundstationName) +
                        "\0")
      elif eventId == ADMIN_MSG_TC_LINK_ABORTED_TO_GS:
        self.severity = ADMIN_MSG_WARN
        self.setMessage("Aborted TC link to " +
                        (TC_PAR_GS_EQUIPMENT_NAME % groundstationName) +
                        "\0")
      elif eventId == ADMIN_MSG_TC_LINK_ABORTED_FROM_GS:
        self.severity = ADMIN_MSG_ALARM
        self.setMessage((TC_PAR_GS_EQUIPMENT_NAME % groundstationName) +
                        " aborted TC link (xxx)" +
                        "\0")
      elif eventId == ADMIN_MSG_TC_AD_SERVICE_AVAILABLE_FROM_GS:
        self.severity = ADMIN_MSG_INFO
        self.setMessage("AD service " +
                        (TC_PAR_VCID % vcId) +
                        " available from " +
                        (TC_PAR_GS_EQUIPMENT_NAME % groundstationName) +
                        ":MAPids=" +
                        (TC_PAR_MAPID % mapId) +
                        "\0")
      elif eventId == ADMIN_MSG_TC_AD_SERVICE_FAILE_IN_GS:
        self.severity = ADMIN_MSG_ALARM
        self.setMessage("Failed to initiate AD service " +
                        (TC_PAR_VCID % vcId) +
                        " in "
                        (TC_PAR_GS_EQUIPMENT_NAME % groundstationName) +
                        "\0")
      elif eventId == ADMIN_MSG_TC_AD_SERVICE_TERMINATED_IN_GS:
        self.severity = ADMIN_MSG_WARN
        self.setMessage("AD service " +
                        (TC_PAR_VCID % vcId) +
                        " terminated in "
                        (TC_PAR_GS_EQUIPMENT_NAME % groundstationName) +
                        "\0")
      elif eventId == ADMIN_MSG_TC_AD_SERVICE_WILL_TERM_IN_GS_BD:
        self.severity = ADMIN_MSG_WARN
        self.setMessage("AD service " +
                        (TC_PAR_VCID % vcId) +
                        " will terminate in "
                        (TC_PAR_GS_EQUIPMENT_NAME % groundstationName) +
                        ":BD TC sent" +
                        "\0")
      elif eventId == ADMIN_MSG_TC_AD_SERVICE_WILL_TERM_IN_GS:
        self.severity = ADMIN_MSG_WARN
        self.setMessage("AD service " +
                        (TC_PAR_VCID % vcId) +
                        " will terminate in "
                        (TC_PAR_GS_EQUIPMENT_NAME % groundstationName) +
                        ":xxxxxxxxxxxxxxx" +
                        "\0")
      elif eventId == ADMIN_MSG_TC_ALL_SERVICES_WILL_TERM_IN_GS:
        self.severity = ADMIN_MSG_WARN
        self.setMessage("All services will terminate in "
                        (TC_PAR_GS_EQUIPMENT_NAME % groundstationName) +
                        ":xxxxxxxxxxxxxxx" +
                        "\0")
      else:
        raise AttributeError("unexpected eventId for ADMIN_MSG_TM")
    else:
      raise AttributeError("unexpected messsageType")
