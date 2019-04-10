#******************************************************************************
# (C) 2019, Stefan Korner, Austria                                            *
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
# PUS Services - Packet Identification                                        *
#                                                                             *
# The packet identification is a 2 step process:                              *
# - step 1: key fields PI1, PI2 identification based on APID, TYPE, SUBTYPE   *
#           result: position and size of PI1 and PI2                          *
# - step 2: packet identification based on APID, TYPE, SUBTYPE, PI1, PI2      *
#           result: packet ID                                                *
#                                                                             *
# Note: The packet information must be loaded from outside.                   *
#       Separate instances for TM and TC packet identification are needed.    *
#       The keys are implemented as tupples.                                  *
#******************************************************************************
import CCSDS.PACKET
import PUS.PACKET

###########
# classes #
###########
# =============================================================================
class PacketIdentificator(object):
  """PUS packet identificator"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """default constructor"""
    self.keyFieldIDs = {}
    self.packetIDs = {}
  # ---------------------------------------------------------------------------
  def addKeyFieldRecord(self,
                        apid, serviceType, serviceSubType,
                        pi1bitPos, pi1bitSize, pi2bitPos, pi2bitSize):
    """adds a record for key field identification"""
    # note: apid can be None - in this case all packets with the same
    #       serviceType and serviceSubType are matching such an entry
    # note: this table is also relevant for non-pus packets - in this case the
    #       serviceType and serviceSubType fields must be None
    # note: pi1bitPos, pi1bitSize and/or pi2bitPos, pi2bitSize can be None - in
    #       this case pi1 and/or pi2 are not used for the packet identification
    # note: when pi1bitPos, pi1bitSize and/or pi2bitPos, pi2bitSize are None,
    #       then the related enytry for the packet identification must contain
    #       as well None in the pi1 and/or pi2 field
    key = (apid, serviceType, serviceSubType)
    value = (pi1bitPos, pi1bitSize, pi2bitPos, pi2bitSize)
    self.keyFieldIDs[key] = value
  # ---------------------------------------------------------------------------
  def addPacketIDrecord(self,
                        apid, serviceType, serviceSubType, pi1, pi2,
                        packetID):
    """adds a record for packet identification"""
    # note: this table is also relevant for non-pus packets - in this case the
    #       serviceType and serviceSubType fields must be None
    key = (apid, serviceType, serviceSubType, pi1, pi2)
    value = packetID
    self.packetIDs[key] = value
  # ---------------------------------------------------------------------------
  def getPacketKey(self, packetDU):
    """retrieves the packet key from the packet data unit"""
    # key field identification
    apid = packetDU.applicationProcessId
    if PUS.PACKET.isPUSpacketDU(packetDU):
      # we have a PUS packet
      serviceType = packetDU.serviceType
      serviceSubType = packetDU.serviceSubType
    else:
      # we have a CCSDS packet
      serviceType = None
      serviceSubType = None
    key1 = (apid, serviceType, serviceSubType)
    if key1 in self.keyFieldIDs:
      pi1bitPos, pi1bitSize, pi2bitPos, pi2bitSize = self.keyFieldIDs[key1]
    else:
      key1 = (None, serviceType, serviceSubType)
      if key1 in self.keyFieldIDs:
        pi1bitPos, pi1bitSize, pi2bitPos, pi2bitSize = self.keyFieldIDs[key1]
      else:
        return None
    # key field extraction
    if pi1bitPos != None:
      pi1 = packetDU.getBits(pi1bitPos, pi1bitSize)
    else:
      pi1 = None
    if pi2bitPos != None:
      pi2 = packetDU.getBits(pi2bitPos, pi2bitSize)
    else:
      pi2 = None
    # packet identification
    key2 = (apid, serviceType, serviceSubType, pi1, pi2)
    if not key2 in self.packetIDs:
      return None
    return self.packetIDs[key2]
