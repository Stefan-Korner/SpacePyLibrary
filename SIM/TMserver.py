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
import UTIL.SYS, UTIL.TASK

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
    if GRND.IF.s_configuration.frameRecordFile:
      try:
        if GRND.IF.s_configuration.frameRecordFormat == "NCTRS":
          LOG_INFO("NCTRS Frame recorded", "GRND")
          # Prepare the TM frame for recording
          actualCCSDStimeDU = \
            UTIL.TIME.getCCSDStimeDU(UTIL.TIME.getActualTime())
          tmDu = GRND.NCTRSDU.TMdataUnit()
          tmDu.setFrame(tmFrameDu.getBufferString())
          tmDu.spacecraftId = self.nctrsTMfields.spacecraftId
          tmDu.dataStreamType = self.nctrsTMfields.dataStreamType
          tmDu.virtualChannelId = self.nctrsTMfields.virtualChannelId
          tmDu.routeId = self.nctrsTMfields.routeId
          tmDu.earthReceptionTime = actualCCSDStimeDU.getBufferString()
          tmDu.sequenceFlag = self.nctrsTMfields.sequenceFlag
          tmDu.qualityFlag = self.nctrsTMfields.qualityFlag
          # ensure a correct size attribute
          tmDu.packetSize = len(tmDu)
          # write the DU to file
          GRND.IF.s_configuration.frameRecordFile.write(tmDu.getBufferString())
          GRND.IF.s_configuration.frameRecordFile.flush()
        elif GRND.IF.s_configuration.frameRecordFormat == "CRYOSAT":
          LOG_INFO("CRYOSAT Frame recorded", "GRND")
          # Prepare the TM frame for recording
          tmDu = GRND.CRYOSATDU.TMframeDataUnit()
          tmDu.setFrame(tmFrameDu.getBufferString())
          tmDu.downlinkTimeSec = 1000   # dummy value
          tmDu.downlinkTimeMicro = 0
          tmDu.numberCorrSymbols = 0
          tmDu.rsErorFlag = 0
          tmDu.spare = 0
          tmDu.padding = 0
          # write the DU to file
          GRND.IF.s_configuration.frameRecordFile.write(tmDu.getBufferString())
          GRND.IF.s_configuration.frameRecordFile.flush()
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
