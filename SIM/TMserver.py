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
# NCTRS TC server                                                             *
#******************************************************************************
import sys
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import GRND.CRYOSATDU, GRND.IF, GRND.NCTRS, GRND.NCTRSDU
import SPACE.OBC
import UTIL.DU, UTIL.SYS, UTIL.TASK, UTIL.TIME

###########
# classes #
###########
# =============================================================================
class TMsender(GRND.NCTRS.TMsender, GRND.IF.TMmcsLink):
  """Subclass of GRND.NCTRS.TMsender and SPACE.OBC.TMsender"""
  # ---------------------------------------------------------------------------
  def __init__(self, portNr, nctrsTMfields):
    """Initialise attributes only"""
    GRND.NCTRS.TMsender.__init__(self, portNr, nctrsTMfields)
  # ---------------------------------------------------------------------------
  def clientAccepted(self):
    """Overloaded from GRND.NCTRS.TMsender"""
    LOG_INFO("NCTRS TM receiver (client) accepted", "GRND")
    # notify the status change
    UTIL.TASK.s_processingTask.setTMconnected()
  # ---------------------------------------------------------------------------
  def pushTMframe(self, tmFrameDu):
    """
    consumes a telemetry frame:
    implementation of GROUND.IF.TMmcsLink.pushTMframe
    """
    recordFile = GRND.IF.s_configuration.frameRecordFile
    if recordFile:
      recordFormat = GRND.IF.s_configuration.frameRecordFormat
      try:
        if recordFormat == "NCTRS" or \
           recordFormat == "NCTRS_ASCII" or \
           recordFormat == "NCTRS_ASCII_DETAILS":
          LOG_INFO(GRND.IF.s_configuration.frameRecordFormat + " Frame recorded", "GRND")
          # Prepare the TM frame for recording
          ertCCSDStimeDU = \
            UTIL.TIME.getERTccsdsTimeDU(UTIL.TIME.getActualTime())
          tmDu = GRND.NCTRSDU.TMdataUnit()
          tmDu.setFrame(tmFrameDu.getBufferString())
          tmDu.spacecraftId = self.nctrsTMfields.spacecraftId
          tmDu.dataStreamType = self.nctrsTMfields.dataStreamType
          tmDu.virtualChannelId = self.nctrsTMfields.virtualChannelId
          tmDu.routeId = self.nctrsTMfields.routeId
          tmDu.earthReceptionTime = ertCCSDStimeDU.getBufferString()
          tmDu.sequenceFlag = self.nctrsTMfields.sequenceFlag
          tmDu.qualityFlag = self.nctrsTMfields.qualityFlag
          # ensure a correct size attribute
          tmDu.packetSize = len(tmDu)
          # write the DU to file
          if recordFormat == "NCTRS":
            recordFile.write(tmDu.getBufferString())
          else:
            # NCTRS_ASCII or NCTRS_ASCII_DETAILS
            recordFile.write("\n" + GRND.IF.s_configuration.frameRecordFormat + " Frame Header:")
            if recordFormat == "NCTRS_ASCII_DETAILS":
              recordFile.write("\ntmDu.packetSize = " + str(tmDu.packetSize))
              recordFile.write("\ntmDu.spacecraftId = " + str(tmDu.spacecraftId))
              recordFile.write("\ntmDu.dataStreamType = " + str(tmDu.dataStreamType))
              recordFile.write("\ntmDu.virtualChannelId = " + str(tmDu.virtualChannelId))
              recordFile.write("\ntmDu.routeId = " + str(tmDu.routeId))
              recordFile.write("\ntmDu.earthReceptionTime = " + str(tmDu.earthReceptionTime))
              recordFile.write("\ntmDu.sequenceFlag = " + str(tmDu.sequenceFlag))
              recordFile.write("\ntmDu.qualityFlag = " + str(tmDu.downlinkTimeSec))
              recordFile.write("\ntmDu.downlinkTimeSec = " + str(tmDu.qualityFlag))
            recordFile.write(UTIL.DU.array2str(tmDu.getBufferHeader()))
            recordFile.write("\n" + GRND.IF.s_configuration.frameRecordFormat + " Frame Body:")
            if recordFormat == "NCTRS_ASCII_DETAILS":
              recordFile.write("\ntmFrameDu.versionNumber = " + str(tmFrameDu.versionNumber))
              recordFile.write("\ntmFrameDu.spacecraftId = " + str(tmFrameDu.spacecraftId))
              recordFile.write("\ntmFrameDu.virtualChannelId = " + str(tmFrameDu.virtualChannelId))
              recordFile.write("\ntmFrameDu.operationalControlField = " + str(tmFrameDu.operationalControlField))
              recordFile.write("\ntmFrameDu.masterChannelFrameCount = " + str(tmFrameDu.masterChannelFrameCount))
              recordFile.write("\ntmFrameDu.virtualChannelFCountLow = " + str(tmFrameDu.virtualChannelFCountLow))
              recordFile.write("\ntmFrameDu.secondaryHeaderFlag = " + str(tmFrameDu.secondaryHeaderFlag))
              recordFile.write("\ntmFrameDu.synchronisationFlag = " + str(tmFrameDu.synchronisationFlag))
              recordFile.write("\ntmFrameDu.packetOrderFlag = " + str(tmFrameDu.packetOrderFlag))
              recordFile.write("\ntmFrameDu.segmentLengthId = " + str(tmFrameDu.segmentLengthId))
              recordFile.write("\ntmFrameDu.firstHeaderPointer = " + str(tmFrameDu.firstHeaderPointer))
              if tmFrameDu.secondaryHeaderFlag:
                recordFile.write("\ntmFrameDu.secondaryHeaderVersionNr = " + str(tmFrameDu.secondaryHeaderVersionNr))
                recordFile.write("\ntmFrameDu.secondaryHeaderSize = " + str(tmFrameDu.secondaryHeaderSize))
                recordFile.write("\ntmFrameDu.virtualChannelFCountHigh = " + str(tmFrameDu.virtualChannelFCountHigh))
            recordFile.write(UTIL.DU.array2str(tmDu.getBufferBody()))
            recordFile.write("\n")
          recordFile.flush()
        elif recordFormat == "CRYOSAT" or \
             recordFormat == "CRYOSAT_ASCII" or \
             recordFormat == "CRYOSAT_ASCII_DETAILS":
          LOG_INFO(GRND.IF.s_configuration.frameRecordFormat + " Frame recorded", "GRND")
          # Prepare the TM frame for recording
          tmDu = GRND.CRYOSATDU.TMframeDataUnit()
          tmDu.setFrame(tmFrameDu.getBufferString())
          timeStamp = UTIL.TIME.getActualTime()
          ertTime = UTIL.TIME.correlateToERTmissionEpoch(timeStamp)
          coarseTime = int(ertTime)
          fineTime = int((ertTime - coarseTime) * 1000000)
          tmDu.downlinkTimeSec = coarseTime
          tmDu.downlinkTimeMicro = fineTime
          tmDu.numberCorrSymbols = 0
          tmDu.rsErorFlag = 0
          tmDu.spare = 0
          tmDu.padding = 0
          # write the DU to file
          if recordFormat == "CRYOSAT":
            recordFile.write(tmDu.getBufferString())
          else:
            # CRYOSAT_ASCII or CRYOSAT_ASCII_DETAILS
            recordFile.write("\n" + GRND.IF.s_configuration.frameRecordFormat + " Frame Header:")
            if recordFormat == "CRYOSAT_ASCII_DETAILS":
              recordFile.write("\ntmDu.downlinkTimeSec = " + str(tmDu.downlinkTimeSec))
              recordFile.write("\ntmDu.downlinkTimeMicro = " + str(tmDu.downlinkTimeMicro))
              recordFile.write("\ntmDu.numberCorrSymbols = " + str(tmDu.numberCorrSymbols))
              recordFile.write("\ntmDu.rsErorFlag = " + str(tmDu.rsErorFlag))
            recordFile.write(UTIL.DU.array2str(tmDu.getBufferHeader()))
            recordFile.write("\n" + GRND.IF.s_configuration.frameRecordFormat + " Frame Body:")
            if recordFormat == "CRYOSAT_ASCII_DETAILS":
              recordFile.write("\ntmFrameDu.versionNumber = " + str(tmFrameDu.versionNumber))
              recordFile.write("\ntmFrameDu.spacecraftId = " + str(tmFrameDu.spacecraftId))
              recordFile.write("\ntmFrameDu.virtualChannelId = " + str(tmFrameDu.virtualChannelId))
              recordFile.write("\ntmFrameDu.operationalControlField = " + str(tmFrameDu.operationalControlField))
              recordFile.write("\ntmFrameDu.masterChannelFrameCount = " + str(tmFrameDu.masterChannelFrameCount))
              recordFile.write("\ntmFrameDu.virtualChannelFCountLow = " + str(tmFrameDu.virtualChannelFCountLow))
              recordFile.write("\ntmFrameDu.secondaryHeaderFlag = " + str(tmFrameDu.secondaryHeaderFlag))
              recordFile.write("\ntmFrameDu.synchronisationFlag = " + str(tmFrameDu.synchronisationFlag))
              recordFile.write("\ntmFrameDu.packetOrderFlag = " + str(tmFrameDu.packetOrderFlag))
              recordFile.write("\ntmFrameDu.segmentLengthId = " + str(tmFrameDu.segmentLengthId))
              recordFile.write("\ntmFrameDu.firstHeaderPointer = " + str(tmFrameDu.firstHeaderPointer))
              if tmFrameDu.secondaryHeaderFlag:
                recordFile.write("\ntmFrameDu.secondaryHeaderVersionNr = " + str(tmFrameDu.secondaryHeaderVersionNr))
                recordFile.write("\ntmFrameDu.secondaryHeaderSize = " + str(tmFrameDu.secondaryHeaderSize))
                recordFile.write("\ntmFrameDu.virtualChannelFCountHigh = " + str(tmFrameDu.virtualChannelFCountHigh))
            recordFile.write(UTIL.DU.array2str(tmDu.getBufferBody()))
            recordFile.write("\n")
          recordFile.flush()
        else:
          LOG_ERROR("invalid FRAME_RECORD_FORMAT: " + recordFormat, "GRND")
      except Exception, ex:
        LOG_ERROR("cannot write to frame recording file", "GRND")
        LOG(str(ex), "GRND")
    if GRND.IF.s_configuration.nctrsTMconn:
      self.sendFrame(tmFrameDu.getBufferString())
  # ---------------------------------------------------------------------------
  def recordFrames(self, recordFileName):
    """
    starts TM frame recording:
    implementation of GROUND.IF.TMmcsLink.recordFrames
    """
    # open the TM frame recording file
    try:
      recordingFile = open(recordFileName, "w")
    except:
      LOG_ERROR("cannot open " + recordFileName, "GRND")
      return
    GRND.IF.s_configuration.frameRecordFile = recordingFile
    # notify the GUI
    UTIL.TASK.s_processingTask.notifyGUItask("FRAME_REC_STARTED")
  # ---------------------------------------------------------------------------
  def stopFrameRecorder(self):
    """
    stops TM frame recording:
    implementation of GROUND.IF.TMmcsLink.stopFrameRecorder
    """
    # open the TM frame recording file
    try:
      GRND.IF.s_configuration.frameRecordFile.close()
      GRND.IF.s_configuration.frameRecordFile = None
    except:
      LOG_ERROR("cannot close frame recording file", "GRND")
    # notify the GUI
    UTIL.TASK.s_processingTask.notifyGUItask("FRAME_REC_STOPPED")
  # ---------------------------------------------------------------------------
  def notifyError(self, errorMessage, data):
    """error notification"""
    LOG_ERROR(errorMessage)
    try:
      LOG(str(data))
    except Exception, ex:
      LOG_WARNING("data passed to notifyError are invalid: " + str(ex))

#############
# functions #
#############
def createTMsender(hostName=None):
  """create the NCTRS TM sender"""
  nctrsTMfields = GRND.NCTRS.NCTRStmFields()
  nctrsTMfields.spacecraftId = int(UTIL.SYS.s_configuration.SPACECRAFT_ID)
  GRND.IF.s_tmMcsLink = TMsender(
    portNr=int(UTIL.SYS.s_configuration.NCTRS_TM_SERVER_PORT),
    nctrsTMfields=nctrsTMfields)
  if not GRND.IF.s_tmMcsLink.openConnectPort(hostName):
    sys.exit(-1)
