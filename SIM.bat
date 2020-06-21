::*****************************************************************************
:: (C) 2018, Stefan Korner, Austria                                           *
::                                                                            *
:: The Space Python Library is free software; you can redistribute it and/or  *
:: modify it under under the terms of the MIT License as published by the     *
:: Massachusetts Institute of Technology.                                     *
::                                                                            *
:: The Space Python Library is distributed in the hope that it will be useful,*
:: but WITHOUT ANY WARRANTY; without even the implied warranty of             *
:: MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the MIT License   *
:: for more details.                                                          *
::*****************************************************************************
:: Start scrip for the SIM simulator.                                         *
:: The file must be adopted if the library is installed in a different folder *
:: than C:\Programming\SpacePyLibrary                                         *
::*****************************************************************************
set PYTHONPATH=C:\Programming\SpacePyLibrary
set TESTENV=C:\Programming\SpacePyLibrary\TESTENV
set HOST=127.0.0.1
set NCTRS_ADMIN_SERVER_PORT=32010
set NCTRS_TC_SERVER_PORT=32009
set NCTRS_TM_SERVER_PORT=22104
set TC_ACK_ACCEPT_SUCC_MNEMO=ACK1
set TC_ACK_ACCEPT_FAIL_MNEMO=NAK1
set TC_ACK_EXESTA_SUCC_MNEMO=ACK1
set TC_ACK_EXESTA_FAIL_MNEMO=NAK1
set TC_ACK_EXEPRO_SUCC_MNEMO=ACK1
set TC_ACK_EXEPRO_FAIL_MNEMO=NAK1
set TC_ACK_EXECUT_SUCC_MNEMO=ACK1
set TC_ACK_EXECUT_FAIL_MNEMO=NAK1
# see also CMD_REP_APPDATA_OFFSET
set TC_ACK_APID_PARAM_BYTE_OFFSET=18
set TC_ACK_SSC_PARAM_BYTE_OFFSET=20
set TC_TT_TIME_FORMAT=CUC4
set TC_TT_TIME_BYTE_OFFSET=11
set TC_TT_PKT_BYTE_OFFSET=17
set TM_CYCLIC_MNEMO=TM_PKT1
set TM_TEST_MNEMO=TESTREP
set TM_TT_TIME_FORMAT=CUC4
set TM_TT_TIME_BYTE_OFFSET=10
set TM_RECORD_FORMAT=NCTRS
set SYS_COLOR_LOG=1
python3 SIM.py dummy
