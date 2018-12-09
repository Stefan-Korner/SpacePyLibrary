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
# Monitoring and Control (M&C) - Telemetry Model                              *
#******************************************************************************
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import MC.IF
import PUS.PACKET, PUS.SERVICES
import UTIL.DU

###########
# classes #
###########
# =============================================================================
class TMmodel(MC.IF.TMmodel):
  """Implementation of the telemetry model"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """Initialise attributes only"""
  # ---------------------------------------------------------------------------
  def pushTMpacket(self, tmPacketDu, ertUTC):
    """
    consumes a telemetry packet:
    implementation of MC.IF.TMmodel.pushTMpacket
    """
    LOG_INFO("pushTMpacket", "TM")
    LOG("APID =    " + str(tmPacketDu.applicationProcessId), "TM")
    LOG("SSC =     " + str(tmPacketDu.sequenceControlCount), "TM")
    if tmPacketDu.dataFieldHeaderFlag == 1:
      # CCSDS packet is a PUS packet
      object.__setattr__(tmPacketDu, "attributeMap2", PUS.PACKET.TM_PACKET_DATAFIELD_HEADER_ATTRIBUTES)
      LOG("TYPE =    " + str(tmPacketDu.serviceType), "TM")
      LOG("SUBTYPE = " + str(tmPacketDu.serviceSubType), "TM")
      # the existence of a CRC for PUS packets is mission dependant
      # for SCOS-2000 compatibility we expect a CRC
      if not tmPacketDu.checkChecksum():
        LOG_ERROR("invalid TM packet CRC", "TM")
      # processing of PUS telecommands
      if tmPacketDu.serviceType == PUS.SERVICES.TC_ACK_TYPE:
        # packet is a PUS TC Acknowledgement command
        MC.IF.s_tcModel.notifyTCack(tmPacketDu.serviceSubType)
    else:
      LOG("non-PUS packet", "TM")
      LOG("tmPacketDu = " + str(tmPacketDu), "TM")

#############
# functions #
#############
def init():
  # initialise singleton(s)
  MC.IF.s_tmModel = TMmodel()
