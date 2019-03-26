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
# Space Simulation - Space Data Definitions                                   #
#******************************************************************************
import os, pickle, time
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import CCSDS.DU, CCSDS.PACKET, CCSDS.TIME, CCSDS.VP
import PUS.PACKET
import SCOS.ENV, SCOS.MIB
import SPACE.IF
import UTIL.DU, UTIL.SYS

###########
# classes #
###########
# =============================================================================
class DefinitionData(object):
  """Data part of the Definitions that can be saved and loaded"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """Empty initialisation"""
    self.creationTime = "1970.01.01 00:00:00"
    self.tmPktDefs = None
    self.tmPktDefsSpidMap = None
    self.tmPktSpidNameMap = None
    self.tmParamDefs = None
    self.tcPktDefs = None
    self.tcPktDefsNameMap = None

# =============================================================================
class DefinitionsImpl(SPACE.IF.Definitions):
  """Manager for definition data"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    self.definitionFileName = SCOS.ENV.s_environment.getRuntimeRoot() + \
        "/testbin/testdata.sim"
    self.definitionData = None
  # ---------------------------------------------------------------------------
  def getDefinitionFileName(self):
    """get the testdata.sim file name incl. path"""
    return self.definitionFileName
  # ---------------------------------------------------------------------------
  def createTMpktDef(self, pidRecord, picRecord, tpcfRecord):
    """creates a TM packet definition"""
    tmPktDef = SPACE.IF.TMpktDef();
    tmPktDef.pktSPID = pidRecord.pidSPID
    if tpcfRecord == None:
      tmPktDef.pktName = "SPID_" + str(pidRecord.pidSPID)
      pktSize = 0
    else:
      # remove white spaces and "&"
      tmPktDef.pktName = tpcfRecord.tpcfName.replace(" ", "_").replace("&", "_").replace(".", "_").replace("-", "_")
      pktSize = tpcfRecord.tpcfSize
    tmPktDef.pktDescr = pidRecord.pidDescr
    tmPktDef.pktAPID = pidRecord.pidAPID
    tmPktDef.pktType = pidRecord.pidType
    tmPktDef.pktSType = pidRecord.pidSType
    if tmPktDef.pktAPID == 0:
      tmPktDef.pktHasDFhdr = False
      tmPktDef.pktDFHsize = 0
    elif tmPktDef.pktType == 0 and tmPktDef.pktSType == 0:
      tmPktDef.pktHasDFhdr = False
      tmPktDef.pktDFHsize = 0
    else:
      tmPktDef.pktHasDFhdr = True
      # pidRecord.pidDFHsize might be 0 even if there is a secondary header
      #                      --> only rely on tmPktDef.pktHasDFhdr if it is > 0
      if pidRecord.pidDFHsize > 0:
        tmPktDef.pktDFHsize = pidRecord.pidDFHsize
      else:
        tmPktDef.pktDFHsize = PUS.PACKET.TM_PACKET_DATAFIELD_HEADER_BYTE_SIZE
    tmPktDef.pktCheck = pidRecord.pidCheck
    tmPktDef.pktPI1off = None
    tmPktDef.pktPI1wid = None
    tmPktDef.pktPI1val = None
    tmPktDef.pktPI2off = None
    tmPktDef.pktPI2wid = None
    tmPktDef.pktPI2val = None
    if picRecord != None:
      if picRecord.picPI1off > -1:
        tmPktDef.pktPI1off = picRecord.picPI1off
        tmPktDef.pktPI1wid = picRecord.picPI1wid
        tmPktDef.pktPI1val = pidRecord.pidPI1
      if picRecord.picPI2off > -1:
        tmPktDef.pktPI2off = picRecord.picPI2off
        tmPktDef.pktPI2wid = picRecord.picPI2wid
        tmPktDef.pktPI2val = pidRecord.pidPI2
    # tpcfRecord.tpcfSize might be 0 even if there is a fixed packet
    #                     --> only rely on tpcfRecord.tpcfSize if it is > 0
    if pktSize > 0:
      # packet size defined: take it
      # tpcfRecord.tpcfSize optionally contains in addition the size of the
      #                     SCOS-2000 packet header (ESA convention) or it
      #                     does not contain this additional offset. This must
      #                     be considered via the configuration entry
      #                     TM_PKT_SIZE_ADD
      tmPktDef.pktSPsize = pktSize + \
          int(UTIL.SYS.s_configuration.TM_PKT_SIZE_ADD)
      tmPktDef.pktSPDFsize = tmPktDef.pktSPsize - \
                             CCSDS.PACKET.PRIMARY_HEADER_BYTE_SIZE
      tmPktDef.pktSPDFdataSize = tmPktDef.pktSPDFsize - tmPktDef.pktDFHsize
      if tmPktDef.pktCheck:
        tmPktDef.pktSPDFdataSize -= CCSDS.DU.CRC_BYTE_SIZE
    else:
      # pktSize == 0: this will be overwritten via tmPktDef.updateSPsize() in
      #               a the processing step 4) of createTMdefinitions()
      tmPktDef.pktSPsize = 0
      tmPktDef.pktSPDFsize = 0
      tmPktDef.pktSPDFdataSize = 0
    # raw value extractions
    tmPktDef.paramLinks = {}
    return tmPktDef
  # ---------------------------------------------------------------------------
  def createTMparamDef(self, pcfRecord, plfRecords, tmPktDefs):
    """creates a TM parameter definition"""
    paramPtc = pcfRecord.pcfPtc
    paramPfc = pcfRecord.pcfPfc
    # getBitWidth(...) can raise an exception --> it is catched by the caller
    bitWidth = getBitWidth(paramPtc, paramPfc)
    # consistency check OK
    tmParamDef = SPACE.IF.TMparamDef()
    tmParamDef.paramName = pcfRecord.pcfName.replace(" ", "_").replace("&", "_").replace(".", "_").replace("-", "_")
    tmParamDef.paramDescr = pcfRecord.pcfDescr
    tmParamDef.paramPtc = paramPtc
    tmParamDef.paramPfc = paramPfc
    tmParamDef.bitWidth = bitWidth
    # related packets
    # This line has been commented due to problems with pickling and
    # unpickling (errornous unpickling of the whole definition data).
    # This backward reference from parameters to packets is not needed
    # in the existing implementation.
    #self.pktLinks = {}
    tmParamDef.minCommutations = 9999
    tmParamDef.maxCommutations = 0
    for plfRecord in plfRecords:
      spid = plfRecord.plfSPID
      if spid in tmPktDefs:
        # consistency check
        isBytePos = getIsBytePos(plfRecord)
        try:
          valueType = getValueType(paramPtc, paramPfc, isBytePos)
        except Exception as ex:
          # inconsistency
          LOG_WARNING("param " + pcfRecord.pcfName + ": " + str(ex) + " ---> ignored", "SPACE")
          continue
        tmPktDef = tmPktDefs[spid]
        paramToPacket = SPACE.IF.TMparamToPkt()
        paramToPacket.paramDef = tmParamDef
        paramToPacket.valueType = valueType
        paramToPacket.pktDef = tmPktDef
        paramToPacket.pktSPID = plfRecord.plfSPID
        paramToPacket.locOffby = plfRecord.plfOffby
        paramToPacket.locOffbi = plfRecord.plfOffbi
        paramToPacket.locNbocc = plfRecord.plfNbocc
        paramToPacket.locLgocc = plfRecord.plfLgocc
        tmParamDef.minCommutations = min(paramToPacket.locNbocc, tmParamDef.minCommutations)
        tmParamDef.maxCommutations = max(paramToPacket.locNbocc, tmParamDef.maxCommutations)
        tmPktDef.appendParamLink(paramToPacket)
        # This line has been commented due to problems with pickling and
        # unpickling (errornous unpickling of the whole definition data).
        # This backward reference from parameters to packets is not needed
        # in the existing implementation.
        #self.pktLinks[spid] = paramToPacket
    tmParamDef.minCommutations = min(tmParamDef.minCommutations, tmParamDef.maxCommutations)
    tmParamDef.maxCommutations = max(tmParamDef.minCommutations, tmParamDef.maxCommutations)
    return tmParamDef
  # ---------------------------------------------------------------------------
  def createTMdefinitions(self, pidMap, picMap, tpcfMap, pcfMap, plfMap):
    """helper method: create TM packet and parameter definitions from MIB tables"""
    tmPktDefs = []
    tmPktDefsSpidMap = {}
    tmPktSpidNameMap = {}
    tmParamDefs = []
    # step 1) create packet definitions
    # pidMap is the driving map for the join
    for spid, pidRecord in pidMap.items():
      picKey = pidRecord.picKey()
      if picKey in picMap:
        statusMessage = "PI1/PI2 depends on (APID,TYPE,STYPE)"
        picRecord = picMap[picKey]
      else:
        # PICrecord with TYPE, SUBTYPE, APID not found (new MIB format)
        # --> search for PICrecord with TYPE, SUBTYPE (old MIB format)
        picKey = pidRecord.picAlternateKey()
        if picKey in picMap:
          statusMessage = "PI1/PI2 depends on (TYPE,STYPE)"
          picRecord = picMap[picKey]
        else:
          statusMessage = "no PI1/PI2"
          picRecord = None
      if spid in tpcfMap:
        tpcfRecord = tpcfMap[spid]
      else:
        tpcfRecord = None
      tmPktDef = self.createTMpktDef(pidRecord, picRecord, tpcfRecord)
      pktName = tmPktDef.pktName
      tmPktDefs.append(tmPktDef)
      tmPktDefsSpidMap[spid] = tmPktDef
      tmPktSpidNameMap[pktName] = spid
      LOG("TM packet " + pktName + "(" + str(spid) + "), " + statusMessage, "SPACE")
    tmPktDefs.sort()
    # step 2) create parameter definitions
    # pcfMap is the driving map for the join
    for paramName, pcfRecord in pcfMap.items():
      if paramName in plfMap:
        plfRecords = plfMap[paramName]
      else:
        plfRecords = []
      try:
        tmParamDef = self.createTMparamDef(pcfRecord, plfRecords, tmPktDefsSpidMap)
      except Exception as ex:
        # inconsistency
        LOG_WARNING("param " + paramName + ": " + str(ex) + " ---> ignored", "SPACE")
        continue
      tmParamDefs.append(tmParamDef)
    tmParamDefs.sort()
    # step 3) update packet definitions
    # tmPktDefs is the driving list for the post processing
    for tmPktDef in tmPktDefs:
      tmPktDef.updateSPsize()
    # step 4) update the global container attributes
    self.definitionData.tmPktDefs = tmPktDefs
    self.definitionData.tmPktDefsSpidMap = tmPktDefsSpidMap
    self.definitionData.tmPktSpidNameMap = tmPktSpidNameMap
    self.definitionData.tmParamDefs = tmParamDefs
  # ---------------------------------------------------------------------------
  def createTCpktDef(self, ccfRecord, cdfMap, cpcMap):
    """creates a TM packet definition"""
    tcPktDef = SPACE.IF.TCpktDef();
    tcPktDef.pktName = ccfRecord.ccfCName
    tcPktDef.pktDescr = ccfRecord.ccfDescr
    tcPktDef.pktDescr2 = ccfRecord.ccfDescr2
    tcPktDef.pktAPID = ccfRecord.ccfAPID
    tcPktDef.pktType = ccfRecord.ccfType
    tcPktDef.pktSType = ccfRecord.ccfSType
    tcPktDef.pktDFHsize = 4
    tcPktDef.pktHasDFhdr = True
    tcPktDef.pktCheck = True
    tcPktDef.pktSPsize = 16
    tcPktDef.pktSPDFsize = 10
    tcPktDef.pktSPDFdataSize = 6
    tcPktDef.tcStructDef = self.createTcToplevelStructDef(tcPktDef.pktName, cdfMap, cpcMap)
    return tcPktDef
  # ---------------------------------------------------------------------------
  def createTcParamDef(self, paramName, defaultValue, cpcMap):
    try:
      cpcRecord = cpcMap[paramName]
      paramName = cpcRecord.cpcPName
      paramPtc = cpcRecord.cpcPtc
      paramPfc = cpcRecord.cpcPfc
      try:
        paramType = getValueType(paramPtc, paramPfc)
        bitWidth = getBitWidth(paramPtc, paramPfc)
        if defaultValue == "":
          defaultValue = cpcRecord.cpcDefVal
      except Exception as ex:
        # inconsistency
        LOG_WARNING("param " + paramName + ": " + str(ex) + " ---> dummy type", "SPACE")
        paramType = UTIL.DU.UNSIGNED
        bitWidth = 0
        defaultValue = 0
    except:
      LOG_WARNING("TC param name " + paramName + " not found in cpc.dat ---> dummy param", "SPACE")
      paramName = "dummy"
      paramType = UTIL.DU.UNSIGNED
      bitWidth = 0
      defaultValue = 0
    # special handling of time parameters
    if paramType == UTIL.DU.TIME:
      # TODO: differentiate between absolute and relative time
      try:
        timeFormat = getTimeFormat(paramPfc)
        return CCSDS.VP.TimeParamDef(paramName,
                                     timeFormat,
                                     defaultValue)
      except Exception as ex:
        # inconsistency
        LOG_WARNING("param " + paramName + ": " + str(ex) + " ---> dummy type", "SPACE")
        paramType = UTIL.DU.UNSIGNED
        bitWidth = 0
        defaultValue = 0
    # default handling of normal parameters
    return CCSDS.VP.SimpleParamDef(paramName,
                                   paramType,
                                   bitWidth,
                                   defaultValue)
  # ---------------------------------------------------------------------------
  def createTcSlotDef(self, sortedCdfRecords, cdfRecordsPos, cpcMap):
    nextCdfRecord = sortedCdfRecords[cdfRecordsPos]
    slotName = nextCdfRecord.cdfPName
    if nextCdfRecord.cdfGrpSize > 0:
      # group repeater definition
      childDef, cdfRecordsPos = self.createTcListDef(sortedCdfRecords, cdfRecordsPos, cpcMap)
    else:
      # parameter definition
      paramName = nextCdfRecord.cdfPName
      defaultValue = nextCdfRecord.cdfValue
      childDef = self.createTcParamDef(paramName, defaultValue, cpcMap)
      cdfRecordsPos += 1
    return (CCSDS.VP.SlotDef(slotName, childDef), cdfRecordsPos)
  # ---------------------------------------------------------------------------
  def createTcStructDef(self, structName, sortedCdfRecords, cdfRecordsPos, cdfRecordsEnd, cpcMap):
    sortedSlotDefs = []
    while cdfRecordsPos < cdfRecordsEnd:
      nextSlotDef, cdfRecordsPos = self.createTcSlotDef(sortedCdfRecords, cdfRecordsPos, cpcMap)
      sortedSlotDefs.append(nextSlotDef)
    return (CCSDS.VP.StructDef(structName, sortedSlotDefs), cdfRecordsPos)
  # ---------------------------------------------------------------------------
  def createTcListDef(self, sortedCdfRecords, cdfRecordsPos, cpcMap):
    nextCdfRecord = sortedCdfRecords[cdfRecordsPos]
    lenParamName = nextCdfRecord.cdfPName
    lenDefaultValue = nextCdfRecord.cdfValue
    lenParamDef = self.createTcParamDef(lenParamName, lenDefaultValue, cpcMap)
    cdfRecordsPos += 1
    cdfRecordsEnd = cdfRecordsPos + nextCdfRecord.cdfGrpSize
    entryDef, cdfRecordsPos = self.createTcStructDef("", sortedCdfRecords, cdfRecordsPos, cdfRecordsEnd, cpcMap)
    return (CCSDS.VP.ListDef(lenParamDef, entryDef), cdfRecordsPos)
  # ---------------------------------------------------------------------------
  def createTcToplevelStructDef(self, structName, cdfMap, cpcMap):
    # try to find a variable packet definition
    try:
      cdfRecords = cdfMap[structName]
    except:
      LOG_WARNING("no variable packet definition " + structName +" in cdf.dat ---> dummy entry", "SPACE")
      cdfRecords = []
    # sort the related variable record definitions
    sortedCdfRecords = sorted(cdfRecords, key=lambda cdfRecord: cdfRecord.cdfBit)
    cdfRecordsPos = 0
    cdfRecordsEnd = len(sortedCdfRecords)
    structDef, cdfRecordsPos = self.createTcStructDef(structName, sortedCdfRecords, cdfRecordsPos, cdfRecordsEnd, cpcMap)
    return structDef
  # ---------------------------------------------------------------------------
  def createTCdefinitions(self, ccfMap, cpcMap, cdfMap):
    """helper method: create TC packet and parameter definitions from MIB tables"""
    tcPktDefs = []
    tcPktDefsNameMap = {}
    # step 1) create packet definitions
    for cName, ccfRecord in ccfMap.items():
      tcPktDef = self.createTCpktDef(ccfRecord, cdfMap, cpcMap)
      pktName = tcPktDef.pktName
      tcPktDefs.append(tcPktDef)
      tcPktDefsNameMap[pktName] = tcPktDef
      LOG("TC packet " + pktName + "(" + str(tcPktDef.pktAPID) + "," + str(tcPktDef.pktType) + "," + str(tcPktDef.pktSType) + ")", "SPACE")
    tcPktDefs.sort()
    self.definitionData.tcPktDefs = tcPktDefs
    self.definitionData.tcPktDefsNameMap = tcPktDefsNameMap
  # ---------------------------------------------------------------------------
  def createDefinitions(self):
    """
    creates the definition data:
    implementation of SPACE.IF.Definitions.createDefinitions
    """
    self.definitionData = DefinitionData()
    # read the mib tables and create the TM/TC definitions
    pidMap, picMap, tpcfMap, pcfMap, plfMap, ccfMap, cpcMap, cdfMap = SCOS.MIB.readAllTables()
    self.createTMdefinitions(pidMap, picMap, tpcfMap, pcfMap, plfMap)
    self.createTCdefinitions(ccfMap, cpcMap, cdfMap)
    d = time.localtime()
    self.definitionData.creationTime = "%04d.%02d.%02d %02d:%02d:%02d" % d[:6]
    # save the definitions
    fileName = self.definitionFileName
    try:
      file = open(fileName, "wb")
      pickle.dump(self.definitionData, file)
      file.close()
    except Exception as ex:
      LOG_ERROR("cannot save definitions: " + str(ex), "SPACE")
  # ---------------------------------------------------------------------------
  def initDefinitions(self):
    """
    initialise the definition data from file or MIB:
    implementation of SPACE.IF.Definitions.initDefinitions
    """
    if self.definitionData == None:
      # try to load the definition data
      fileName = self.definitionFileName
      try:
        os.stat(fileName)
        try:
          file = open(fileName, "rb")
          self.definitionData = pickle.load(file)
          file.close()
        except Exception as ex:
          LOG_ERROR("cannot load definitions: " + str(ex), "SPACE")
          self.createDefinitions()
      except:
        # definition file not present
        self.createDefinitions()
  # ---------------------------------------------------------------------------
  def getTMpktDefByIndex(self, index):
    """
    returns a TM packet definition:
    implementation of SPACE.IF.Definitions.getTMpktDefByIndex
    """
    # load or initialise on demand
    self.initDefinitions()
    if index < 0 or index > len(self.definitionData.tmPktDefs):
      return None
    return self.definitionData.tmPktDefs[index]
  # ---------------------------------------------------------------------------
  def getTMpktDefBySPID(self, spid):
    """
    returns a TM packet definition:
    implementation of SPACE.IF.Definitions.getTMpktDefBySPID
    """
    # load or initialise on demand
    self.initDefinitions()
    if spid in self.definitionData.tmPktDefsSpidMap:
      return self.definitionData.tmPktDefsSpidMap[spid]
    return None
  # ---------------------------------------------------------------------------
  def getSPIDbyPktName(self, name):
    """
    returns the packet SPID for a packet name:
    implementation of SPACE.IF.Definitions.getSPIDbyPktName
    """
    # load or initialise on demand
    self.initDefinitions()
    if name in self.definitionData.tmPktSpidNameMap:
      return self.definitionData.tmPktSpidNameMap[name]
    return -1
  # ---------------------------------------------------------------------------
  def getTMpktDefs(self):
    """
    returns the TM packet definitions:
    implementation of SPACE.IF.Definitions.getTMpktDefs
    """
    # load or initialise on demand
    self.initDefinitions()
    return self.definitionData.tmPktDefs
  # ---------------------------------------------------------------------------
  def getTMparamDefs(self):
    """
    returns the TM parameter definitions:
    implementation of SPACE.IF.Definitions.getTMparamDefs
    """
    # load or initialise on demand
    self.initDefinitions()
    return self.definitionData.tmParamDefs
  # ---------------------------------------------------------------------------
  def getTMpacketInjectData(self,
                            pktMnemonic,
                            params,
                            values,
                            dataField=None,
                            segmentationFlags=CCSDS.PACKET.UNSEGMENTED):
    """
    returns the data that are used for packet injection:
    implementation of SPACE.IF.Definitions.getTMpacketInjectData
    """
    pktSPID = self.getSPIDbyPktName(pktMnemonic)
    if pktSPID == -1:
      return None
    return SPACE.IF.TMpacketInjectData(pktSPID,
                                       pktMnemonic,
                                       params,
                                       values,
                                       dataField,
                                       segmentationFlags)
  # ---------------------------------------------------------------------------
  def getTMpacketInjectDataBySPID(self,
                                  spid,
                                  params,
                                  values,
                                  dataField=None,
                                  segmentationFlags=CCSDS.PACKET.UNSEGMENTED):
    """
    returns the data that are used for packet injection:
    implementation of SPACE.IF.Definitions.getTMpacketInjectDataBySPID
    """
    pktDef = self.getTMpktDefBySPID(spid)
    if pktDef == None:
      return None
    return SPACE.IF.TMpacketInjectData(spid,
                                       pktDef.pktName,
                                       params,
                                       values,
                                       dataField,
                                       segmentationFlags)
  # ---------------------------------------------------------------------------
  def getTCpktDefs(self):
    """
    returns the TC packet definitions:
    implementation of SPACE.IF.Definitions.getTCpktDefs
    """
    # load or initialise on demand
    self.initDefinitions()
    return self.definitionData.tcPktDefs
  # ---------------------------------------------------------------------------
  def getTCpktDefByIndex(self, index):
    """
    returns a TC packet definition:
    implementation of SPACE.IF.Definitions.getTCpktDefByIndex
    """
    # load or initialise on demand
    self.initDefinitions()
    if index < 0 or index > len(self.definitionData.tcPktDefs):
      return None
    return self.definitionData.tcPktDefs[index]
  # ---------------------------------------------------------------------------
  def getTCpktDefByName(self, name):
    """
    returns a TC packet definition:
    implementation of SPACE.IF.Definitions.getTCpktDefByName
    """
    # load or initialise on demand
    self.initDefinitions()
    if name in self.definitionData.tcPktDefsNameMap:
      return self.definitionData.tcPktDefsNameMap[name]
    return None
  # ---------------------------------------------------------------------------
  def getTCpacketInjectData(self,
                            pktMnemonic,
                            route,
                            dataField=None,
                            segmentationFlags=CCSDS.PACKET.UNSEGMENTED):
    """
    returns the data that are used for packet injection:
    implementation of SPACE.IF.Definitions.getTCpacketInjectData
    """
    if pktMnemonic not in self.definitionData.tcPktDefsNameMap:
      return None
    return SPACE.IF.TCpacketInjectData(pktMnemonic,
                                       route,
                                       dataField,
                                       segmentationFlags)

