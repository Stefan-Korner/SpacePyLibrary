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
# Tutorial - Example_2                                                        *
#******************************************************************************
from UTIL.SYS import LOG, LOG_INFO, LOG_WARNING, LOG_ERROR

########
# main #
########
# different loggings
LOG("this is a simple message")
LOG_INFO("this is an info message")
LOG_WARNING("this is a warning message")
LOG_ERROR("this is an error message")
