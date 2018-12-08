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
# Monitoring and Control (M&C) - Telecommand Model                            *
#******************************************************************************
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import CS.CNCclient, CS.EDENclient
import EGSE.IF
import MC.IF
import UTIL.DU

###########
# classes #
###########
# =============================================================================
class TCmodel(MC.IF.TCmodel):
  """Implementation of the telecommand model"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """Initialise attributes only"""
  # ---------------------------------------------------------------------------
  def generateTCpacket(self, tcPacketData):
    """
    generates a TC packet:
    implementation of MC.IF.TCmodel.generateTCpacket
    """
    # create the TC packet
    tcPacketDu = MC.IF.s_tcPacketGenerator.getTCpacket(tcPacketData.pktName)
    if tcPacketDu == None:
      LOG_ERROR("packet creation failed: pktName = " + str(pktName), "TC")
      return False
    if tcPacketDu.dataFieldHeaderFlag:
      LOG("PUS Packet:" + UTIL.DU.array2str(tcPacketDu.getBufferString()[0:min(16,len(tcPacketDu))]), "TC")
    else:
      LOG("CCSDS Packet:" + UTIL.DU.array2str(tcPacketDu.getBufferString()[0:min(16,len(tcPacketDu))]), "TC")
    # send the TC packet
    route = tcPacketData.route
    return self.pushTCpacket(tcPacketDu, route)
  # ---------------------------------------------------------------------------
  def pushTCpacket(self, tcPacketDu, route):
    """
    consumes a telecommand packet:
    implementation of MC.IF.TCmodel.pushTCpacket
    """
    LOG_INFO("pushTCpacket", "TC")
    LOG("Route: " + route, "TC")
    if route == "CNC":
      if not EGSE.IF.s_cncClientConfiguration.connected:
        LOG_ERROR("route CNC is not initialized", "TC")
        return False
      CS.CNCclient.s_client.pushTCpacket(tcPacketDu)
    elif route == "EDEN_SPACE":
      if not EGSE.IF.s_edenClientConfiguration.connected:
        LOG_ERROR("route EDEN_SPACE is not initialized", "TC")
        return False
      CS.EDENclient.s_client.pushTcSpace(tcPacketDu)
    elif route == "EDEN_SCOE":
      if not EGSE.IF.s_edenClientConfiguration.connected:
        LOG_ERROR("route EDEN_SCOE is not initialized", "TC")
        return False
      CS.EDENclient.s_client.pushTcScoe(tcPacketDu)
    elif route == "EDEN2_SPACE":
      if not EGSE.IF.s_edenClientConfiguration.connected2:
        LOG_ERROR("route EDEN2_SPACE is not initialized", "TC")
        return False
      CS.EDENclient.s_client2.pushTcSpace(tcPacketDu)
    elif route == "EDEN2_SCOE":
      if not EGSE.IF.s_edenClientConfiguration.connected2:
        LOG_ERROR("route EDEN2_SCOE is not initialized", "TC")
        return False
      CS.EDENclient.s_client2.pushTcScoe(tcPacketDu)
    else:
      LOG_ERROR("invalid route for TC packet: " + route, "TC")
      return False
    return True

#############
# functions #
#############
def init():
  # initialise singleton(s)
  MC.IF.s_tcModel = TCmodel()
