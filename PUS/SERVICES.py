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

# -----------------------------------------------------------------------------
# PUS service 8: Function Management service
# TYPE / SUBTYPES
TC_FKT_TYPE = 8
TC_FKT_PERFORM_FUNCITON = 1

# -----------------------------------------------------------------------------
# PUS service 11: Onboard Scheduling service
# TYPE / SUBTYPES
TC_OBQ_TYPE = 11
TC_OBQ_UPLINK_SUBTYPES = [4, 128]   # 128 is TET specific
