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
# FRAME layer - NCTRS frame file replayer                                     *
#******************************************************************************
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import CS.FRAMEmodel
import GRND.NCTRS
import UTIL.TASK

###########
# classes #
###########
# =============================================================================
class FrameReplayer(object):
  """Replayer of NCTRS frame files"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """default constructor"""
    self.running = False
    self.nctrsFramesFile = None
    self.frameRateMs = None
    self.frameNr = 0
  # ---------------------------------------------------------------------------
  def startReplay(self, replayFileName, frameRateMs):
    """starts reading NCTRS frames from a replay file"""
    LOG_WARNING("startReplay(" + replayFileName + ")", "FRAME")
    # read the NCTRS frames file
    try:
      self.nctrsFramesFile = open(replayFileName, "rb")
    except:
      LOG_ERROR("cannot read " + replayFileName, "FRAME")
      return False
    self.frameRateMs = frameRateMs
    self.running = True
    self.frameNr = 0
    UTIL.TASK.s_processingTask.notifyGUItask("UPDATE_REPLAY")
    # read the first frame, other frames are read automatically
    self.readFrame()
  # ---------------------------------------------------------------------------
  def stopReplay(self):
    """stops reading NCTRS frames"""
    LOG_WARNING("stopReplay", "FRAME")
    self.running = False
    if self.nctrsFramesFile != None:
      self.nctrsFramesFile.close()
      self.nctrsFramesFile = None
    self.frameRateMs = None
    UTIL.TASK.s_processingTask.notifyGUItask("UPDATE_REPLAY")
  # ---------------------------------------------------------------------------
  def readFrame(self):
    """reads the next NCTRS frame from the replay file"""
    # skip when the replay is not running anymore
    if not self.running:
      return
    # read the next NCTRS frame
    try:
      tmDu = GRND.NCTRS.readNCTRSframe(self.nctrsFramesFile)
    except Exception, ex:
      errorMessage = str(ex)
      if errorMessage != "":
        LOG_ERROR(errorMessage)
      self.stopReplay()
      return
    # extract the TM frame from the NCTRS data unit
    # and send it to the frame processing
    frame = tmDu.getFrame()
    self.frameNr += 1
    CS.FRAMEmodel.s_frameModel.receiveTMframe(frame)
    UTIL.TASK.s_processingTask.notifyGUItask("UPDATE_REPLAY_NR")
    # read the next frame later
    UTIL.TASK.s_processingTask.createTimeHandler(self.frameRateMs,
                                                 self.readFrame)

####################
# global variables #
####################
# NCTRS clients are singletons
s_frameReplayer = None

#############
# functions #
#############
def init():
  """initialise singleton(s)"""
  global s_frameReplayer
  s_frameReplayer = FrameReplayer()
