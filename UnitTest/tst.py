#!/usr/bin/env python
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
# Unit Tests                                                                  *
#******************************************************************************
import EN_SPACE.DEF

# for generation of pid.dat
#for pktRecord in EN_SPACE.DEF.TMTC_TM_PACKETS:
#  tmPktDef = EN_SPACE.DEF.TMpktDef(pktRecord)
#  print str(tmPktDef.tmtc_grp) + "\t" + \
#        str(tmPktDef.tmtc_code) + "\t" + \
#        str(tmPktDef.pktAPID) + "\t" + \
#        str(tmPktDef.tmtc_ctrlRecFlag) + "\t" + \
#        str(tmPktDef.tmtc_ctrlErrorFlag) + "\t" + \
#        str(tmPktDef.pktSPID)  + "\t" + \
#        tmPktDef.pktDescr  + "\t" + \
#        "\t" + \
#        "-1\t" + \
#        "0\t" + \
#        "N\t" + \
#        "\t" + \
#        "\t" + \
#        "0\t" + \
#        "\t"

# for generation of tpcf.dat
#for pktRecord in EN_SPACE.DEF.TMTC_TM_PACKETS:
#  tmPktDef = EN_SPACE.DEF.TMpktDef(pktRecord)
#  print str(tmPktDef.pktSPID) + "\t" + \
#        tmPktDef.pktName  + "\t" + \
#        "0"

# for generation of HFAconfig
#for pktRecord in EN_SPACE.DEF.TMTC_TM_PACKETS:
#  tmPktDef = EN_SPACE.DEF.TMpktDef(pktRecord)
#  print "0\tHFATM\t" + str(tmPktDef.pktSPID) + "\t65535\t"

# for generation of ccf.dat
#for pktRecord in EN_SPACE.DEF.TMTC_TM_PACKETS:
#  tmPktDef = EN_SPACE.DEF.TMpktDef(pktRecord)
#  if tmPktDef.pktName[0:2] == "OK":
#    print "CMD" + tmPktDef.pktName[2:] + "\tCMD" + tmPktDef.pktDescr[2:] + "\tEnMAP Command CMD" + tmPktDef.pktDescr[2:] + "\tS\tN\tENMAP_TC\t" + str(tmPktDef.tmtc_grp) + "\t" + str(tmPktDef.tmtc_code) + "\t" + str(tmPktDef.pktAPID) + "\t0\tA\tY\t\t\t" + str(tmPktDef.pktAPID) + "\tN\t0\t\t\t8"

# for generation of cdf.dat
for pktRecord in EN_SPACE.DEF.TMTC_TM_PACKETS:
  tmPktDef = EN_SPACE.DEF.TMpktDef(pktRecord)
  if tmPktDef.pktName[0:2] == "OK":
    print "CMD" + tmPktDef.pktName[2:] + "\tE\tNumerical Test Parameter\t32\t0\t0\tUINT_32\tR\t0\t"
    print "CMD" + tmPktDef.pktName[2:] + "\tE\tString Test Parameter\t0\t32\t0\tV_STRING\tR\t\t"
    print "CMD" + tmPktDef.pktName[2:] + "\tA\tEnMAP Trailer\t280\t9999\t0\t\tR\t0\t"
