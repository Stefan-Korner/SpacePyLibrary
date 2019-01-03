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
# SCOS-2000 Functionality - Environment                                       *
#******************************************************************************
import os, sys
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import UTIL.SYS

###########
# classes #
###########
# =============================================================================
class Environment(object):
  """Manager for environment data"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """initialise from environment variables"""
    self.hostName = os.getenv("HOST")
    self.runtimeRoot = os.getenv("TESTENV")
    if self.runtimeRoot == None:
      LOG_ERROR("TESTENV not initialised")
      sys.exit(-1)
  # ---------------------------------------------------------------------------
  def getRuntimeRoot(self):
    """Get the runtime root directory where the data are stored"""
    return self.runtimeRoot
  # ---------------------------------------------------------------------------
  def mibDir(self):
    """Get the MIB directory"""
    return self.runtimeRoot + "/data/ASCII"
  # ---------------------------------------------------------------------------
  def tmFilesDir(self):
    """Get the TM replay files directory"""
    return self.runtimeRoot + "/data/tmFiles"

####################
# global variables #
####################
# environment is a singleton
s_environment = Environment()
