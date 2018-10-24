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
# Space Simulation - Onboard Queue                                            *
#******************************************************************************
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import CCSDS.PACKET, CCSDS.TIME
import PUS.PACKET, PUS.SERVICES
import SPACE.IF
import UTIL.SYS, UTIL.TASK, UTIL.TCO, UTIL.TIME

#############
# constants #
#############
CHECK_CYCLIC_PERIOD_MS = 100

###########
# classes #
###########
# =============================================================================
class OnboardQueueImpl(SPACE.IF.OnboardQueue):
  """Implementation of the onboard computer"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """Initialise attributes only"""
    self.ttTtimeFormat = CCSDS.TIME.timeFormat(UTIL.SYS.s_configuration.TM_TT_TIME_FORMAT)
    self.ttTimeByteOffset = int(UTIL.SYS.s_configuration.TC_TT_TIME_BYTE_OFFSET)
    self.ttByteOffset = int(UTIL.SYS.s_configuration.TC_TT_PKT_BYTE_OFFSET)
    self.queue = {}
    self.checkCyclicCallback()
  # ---------------------------------------------------------------------------
  def getQueue(self):
    """
    returns the onboard queue:
    implementation of SPACE.IF.OnboardQueue.getQueue
    """
    return self.queue
  # ---------------------------------------------------------------------------
  def pushMngPacket(self, tcPacketDu):
    """
    consumes a management telecommand packet:
    implementation of SPACE.IF.OnboardQueue.pushMngPacket
    """
    LOG_INFO("pushMngPacket", "OBQ")
    LOG("APID =    " + str(tcPacketDu.applicationProcessId), "OBQ")
    LOG("TYPE =    " + str(tcPacketDu.serviceType), "OBQ")
    LOG("SUBTYPE = " + str(tcPacketDu.serviceSubType), "OBQ")
    LOG("SSC =     " + str(tcPacketDu.sequenceControlCount), "OBQ")
    # check if the packet is a TT uplink command
    if tcPacketDu.serviceSubType in PUS.SERVICES.TC_OBQ_UPLINK_SUBTYPES:
      # extract the embedded TT packet from the TT uplink command
      # consider also the CRC (2 bytes)
      ttPacketMaxSize = len(tcPacketDu) - self.ttByteOffset - 2
      if ttPacketMaxSize <= CCSDS.PACKET.PRIMARY_HEADER_BYTE_SIZE:
        LOG_ERROR("cannot extract TT packet, not enought bytes", "OBQ")
        LOG(str(tcPacketDu), "OBQ")
        return
      ttPacketData = tcPacketDu.getBytes(self.ttByteOffset, ttPacketMaxSize)
      ttPacketDu = PUS.PACKET.TCpacket(ttPacketData)
      ttPacketSize = CCSDS.PACKET.PRIMARY_HEADER_BYTE_SIZE + ttPacketDu.packetLength + 1
      # consistency checks
      if ttPacketSize < CCSDS.PACKET.PRIMARY_HEADER_BYTE_SIZE:
        LOG_ERROR("packetLength of TT packet too small", "OBQ")
        LOG(str(ttPacketDu), "OBQ")
        return
      if ttPacketSize > ttPacketMaxSize:
        LOG_ERROR("packetLength of TT packet too large", "OBQ")
        LOG(str(ttPacketDu), "OBQ")
        return
      # resize the ttPacketDu to match the packetLength
      ttPacketDu.setLen(ttPacketSize)
      if not ttPacketDu.checkChecksum():
        LOG_ERROR("invalid TT packet CRC", "OBQ")
        LOG(str(ttPacketDu), "OBQ")
        return
      # calculate the execution time
      obtExecTime = tcPacketDu.getTime(self.ttTimeByteOffset, self.ttTtimeFormat)
      ttExecTime = UTIL.TCO.correlateFromOBTmissionEpoch(obtExecTime)
      SPACE.IF.s_onboardQueue.insertTTpacket(ttExecTime, ttPacketDu)
  # ---------------------------------------------------------------------------
  def insertTTpacket(self, ttExecTime, ttPacketDu):
    """
    inserts a time-tagged telecommand packet into the command queue
    """
    LOG("insertTTpacket(" + UTIL.TIME.getASDtimeStr(ttExecTime) + ")", "OBQ")
    self.queue[ttExecTime] = ttPacketDu
    UTIL.TASK.s_processingTask.notifyGUItask("TT_PACKET")
  # ---------------------------------------------------------------------------
  def checkCyclicCallback(self):
    """timer triggered"""
    UTIL.TASK.s_processingTask.createTimeHandler(CHECK_CYCLIC_PERIOD_MS,
                                                 self.checkCyclicCallback)
    # check if execution times in the queue are expired
    ttExecTimes = self.queue.keys()
    ttExecTimes = sorted(ttExecTimes)
    actualTime = UTIL.TIME.getActualTime()
    cmdsDeleted = False
    for ttExecTime in ttExecTimes:
      if ttExecTime <= actualTime:
        # execution time has expired ---> process the packet
        ttPacketDu = self.queue[ttExecTime]
        SPACE.IF.s_onboardComputer.processTCpacket(
          ttPacketDu,
          SPACE.IF.s_configuration.obqAck1,
          SPACE.IF.s_configuration.obqAck2,
          SPACE.IF.s_configuration.obqAck3,
          SPACE.IF.s_configuration.obqAck4)
        # remove command
        del self.queue[ttExecTime]
        cmdsDeleted = True
      else:
        break
    if cmdsDeleted:
      UTIL.TASK.s_processingTask.notifyGUItask("TT_PACKET")

#############
# functions #
#############
def init():
  # initialise singleton(s)
  SPACE.IF.s_onboardQueue = OnboardQueueImpl()
