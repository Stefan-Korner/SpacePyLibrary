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
# FRAME layer model                                                           *
#******************************************************************************
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import CCSDS.PACKET, CCSDS.PACKETIZER, CCSDS.TCENCODER
import CS.NCTRSclient
import GRND.IF, GRND.NCTRS
import MC.IF
import PUS.PACKET
import UTIL.DU, UTIL.SYS, UTIL.TASK

#############
# constants #
#############
SEND_AS_PACKET = 0
SEND_AS_FRAME = 1
SEND_AS_CLTU = 2

###########
# classes #
###########
# =============================================================================
class FrameModel(CCSDS.PACKETIZER.Packetizer, CCSDS.TCENCODER.TCencoder):
  """Implementation of the CS side frame processing"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """Initialise attributes only"""
    frameVCID = int(UTIL.SYS.s_configuration.TM_TRANSFER_FRAME_VCID)
    CCSDS.PACKETIZER.Packetizer.__init__(self, frameVCID)
    CCSDS.TCENCODER.TCencoder.__init__(self)
    self.ignoreIdlePackets = (UTIL.SYS.s_configuration.IGNORE_IDLE_PACKETS == "1")
  # ---------------------------------------------------------------------------
  def sendTCpacket(self, tcPacketDu, sendFormat):
    """sends a TM packet"""
    if sendFormat == SEND_AS_PACKET:
      LOG_INFO("TC packet ready for sending", "FRAME")
      CS.NCTRSclient.s_tcClient.sendTCpacket(tcPacketDu.getBufferString())
    else:
      self.pushTCpacket(tcPacketDu.getBufferString(), sendFormat == SEND_AS_CLTU)
    return True
  # ---------------------------------------------------------------------------
  def notifyTCframeCallback(self, frameDU):
    """notifies when the next TC frame is assembled"""
    # overloaded from TCencoder
    LOG("FrameModel.notifyTCframeCallback" + frameDU.getDumpString(), "FRAME")
    LOG_WARNING("frame cannot be directly sent, there is no NCTRS service", "FRAME")
  # ---------------------------------------------------------------------------
  def notifyCLTUcallback(self, cltu):
    """notifies when the next CLTU is assembled"""
    # overloaded from TCencoder
    LOG("FrameModel.notifyCLTUcallback" + UTIL.DU.array2str(cltu), "FRAME")
    CS.NCTRSclient.s_tcClient.sendCltu(cltu)
  # ---------------------------------------------------------------------------
  def receiveTMframe(self, tmFrame):
    """TM frame received"""
    LOG_INFO("TM frame received", "FRAME")
    self.pushTMframe(tmFrame)
  # ---------------------------------------------------------------------------
  def notifyTMpacketCallback(self, binPacket):
    """notifies when the next TM packet is assembled"""
    # overloaded from Packetizer
    if self.ignoreIdlePackets:
      apid = CCSDS.PACKET.getApplicationProcessId(binPacket)
      if apid == CCSDS.PACKET.IDLE_PKT_APID:
        return
    if PUS.PACKET.isPUSpacket(binPacket):
      # PUS packet
      tmPacketDu = PUS.PACKET.TMpacket(binPacket)
      LOG_INFO("PUS TM packet extracted", "FRAME")
    else:
      # CCSDS packet
      tmPacketDu = CCSDS.PACKET.TMpacket(binPacket)
      LOG_INFO("CCSDS TM packet extracted", "FRAME")
    MC.IF.s_tmModel.pushTMpacket(tmPacketDu, None)

####################
# global variables #
####################
# frame model singletons
s_frameModel = None

#############
# functions #
#############
# functions to encapsulate access to s_frameModel
# -----------------------------------------------------------------------------
def init():
  """initialise singleton(s)"""
  global s_frameModel
  s_frameModel = FrameModel()
