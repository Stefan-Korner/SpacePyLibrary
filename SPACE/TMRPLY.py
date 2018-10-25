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
# Space Simulation - Telemetry Packet Replayer                                *
#******************************************************************************
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import CCSDS.PACKET
import PUS.PACKET
import SCOS.ENV
import SPACE.IF
import UTIL.SYS, UTIL.TIME

#############
# constants #
#############
MAX_PKT_NAME = 12

###########
# classes #
###########
# =============================================================================
class TMpacketReplayerImpl(SPACE.IF.TMpacketReplayer):
  """Implementation of the telemetry packet replayer"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """default constructor"""
    self.items = []
  # ---------------------------------------------------------------------------
  def readReplayFile(self, replayFileName):
    """
    reads TM packets and directives from a replay file
    implementation of SPACE.IF.TMpacketReplayer.readReplayFile
    """
    LOG_WARNING("replayPackets(" + replayFileName + ")", "SPACE")
    useSPIDasKey = (UTIL.SYS.s_configuration.TM_REPLAY_KEY == "SPID") 
    # read the TM packets file
    try:
      tmPacketsFile = open(replayFileName)
    except:
      LOG_ERROR("cannot read " + replayFileName, "SPACE")
      return False
    fileContents = tmPacketsFile.readlines()
    tmPacketsFile.close()
    # load TM packets: parse the file
    lineNr = 0
    segmentationFlags = CCSDS.PACKET.UNSEGMENTED
    for line in fileContents:
      lineNr += 1
      if len(line) == 0:
        # empty line
        continue
      if line[0] == "#":
        # comment
        continue
      # parse the line
      tokens = line.split("(")
      token0 = tokens[0].strip()
      sleepVal = -1
      obtVal = ""
      ertVal = ""
      pktSPID = -1
      pktMnemo = ""
      rawPkt = None
      params = ""
      values = ""
      dataField = None
      if len(tokens) == 1:
        if token0 == "":
          # empty line (should be already handled above)
          continue
        if token0[0] == "#":
          # comment (should be already handled above)
          continue
        if token0 == "firstSegment":
          segmentationFlags = CCSDS.PACKET.FIRST_SEGMENT
          continue
        if token0 == "lastSegment":
          segmentationFlags = CCSDS.PACKET.LAST_SEGMENT
          continue
        # TM packet without parameters
        # could contain the datafield in hex
        tokens = line.split("[")
        token0 = tokens[0].strip()
        if len(token0) > MAX_PKT_NAME:
          # raw packet defined in hex withoutSpaces
          rawPkt = UTIL.DU.str2array(token0, True)
        elif useSPIDasKey:
          try:
            pktSPID = int(token0)
          except:
            LOG_ERROR("syntax error in line " + str(lineNr) + " of " + replayFileName, "SPACE")
            self.items = []
            return False
          pktMnemo = "?"
        else:
          pktMnemo = token0
        if len(tokens) > 1:
          # TM packet has a data field
          # remove a close brake from the reminder
          token1 = tokens[1].split("]")[0].strip()
          dataFieldInfo = token1.split(None, 1)
          if len(dataFieldInfo) < 2:
            LOG_ERROR("syntax error in line " + str(lineNr) + " of " + replayFileName, "SPACE")
          else:
            dataFieldOffset = int(dataFieldInfo[0], 16)
            dataFieldData = UTIL.DU.str2array(dataFieldInfo[1])
            dataField = [dataFieldOffset, dataFieldData]
      else:
        # remove a close brake from the reminder
        token1 = tokens[1].split(")")[0].strip()
        if token0 == "sleep":
          # sleep statement
          try:
            sleepVal = int(token1)
          except:
            LOG_ERROR("syntax error in line " + str(lineNr) + " of " + replayFileName, "SPACE")
            self.items = []
            return False
        elif token0 == "obt":
          # onboard time
          obtVal = token1
        elif token0 == "ert":
          # earth reception time
          ertVal = token1
        else:
          # TM packet with parameters
          if useSPIDasKey:
            try:
              pktSPID = int(token0)
            except:
              LOG_ERROR("syntax error in line " + str(lineNr) + " of " + replayFileName, "SPACE")
              self.items = []
              return False
            pktMnemo = "?"
          else:
            pktMnemo = token0
            pktSPID = -1
          paramValueTokens = token1.split(",")
          for paramValueToken in paramValueTokens:
            paramValueSplit = paramValueToken.split("=")
            if len(paramValueSplit) != 2:
              LOG_ERROR("syntax error in line " + str(lineNr) + " of " + replayFileName, "SPACE")
              self.items = []
              return False
            paramName = paramValueSplit[0].strip()
            paramValue = paramValueSplit[1].strip()
            if params == "":
              params += paramName
              values += paramValue
            else:
              params += "," + paramName
              values += "," + paramValue
      # line parsed
      if sleepVal != -1:
        # sleep statement
        self.items.append((SPACE.IF.RPLY_SLEEP, sleepVal))
      elif obtVal != "":
        # obt statement
        obtTime = UTIL.TIME.getTimeFromASDstr(obtVal)
        self.items.append((SPACE.IF.RPLY_OBT, obtTime))
      elif ertVal != "":
        # ert statement
        ertTime = UTIL.TIME.getTimeFromASDstr(ertVal)
        self.items.append((SPACE.IF.RPLY_ERT, ertTime))
      else:
        # TM packet statement --> create the TM packet
        if rawPkt != None:
          self.items.append((SPACE.IF.RPLY_RAWPKT, rawPkt))
        else:
          if useSPIDasKey:
            tmPacketData = SPACE.IF.s_definitions.getTMpacketInjectDataBySPID(
              pktSPID, params, values, dataField, segmentationFlags)
          else:
            tmPacketData = SPACE.IF.s_definitions.getTMpacketInjectData(
              pktMnemo, params, values, dataField, segmentationFlags)
          # check the TM packet
          if tmPacketData == None:
            LOG_ERROR("error in line " + str(lineNr) + " of " + replayFileName, "SPACE")
            self.items = []
            return False
          self.items.append((SPACE.IF.RPLY_PKT, tmPacketData))
        # change the state of the segmentationFlags
        # Note: this is global and not per APID
        if segmentationFlags == CCSDS.PACKET.FIRST_SEGMENT:
          segmentationFlags = CCSDS.PACKET.CONTINUATION_SEGMENT
        elif segmentationFlags == CCSDS.PACKET.LAST_SEGMENT:
          segmentationFlags = CCSDS.PACKET.UNSEGMENTED
    return True
  # ---------------------------------------------------------------------------
  def getItems(self):
    """
    returns items from the replay file
    implementation of SPACE.IF.TMpacketReplayer.getItems
    """
    return self.items
  # ---------------------------------------------------------------------------
  def getNextItem(self):
    """
    returns next item from the replay list or None
    implementation of SPACE.IF.TMpacketReplayer.getNextItem
    """
    if len(self.items) > 0:
      return self.items.pop(0)
    return None

#############
# functions #
#############
def init():
  # initialise singleton(s)
  SPACE.IF.s_tmPacketReplayer = TMpacketReplayerImpl()
