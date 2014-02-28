#******************************************************************************
# (C) 2014, Stefan Korner, Austria                                            *
#                                                                             *
# The Space Python Library is free software; you can redistribute it and/or   *
# modify it under the terms of the GNU Lesser General Public License as       *
# published by the Free Software Foundation; either version 2.1 of the        *
# License, or (at your option) any later version.                             *
#                                                                             *
# The Space C++ Library is distributed in the hope that it will be useful,    *
# but WITHOUT ANY WARRANTY; without even the implied warranty of              *
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser     *
# General Public License for more details.                                    *
#******************************************************************************
# Utilities - BCH Encoding                                                    *
#                                                                             *
# The CLTU encoding is based on a (63,56) modified                            *
# Bose-Chaudhuri-Hocquenghem (BCH) code.                                      *
# The implementation of the BCH encoding is performed with a constant         *
# galois field to ensure good performance.                                    *
#******************************************************************************

#############
# constants #
#############
# the BCH encoding divides the data into code blocks,
# each with 7 netto bytes and 1 check byte
#
# +---+---+---+---+---+---+---+---+
# |BY1|BY2|BY3|BY4|BY5|BY6|BY7|CHK|
# +---+---+---+---+---+---+---+---+
#
# size of the BCH code block
CODE_BLOCK_SIZE = 8
# galois field with all possible shift register states/transitions
# this static table speeds up the BCH encoding / checking
# it is a 128 x 256 bytes field:
# the 1st index [0]...[127] defines the possible states of the shift register
# the 2nd index [0]...[255] defines the possible input values
# the values [0]...[127] defines the next state of the shift register
#
#     |    0 |    1 |    2 | ... |  255
# ----+------+------+------+-----+-----
#   0 | 0x00 | 0x45 | 0x45 | ... | 0x59
# ----+------+------+------+-----+-----
#   1 | 0x4F | 0x0A | 0x0A | ... | 0x16
# ----+------+------+------+-----+-----
#   2 | 0x5B | 0x1E | 0x1E | ... | 0x02
# ----+------+------+------+-----+-----
#   : |   :  |   :  |   :  |     |   :
# ----+------+------+------+-----+-----
# 127 | 0x1C | 0x59 | 0x59 | ... | 0x45
#
s_shiftRegisterStateTransitions = []

#############
# functions #
#############
# -----------------------------------------------------------------------------
def generateShiftRegisterValues():
  """generates the values of the galois field"""
  global s_shiftRegisterStateTransitions
  for sregState in range(0, 128):
    transitionField = []
    for value in range(0, 256):
      sreg = sregState               # handle the next shift register state
      mask = 0x80
      while mask != 0:
        sreg <<= 1                   # shift 7 bits in shift register left
        overflow = (sreg & 0x80) > 0 # check if overflow
        if (value & mask) > 0:       # add the value with the mask
          overflow = not overflow    # join with overflow
        if overflow:                 # depending on overflow
          sreg ^= 0x45               # add bits 0, 2, 6
        mask >>= 1                   # shift 7 bits in shift register right
      sreg &= 0x7F                   # keep 7 bits
      transitionField.append(sreg)
    s_shiftRegisterStateTransitions.append(transitionField)
# -----------------------------------------------------------------------------
def encodeStart():
  """starts the BCH encoding with the initial shift register state"""
  return 0
# -----------------------------------------------------------------------------
def encodeStep(sreg, value):
  """performs an icremental step in the BCH encoding: 1,...,7 """
  global s_shiftRegisterStateTransitions
  return s_shiftRegisterStateTransitions[sreg][value]
# -----------------------------------------------------------------------------
def encodeStop(sreg):
  """final step: returns the BCH code from the shift register state"""
  sreg ^= 0xFF           # invert the shift register state
  sreg <<= 1             # make it the 7 most sign. bits
  return (sreg & 0xFE)   # filter the 7 most sign bits

###########################
# Initialisation sequence #
###########################
# initialise the galois field
generateShiftRegisterValues()
