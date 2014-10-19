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
# Utilities - CRC Checksum Calculation                                        *
#                                                                             *
# CCSDS packets and Transfer Frames may contain a trailing CRC checksum.      *
#******************************************************************************

#############
# functions #
#############
def calculate(byteArray):
  """calculates the CRC from the byte array"""
  # 32 bit shift register for CRC generation
  # D0  - D15  :CRC shift register
  # D16        : MSB after shift
  # D17 - D31  : not used
  # shift register preset with all ones
  shiftReg = 0x0000FFFF
  # generator polynom D0-D15: X^16 + X^12 + X^5 + X^0
  polynom = 0x00001021
  arraySize = len(byteArray)
  i = 0
  while i < arraySize:
    nextByte = byteArray[i]
    # loop over 8 bit
    bitNo = 7
    while bitNo >= 0:
      # evaluate bit in data string
      mask = (1 << bitNo)
      if (nextByte & mask) > 0:
        # set D16 in help var. EXOR with shift
        h = 0x00010000
      else:
        h = 0
      # clock the shift register
      shiftReg <<= 1
      # evaluate the bit that falls out of the shift register,
      # simultaneously add the input data bit (rightmost + in diagram),
      # this covers the X^16 term
      if (h ^ (shiftReg & 0x00010000)) > 0:
        # check D16 in shift and then here, the level behind GATE A is one
        # add (i.e. XOR) the X^0 + X^5 + X^12 polynome to the shift register
        shiftReg ^= polynom
      # the else branch is empty, as the level behind gate A is 0
      # and XORing with zero has no effect
      bitNo -= 1
    i += 1
  return (shiftReg & 0x0000FFFF)
