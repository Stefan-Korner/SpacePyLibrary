#!/bin/csh
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
# Start scrip for TM frame to TM packet converter.                            *
#******************************************************************************
# Command line: FRAME2PACKET.csh <frame dump file name> <packet file name>    *
#******************************************************************************
setenv PYTHON python3
setenv PYTHONPATH ${HOME}/Python/SpacePyLibrary
${PYTHON} FRAME2PACKET.py $1 $2
