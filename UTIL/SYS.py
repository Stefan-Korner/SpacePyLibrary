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
# Utilities - System Module                                                   *
#******************************************************************************
import os

#############
# constants #
#############
ESCAPE_STR = "\033"
LOG_STR = ""
INFO_STR = ESCAPE_STR + "[30;102m"
WARNING_STR = ESCAPE_STR + "[30;103m"
ERROR_STR = ESCAPE_STR + "[30;101m"
RESET_STR = ESCAPE_STR + "[39;49m"

###########
# classes #
###########
# =============================================================================
class Error(Exception):
  """module specific exception to support selective catching"""
  pass

# =============================================================================
class Logger(object):
  """interface for logger implementation"""
  # ---------------------------------------------------------------------------
  def setColorLogging(self, enable):
    """enables/disables color logging"""
    pass
  # ---------------------------------------------------------------------------
  def _log(self, message, subsystem):
    """logs a message"""
    raise Error("Logger interface method _log() not implemented")
  # ---------------------------------------------------------------------------
  def _logInfo(self, message, subsystem):
    """logs an info message"""
    raise Error("Logger interface method _logInfo() not implemented")
  # ---------------------------------------------------------------------------
  def _logWarning(self, message, subsystem):
    """logs a warning message"""
    raise Error("Logger interface method _logWarning() not implemented")
  # ---------------------------------------------------------------------------
  def _logError(self, message, subsystem):
    """logs an error message"""
    raise Error("Logger interface method _logError() not implemented")

