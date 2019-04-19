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
# SCOS - Mission Database (MIB) handling                                      *
# implements (partly) egos-mcs-s2k-icd-0001-version69_signed.pdf              *
#******************************************************************************
import SCOS.ENV

###########
# classes #
###########
# =============================================================================
class PIDrecord:
  """MIB record from pid.dat"""
  # ---------------------------------------------------------------------------
  def __init__(self, fields):
    """initialise selected attributes from the record"""
    self.pidType = int(fields[0])
    self.pidSType = int(fields[1])
    self.pidAPID = int(fields[2])
    self.pidPI1 = int(fields[3])
    self.pidPI2 = int(fields[4])
    self.pidSPID = int(fields[5])
    self.pidDescr = fields[6]
    self.pidTPDS = int(fields[8])
    self.pidDFHsize = int(fields[9])
    self.pidCheck = bool(int((fields[13]+"0")[0]))
  # ---------------------------------------------------------------------------
  def key(self):
    """record key"""
    return self.pidSPID
  # ---------------------------------------------------------------------------
  def picKey(self):
    """foreign key to PICrecord"""
    return str([self.pidType, self.pidSType, self.pidAPID])
  # ---------------------------------------------------------------------------
  def picAlternateKey(self):
    """foreign key to PICrecord"""
    return str([self.pidType, self.pidSType, -1])

# =============================================================================
class PICrecord:
  """MIB record from pic.dat"""
  # ---------------------------------------------------------------------------
  def __init__(self, fields):
    """initialise selected attributes from the record"""
    self.picType = int(fields[0])
    self.picSType = int(fields[1])
    self.picPI1off = int(fields[2])
    self.picPI1wid = int(fields[3])
    self.picPI2off = int(fields[4])
    self.picPI2wid = int(fields[5])
    if len(fields) >= 7:
      # SCOS 5 supports an additional field with APID
      # note: there might also a dummy entry with a line break
      try:
        self.picAPID = int(fields[6])
      except:
        self.picAPID = -1
    else:
      # SCOS 3.1
      self.picAPID = -1
  # ---------------------------------------------------------------------------
  def key(self):
    """record key"""
    return str([self.picType, self.picSType, self.picAPID])

# =============================================================================
class TPCFrecord:
  """MIB record from pid.dat"""
  # ---------------------------------------------------------------------------
  def __init__(self, fields):
    """initialise selected attributes from the record"""
    self.tpcfSPID = int(fields[0])
    self.tpcfName = fields[1]
    if len(fields) >= 3:
      # optional field with length
      # note: there might also a dummy entry with a line break
      try:
        self.tpcfSize = int(fields[2])
      except:
        self.tpcfSize = 0
    else:
      # no optional field with length
      self.tpcfSize = 0
  # ---------------------------------------------------------------------------
  def key(self):
    """record key"""
    return self.tpcfSPID

# =============================================================================
class PCFrecord:
  """MIB record from pcf.dat"""
  # ---------------------------------------------------------------------------
  def __init__(self, fields):
    """initialise selected attributes from the record"""
    self.pcfName = fields[0]
    self.pcfDescr = fields[1]
    self.pcfPtc = int(fields[4])
    self.pcfPfc = int(fields[5])
  # ---------------------------------------------------------------------------
  def key(self):
    """record key"""
    return self.pcfName

# =============================================================================
class PLFrecord:
  """MIB record from plf.dat"""
  # ---------------------------------------------------------------------------
  def __init__(self, fields):
    """initialise selected attributes from the record"""
    self.plfName = fields[0]
    self.plfSPID = int(fields[1])
    self.plfOffby = int(fields[2])
    self.plfOffbi = int(fields[3])
    # fields could be empty
    plfNbocc = fields[4]
    if plfNbocc == "":
      self.plfNbocc = 1
    else:
      self.plfNbocc = int(plfNbocc)
    plfLgocc = fields[5]
    if plfLgocc == "":
      self.plfLgocc = 0
    else:
      self.plfLgocc = int(plfLgocc)
  # ---------------------------------------------------------------------------
  def key(self):
    """record key"""
    return self.plfName

# =============================================================================
class VPDrecord:
  """MIB record from vpd.dat"""
  # ---------------------------------------------------------------------------
  def __init__(self, fields):
    """initialise selected attributes from the record"""
    self.vpdTPSD = int(fields[0])
    self.vpdPos = int(fields[1])
    self.vpdName = fields[2]
    # this field could be empty
    vpdGrpSize = fields[3]
    if vpdGrpSize == "":
      self.vpdGrpSize = 0
    else:
      self.vpdGrpSize = int(vpdGrpSize)
  # ---------------------------------------------------------------------------
  def key(self):
    """record key"""
    return self.vpdTPSD

# =============================================================================
class CCFrecord:
  """MIB record from ccf.dat"""
  # ---------------------------------------------------------------------------
  def __init__(self, fields):
    """initialise selected attributes from the record"""
    self.ccfCName = fields[0]
    self.ccfDescr = fields[1]
    self.ccfDescr2 = fields[2]
    ccfType = fields[6]
    if ccfType == "":
      self.ccfType = -1
    else:
      self.ccfType = int(ccfType)
    ccfSType = fields[7]
    if ccfSType == "":
      self.ccfSType = -1
    else:
      self.ccfSType = int(ccfSType)
    self.ccfAPID = int(fields[8])
    self.ccfNPars = int(fields[9])
  # ---------------------------------------------------------------------------
  def key(self):
    """record key"""
    return self.ccfCName

