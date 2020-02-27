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
import cPickle as pickle
import os, time
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import CCSDS.DU, CCSDS.PACKET, CCSDS.TIME
import PUS.PACKET, PUS.PKTID, PUS.VP
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
    self.tmPktIdentificator = None
    self.tmParamDefs = None
    self.tcPktDefs = None
    self.tcPktDefsNameMap = None
    self.tcPktIdentificator = None

# =============================================================================
class DefinitionsImpl(SPACE.IF.Definitions):
  """Manager for definition data"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    self.definitionFileName = SCOS.ENV.s_environment.getRuntimeRoot() + \
        "/testbin/testdata.sim"
    self.definitionData = None
    self.tmParamLengthBytes = int(UTIL.SYS.s_configuration.TM_PARAM_LENGTH_BYTES)
    self.tcParamLengthBytes = int(UTIL.SYS.s_configuration.TC_PARAM_LENGTH_BYTES)
  # ---------------------------------------------------------------------------
  def getDefinitionFileName(self):
    """get the testdata.sim file name incl. path"""
    return self.definitionFileName
  # ---------------------------------------------------------------------------
  def createTMpktDef(self, pidRecord, picRecord, tpcfRecord, vpdMap, pcfMap):
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
    tmPktDef.tmStructDef = self.createTmToplevelStructDef(pidRecord.pidTPSD, vpdMap, pcfMap)
    return tmPktDef
  # ---------------------------------------------------------------------------
  def createTMfixedParamDef(self, pcfRecord, plfRecords, tmPktDefs):
    """creates a TM fixed parameter definition"""
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
        except Exception, ex:
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
  def createTmVarParamDef(self, paramName, pcfMap):
    isReadOnly = False
    try:
      pcfRecord = pcfMap[paramName]
      paramPtc = pcfRecord.pcfPtc
      paramPfc = pcfRecord.pcfPfc
      try:
        paramType = getValueType(paramPtc, paramPfc)
        bitWidth = getBitWidth(paramPtc, paramPfc)
        defaultValue = pcfRecord.pcfParVal
        if defaultValue == "" and UTIL.DU.isNumber(paramType):
          defaultValue = 0
      except Exception, ex:
        # inconsistency
        LOG_WARNING("param " + paramName + ": " + str(ex) + " ---> dummy type", "SPACE")
        paramType = UTIL.DU.UNSIGNED
        bitWidth = 8
        defaultValue = 0
    except:
      LOG_WARNING("TM param name " + paramName + " not found in pcf.dat ---> dummy param", "SPACE")
      paramName = "dummy"
      paramType = UTIL.DU.UNSIGNED
      bitWidth = 8
      defaultValue = 0
    # special handling of time parameters
    if paramType == UTIL.DU.TIME:
      # TODO: differentiate between absolute and relative time
      try:
        timeFormat = getTimeFormat(paramPfc)
        return PUS.VP.TimeParamDef(paramName,
                                   timeFormat,
                                   defaultValue,
                                   isReadOnly)
      except Exception, ex:
        # inconsistency
        LOG_WARNING("param " + paramName + ": " + str(ex) + " ---> dummy type", "SPACE")
        paramType = UTIL.DU.UNSIGNED
        bitWidth = 8
        defaultValue = 0
    # special handling of variable size parameters
    if bitWidth == 0:
      # TODO: consider also information in the MIB
      lengthBytes = self.tcParamLengthBytes
      return PUS.VP.VariableParamDef(paramName,
                                     paramType,
                                     lengthBytes,
                                     defaultValue,
                                     isReadOnly)
    # default handling of normal parameters
    return PUS.VP.SimpleParamDef(paramName,
                                 paramType,
                                 bitWidth,
                                 defaultValue,
                                 isReadOnly)
  # ---------------------------------------------------------------------------
  def createTmSlotDef(self, sortedVpdRecords, vpdRecordsPos, pcfMap):
    nextVpdRecord = sortedVpdRecords[vpdRecordsPos]
    slotName = nextVpdRecord.vpdDisDesc
    isReadOnly = False
    # TODO: consider also fixed areas that don't have a related PCF record,
    #       this is defined via vpdFixRep != 0
    if nextVpdRecord.vpdGrpSize > 0:
      # group repeater definition
      childDef, vpdRecordsPos = self.createTmListDef(sortedVpdRecords, vpdRecordsPos, pcfMap)
    else:
      # parameter definition
      paramName = nextVpdRecord.vpdName
      childDef = self.createTmVarParamDef(paramName, pcfMap)
      vpdRecordsPos += 1
    return (PUS.VP.SlotDef(slotName, childDef), vpdRecordsPos)
  # ---------------------------------------------------------------------------
  def createTmStructDef(self, structName, sortedVpdRecords, vpdRecordsPos, vpdRecordsEnd, pcfMap):
    sortedSlotDefs = []
    while vpdRecordsPos < vpdRecordsEnd:
      nextSlotDef, vpdRecordsPos = self.createTmSlotDef(sortedVpdRecords, vpdRecordsPos, pcfMap)
      sortedSlotDefs.append(nextSlotDef)
    return (PUS.VP.StructDef(structName, sortedSlotDefs), vpdRecordsPos)
  # ---------------------------------------------------------------------------
  def createTmListDef(self, sortedVpdRecords, vpdRecordsPos, pcfMap):
    nextVpdRecord = sortedVpdRecords[vpdRecordsPos]
    lenParamName = nextVpdRecord.vpdName
    lenParamDef = self.createTmVarParamDef(lenParamName, pcfMap)
    vpdRecordsPos += 1
    vpdRecordsEnd = vpdRecordsPos + nextVpdRecord.vpdGrpSize
    entryDef, vpdRecordsPos = self.createTmStructDef("", sortedVpdRecords, vpdRecordsPos, vpdRecordsEnd, pcfMap)
    return (PUS.VP.ListDef(lenParamDef, entryDef), vpdRecordsPos)
  # ---------------------------------------------------------------------------
  def createTmToplevelStructDef(self, structID, vpdMap, pcfMap):
    structName = str(structID)
    # try to find a variable packet definition
    try:
      vpdRecords = vpdMap[structID]
    except:
      vpdRecords = []
    # sort the related variable record definitions
    sortedVpdRecords = sorted(vpdRecords, key=lambda vpdRecord: vpdRecord.vpdPos)
    vpdRecordsPos = 0
    vpdRecordsEnd = len(sortedVpdRecords)
    structDef, vpdRecordsPos = self.createTmStructDef(structName, sortedVpdRecords, vpdRecordsPos, vpdRecordsEnd, pcfMap)
    return structDef
  # ---------------------------------------------------------------------------
  def createTMdefinitions(self, pidMap, picMap, tpcfMap, pcfMap, plfMap, vpdMap):
    """helper method: create TM packet and parameter definitions from MIB tables"""
    tmPktDefs = []
    tmPktDefsSpidMap = {}
    tmPktSpidNameMap = {}
    tmParamDefs = []
    tmPktIdentificator = PUS.PKTID.PacketIdentificator()
    # step 1) create packet definitions and packet ID records
    # pidMap is the driving map for the join
    for spid, pidRecord in pidMap.iteritems():
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
      tmPktDef = self.createTMpktDef(pidRecord, picRecord, tpcfRecord, vpdMap, pcfMap)
      pktName = tmPktDef.pktName
      tmPktDefs.append(tmPktDef)
      tmPktDefsSpidMap[spid] = tmPktDef
      tmPktSpidNameMap[pktName] = spid
      if pidRecord.pidTPSD != -1:
        statusMessage += ", variable"
      LOG("TM packet " + pktName + "(" + str(spid) + "), " + statusMessage, "SPACE")
      # create the packet ID record for the packet identification
      apid = pidRecord.pidAPID
      serviceType = pidRecord.pidType
      serviceSubType = pidRecord.pidSType
      pi1 = pidRecord.pidPI1
      if pi1 <= 0:
        pi1 = None
      pi2 = pidRecord.pidPI2
      if pi2 <= 0:
        pi2 = None
      packetID = spid
      tmPktIdentificator.addPacketIDrecord(
        apid,
        serviceType,
        serviceSubType,
        pi1,
        pi2,
        packetID)
    tmPktDefs.sort()
    # step 2) create parameter definitions
    # pcfMap is the driving map for the join
    for paramName, pcfRecord in pcfMap.iteritems():
      if paramName in plfMap:
        plfRecords = plfMap[paramName]
      else:
        plfRecords = []
      try:
        tmParamDef = self.createTMfixedParamDef(pcfRecord, plfRecords, tmPktDefsSpidMap)
      except Exception, ex:
        # inconsistency
        LOG_WARNING("param " + paramName + ": " + str(ex) + " ---> ignored", "SPACE")
        continue
      tmParamDefs.append(tmParamDef)
    tmParamDefs.sort()
    # step 3) update packet definitions
    # tmPktDefs is the driving list for the post processing
    for tmPktDef in tmPktDefs:
      tmPktDef.updateSPsize()
    # step 4) update the packet key field records for the packet identification
    # picMap is the driving map
    for picKey, picRecord in picMap.iteritems():
      apid = picRecord.picAPID
      if apid == -1:
        apid = None
      serviceType = picRecord.picType
      serviceSubType = picRecord.picSType
      pi1bitPos = picRecord.picPI1off
      if pi1bitPos == -1:
        pi1bitPos = None
        pi1bitSize = None
      else:
        pi1bitSize = picRecord.picPI1wid
      pi2bitPos = picRecord.picPI2off
      if pi2bitPos == -1:
        pi2bitPos = None
        pi2bitSize = None
      else:
        pi2bitSize = picRecord.picPI2wid
      tmPktIdentificator.addKeyFieldRecord(
        apid,
        serviceType,
        serviceSubType,
        pi1bitPos,
        pi1bitSize,
        pi2bitPos,
        pi2bitSize)
    # step 5) update the global container attributes
    self.definitionData.tmPktDefs = tmPktDefs
    self.definitionData.tmPktDefsSpidMap = tmPktDefsSpidMap
    self.definitionData.tmPktSpidNameMap = tmPktSpidNameMap
    self.definitionData.tmPktIdentificator = tmPktIdentificator
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
    # TODO: use the correct values from the MIB or from the configuration
    tcPktDef.pktDFHsize = 4
    tcPktDef.pktHasDFhdr = True
    tcPktDef.pktCheck = True
    tcPktDef.pktSPsize = 16
    tcPktDef.pktSPDFsize = 10
    tcPktDef.pktSPDFdataSize = 6
    tcPktDef.tcStructDef = self.createTcToplevelStructDef(tcPktDef.pktName, cdfMap, cpcMap)
    return tcPktDef
  # ---------------------------------------------------------------------------
  def createTcParamDef(self, paramName, defaultValue, cpcMap, isReadOnly):
    try:
      cpcRecord = cpcMap[paramName]
      paramPtc = cpcRecord.cpcPtc
      paramPfc = cpcRecord.cpcPfc
      try:
        paramType = getValueType(paramPtc, paramPfc)
        bitWidth = getBitWidth(paramPtc, paramPfc)
        if defaultValue == "":
          defaultValue = cpcRecord.cpcDefVal
      except Exception, ex:
        # inconsistency
        LOG_WARNING("param " + paramName + ": " + str(ex) + " ---> dummy type", "SPACE")
        paramType = UTIL.DU.UNSIGNED
        bitWidth = 8
        defaultValue = 0
    except:
      LOG_WARNING("TC param name " + paramName + " not found in cpc.dat ---> dummy param", "SPACE")
      paramName = "dummy"
      paramType = UTIL.DU.UNSIGNED
      bitWidth = 8
      defaultValue = 0
    # special handling of time parameters
    if paramType == UTIL.DU.TIME:
      # TODO: differentiate between absolute and relative time
      try:
        timeFormat = getTimeFormat(paramPfc)
        return PUS.VP.TimeParamDef(paramName,
                                   timeFormat,
                                   defaultValue,
                                   isReadOnly)
      except Exception, ex:
        # inconsistency
        LOG_WARNING("param " + paramName + ": " + str(ex) + " ---> dummy type", "SPACE")
        paramType = UTIL.DU.UNSIGNED
        bitWidth = 8
        defaultValue = 0
    # special handling of variable size parameters
    if bitWidth == 0:
      # TODO: consider also information in the MIB
      lengthBytes = self.tcParamLengthBytes
      return PUS.VP.VariableParamDef(paramName,
                                     paramType,
                                     lengthBytes,
                                     defaultValue,
                                     isReadOnly)
    # default handling of normal parameters
    return PUS.VP.SimpleParamDef(paramName,
                                 paramType,
                                 bitWidth,
                                 defaultValue,
                                 isReadOnly)
  # ---------------------------------------------------------------------------
  def createTcSlotDef(self, sortedCdfRecords, cdfRecordsPos, cpcMap):
    nextCdfRecord = sortedCdfRecords[cdfRecordsPos]
    slotName = nextCdfRecord.cdfDescr
    isReadOnly = (nextCdfRecord.cdfElType != "E")
    # TODO: consider also fixed areas that don't have a related CPC record,
    #       this is defined via cdfElType == "A"
    if nextCdfRecord.cdfGrpSize > 0:
      # group repeater definition
      childDef, cdfRecordsPos = self.createTcListDef(sortedCdfRecords, cdfRecordsPos, cpcMap, isReadOnly)
    else:
      # parameter definition
      paramName = nextCdfRecord.cdfPName
      defaultValue = nextCdfRecord.cdfValue
      childDef = self.createTcParamDef(paramName, defaultValue, cpcMap, isReadOnly)
      cdfRecordsPos += 1
    return (PUS.VP.SlotDef(slotName, childDef), cdfRecordsPos)
  # ---------------------------------------------------------------------------
  def createTcStructDef(self, structName, sortedCdfRecords, cdfRecordsPos, cdfRecordsEnd, cpcMap):
    sortedSlotDefs = []
    while cdfRecordsPos < cdfRecordsEnd:
      nextSlotDef, cdfRecordsPos = self.createTcSlotDef(sortedCdfRecords, cdfRecordsPos, cpcMap)
      sortedSlotDefs.append(nextSlotDef)
    return (PUS.VP.StructDef(structName, sortedSlotDefs), cdfRecordsPos)
  # ---------------------------------------------------------------------------
  def createTcListDef(self, sortedCdfRecords, cdfRecordsPos, cpcMap, isReadOnly):
    nextCdfRecord = sortedCdfRecords[cdfRecordsPos]
    lenParamName = nextCdfRecord.cdfPName
    lenDefaultValue = nextCdfRecord.cdfValue
    lenParamDef = self.createTcParamDef(lenParamName, lenDefaultValue, cpcMap, isReadOnly)
    cdfRecordsPos += 1
    cdfRecordsEnd = cdfRecordsPos + nextCdfRecord.cdfGrpSize
    entryDef, cdfRecordsPos = self.createTcStructDef("", sortedCdfRecords, cdfRecordsPos, cdfRecordsEnd, cpcMap)
    return (PUS.VP.ListDef(lenParamDef, entryDef), cdfRecordsPos)
  # ---------------------------------------------------------------------------
  def createTcToplevelStructDef(self, structName, cdfMap, cpcMap):
    # try to find a variable packet definition
    try:
      cdfRecords = cdfMap[structName]
    except:
      LOG_WARNING("no variable packet definition " + structName + " in cdf.dat ---> dummy entry", "SPACE")
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
    tcPktIdentificator = PUS.PKTID.PacketIdentificator()
    # step 1) create packet definitions and records for the packet identification
    for cName, ccfRecord in ccfMap.items():
      tcPktDef = self.createTCpktDef(ccfRecord, cdfMap, cpcMap)
      pktName = tcPktDef.pktName
      tcPktDefs.append(tcPktDef)
      tcPktDefsNameMap[pktName] = tcPktDef
      # create the records for the packet identification:
      # the packet must be a PUS packet
      serviceType = tcPktDef.pktType
      serviceSubType = tcPktDef.pktSType
      if serviceType <= 0 or serviceSubType <= 0:
        LOG("TC packet " + pktName + "(" + str(tcPktDef.pktAPID) + "," + str(tcPktDef.pktType) + "," + str(tcPktDef.pktSType) + ")", "SPACE")
        continue
      apid = tcPktDef.pktAPID
      packetID = tcPktDef.pktName
      pi1 = None
      pi1bitPos = None
      pi1bitSize = None
      pi2 = None
      pi2bitPos = None
      pi2bitSize = None
      # PI1 or PI2 can only be used if the packet has a structure definition
      if tcPktDef.tcStructDef != None:
        # try to identify the PI1:
        # this must be the first parameter and it must be constant
        toplevelSlots = tcPktDef.tcStructDef.slotDefs
        if len(toplevelSlots) >= 1:
          slot1Def = toplevelSlots[0]
          childDef = slot1Def.childDef
          childType = type(childDef)
          if childType == PUS.VP.SimpleParamDef and childDef.isReadOnly:
            paramType = childDef.getParamType()
            if paramType == UTIL.DU.BITS or paramType == UTIL.DU.UNSIGNED:
              pi1 = int(childDef.defaultValue)
              pi1bytePos = CCSDS.PACKET.PRIMARY_HEADER_BYTE_SIZE + tcPktDef.pktDFHsize
              pi1bitPos = pi1bytePos << 3
              pi1bitSize = childDef.bitWidth
              tcPktDef.pktPI1off = pi1bitPos
              tcPktDef.pktPI1wid = pi1bitSize
              tcPktDef.pktPI1val = pi1
        # try to identify the PI2:
        # this must be the second parameter and it must be constant
        if pi1 != None and len(toplevelSlots) >= 2:
          slot2Def = toplevelSlots[1]
          childDef = slot2Def.childDef
          childType = type(childDef)
          if childType == PUS.VP.SimpleParamDef and childDef.isReadOnly:
            paramType = childDef.getParamType()
            if paramType == UTIL.DU.BITS or paramType == UTIL.DU.UNSIGNED:
              pi2 = int(childDef.defaultValue)
              pi2bytePos = (pi2bitPos + pi2bitSize + 7) >> 3
              pi2bitPos = pi2bytePos << 3
              pi2bitSize = childDef.bitWidth
              tcPktDef.pktPI2off = pi2bitPos
              tcPktDef.pktPI2wid = pi2bitSize
              tcPktDef.pktPI2val = pi2
      # add records for the packet identification
      LOG("TC packet " + pktName + "(" + str(apid) + "," + str(serviceType) + "," + str(serviceSubType) + "," + str(pi1) + "," + str(pi2) + ")", "SPACE")
      try:
        tcPktIdentificator.addPacketIDrecord(
          apid,
          serviceType,
          serviceSubType,
          pi1,
          pi2,
          packetID)
        tcPktIdentificator.addKeyFieldRecord(
          apid,
          serviceType,
          serviceSubType,
          pi1bitPos,
          pi1bitSize,
          pi2bitPos,
          pi2bitSize)
      except Exception, ex:
        LOG_WARNING("Packet " + pktName + " cannot be explicitly used for packet identification", "SPACE")
        LOG_WARNING(str(ex), "SPACE")
    tcPktDefs.sort()
    # step 2) update the global container attributes
    self.definitionData.tcPktDefs = tcPktDefs
    self.definitionData.tcPktDefsNameMap = tcPktDefsNameMap
    self.definitionData.tcPktIdentificator = tcPktIdentificator
  # ---------------------------------------------------------------------------
  def createDefinitions(self):
    """
    creates the definition data:
    implementation of SPACE.IF.Definitions.createDefinitions
    """
    self.definitionData = DefinitionData()
    # read the mib tables and create the TM/TC definitions
    pidMap, picMap, tpcfMap, pcfMap, plfMap, vpdMap, ccfMap, cpcMap, cdfMap = SCOS.MIB.readAllTables()
    self.createTMdefinitions(pidMap, picMap, tpcfMap, pcfMap, plfMap, vpdMap)
    self.createTCdefinitions(ccfMap, cpcMap, cdfMap)
    d = time.localtime()
    self.definitionData.creationTime = "%04d.%02d.%02d %02d:%02d:%02d" % d[:6]
    # save the definitions
    fileName = self.definitionFileName
    try:
      file = open(fileName, "w")
      pickle.dump(self.definitionData, file)
      file.close()
    except Exception, ex:
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
          file = open(fileName, "r")
          self.definitionData = pickle.load(file)
          file.close()
        except Exception, ex:
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
                            tmStruct,
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
                                       tmStruct,
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
                                       tmStruct,
                                       dataField,
                                       segmentationFlags)
  # ---------------------------------------------------------------------------
  def getTMpacketKey(self, tmPacketDu):
    """
    retrieves the SPID from the TM packet data unit:
    implementation of SPACE.IF.Definitions.getTMpacketKey
    """
    return self.definitionData.tmPktIdentificator.getPacketKey(tmPacketDu)
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
                            tcStruct):
    """
    returns the data that are used for packet injection:
    implementation of SPACE.IF.Definitions.getTCpacketInjectData
    """
    if pktMnemonic not in self.definitionData.tcPktDefsNameMap:
      return None
    return SPACE.IF.TCpacketInjectData(pktMnemonic,
                                       route,
                                       tcStruct)
  # ---------------------------------------------------------------------------
  def getTCpacketKey(self, tcPacketDu):
    """
    retrieves the TC packet name from the TC packet data unit:
    implementation of SPACE.IF.Definitions.getTCpacketKey
    """
    return self.definitionData.tcPktIdentificator.getPacketKey(tcPacketDu)

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
