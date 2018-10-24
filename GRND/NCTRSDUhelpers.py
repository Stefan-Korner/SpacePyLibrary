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
# Ground Simulation - NCTRS Data Units Module helpers                         *
# implements EGOS-NIS-NCTR-ICD-0002-i4r0.2 (Signed).pdf                       *
#******************************************************************************
import GRND.NCTRSDU

#############
# functions #
#############
# -----------------------------------------------------------------------------
def ackStr(acknowledgement):
  """returns the stringified acknowledgement"""
  if acknowledgement == GRND.NCTRSDU.TC_ACK_UV_ACCEPT_CONFIRM:
    return "UV_ACCEPT_CONFIRM"
  if acknowledgement == GRND.NCTRSDU.TC_ACK_UV_ACCEPT_FAILURE:
    return "UV_ACCEPT_FAILURE"
  if acknowledgement == GRND.NCTRSDU.TC_ACK_UV_TRANSMIT_CONFIRM:
    return "UV_TRANSMIT_CONFIRM"
  if acknowledgement == GRND.NCTRSDU.TC_ACK_UV_TRANSMIT_FAILURE:
    return "UV_TRANSMIT_FAILURE"
  if acknowledgement == GRND.NCTRSDU.TC_ACK_UV_TRANSFER_CONFIRM:
    return "UV_TRANSFER_CONFIRM"
  if acknowledgement == GRND.NCTRSDU.TC_ACK_UV_TRANSFER_FAILURE:
    return "UV_TRANSFER_FAILURE"
  return "???"
