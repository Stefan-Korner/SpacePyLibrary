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
# Utilities - TCP/IP Module                                                   *
#******************************************************************************
import socket, struct, sys
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR

###########
# classes #
###########
# =============================================================================
class DataSocketHandler(object):
  """TCP/IP data socket handler"""
  # ---------------------------------------------------------------------------
  def __init__(self, task):
    """Initialise attributes only"""
    self.task = task
    self.dataSocket = None
  # ---------------------------------------------------------------------------
  def enableDataSocket(self, dataSocket):
    """Enables the data socket"""
    if self.dataSocket != None:
      LOG_ERROR("Data socket already open!")
      return
    self.dataSocket = dataSocket
    # register the data socket
    self.task.createFileHandler(self.dataSocket,
                                self.receiveCallback)
  # ---------------------------------------------------------------------------
  def receiveCallback(self, socket, stateMask):
    """Callback when data are received"""
    LOG_ERROR("DataSocketHandler.receiveCallback not implemented")
    sys.exit(-1)
  # ---------------------------------------------------------------------------
  def disableDataSocket(self):
    """Disables the data socket socket"""
    # check if the receive socket is already open
    if self.dataSocket == None:
      LOG_ERROR("Data socket not open!")
      return
    # unregister the receive socket
    self.task.deleteFileHandler(self.dataSocket)
    # close the data socket
    try:
      self.dataSocket.close()
    except Exception, ex:
      LOG_ERROR("Close of data socket failed: " + str(ex))
    self.dataSocket = None

# =============================================================================
class Client(DataSocketHandler):
  """TCP/IP client"""
  # ---------------------------------------------------------------------------
  def __init__(self, task):
    """Delegates to parent implementation"""
    DataSocketHandler.__init__(self, task)
  # ---------------------------------------------------------------------------
  def connectToServer(self, serverHost, serverPort):
    """Connects to the server"""
    # create the data socket
    try:
      dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except Exception, ex:
      LOG_ERROR("Creation of data socket failed: " + str(ex))
      return None
    # connect the data socket to the server
    try:
      dataSocket.connect((serverHost, serverPort))
    except Exception, ex:
      LOG_ERROR("Connection to server " + str(serverPort) + "@" + serverHost + " failed: " + str(ex))
      return None
    # use the data socket
    self.enableDataSocket(dataSocket)
    return dataSocket
  # ---------------------------------------------------------------------------
  def disconnectFromServer(self):
    """Disonnects from server"""
    self.disableDataSocket()

# =============================================================================
class Server(object):
  """TCP/IP server, only handles the connect socket"""
  # ---------------------------------------------------------------------------
  def __init__(self, task, portNr):
    """Initialise attributes only"""
    self.task = task
    self.portNr = portNr
    self.connectSocket = None
  # ---------------------------------------------------------------------------
  def openConnectPort(self, hostName=None):
    """Open the connect port"""
    # check if the port is already open
    if self.connectSocket != None:
      LOG_ERROR("Connect port already open!")
      return False
    # create the server socket
    try:
      connectSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except Exception, ex:
      LOG_ERROR("Can't create server socket: " + str(ex))
      return False
    # set the socket linger
    try:
      connectSocket.setsockopt(socket.SOL_SOCKET,
                               socket.SO_LINGER,
                               struct.pack('ii', 1, 10))
    except Exception, ex:
      LOG_ERROR("Can't set socket linger: " + str(ex))
      connectSocket.close()
      return False
    # set the socket reuse address
    try:
      connectSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except Exception, ex:
      LOG_ERROR("Can't set socket reuse address: " + str(ex))
      connectSocket.close()
      return False
    # bind the server socket
    if hostName == None:
      hostName = socket.gethostname()
    try:
      connectSocket.bind((hostName, self.portNr))
    except Exception, ex:
      LOG_ERROR("Bind the server socket: " + str(ex))
      connectSocket.close()
      return False
    # listen on the server socket
    try:
      connectSocket.listen(5)
    except Exception, ex:
      LOG_ERROR("Listen on the server socket: " + str(ex))
      connectSocket.close()
      return False
    self.connectSocket = connectSocket
    # attach the server socket to the event loop
    self.task.createFileHandler(self.connectSocket,
                                self.connectCallback)
    return True
  # ---------------------------------------------------------------------------
  def connectCallback(self, socket, stateMask):
    """Callback when a client has connected"""
    # accept the client connection
    try:
      clientSocket,clientHost = self.connectSocket.accept()
    except Exception, ex:
      LOG_ERROR("Accept of the client connection failed: " + str(ex))
      return
    # delegate the remaing processing
    self.accepted(clientSocket)
  # ---------------------------------------------------------------------------
  def accepted(self, clientSocket):
    """Shall be overloaded by derived classes"""
    pass
  # ---------------------------------------------------------------------------
  def closeConnectPort(self):
    """Close the connect port"""
    # check if the port is already open
    if self.connectSocket == None:
      LOG_ERROR("Connect port not open!")
      return
    try:
      self.connectSocket.close()
    except Exception, ex:
      LOG_ERROR("Close of connect port failed: " + str(ex))
      self.connectSocket = None
      return
    self.connectSocket = None

# =============================================================================
class SingleClientServer(Server, DataSocketHandler):
  """TCP/IP server that handles a single client"""
  # ---------------------------------------------------------------------------
  def __init__(self, task, portNr):
    """Delegates to parent implementations"""
    Server.__init__(self, task, portNr)
    DataSocketHandler.__init__(self, task)
  # ---------------------------------------------------------------------------
  def accepted(self, clientSocket):
    """Overloaded from Server"""
    # unregister the connect socket
    self.task.deleteFileHandler(self.connectSocket)
    # enable the client socket for data reception
    self.enableDataSocket(clientSocket)
    # call the hook
    self.clientAccepted()
  # ---------------------------------------------------------------------------
  def clientAccepted(self):
    """hook for derived classes"""
    pass
  # ---------------------------------------------------------------------------
  def disconnectClient(self):
    """Disonnects the client"""
    self.disableDataSocket()
    # register the connect socket
    self.task.createFileHandler(self.connectSocket,
                                self.connectCallback)
