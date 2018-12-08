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
import CCSDS.PACKET
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

# =============================================================================
class TMparamToPkt(object):
  """Contains the data for a single raw value extraction"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    self.paramDef = None
    self.valueType = None
    self.pktDef = None
    self.pktSPID = None
    self.locOffby = None
    self.locOffbi = None
    self.locNbocc = None
    self.locLgocc = None
  # ---------------------------------------------------------------------------
  def __str__(self):
    """string representation"""
    retVal = "\n"
    retVal += "   valueType = " + str(self.valueType) + "\n"
    retVal += "   pktSPID = " + str(self.pktSPID) + "\n"
    retVal += "   locOffby = " + str(self.locOffby) + "\n"
    retVal += "   locOffbi = " + str(self.locOffbi) + "\n"
    retVal += "   locNbocc = " + str(self.locNbocc) + "\n"
    retVal += "   locLgocc = " + str(self.locLgocc) + "\n"
    return retVal

# =============================================================================
class TMparamExtraction(object):
  """Defines a dedicated parameter extraction in a packet"""
  # ---------------------------------------------------------------------------
  def __init__(self, bitPos, bitWidth, name, descr, valueType, piValue=False):
    self.bitPos = bitPos
    self.bitWidth = bitWidth
    self.name = name
    self.descr = descr
    self.valueType = valueType
    self.piValue = piValue
  # ---------------------------------------------------------------------------
  def __cmp__(self, other):
    """supports sorting by packet location"""
    if other == None:
      return 1
    if self.bitPos > other.bitPos:
      return 1
    if self.bitPos < other.bitPos:
      return -1
    return 0
  # ---------------------------------------------------------------------------
  def __lt__(self, other):
    """compares if self < other"""
    if other == None:
      return False
    return (self.bitPos < other.bitPos)

# =============================================================================
class TMpktDef(object):
  """Contains the most important definition data of a TM packet"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    self.pktSPID = None
    self.pktName = None
    self.pktDescr = None
    self.pktAPID = None
    self.pktType = None
    self.pktSType = None
    self.pktDFHsize = None
    self.pktHasDFhdr = None
    self.pktCheck = None
    self.pktPI1off = None
    self.pktPI1wid = None
    self.pktPI1val = None
    self.pktPI2off = None
    self.pktPI2wid = None
    self.pktPI2val = None
    self.pktSPsize = None
    self.pktS2Ksize = None
    self.pktSPDFsize = None
    self.pktSPDFdataSize = None
    self.paramLinks = None
  # ---------------------------------------------------------------------------
  def __cmp__(self, other):
    """supports sorting by SPID"""
    if other == None:
      return 1
    if self.pktSPID > other.pktSPID:
      return 1
    if self.pktSPID < other.pktSPID:
      return -1
    return 0
  # ---------------------------------------------------------------------------
  def __lt__(self, other):
    """compares if self < other"""
    if other == None:
      return False
    return (self.pktSPID < other.pktSPID)
  # ---------------------------------------------------------------------------
  def appendParamLink(self, paramToPacket):
    """used to append later on links to related parameters"""
    paramName = paramToPacket.paramDef.paramName
    self.paramLinks[paramName] = paramToPacket
  # ---------------------------------------------------------------------------
  def rangeOverlap(self, bitPos1, bitWidth1, bitPos2, bitWidth2):
    """checks if two ranges overlap"""
    if bitPos1 == None or bitPos2 == None:
      return False
    nextBitPos1 = bitPos1 + bitWidth1
    nextBitPos2 = bitPos2 + bitWidth2
    return (nextBitPos1 > bitPos2 and nextBitPos2 > bitPos1)
  # ---------------------------------------------------------------------------
  def getParamExtraction(self, paramName):
    """returns a parameter extraction of a related parameters"""
    if paramName not in self.paramLinks:
      return None
    paramToPacket = self.paramLinks[paramName]
    paramDef = paramToPacket.paramDef
    paramDescr = paramDef.paramDescr
    bitWidth = paramDef.bitWidth
    valueType = paramToPacket.valueType
    pktSPID = paramToPacket.pktSPID
    locOffby = paramToPacket.locOffby
    locOffbi =  paramToPacket.locOffbi
    locNbocc = paramToPacket.locNbocc
    locLgocc = paramToPacket.locLgocc
    bitStartPos = locOffbi + (locOffby * 8)
    # check if a parameter commutation is qualified
    nameElements = paramName.split("#")
    if len(nameElements) == 1:
      # normal parameter
      paramExtraction = TMparamExtraction(bitStartPos, bitWidth, paramName, paramDescr, valueType)
    else:
      # supercommutated parameter
      commutation = int(nameElements[1])
      if commutation < 1:
        LOG_WARNING("param " + nameElements[0] + " has invalid commutation " + nameElements[1], "SPACE")
        return None
      bitPos = bitStartPos + (locLgocc * (commutation - 1))
      paramExtraction = TMparamExtraction(bitPos, bitWidth, fieldName, paramDescr, valueType)
    return paramExtraction
  # ---------------------------------------------------------------------------
  def getParamExtractions(self):
    """returns all parameter extractions, ordered by packet location"""
    retVal = []
    # insert PI1 and PI2 (if defined)
    pi1BitPos = None
    pi1BitWidth = None
    if self.pktPI1val != None:
      pi1BitPos = self.pktPI1off * 8
      pi1BitWidth = self.pktPI1wid
      pi1ValueName = self.pktName + "_PI1VAL"
      pi1ValueDescr = "PI1 Value"
      paramExtraction = TMparamExtraction(pi1BitPos, pi1BitWidth, pi1ValueName, pi1ValueDescr, UTIL.DU.BITS, True)
      retVal.append(paramExtraction)
    pi2BitPos = None
    pi2BitWidth = None
    if self.pktPI2val != None:
      pi2BitPos = self.pktPI2off * 8
      pi2BitWidth = self.pktPI2wid
      if self.rangeOverlap(pi1BitPos, pi1BitWidth, pi2BitPos, pi2BitWidth):
        LOG_WARNING("PI1 and PI2 overlap ---> PI2 ignored", "SPACE")
      else:
        pi2ValueName = self.pktName + "_PI2VAL"
        pi2ValueDescr = "PI2 Value"
        paramExtraction = TMparamExtraction(pi2BitPos, pi2BitWidth, pi2ValueName, pi2ValueDescr, UTIL.DU.BITS, True)
        retVal.append(paramExtraction)
    # insert other parameters
    for paramName, paramToPacket in self.paramLinks.items():
      paramDef = paramToPacket.paramDef
      paramDescr = paramDef.paramDescr
      bitWidth = paramDef.bitWidth
      valueType = paramToPacket.valueType
      pktSPID = paramToPacket.pktSPID
      locOffby = paramToPacket.locOffby
      locOffbi =  paramToPacket.locOffbi
      locNbocc = paramToPacket.locNbocc
      locLgocc = paramToPacket.locLgocc
      bitStartPos = locOffbi + (locOffby * 8)
      if paramToPacket.locNbocc == 1:
        # single location of the parameter in the packet
        if self.rangeOverlap(pi1BitPos, pi1BitWidth, bitStartPos, bitWidth):
          LOG_WARNING("param " + paramName + " overlaps PI1 ---> ignored", "SPACE")
          continue
        if self.rangeOverlap(pi2BitPos, pi2BitWidth, bitStartPos, bitWidth):
          LOG_WARNING("param " + paramName + " overlaps PI2 ---> ignored", "SPACE")
          continue
        paramExtraction = TMparamExtraction(bitStartPos, bitWidth, paramName, paramDescr, valueType)
        retVal.append(paramExtraction)
      else:
        # supercommutated parameter
        for i in range(paramToPacket.locNbocc):
          fieldName = paramDef.getCommutatedParamName(i)
          bitPos = bitStartPos + (locLgocc * i)
          if self.rangeOverlap(pi1BitPos, pi1BitWidth, bitPos, bitWidth):
            LOG_WARNING("param " + fieldName + " overlaps PI1 ---> ignored", "SPACE")
            continue
          if self.rangeOverlap(pi2BitPos, pi2BitWidth, bitPos, bitWidth):
            LOG_WARNING("param " + fieldName + " overlaps PI2 ---> ignored", "SPACE")
            continue
          paramExtraction = TMparamExtraction(bitPos, bitWidth, fieldName, paramDescr, valueType)
          retVal.append(paramExtraction)
    retVal.sort()
    return retVal
  # ---------------------------------------------------------------------------
  def __str__(self):
    """string representation"""
    retVal = "\n"
    retVal += " pktSPID = " + str(self.pktSPID) + "\n"
    retVal += " pktName = " + str(self.pktName) + "\n"
    retVal += " pktDescr = " + str(self.pktDescr) + "\n"
    retVal += " pktAPID = " + str(self.pktAPID) + "\n"
    retVal += " pktType = " + str(self.pktType) + "\n"
    retVal += " pktSType = " + str(self.pktSType) + "\n"
    retVal += " pktDFHsize = " + str(self.pktDFHsize) + "\n"
    retVal += " pktHasDFhdr = " + str(self.pktHasDFhdr) + "\n"
    retVal += " pktCheck = " + str(self.pktCheck) + "\n"
    retVal += " pktPI1off = " + str(self.pktPI1off) + "\n"
    retVal += " pktPI1wid = " + str(self.pktPI1wid) + "\n"
    retVal += " pktPI1val = " + str(self.pktPI1val) + "\n"
    retVal += " pktPI2off = " + str(self.pktPI2off) + "\n"
    retVal += " pktPI2wid = " + str(self.pktPI2wid) + "\n"
    retVal += " pktPI2val = " + str(self.pktPI2val) + "\n"
    retVal += " pktSPsize = " + str(self.pktSPsize) + "\n"
    retVal += " pktS2Ksize = " + str(self.pktS2Ksize) + "\n"
    retVal += " pktSPDFsize = " + str(self.pktSPDFsize) + "\n"
    retVal += " pktSPDFdataSize = " + str(self.pktSPDFsize) + "\n"
    retVal += " paramLinks =\n"
    for paramToPacket in self.paramLinks.values():
      retVal += "  paramToPacket = " + str(paramToPacket)
    return retVal