# =============================================================================
class DefaultLogger(Logger):
  """simple logger that logs via print"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """defines the printout format"""
    self.childDefaultLogger = None
    self.childLoggers = {}
    self.logFile = None
    self.setColorLogging(False)
  # ---------------------------------------------------------------------------
  def setColorLogging(self, enable):
    """enables/disables color logging"""
    if enable:
      self.logStr = LOG_STR
      self.infoStr = INFO_STR
      self.warningStr = WARNING_STR
      self.errorStr = ERROR_STR
      self.resetStr = RESET_STR
    else:
      self.logStr = ""
      self.infoStr = "INFO: "
      self.warningStr = "WARNING: "
      self.errorStr = "ERROR: "
      self.resetStr = ""
    # delegate also to child loggers
    if self.childDefaultLogger != None:
      self.childDefaultLogger.setColorLogging(enable)
    for subsystem in self.childLoggers.values():
      childLogger.setColorLogging(enable)
  # ---------------------------------------------------------------------------
  def _log(self, message, subsystem):
    """logs a message"""
    if self.logFile != None:
      if subsystem == None:
        self.logFile.write(self.logStr + message + self.resetStr + "\n")
      else:
        self.logFile.write(self.logStr + "[" + subsystem + "] " + message + self.resetStr + "\n")
      self.logFile.flush()
    elif subsystem in self.childLoggers:
      self.childLoggers[subsystem]._log(message, subsystem)
    elif self.childDefaultLogger != None:
      self.childDefaultLogger._log(message, subsystem)
    else:
      if subsystem == None:
        print self.logStr + message + self.resetStr
      else:
        print self.logStr + "[" + subsystem + "] " + message + self.resetStr
  # ---------------------------------------------------------------------------
  def _logInfo(self, message, subsystem):
    """logs an info message"""
    if self.logFile != None:
      if subsystem == None:
        self.logFile.write(self.infoStr + message + self.resetStr + "\n")
      else:
        self.logFile.write(self.infoStr + "[" + subsystem + "] " + message + self.resetStr + "\n")
      self.logFile.flush()
    elif subsystem in self.childLoggers:
      self.childLoggers[subsystem]._logInfo(message, subsystem)
    elif self.childDefaultLogger != None:
      self.childDefaultLogger._logInfo(message, subsystem)
    else:
      if subsystem == None:
        print self.infoStr + message + self.resetStr
      else:
        print self.infoStr + "[" + subsystem + "] " + message + self.resetStr
  # ---------------------------------------------------------------------------
  def _logWarning(self, message, subsystem):
    """logs a warning message"""
    if self.logFile != None:
      if subsystem == None:
        self.logFile.write(self.warningStr + message + self.resetStr + "\n")
      else:
        self.logFile.write(self.warningStr + "[" + subsystem + "] " + message + self.resetStr + "\n")
      self.logFile.flush()
    elif subsystem in self.childLoggers:
      self.childLoggers[subsystem]._logWarning(message, subsystem)
    elif self.childDefaultLogger != None:
      self.childDefaultLogger._logWarning(message, subsystem)
    else:
      if subsystem == None:
        print self.warningStr + message + self.resetStr
      else:
        print self.warningStr + "[" + subsystem + "] " + message + self.resetStr
  # ---------------------------------------------------------------------------
  def _logError(self, message, subsystem):
    """logs an error message"""
    if self.logFile != None:
      if subsystem == None:
        self.logFile.write(self.errorStr + message + self.resetStr + "\n")
      else:
        self.logFile.write(self.errorStr + "[" + subsystem + "] " + message + self.resetStr + "\n")
      self.logFile.flush()
    elif subsystem in self.childLoggers:
      self.childLoggers[subsystem]._logError(message, subsystem)
    elif self.childDefaultLogger != None:
      self.childDefaultLogger._logError(message, subsystem)
    else:
      if subsystem == None:
        print self.errorStr + message + self.resetStr
      else:
        print self.errorStr + "[" + subsystem + "] " + message + self.resetStr
  # ---------------------------------------------------------------------------
  def registerChildLogger(self, childLogger, subsystem=None):
    """
    registers a child logger,
    either for a specific subsystem or as replacement for default logs
    """
    if subsystem == None:
      self.childDefaultLogger = childLogger
    else:
      self.childLoggers[subsystem] = childLogger
  # ---------------------------------------------------------------------------
  def unregisterChildLogger(self, subsystem=None):
    """
    unregisters a child logger,
    either for a specific subsystem or for default logs
    """
    if subsystem == None:
      self.childDefaultLogger = None
    else:
      del self.childLoggers[subsystem]
  # ---------------------------------------------------------------------------
  def enableFileLogging(self, fileName):
    """enables logging to a file"""
    if self.logFile != None:
      self.logFile.close()
    try:
      self.logFile = open(fileName, "w")
    except:
      self.logFile = None
      LOG_WARNING("Can not open log file " + fileName)
  # ---------------------------------------------------------------------------
  def disableFileLogging(self):
    """disables logging to a file"""
    if self.logFile != None:
      self.logFile.close()
      self.logFile = None

# =============================================================================
class Configuration(object):
  """configuration manager"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """set an empty configuration dictionary"""
    self.configDictionary = {}
  # ---------------------------------------------------------------------------
  def setDefaults(self, defaults):
    """set default values of configuration variables"""
    global s_logger
    LOG_INFO("configuration variables")
    for default in defaults:
      configVar = default[0]
      # the default value can be overruled by an environment variable
      configVal = os.getenv(configVar)
      if configVal == None:
        configVal = default[1]
        LOG(configVar + " = " + configVal + " (default)")
      else:
        LOG(configVar + " = " + configVal + " (env)")
      # special handling of configuration variables inside the SYS module
      if configVar == "SYS_COLOR_LOG":
        s_logger.setColorLogging(configVal == "1")
      self.configDictionary[configVar] = configVal
  # ---------------------------------------------------------------------------
  def __getattr__(self, name):
    """read access to configuration variables"""
    # try first access to fields from attribute map 1
    if name in self.configDictionary:
      return self.configDictionary[name]
    raise AttributeError("configuration variable not found")

####################
# global variables #
####################
# configuration is a singleton
s_configuration = Configuration()
# logger is a singleton
s_logger = DefaultLogger()

#############
# functions #
#############
def LOG(message, subsystem=None):
  """convenience wrapper for logging"""
  s_logger._log(message, subsystem)
def LOG_INFO(message, subsystem=None):
  """convenience wrapper for info logging"""
  s_logger._logInfo(message, subsystem)
def LOG_WARNING(message, subsystem=None):
  """convenience wrapper for warning logging"""
  s_logger._logWarning(message, subsystem)
def LOG_ERROR(message, subsystem=None):
  """convenience wrapper for error logging"""
  s_logger._logError(message, subsystem)
