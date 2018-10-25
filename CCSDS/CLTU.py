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
# CCSDS Stack - CLTU Handling Module                                          *
#******************************************************************************
import array
import UTIL.BCH

#############
# constants #
#############
# CLTU header
CLTU_START_SEQUENCE = [0xEB, 0x90]
CLTU_START_SEQUENCE_SIZE = len(CLTU_START_SEQUENCE)
# fill bytes for last code block
CLTU_FILL_BYTE = 0x55
# compliant with SCOS-2000
CLTU_TRAILER_SEQUENCE = [0x55, 0x55, 0x55, 0x55, 0x55, 0x55, 0x55, 0x55]
# compliant with CCSDS specification
#CLTU_TRAILER_SEQUENCE = [0xC5, 0xC5, 0xC5, 0xC5, 0xC5, 0xC5, 0xC5, 0x79]
CLTU_TRAILER_SEQUENCE_SIZE = len(CLTU_TRAILER_SEQUENCE)
# derived constants
BCH_NETTO_SIZE = UTIL.BCH.CODE_BLOCK_SIZE - 1
BCH_MAX_NETTO_INDEX = BCH_NETTO_SIZE - 1

#############
# functions #
#############
# -----------------------------------------------------------------------------
def encodeCltu(frame):
  """Converts a TC Frame into a CLTU"""
  # iterate over the frame bytes, which are copied
  # into the CLTU body together with BCH code bytes
  frameIdx = 0
  frameSize = len(frame)
  nrCltuCodeBlocks = (frameSize + BCH_MAX_NETTO_INDEX) // BCH_NETTO_SIZE
  cltuBodySize = nrCltuCodeBlocks * UTIL.BCH.CODE_BLOCK_SIZE
  cltuBody = array.array("B", [0] * cltuBodySize)
  cltuBodyIdx = 0
  codeBlkIdx = 0
  while frameIdx < frameSize:
    # handle start of a code block
    if codeBlkIdx == 0:
      sreg = UTIL.BCH.encodeStart()
    # take the next byte from the frame for the CLTU and the BCH encoding
    nextByte = frame[frameIdx]
    cltuBody[cltuBodyIdx] = nextByte
    sreg = UTIL.BCH.encodeStep(sreg, nextByte)
    frameIdx += 1
    cltuBodyIdx += 1
    codeBlkIdx += 1
    # handle end of a code block
    if codeBlkIdx >= BCH_NETTO_SIZE:
      code = UTIL.BCH.encodeStop(sreg)
      cltuBody[cltuBodyIdx] = code
      cltuBodyIdx += 1
      codeBlkIdx = 0
  # fill up remaining bytes in the cltuBody (incl. BCH code byte)
  while cltuBodyIdx < cltuBodySize:
    nextByte = CLTU_FILL_BYTE
    cltuBody[cltuBodyIdx] = nextByte
    sreg = UTIL.BCH.encodeStep(sreg, nextByte)
    cltuBodyIdx += 1
    codeBlkIdx += 1
    # handle end of the code block
    if codeBlkIdx >= BCH_NETTO_SIZE:
      code = UTIL.BCH.encodeStop(sreg)
      cltuBody[cltuBodyIdx] = code
      cltuBodyIdx += 1
  # CLTU body is completely processed
  return (array.array("B", CLTU_START_SEQUENCE) +
          cltuBody +
          array.array("B", CLTU_TRAILER_SEQUENCE))
# -----------------------------------------------------------------------------
def decodeCltu(cltu):
  """Converts a CLTU into a TC Frame"""
  # Note: the returned frame might contain additional fill bytes,
  #       these bytes must be removed at the frame layer
  # calculate the frame size from the CLTU size
  cltuSize = len(cltu)
  cltuBodySize = cltuSize - CLTU_START_SEQUENCE_SIZE - CLTU_TRAILER_SEQUENCE_SIZE
  # check general CLTU properties
  if cltuBodySize < 0:
    return None
  if cltuBodySize % UTIL.BCH.CODE_BLOCK_SIZE != 0:
    return None
  if cltu[:CLTU_START_SEQUENCE_SIZE] != array.array("B", CLTU_START_SEQUENCE):
    return None
  if cltu[-CLTU_TRAILER_SEQUENCE_SIZE:] != array.array("B", CLTU_TRAILER_SEQUENCE):
    return None
  # iterate over the CLTU body bytes, which are copied
  # into the frame, BCH code is checked during the iteration
  nrCltuCodeBlocks = cltuBodySize // UTIL.BCH.CODE_BLOCK_SIZE
  frameSize = nrCltuCodeBlocks * BCH_NETTO_SIZE
  frame = array.array("B", [0] * frameSize)
  frameIdx = 0
  cltuIdx = CLTU_START_SEQUENCE_SIZE
  codeBlkIdx = 0
  while frameIdx < frameSize:
    # handle start of a code block
    if codeBlkIdx == 0:
      sreg = UTIL.BCH.encodeStart()
    # take the next byte from the CLTU for the frame and the BCH decoding
    nextByte = cltu[cltuIdx]
    frame[frameIdx] = nextByte
    sreg = UTIL.BCH.encodeStep(sreg, nextByte)
    frameIdx += 1
    cltuIdx += 1
    codeBlkIdx += 1
    # handle end of a code block
    if codeBlkIdx >= BCH_NETTO_SIZE:
      code = UTIL.BCH.encodeStop(sreg)
      if cltu[cltuIdx] != code:
        return None
      cltuIdx += 1
      codeBlkIdx = 0
  return frame
# -----------------------------------------------------------------------------
def checkCltu(cltu):
  """Checks the consistency of a CLTU"""
  # calculate the frame size from the CLTU size
  cltuSize = len(cltu)
  cltuTrailerStartIdx = cltuSize - CLTU_TRAILER_SEQUENCE_SIZE
  cltuBodySize = cltuTrailerStartIdx - CLTU_START_SEQUENCE_SIZE
  # check general CLTU properties
  if cltuBodySize < 0:
    return False, "cltuBodySize too short"
  if cltuBodySize % UTIL.BCH.CODE_BLOCK_SIZE != 0:
    return False, "wrong cltuBodySize"
  for i in range(0, CLTU_START_SEQUENCE_SIZE):
    if cltu[i] != CLTU_START_SEQUENCE[i]:
      return False, "wrong cltu start sequence"
  for i in range(-CLTU_TRAILER_SEQUENCE_SIZE, 0):
    if cltu[i] != CLTU_TRAILER_SEQUENCE[i]:
      return False, "wrong cltu trailer sequence"
  # iterate over the CLTU body bytes and check the BCH code
  nrCltuCodeBlocks = cltuBodySize // UTIL.BCH.CODE_BLOCK_SIZE
  frameSize = nrCltuCodeBlocks * BCH_NETTO_SIZE
  cltuIdx = CLTU_START_SEQUENCE_SIZE
  codeBlkIdx = 0
  while cltuIdx < cltuTrailerStartIdx:
    # handle start of a code block
    if codeBlkIdx == 0:
      sreg = UTIL.BCH.encodeStart()
    # take the next byte from the CLTU for the frame and the BCH decoding
    nextByte = cltu[cltuIdx]
    sreg = UTIL.BCH.encodeStep(sreg, nextByte)
    cltuIdx += 1
    codeBlkIdx += 1
    # handle end of a code block
    if codeBlkIdx >= BCH_NETTO_SIZE:
      code = UTIL.BCH.encodeStop(sreg)
      if cltu[cltuIdx] != code:
        return False, "wrong BCH check byte"
      cltuIdx += 1
      codeBlkIdx = 0
  return True, "cltu OK"