# =============================================================================
class TMparamDef(object):
  """Contains the most important definition data of a TM parameter"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    self.paramName = None
    self.paramDescr = None
    self.paramPtc = None
    self.paramPfc = None
    self.bitWidth = None
    self.minCommutations = None
    self.maxCommutations = None
  # ---------------------------------------------------------------------------
  def __cmp__(self, other):
    """supports sorting by paramName"""
    if other == None:
      return 1
    if self.paramName > other.paramName:
      return 1
    if self.paramName < other.paramName:
      return -1
    return 0
  # ---------------------------------------------------------------------------
  def __lt__(self, other):
    """compares if self < other"""
    if other == None:
      return False
    return (self.paramName < other.paramName)
  # ---------------------------------------------------------------------------
  def getCommutatedParamName(self, commutation):
    """returns the commutated param name"""
    return self.paramName + '_' + ("%04d" % commutation)
  # ---------------------------------------------------------------------------
  def __str__(self):
    """string representation"""
    retVal = "\n"
    retVal += " paramName = " + str(self.paramName) + "\n"
    retVal += " paramDescr = " + str(self.paramDescr) + "\n"
    retVal += " paramPtc = " + str(self.paramPtc) + "\n"
    retVal += " paramPfc = " + str(self.paramPfc) + "\n"
    retVal += " bitWidth = " + str(self.bitWidth) + "\n"
    # These lines have been commented due to problems with pickling and
    # unpickling (errornous unpickling of the whole definition data).
    # This backward reference from parameters to packets is not needed
    # in the existing implementation.
    #retVal += " pktLinks =\n"
    #for paramToPacket in self.pktLinks.values():
    #  retVal += "  paramToPacket = " + str(paramToPacket)
    retVal += " minCommutations = " + str(self.minCommutations) + "\n"
    retVal += " maxCommutations = " + str(self.maxCommutations) + "\n"
    return retVal

# =============================================================================
class TMpacketInjectData(object):
  """Data of a TM packet that can be injected"""
  # ---------------------------------------------------------------------------
  def __init__(self,
               pktSPID,
               pktMnemonic,
               params,
               values,
               dataField,
               segmentationFlags):
    """Initialisation with default data"""
    self.pktName = pktMnemonic
    self.pktSPID = pktSPID
    self.parameterValuesList = []
    self.dataField = dataField
    self.segmentationFlags = segmentationFlags
    if params == "" or values == "":
      return
    # there are parameter-names and parameter-values
    paramsLst = params.split(",")
    valuesLst = values.split(",")
    # both parts must match
    if len(paramsLst) != len(valuesLst):
      LOG_WARNING("parameter-names or parameter-values have different size")
      return
    # create the return list
    for i in range(len(valuesLst)):
      param = paramsLst[i].strip().strip("{").strip("}")
      value = valuesLst[i].strip().strip("{").strip("}")
      if (len(param) > 0) and (len(value) > 0):
        self.parameterValuesList.append([param,value])

# =============================================================================
class TCpktDef(object):
  """Contains the most important definition data of a TC packet"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    self.pktName = None
    self.pktDescr = None
    self.pktDescr2 = None
    self.pktAPID = None
    self.pktType = None
    self.pktSType = None
    self.pktDFHsize = None
    self.pktHasDFhdr = None
    self.pktCheck = None
    self.pktSPsize = None
    self.pktSPDFsize = None
    self.pktSPDFdataSize = None
  # ---------------------------------------------------------------------------
  def __cmp__(self, other):
    """supports sorting by SPID"""
    if other == None:
      return 1
    if self.pktName > other.pktName:
      return 1
    if self.pktName < other.pktName:
      return -1
    return 0
  # ---------------------------------------------------------------------------
  def __lt__(self, other):
    """compares if self < other"""
    if other == None:
      return False
    return (self.pktName < other.pktName)
  # ---------------------------------------------------------------------------
  def __str__(self):
    """string representation"""
    retVal = "\n"
    retVal += " pktName = " + str(self.pktName) + "\n"
    retVal += " pktDescr = " + str(self.pktDescr) + "\n"
    retVal += " pktDescr2 = " + str(self.pktDescr2) + "\n"
    retVal += " pktAPID = " + str(self.pktAPID) + "\n"
    retVal += " pktType = " + str(self.pktType) + "\n"
    retVal += " pktSType = " + str(self.pktSType) + "\n"
    retVal += " pktDFHsize = " + str(self.pktDFHsize) + "\n"
    retVal += " pktHasDFhdr = " + str(self.pktHasDFhdr) + "\n"
    retVal += " pktCheck = " + str(self.pktCheck) + "\n"
    retVal += " pktSPsize = " + str(self.pktSPsize) + "\n"
    retVal += " pktSPDFsize = " + str(self.pktSPDFsize) + "\n"
    retVal += " pktSPDFdataSize = " + str(self.pktSPDFsize) + "\n"
    return retVal

