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
# Supplement to TM/TC processing - Telemetry Recorder                         *
#******************************************************************************
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import SUPP.IF
import UTIL.TASK, UTIL.TCO, UTIL.TIME

###########
# classes #
###########
# =============================================================================
class PacketRecorder(SUPP.IF.TMrecorder):
  """Recorder of TM packets"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """default constructor"""
    self.tmPacketsFile = None
    self.tmPacketsNr = 0
  # ---------------------------------------------------------------------------
  def startRecording(self, recordFileName):
    """
    starts recording of TM packets,
    implementation of SUPP.IF.TMrecorder.startRecording
    """
    LOG_WARNING("startRecording(" + recordFileName + ")", "TM")
    try:
      self.tmPacketsFile = open(recordFileName, "w")
    except:
      LOG_ERROR("cannot open " + recordFileName, "TM")
      return False
    self.tmPacketsFile.write("##############################################\n")
    self.tmPacketsFile.write("# TM packet replay file with hex raw packets #\n")
    self.tmPacketsFile.write("##############################################\n")
    self.tmPacketsNr = 0
    UTIL.TASK.s_processingTask.notifyGUItask("PACKET_REC_STARTED")
  # ---------------------------------------------------------------------------
  def stopRecording(self):
    """
    stops recording of TM packets,
    implementation of SUPP.IF.TMrecorder.stopRecording
    """
    LOG_WARNING("startRecording", "TM")
    if self.tmPacketsFile != None:
      self.tmPacketsFile.close()
      self.tmPacketsFile = None
    UTIL.TASK.s_processingTask.notifyGUItask("PACKET_REC_STOPPED")
  # ---------------------------------------------------------------------------
  def isRecording(self):
    """
    returns recording status,
    implementation of SUPP.IF.TMrecorder.isRecording
    """
    return (self.tmPacketsFile != None)
  # ---------------------------------------------------------------------------
  def pushTMpacket(self, tmPacketDu, ertUTC):
    """
    consumes a telemetry packet,
    implementation of SUPP.IF.TMrecorder.pushTMpacket
    """
    if self.tmPacketsFile == None:
      return
    self.tmPacketsNr += 1
    LOG("record TM packet " + str(self.tmPacketsNr), "TM")
    self.tmPacketsFile.write("# packet " + str(self.tmPacketsNr) + "\n")
    if ertUTC:
      ertTime = UTIL.TCO.correlateToERTmissionEpoch(ertUTC)
      ertTimeStr = UTIL.TIME.getASDtimeStr(ertTime)
      self.tmPacketsFile.write(ertTimeStr + "\n")
    rawTmPacket = tmPacketDu.getBuffer()
    for byte in rawTmPacket:
      self.tmPacketsFile.write("%02X" % byte)
    self.tmPacketsFile.write("\n")

#############
# functions #
#############
def init():
  """initialise singleton(s)"""
  SUPP.IF.s_tmRecorder = PacketRecorder()
