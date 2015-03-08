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
# Space Simulation - Space Data Definitions                                   #
#******************************************************************************
import os, cPickle, time
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import CCSDS.PACKET
import PUS.PACKET
import SCOS.ENV, SCOS.MIB
import SPACE.IF

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

# =============================================================================
class DefinitionsImpl(SPACE.IF.Definitions):
  """Manager for definition data"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    self.definitionData = None
  # ---------------------------------------------------------------------------
  def createTMpktDef(self, pidRecord, picRecord, tpcfRecord):
    """creates a TM packet definition"""
    tmPktDef = SPACE.IF.TMpktDef();
    pktSize = None
    tmPktDef.pktSPID = pidRecord.pidSPID
    tmPktDef.pktIsVP = True
    if tpcfRecord == None:
      tmPktDef.pktName = "SPID_" + str(pidRecord.pidSPID)
    else:
      # remove white spaces and "&"
      tmPktDef.pktName = tpcfRecord.tpcfName.replace(" ", "_").replace("&", "_").replace(".", "_").replace("-", "_")
      if tpcfRecord.tpcfSize > 0:
        # fixed packet
        pktSize = tpcfRecord.tpcfSize
        tmPktDef.pktIsVP = False
    tmPktDef.pktDescr = pidRecord.pidDescr
    tmPktDef.pktAPID = pidRecord.pidAPID
    tmPktDef.pktType = pidRecord.pidType
    tmPktDef.pktSType = pidRecord.pidSType
    tmPktDef.pktDFHsize = pidRecord.pidDFHsize
    tmPktDef.pktHasDFhdr = pidRecord.pidDFHsize > 6
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
    # calculate size values which are common for fixed and variable packets
    if tmPktDef.pktIsVP:
      # pure variable packet
      tmPktDef.pktSPsize = CCSDS.PACKET.PRIMARY_HEADER_BYTE_SIZE + tmPktDef.pktDFHsize + SCOS.ENV.VPD_DATA_SPACE
      if tmPktDef.pktCheck:
        tmPktDef.pktSPsize += CCSDS.PACKET.CRC_BYTE_SIZE
      tmPktDef.pktS2Ksize = SCOS.ENV.SCOS_PACKET_HEADER_SIZE + tmPktDef.pktSPsize
    else:
      # fixed packet
      # Anomaly in the DLR MIB: the SCOS packet size defined in TPCF_SIZE
      # contains only the source packet size without the SCOS packet header.
      # This can be identified in most cases if the SCOS packet header size
      # is larger than the whole SCOS packet size
      if SCOS.ENV.SCOS_PACKET_HEADER_SIZE > pktSize:
        tmPktDef.pktSPsize = pktSize
        tmPktDef.pktS2Ksize = tmPktDef.pktSPsize + SCOS.ENV.SCOS_PACKET_HEADER_SIZE
      else:
        tmPktDef.pktS2Ksize = pktSize
        tmPktDef.pktSPsize = tmPktDef.pktS2Ksize - SCOS.ENV.SCOS_PACKET_HEADER_SIZE
    tmPktDef.pktSPDFsize = tmPktDef.pktSPsize - CCSDS.PACKET.PRIMARY_HEADER_BYTE_SIZE
    tmPktDef.pktSPDFdataSize = tmPktDef.pktSPDFsize
    if tmPktDef.pktHasDFhdr:
      tmPktDef.pktSPDFdataSize -= PUS.PACKET.TM_PACKET_DATAFIELD_HEADER_BYTE_SIZE
    if tmPktDef.pktCheck:
      tmPktDef.pktSPDFdataSize -= CCSDS.PACKET.CRC_BYTE_SIZE
    # raw value extractions
    tmPktDef.paramLinks = {}
    return tmPktDef
  # ---------------------------------------------------------------------------
  def createTMparamDef(self, pcfRecord, plfRecords, tmPktDefs):
    """creates a TM parameter definition"""
    tmParamDef = SPACE.IF.TMparamDef()
    tmParamDef.paramName = pcfRecord.pcfName.replace(" ", "_").replace("&", "_").replace(".", "_").replace("-", "_")
    tmParamDef.paramDescr = pcfRecord.pcfDescr
    tmParamDef.paramPtc = pcfRecord.pcfPtc
    tmParamDef.paramPfc = pcfRecord.pcfPfc
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
        tmPktDef = tmPktDefs[spid]
        paramToPacket = SPACE.IF.TMparamToPkt(tmParamDef, tmPktDef, plfRecord)
        tmParamDef.minCommutations = min(paramToPacket.locNbocc, tmParamDef.minCommutations)
        tmParamDef.maxCommutations = max(paramToPacket.locNbocc, tmParamDef.maxCommutations)
        tmPktDef.appendParamLink(paramToPacket)
      else:
        paramToPacket = SPACE.IF.TMparamToPkt(tmParamDef, None, plfRecord)
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
    for spid, pidRecord in pidMap.iteritems():
      picKey = pidRecord.picKey()
      # ignore packets with invalid datafield header size (e.g. for EnMAP)
      if pidRecord.pidDFHsize == 0:
        continue
      if picKey in picMap:
        picRecord = picMap[picKey]
      else:
        picRecord = None
      if spid in tpcfMap:
        tpcfRecord = tpcfMap[spid]
      else:
        tpcfRecord = None
      tmPktDef = self.createTMpktDef(pidRecord, picRecord, tpcfRecord)
      pktName = tmPktDef.pktName
      tmPktDefs.append(tmPktDef)
      tmPktDefsSpidMap[spid] = tmPktDef
      tmPktSpidNameMap[pktName.upper()] = spid
    tmPktDefs.sort()
    # step 2) create parameter definitions
    # pcfMap is the driving map for the join
    for paramName, pcfRecord in pcfMap.iteritems():
      if paramName in plfMap:
        plfRecords = plfMap[paramName]
      else:
        plfRecords = []
      tmParamDef = self.createTMparamDef(pcfRecord, plfRecords, tmPktDefsSpidMap)
      tmParamDefs.append(tmParamDef)
    tmParamDefs.sort()
    self.definitionData.tmPktDefs = tmPktDefs
    self.definitionData.tmPktDefsSpidMap = tmPktDefsSpidMap
    self.definitionData.tmPktSpidNameMap = tmPktSpidNameMap
    self.definitionData.tmParamDefs = tmParamDefs
  # ---------------------------------------------------------------------------
  def createDefinitions(self):
    """
    creates the definition data:
    implementation of SPACE.IF.Definitions.createDefinitions
    """
    self.definitionData = DefinitionData()
    # read the mib tables
    pidMap = SCOS.MIB.readTable("pid.dat")
    picMap = SCOS.MIB.readTable("pic.dat")
    tpcfMap = SCOS.MIB.readTable("tpcf.dat")
    pcfMap = SCOS.MIB.readTable("pcf.dat")
    plfMap = SCOS.MIB.readTable("plf.dat", uniqueKeys=False)
    self.createTMdefinitions(pidMap, picMap, tpcfMap, pcfMap, plfMap)
    d = time.localtime()
    self.definitionData.creationTime = "%04d.%02d.%02d %02d:%02d:%02d" % d[:6]
    # save the definitions
    fileName = SCOS.ENV.s_environment.definitionFileName()
    try:
      file = open(fileName, "w")
      cPickle.dump(self.definitionData, file)
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
      fileName = SCOS.ENV.s_environment.definitionFileName()
      try:
        os.stat(fileName)
        try:
          file = open(fileName, "r")
          self.definitionData = cPickle.load(file)
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
    upperName = name.upper()
    if upperName in self.definitionData.tmPktSpidNameMap:
      return self.definitionData.tmPktSpidNameMap[upperName]
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
  def getTMpacketInjectData(self, pktMnemonic, params, values):
    """
    returns the data that are used for packet injection:
    implementation of SPACE.IF.Definitions.getTMpacketInjectData
    """
    pktSPID = self.getSPIDbyPktName(pktMnemonic)
    if pktSPID == -1:
      return None
    return SPACE.IF.TMpacketInjectData(pktSPID, pktMnemonic, params, values)
  # ---------------------------------------------------------------------------
  def getTMpacketInjectDataBySPID(self, spid, params, values):
    """
    returns the data that are used for packet injection:
    implementation of SPACE.IF.Definitions.getTMpacketInjectDataBySPID
    """
    pktDef = self.getTMpktDefBySPID(spid)
    if pktDef == None:
      return None
    return SPACE.IF.TMpacketInjectData(spid, pktDef.pktName, params, values)

#############
# functions #
#############
def init():
  # initialise singleton(s)
  SPACE.IF.s_definitions = DefinitionsImpl()