#############
# functions #
#############
def init():
  """initialise singleton(s)"""
  SPACE.IF.s_definitions = DefinitionsImpl()
# -----------------------------------------------------------------------------
def getBitWidth(paramPtc, paramPfc):
  """calculates the bit width based on the parameter definition in the MIB"""
  if paramPtc == 1:
    if paramPfc == 0:
      # unsigned integer (boolean parameter)
      return 1
  elif paramPtc == 2:
    if paramPfc <= 32:
      # unsigned integer (enumeration parameter)
      return paramPfc
  elif paramPtc == 3:
    # unsigned integer
    if paramPfc <= 12:
      return paramPfc + 4
    elif paramPfc == 13:
      return 24
    elif paramPfc == 14:
      return 32
    elif paramPfc == 15:
      # not supported by SCOS-2000
      return 48
    elif paramPfc == 16:
      # not supported by SCOS-2000
      return 64
  elif paramPtc == 4:
    # signed integer
    if paramPfc <= 12:
      return paramPfc + 4
    elif paramPfc == 13:
      return 24
    elif paramPfc == 14:
      return 32
    elif paramPfc == 15:
      # not supported by SCOS-2000
      return 48
    elif paramPfc == 16:
      # not supported by SCOS-2000
      return 64
  elif paramPtc == 5:
    # floating point
    if paramPfc == 1:
      # simple precision real (IEEE)
      return 32
    elif paramPfc == 2:
      # double precision real (IEEE)
      return 64
    elif paramPfc == 3:
      # simple precision real (MIL 1750A)
      return 32
    elif paramPfc == 4:
      # extended precision real (MIL 1750a)
      return 48
  elif paramPtc == 6:
    # bit string
    if paramPfc == 0:
      # variable bit string, not supported by SCOS-2000
      pass
    elif paramPfc <= 32:
      # fixed length bit strings, unsigned integer in SCOS-2000
      return paramPfc
  elif paramPtc == 7:
    # octet string
    if paramPfc == 0:
      # variable octet string, not supported by SCOS-2000 fixed TM
      # zero indicates variable length
      return 0
    else:
      # fixed length octet strings
      return paramPfc * 8
  elif paramPtc == 8:
    # ASCII string
    if paramPfc == 0:
      # variable ASCII string, not supported by SCOS-2000 fixed TM
      # zero indicates variable length
      return 0
    else:
      # fixed length ASCII strings
      return paramPfc * 8
  elif paramPtc == 9:
    # absolute time
    if paramPfc == 0:
      # variable length, not supported by SCOS-2000 TM
      pass
    elif paramPfc == 1:
      # CDS format, without microseconds
      return 48
    elif paramPfc == 2:
      # CDS format, with microseconds
      return 64
    elif paramPfc <= 6:
      # CUC format, 1st octet coarse time, 2nd - n-th octet for fine time
      return (paramPfc - 2) * 8
    elif paramPfc <= 10:
      # CUC format, 1st & 2nd octet coarse time, 3rd - n-th octet for fine time
      return (paramPfc - 5) * 8
    elif paramPfc <= 14:
      # CUC format, 1st - 3rd octet coarse time, 4th - n-th octet for fine time
      return (paramPfc - 8) * 8
    elif paramPfc <= 18:
      # CUC format, 1st - 4th octet coarse time, 5th - n-th octet for fine time
      return (paramPfc - 11) * 8
  elif paramPtc == 10:
    # relative time
    if paramPfc <= 2:
      # not used
      pass
    elif paramPfc <= 6:
      # CUC format, 1st octet coarse time, 2nd - n-th octet for fine time
      return (paramPfc - 2) * 8
    elif paramPfc <= 10:
      # CUC format, 1st & 2nd octet coarse time, 3rd - n-th octet for fine time
      return (paramPfc - 5) * 8
    elif paramPfc <= 14:
      # CUC format, 1st - 3rd octet coarse time, 4th - n-th octet for fine time
      return (paramPfc - 8) * 8
    elif paramPfc <= 18:
      # CUC format, 1st - 4th octet coarse time, 5th - n-th octet for fine time
      return (paramPfc - 11) * 8
  elif paramPtc == 11:
    # deduced parameter, N/A
    pass
  elif paramPtc == 13:
    # saved synthetic parameter, N/A
    pass
  # illegal ptc/pfc combination
  raise Exception("ptc/pfc combination " + str(paramPtc) + "/" + str(paramPfc) + " not supported")