# =============================================================================
class CPCrecord:
  """MIB record from pcp.dat"""
  # ---------------------------------------------------------------------------
  def __init__(self, fields):
    """initialise selected attributes from the record"""
    self.cpcPName = fields[0]
    self.cpcDescr = fields[1]
    self.cpcPtc = int(fields[2])
    self.cpcPfc = int(fields[3])
    self.cpcDefVal = fields[12]
  # ---------------------------------------------------------------------------
  def key(self):
    """record key"""
    return self.cpcPName

# =============================================================================
class CDFrecord:
  """MIB record from cdf.dat"""
  # ---------------------------------------------------------------------------
  def __init__(self, fields):
    """initialise selected attributes from the record"""
    self.cdfCName = fields[0]
    self.cdfElType = fields[1]
    self.cdfDescr = fields[2]
    self.cdfBit = int(fields[4])
    # this field could be empty
    cdfGrpSize = fields[5]
    if cdfGrpSize == "":
      self.cdfGrpSize = 0
    else:
      self.cdfGrpSize = int(cdfGrpSize)
    self.cdfPName = fields[6]
    self.cdfValue = fields[8]
  # ---------------------------------------------------------------------------
  def key(self):
    """record key"""
    return self.cdfCName

#############
# functions #
#############
# -----------------------------------------------------------------------------
def getMinFieldNr(tableName):
  """helper function: returns the minimun number of record fields"""
  if tableName == "pid.dat":
    return 14
  if tableName == "pic.dat":
    return 6
  if tableName == "tpcf.dat":
    return 2
  if tableName == "pcf.dat":
    return 6
  if tableName == "plf.dat":
    return 6
  if tableName == "vpd.dat":
    return 4
  if tableName == "ccf.dat":
    return 6
  if tableName == "cpc.dat":
    return 13
  if tableName == "cdf.dat":
    return 9
  raise Exception("invalid table name: " + tableName)

# -----------------------------------------------------------------------------
def createRecord(tableName, fields):
  """helper function: factory function"""
  if tableName == "pid.dat":
    return PIDrecord(fields)
  if tableName == "pic.dat":
    return PICrecord(fields)
  if tableName == "tpcf.dat":
    return TPCFrecord(fields)
  if tableName == "pcf.dat":
    return PCFrecord(fields)
  if tableName == "plf.dat":
    return PLFrecord(fields)
  if tableName == "vpd.dat":
    return VPDrecord(fields)
  if tableName == "ccf.dat":
    return CCFrecord(fields)
  if tableName == "cpc.dat":
    return CPCrecord(fields)
  if tableName == "cdf.dat":
    return CDFrecord(fields)
  raise Exception("invalid table name: " + tableName)

# -----------------------------------------------------------------------------
def readTable(tableName, uniqueKeys = True):
  """Reads a MIB table"""
  # getMinFieldNr raise an exception in case on an invalid table name
  # ---> used for consistency check
  # ---> the result value is used later on in this function
  minFieldNr = getMinFieldNr(tableName)
  mibDir = SCOS.ENV.s_environment.mibDir()
  tableFile = open(mibDir + "/" + tableName)
  tableFileContents = tableFile.readlines()
  tableFile.close()
  tableMap = {}
  lineNr = 1
  for line in tableFileContents:
    try:
      # tab separated table, remove line break
      fields = line[:-1].split("\t")
      if len(fields) < minFieldNr:
        raise Exception(tableName + ": line " + str(lineNr) + " has wrong structure")
      record = createRecord(tableName, fields)
      key = record.key()
      if uniqueKeys:
        if key in tableMap:
          raise Exception(tableName + ": multiple records assigned for key " + str(key))
        tableMap[key] = record
      else:
        # multiple keys allowed ---> use a list for all records with same key
        if not key in tableMap:
          # first record with this key
          tableMap[key] = []
        tableMap[key].append(record)
      lineNr += 1
    except Exception, ex:
      raise Exception(tableName + ": line " + str(lineNr) + ": " + str(ex))
  return tableMap

# -----------------------------------------------------------------------------
def readAllTables():
  """Reads all MIB tables"""
  pidMap = SCOS.MIB.readTable("pid.dat")
  picMap = SCOS.MIB.readTable("pic.dat")
  tpcfMap = SCOS.MIB.readTable("tpcf.dat")
  pcfMap = SCOS.MIB.readTable("pcf.dat")
  plfMap = SCOS.MIB.readTable("plf.dat", uniqueKeys=False)
  vpdMap = SCOS.MIB.readTable("vpd.dat", uniqueKeys=False)
  ccfMap = SCOS.MIB.readTable("ccf.dat")
  cpcMap = SCOS.MIB.readTable("cpc.dat")
  cdfMap = SCOS.MIB.readTable("cdf.dat", uniqueKeys=False)
  return (pidMap, picMap, tpcfMap, pcfMap, plfMap, vpdMap, ccfMap, cpcMap, cdfMap)
