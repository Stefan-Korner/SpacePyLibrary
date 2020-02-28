#******************************************************************************
# (C) 2020, Stefan Korner, Austria                                            *
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
# Supplement to TM/TC processing - Interface                                          *
#******************************************************************************
import string
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import CCSDS.DU, CCSDS.PACKET
import UTIL.DU

###########
# classes #
###########
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
    self.pktSPDFsize = None
    self.pktSPDFdataSize = None
    self.paramLinks = None
    self.tmStructDef = None
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
  def updateSPsize(self):
    """updates the source packet size from parameter positions"""
    totalBitEndPos = CCSDS.PACKET.PRIMARY_HEADER_BYTE_SIZE * 8
    if self.pktHasDFhdr:
      totalBitEndPos += self.pktDFHsize * 8
    if self.pktPI1off != None:
      pi1BitEndPos = (self.pktPI1off * 8) + self.pktPI1wid
      totalBitEndPos = max(totalBitEndPos, pi1BitEndPos)
    if self.pktPI2off != None:
      pi2BitEndPos = (self.pktPI2off * 8) + self.pktPI2wid
      totalBitEndPos = max(totalBitEndPos, pi2BitEndPos)
    # search the end position of all parameters
    for paramName, paramToPacket in self.paramLinks.items():
      paramDef = paramToPacket.paramDef
      bitWidth = paramDef.bitWidth
      locOffby = paramToPacket.locOffby
      locOffbi =  paramToPacket.locOffbi
      locNbocc = paramToPacket.locNbocc
      locLgocc = paramToPacket.locLgocc
      bitStartPos = locOffbi + (locOffby * 8)
      for i in range(paramToPacket.locNbocc):
        fieldName = paramDef.getCommutatedParamName(i)
        bitPos = bitStartPos + (locLgocc * i)
        bitEndPos = bitPos + bitWidth
        if bitEndPos > totalBitEndPos:
          totalBitEndPos = bitEndPos
    # update source packet size
    totalByteEndPos = (totalBitEndPos + 7) // 8
    if self.pktCheck:
      pktSPsize = totalByteEndPos + CCSDS.DU.CRC_BYTE_SIZE
    else:
      pktSPsize = totalByteEndPos
    if self.pktSPsize < pktSPsize:
      self.pktSPsize = pktSPsize
    # update also other related attributes
    self.pktSPDFsize = self.pktSPsize - CCSDS.PACKET.PRIMARY_HEADER_BYTE_SIZE
    if self.pktHasDFhdr:
      self.pktSPDFdataSize = self.pktSPDFsize - self.pktDFHsize
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
      paramExtraction = TMparamExtraction(bitPos, bitWidth, paramName, paramDescr, valueType)
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
    for paramName, paramToPacket in self.paramLinks.iteritems():
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
    retVal += " pktSPDFsize = " + str(self.pktSPDFsize) + "\n"
    retVal += " pktSPDFdataSize = " + str(self.pktSPDFsize) + "\n"
    retVal += " paramLinks =\n"
    for paramToPacket in self.paramLinks.values():
      retVal += "  paramToPacket = " + str(paramToPacket)
    retVal += " tmStructDef = " + str(self.tmStructDef) + "\n"
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
               tmStruct,
               dataField,
               segmentationFlags):
    """Initialisation with default data"""
    self.pktName = pktMnemonic
    self.pktSPID = pktSPID
    self.parameterValuesList = []
    self.tmStruct = tmStruct
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
    self.pktPI1off = None
    self.pktPI1wid = None
    self.pktPI1val = None
    self.pktPI2off = None
    self.pktPI2wid = None
    self.pktPI2val = None
    self.pktSPsize = None
    self.pktSPDFsize = None
    self.pktSPDFdataSize = None
    self.tcStructDef = None
  # ---------------------------------------------------------------------------
  def __cmp__(self, other):
    """supports sorting by pktName"""
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
    retVal += " pktPI1off = " + str(self.pktPI1off) + "\n"
    retVal += " pktPI1wid = " + str(self.pktPI1wid) + "\n"
    retVal += " pktPI1val = " + str(self.pktPI1val) + "\n"
    retVal += " pktPI2off = " + str(self.pktPI2off) + "\n"
    retVal += " pktPI2wid = " + str(self.pktPI2wid) + "\n"
    retVal += " pktPI2val = " + str(self.pktPI2val) + "\n"
    retVal += " pktSPsize = " + str(self.pktSPsize) + "\n"
    retVal += " pktSPDFsize = " + str(self.pktSPDFsize) + "\n"
    retVal += " pktSPDFdataSize = " + str(self.pktSPDFsize) + "\n"
    retVal += " tcStructDef = " + str(self.tcStructDef) + "\n"
    return retVal

# =============================================================================
class TCpacketInjectData(object):
  """Data of a TC packet that can be injected"""
  # ---------------------------------------------------------------------------
  def __init__(self,
               pktMnemonic,
               route,
               tcStruct):
    """Initialisation with default data"""
    self.pktName = pktMnemonic
    self.route = route
    self.tcStruct = tcStruct

##############
# interfaces #
##############
# =============================================================================
class Definitions(object):
  """Interface for definition data"""
  # ---------------------------------------------------------------------------
  def getDefinitionFileName(self):
    """get the testdata.sim file name incl. path"""
    pass
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
                            tmStruct,
                            dataField=None,
                            segmentationFlags=CCSDS.PACKET.UNSEGMENTED):
    """returns the data that are used for packet injection"""
    pass
  # ---------------------------------------------------------------------------
  def getTMpacketInjectDataBySPID(self,
                                  spid,
                                  params,
                                  values,
                                  tmStruct,
                                  dataField=None,
                                  segmentationFlags=CCSDS.PACKET.UNSEGMENTED):
    """returns the data that are used for packet injection"""
    pass
  # ---------------------------------------------------------------------------
  def getTMpacketKey(self, tmPacketDu):
    """retrieves the SPID from the TM packet data unit"""
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
                            tcStruct):
    """returns the data that are used for packet injection"""
    pass
  # ---------------------------------------------------------------------------
  def getTCpacketKey(self, tcPacketDu):
    """retrieves the TC packet name from the TC packet data unit"""
    pass

####################
# global variables #
####################
# definitions is a singleton
s_definitions = None