# -----------------------------------------------------------------------------
def getIsBytePos(plfRecord):
  """
  Checks if the parameter is located byte aligned.
  This check is also performed for super-commutated parameters.
  """
  if plfRecord.plfOffbi != 0:
    return False
  # at least first occurence is byte aligned
  if plfRecord.plfNbocc == 1:
    return True
  # super-commutated parameter
  return ((plfRecord.plfLgocc % 8) == 0)
# -----------------------------------------------------------------------------
def getValueType(paramPtc, paramPfc, isBytePos=True):
  """Returns the type of a parameter"""
  # TODO: differentiate between absolute and relative time
  if paramPfc < 0:
    # not allowed --> exception will be raised
    pass
  if paramPtc == 1:
    # boolean parameter
    if paramPfc == 0:
      return UTIL.DU.BITS
  elif paramPtc == 2:
    # enumeration parameter
    if (paramPfc == 8) or (paramPfc == 16) or (paramPfc == 24) or (paramPfc == 32):
      if isBytePos:
        return UTIL.DU.UNSIGNED
      else:
        return UTIL.DU.BITS
    elif (paramPfc > 0) and (paramPfc < 32):
      return UTIL.DU.BITS
  elif paramPtc == 3:
    # unsigned integer
    if (paramPfc == 4) or (paramPfc == 12) or (paramPfc == 13) or (paramPfc == 14):
      if isBytePos:
        return UTIL.DU.UNSIGNED
      else:
        return UTIL.DU.BITS
    elif (paramPfc == 15) or (paramPfc == 16):
      # not supported by SCOS-2000
      if isBytePos:
        return UTIL.DU.UNSIGNED
    elif (paramPfc > 0) and (paramPfc < 12):
      return UTIL.DU.BITS
  elif paramPtc == 4:
    # signed integer
    if (paramPfc == 4) or (paramPfc == 12) or (paramPfc == 13) or (paramPfc == 14):
      if isBytePos:
        return UTIL.DU.SIGNED
      else:
        return UTIL.DU.SBITS
    elif (paramPfc == 15) or (paramPfc == 16):
      # not supported by SCOS-2000
      if isBytePos:
        return UTIL.DU.SIGNED
    elif (paramPfc > 0) and (paramPfc < 12):
      return UTIL.DU.SBITS
  elif paramPtc == 5:
    # floating point
    if (paramPfc == 1) or (paramPfc == 2):
      # simple/double precision real (IEEE)
      return UTIL.DU.FLOAT
    elif (paramPfc == 3) or (paramPfc == 4):
      # simple/extended precision real (MIL 1750A): not implemented
      pass
  elif paramPtc == 6:
    # bit string
    if paramPfc == 0:
      # variable bit string, not supported by SCOS-2000, not implemented
      pass
    elif (paramPfc == 8) or (paramPfc == 16) or (paramPfc == 24) or (paramPfc == 32):
      # fixed length bit strings, unsigned integer in SCOS-2000
      if isBytePos:
        return UTIL.DU.UNSIGNED
      else:
        return UTIL.DU.BITS
    elif (paramPfc > 0) and (paramPfc < 32):
      # fixed length bit strings, unsigned integer in SCOS-2000
      return UTIL.DU.BITS
  elif paramPtc == 7:
    # octet string
    if paramPfc == 0:
      # variable octet string, not supported by SCOS-2000 fixed TM
      return UTIL.DU.BYTES
    else:
      # fixed length octet strings
      return UTIL.DU.BYTES
  elif paramPtc == 8:
    # ASCII string
    if paramPfc == 0:
      # variable ASCII string, not supported by SCOS-2000 fixed TM
      return UTIL.DU.STRING
    else:
      # fixed length ASCII strings
      return UTIL.DU.STRING
  elif paramPtc == 9:
    # absolute time
    if paramPfc == 0:
      # variable length, not supported by SCOS-2000 TM
      pass
    elif (paramPfc == 1) or (paramPfc == 2):
      # CDS format
      return UTIL.DU.TIME
    elif (paramPfc >= 3) and (paramPfc <= 18):
      # CUC format
      return UTIL.DU.TIME
  elif paramPtc == 10:
    # relative time
    if paramPfc <= 2:
      # not used
      pass
    elif paramPfc <= 18:
      # CUC format
      return UTIL.DU.TIME
  elif paramPtc == 11:
    # deduced parameter, N/A
    pass
  elif paramPtc == 13:
    # saved synthetic parameter, N/A
    pass
  # illegal ptc/pfc combination
  raise Exception("ptc/pfc combination " + str(paramPtc) + "/" + str(paramPfc) + " not supported")
# -----------------------------------------------------------------------------
def getTimeFormat(paramPfc):
  """Returns the format of a time parameter"""
  if paramPfc == 1:
    # CDS format, without microseconds
    return CCSDS.TIME.TIME_FORMAT_CDS1
  elif paramPfc == 2:
    # CDS format, with microseconds
    return CCSDS.TIME.TIME_FORMAT_CDS2
  elif paramPfc == 15:
    # CUC format, 1st - 4th octet coarse time
    return TIME_FORMAT_CUC0
  elif paramPfc == 16:
    # CUC format, 1st - 4th octet coarse time, 5th octet for fine time
    return TIME_FORMAT_CUC1
  elif paramPfc == 17:
    # CUC format, 1st - 4th octet coarse time, 5th - 6th octet for fine time
    return TIME_FORMAT_CUC2
  elif paramPfc == 18:
    # CUC format, 1st - 4th octet coarse time, 5th - 7th octet for fine time
    return TIME_FORMAT_CUC3
  # illegal pfc value
  raise Exception("pfc value " + str(paramPfc) + " for time parameters not supported")
