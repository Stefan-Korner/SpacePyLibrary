::*****************************************************************************
:: (C) 2014, Stefan Korner, Austria                                           *
::                                                                            *
:: The Space Python Library is free software; you can redistribute it and/or  *
:: modify it under the terms of the GNU Lesser General Public License as      *
:: published by the Free Software Foundation; either version 2.1 of the       *
:: License, or (at your option) any later version.                            *
::                                                                            *
:: The Space Python Library is distributed in the hope that it will be useful,*
:: but WITHOUT ANY WARRANTY; without even the implied warranty of             *
:: MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser    *
:: General Public License for more details.                                   *
::*****************************************************************************
:: Start scrip for the SCOE.                                                  *
::*****************************************************************************
set TC_ACK_ACCEPT_SUCC_MNEMO=TC_ACK_1_1
set TC_ACK_ACCEPT_FAIL_MNEMO=TC_ACK_1_2
set TC_ACK_EXESTA_SUCC_MNEMO=TC_ACK_1_3
set TC_ACK_EXESTA_FAIL_MNEMO=TC_ACK_1_4
set TC_ACK_EXEPRO_SUCC_MNEMO=TC_ACK_1_5
set TC_ACK_EXEPRO_FAIL_MNEMO=TC_ACK_1_6
set TC_ACK_EXECUT_SUCC_MNEMO=TC_ACK_1_7
set TC_ACK_EXECUT_FAIL_MNEMO=TC_ACK_1_8
set TC_ACK_APID_PARAM_BYTE_OFFSET=10
set TC_ACK_SSC_PARAM_BYTE_OFFSET=12
set TM_CYCLIC_MNEMO=ZYCLIC
set TCO_MISSION_EPOCH_STR="1970.001.00.00.00.000000"
set scosii_homedir=D:\Programming\SpacePyLibrary\scosii_homedir
set PYTHONPATH=D:\Programming\SpacePyLibrary;D:\Programming\SpacePyLibrary\UnitTest
set HOST=192.168.1.105
python SCOE.py dummy




