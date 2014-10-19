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
