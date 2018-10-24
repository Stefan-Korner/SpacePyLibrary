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
# CCSDS Stack - Telecommand Segmentation Module helpers                       *
#******************************************************************************
import CCSDS.SEGMENT

#############
# functions #
#############
# -----------------------------------------------------------------------------
def portionStr(sequenceFlags):
  """returns the stringified acknowledgement"""
  if sequenceFlags == CCSDS.SEGMENT.FIRST_PORTION:
    return "FIRST_PORTION"
  if sequenceFlags == CCSDS.SEGMENT.MIDDLE_PORTION:
    return "MIDDLE_PORTION"
  if sequenceFlags == CCSDS.SEGMENT.LAST_PORTION:
    return "LAST_PORTION"
  if sequenceFlags == CCSDS.SEGMENT.UNSEGMENTED:
    return "UNSEGMENTED"
  return "???"
