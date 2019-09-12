#!/usr/bin/env python
#******************************************************************************
# (C) 2019, Stefan Korner, Austria                                            *
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
# Tutorial - Example_4                                                        *
#******************************************************************************
from UTIL.SYS import LOG
import UTIL.SYS

#############
# constants #
#############
SYS_CONFIGURATION = [
  ["ENV_VAR_1", "123"],
  ["ENV_VAR_2", "second configuration variable"]]

########
# main #
########
# initialise the system configuration
UTIL.SYS.s_configuration.setDefaults(SYS_CONFIGURATION)
# fetch the configuration items and print it
LOG("ENV_VAR_1 = " + UTIL.SYS.s_configuration.ENV_VAR_1)
LOG("ENV_VAR_2 = " + UTIL.SYS.s_configuration.ENV_VAR_2)