# =============================================================================
class TCpacketInjectData(object):
  """Data of a TC packet that can be injected"""
  # ---------------------------------------------------------------------------
  def __init__(self,
               pktMnemonic,
               route,
               dataField,
               segmentationFlags):
    """Initialisation with default data"""
    self.pktName = pktMnemonic
    self.route = route
    self.dataField = dataField
    self.segmentationFlags = segmentationFlags

##############
# interfaces #
##############
# =============================================================================
class Definitions(object):
  """Interface for definition data"""
  # ---------------------------------------------------------------------------
  def createDefinitions(self):
    """creates the definition data"""
    pass
  # ---------------------------------------------------------------------------
  def initDefinitions(self):
    """initialise the definition data from file or MIB"""
    pass
  # ---------------------------------------------------------------------------
  def getTMpktDefByIndex(self, index):
    """returns a TM packet definition"""
    pass
  # ---------------------------------------------------------------------------
  def getTMpktDefBySPID(self, spid):
    """returns a TM packet definition"""
    pass
  # ---------------------------------------------------------------------------
  def getSPIDbyPktName(self, name):
    """returns the packet SPID for a packet name"""
    pass
  # ---------------------------------------------------------------------------
  def getTMpktDefs(self):
    """returns the TM packet definitions"""
    pass
  # ---------------------------------------------------------------------------
  def getTMparamDefs(self):
    """returns the TM parameter definitions"""
    pass
  # ---------------------------------------------------------------------------
  def getTMpacketInjectData(self,
                            pktMnemonic,
                            params,
                            values,
                            dataField=None,
                            segmentationFlags=CCSDS.PACKET.UNSEGMENTED):
    """returns the data that are used for packet injection"""
    pass
  # ---------------------------------------------------------------------------
  def getTMpacketInjectDataBySPID(self,
                                  spid,
                                  params,
                                  values,
                                  dataField=None,
                                  segmentationFlags=CCSDS.PACKET.UNSEGMENTED):
    """returns the data that are used for packet injection"""
    pass
  # ---------------------------------------------------------------------------
  def getTCpktDefs(self):
    """returns the TC packet definitions"""
    pass
  # ---------------------------------------------------------------------------
  def getTCpktDefByIndex(self, index):
    """returns a TC packet definition"""
    pass
  # ---------------------------------------------------------------------------
  def getTCpktDefByName(self, name):
    """returns a TC packet definition"""
    pass
  # ---------------------------------------------------------------------------
  def getTCpacketInjectData(self,
                            pktMnemonic,
                            route,
                            dataField=None,
                            segmentationFlags=CCSDS.PACKET.UNSEGMENTED):
    """returns the data that are used for packet injection"""
    pass

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
  def notifyMILdatablockDistribution(self, rtAddress, dataBlock):
    """The mRT has received on the MIL Bus a data block from the BC"""
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
                  parameterValues=[],
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
# definitions is a singleton
s_definitions = None
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
