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
# PUS Services - Service Definition                                           *
#******************************************************************************

#############
# constants #
#############
# -----------------------------------------------------------------------------
# PUS service 1: Telecommand Verification Service 
# SUBTYPES
TC_ACK_ACCEPT_SUCC = 1
TC_ACK_ACCEPT_FAIL = 2
TC_ACK_EXESTA_SUCC = 3
TC_ACK_EXESTA_FAIL = 4
TC_ACK_EXEPRO_SUCC = 5
TC_ACK_EXEPRO_FAIL = 6
TC_ACK_EXECUT_SUCC = 7
TC_ACK_EXECUT_FAIL = 8
# The position (offset) of the PUS service 1 attributes are global properties
# that can be changed via service1_setTCackParamsProperties()
DEFAULT_TC_ACK_APID_PARAM_BYTE_OFFSET = 10
DEFAULT_TC_ACK_SSC_PARAM_BYTE_OFFSET = 12
TC_ACK_APID_PARAM_BYTE_LENGTH = 2
TC_ACK_SSC_PARAM_BYTE_LENGTH = 2
TC_ACK_APID_PARAM_MASK = 0x1800
TC_ACK_SSC_PARAM_MASK = 0xC000

# -----------------------------------------------------------------------------
# PUS service 8: Function Management service
# TYPE / SUBTYPES
TC_FKT_TYPE = 8
TC_FKT_PERFORM_FUNCTION = 1

# -----------------------------------------------------------------------------
# PUS service 11: Onboard Scheduling service
# TYPE / SUBTYPES
TC_OBQ_TYPE = 11
TC_OBQ_UPLINK_SUBTYPES = [4, 128]   # 128 is TET specific

####################
# global variables #
####################
# The position (offset) of the PUS service 1 attributes are global properties
# that can be changed via service1_setTCackParamsProperties()
s_tcAckAPIDparamByteOffset = DEFAULT_TC_ACK_APID_PARAM_BYTE_OFFSET
s_tcAckSSCparamByteOffset = DEFAULT_TC_ACK_SSC_PARAM_BYTE_OFFSET

#############
# functions #
#############
# -----------------------------------------------------------------------------
def service1_setTCackParamsProperties(tcAckAPIDparamByteOffset,
                                      tcAckSSCparamByteOffset):
  """changes the global positions of the PUS service 1 attributes"""
  s_tcAckAPIDparamByteOffset = tcAckAPIDparamByteOffset
  s_tcAckSSCparamByteOffset = tcAckSSCparamByteOffset
# -----------------------------------------------------------------------------
def service1_getTCackMinPacketSize():
  """returns the minimal size of a PUS service 1 packet"""
  return (s_tcAckSSCparamByteOffset +
          TC_ACK_SSC_PARAM_BYTE_LENGTH +
          CCSDS.PACKET.CRC_BYTE_SIZE)
# -----------------------------------------------------------------------------
def service1_getTCackAPID(pusTMpacketDU):
  """retrieves the APID of the related TC packet in the datafield attribute"""
  # filters the relevant bits"""
  return (packet.getUnsigned(s_tcAckAPIDparamByteOffset,
                             TC_ACK_APID_PARAM_BYTE_LENGTH) |
          TC_ACK_APID_PARAM_MASK)
# -----------------------------------------------------------------------------
def service1_setTCackAPID(pusTMpacketDU, apid):
  """sets the APID of the related TC packet in the datafield attribute"""
  # filters the relevant bits"""
  packet.setUnsigned(s_tcAckAPIDparamByteOffset,
                     TC_ACK_APID_PARAM_BYTE_LENGTH,
                     apid | TC_ACK_APID_PARAM_MASK)
# -----------------------------------------------------------------------------
def service1_getTCackSSC(pusTMpacketDU):
  """retrieves the SSC of the related TC packet in the datafield attribute"""
  # filters the relevant bits"""
  return (packet.getUnsigned(s_tcAckSSCparamByteOffset,
                             TC_ACK_SSC_PARAM_BYTE_LENGTH) |
          TC_ACK_SSC_PARAM_MASK)
# -----------------------------------------------------------------------------
def service1_setTCackSSC(pusTMpacketDU, ssc):
  """sets the SSC of the related TC packet in the datafield attribute"""
  # filters the relevant bits"""
  packet.setUnsigned(s_tcAckSSCparamByteOffset,
                     TC_ACK_SSC_PARAM_BYTE_LENGTH,
                     ssc | TC_ACK_SSC_PARAM_BYTE_LENGTH)
