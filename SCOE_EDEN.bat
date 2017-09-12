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
set EGSE_PROTOCOL=EDEN
set HOST=127.0.0.1
set CCS_SERVER_PORT2=48570
set TC_ACK_ACCEPT_SUCC_MNEMO=ACK1
set TC_ACK_ACCEPT_FAIL_MNEMO=NAK1
set TC_ACK_EXESTA_SUCC_MNEMO=ACK2
set TC_ACK_EXESTA_FAIL_MNEMO=NAK2
set TC_ACK_EXEPRO_SUCC_MNEMO=ACK3
set TC_ACK_EXEPRO_FAIL_MNEMO=NAK3
set TC_ACK_EXECUT_SUCC_MNEMO=ACK4
set TC_ACK_EXECUT_FAIL_MNEMO=NAK4
set TC_ACK_APID_PARAM_BYTE_OFFSET=18
set TC_ACK_SSC_PARAM_BYTE_OFFSET=20
set TC_FKT_ID_BYTE_OFFSET=10
set TC_FKT_ID_BYTE_SIZE=4
set TM_TT_TIME_FORMAT=CUC4
set TM_TT_TIME_BYTE_OFFSET=10
set TM_CYCLIC_MNEMO=TM_PKT1
set scosii_homedir=D:\Programming\SpacePyLibrary\scosii_homedir
set PYTHONPATH=D:\Programming\SpacePyLibrary;D:\Programming\SpacePyLibrary\UnitTest
python SCOE.py dummy
