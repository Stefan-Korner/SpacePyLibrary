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
import CS.CNCclient, CS.EDENclient, CS.FRAMEmodel
import EGSE.IF
import GRND.IF
import MC.IF
import PUS.SERVICES

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
      LOG_ERROR("packet creation failed: pktName = " + str(tcPacketData.pktName), "TC")
      return False
    if tcPacketDu.dataFieldHeaderFlag:
      LOG("PUS Packet:" + tcPacketDu.getDumpString(16), "TC")
    else:
      LOG("CCSDS Packet:" + tcPacketDu.getDumpString(16), "TC")
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
    elif route == "NCTRS_PACKET":
      if not GRND.IF.s_clientConfiguration.nctrsTCconn:
        LOG_ERROR("route NCTRS is not initialized", "TC")
        return False
      return CS.FRAMEmodel.s_frameModel.sendTCpacket(tcPacketDu,
        CS.FRAMEmodel.SEND_AS_PACKET)
    elif route == "NCTRS_FRAME":
      if not GRND.IF.s_clientConfiguration.nctrsTCconn:
        LOG_ERROR("route NCTRS is not initialized", "TC")
        return False
      return CS.FRAMEmodel.s_frameModel.sendTCpacket(tcPacketDu,
        CS.FRAMEmodel.SEND_AS_FRAME)
    elif route == "NCTRS_CLTU":
      if not GRND.IF.s_clientConfiguration.nctrsTCconn:
        LOG_ERROR("route NCTRS is not initialized", "TC")
        return False
      return CS.FRAMEmodel.s_frameModel.sendTCpacket(tcPacketDu,
        CS.FRAMEmodel.SEND_AS_CLTU)
    else:
      LOG_ERROR("invalid route for TC packet: " + route, "TC")
      LOG("use instead: CNC | EDEN_SPACE | EDEN_SCOE | EDEN2_SPACE | EDEN2_SCOE |", "TC")
      LOG("             NCTRS_PACKET | NCTRS_FRAME | NCTRS_CLTU", "TC")
      return False
    return True
  # ---------------------------------------------------------------------------
  def notifyTCack(self, tcAckSubType):
    """
    notifies a PUS service 1 acknowledgement:
    implementation of MC.IF.TCmodel.notifyTCack
    """
    # packet is a PUS TC Acknowledgement command
    if tcAckSubType == PUS.SERVICES.TC_ACK_ACCEPT_SUCC:
      LOG_INFO("--> TC_ACK_ACCEPT_SUCC", "TC")
    elif tcAckSubType == PUS.SERVICES.TC_ACK_ACCEPT_FAIL:
      LOG_ERROR("--> TC_ACK_ACCEPT_FAIL", "TC")
    elif tcAckSubType == PUS.SERVICES.TC_ACK_EXESTA_SUCC:
      LOG_INFO("--> TC_ACK_EXESTA_SUCC", "TC")
    elif tcAckSubType == PUS.SERVICES.TC_ACK_EXESTA_FAIL:
      LOG_ERROR("--> TC_ACK_EXESTA_FAIL", "TC")
    elif tcAckSubType == PUS.SERVICES.TC_ACK_EXEPRO_SUCC:
      LOG_INFO("--> TC_ACK_EXEPRO_SUCC", "TC")
    elif tcAckSubType == PUS.SERVICES.TC_ACK_EXEPRO_FAIL:
      LOG_ERROR("--> TC_ACK_EXEPRO_FAIL", "TC")
    elif tcAckSubType == PUS.SERVICES.TC_ACK_EXECUT_SUCC:
      LOG_INFO("--> TC_ACK_EXECUT_SUCC", "TC")
    elif tcAckSubType == PUS.SERVICES.TC_ACK_EXECUT_FAIL:
      LOG_ERROR("--> TC_ACK_EXECUT_FAIL", "TC")
    else:
      LOG_ERROR("unexpected TC Acknowledgement SubType: " + str(tcAckSubType), "TC")

#############
# functions #
#############
def init():
  """initialise singleton(s)"""
  MC.IF.s_tcModel = TCmodel()
