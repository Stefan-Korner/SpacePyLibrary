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
class Server(object):
  """TCP/IP server"""
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
    except Exception as ex:
      LOG_ERROR("Can't create server socket: " + str(ex))
      return False
    # set the socket linger
    try:
      connectSocket.setsockopt(socket.SOL_SOCKET,
                               socket.SO_LINGER,
                               struct.pack('ii', 1, 10))
    except Exception as ex:
      LOG_ERROR("Can't set socket linger: " + str(ex))
      connectSocket.close()
      return False
    # set the socket reuse address
    try:
      connectSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except Exception as ex:
      LOG_ERROR("Can't set socket reuse address: " + str(ex))
      connectSocket.close()
      return False
    # bind the server socket
    if hostName == None:
      hostName = socket.gethostname()
    try:
      connectSocket.bind((hostName, self.portNr))
    except Exception as ex:
      LOG_ERROR("Bind the server socket: " + str(ex))
      connectSocket.close()
      return False
    # listen on the server socket
    try:
      connectSocket.listen(5)
    except Exception as ex:
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
    except Exception as ex:
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
    except Exception as ex:
      LOG_ERROR("Close of connect port failed: " + str(ex))
      self.connectSocket = None
      return
    self.connectSocket = None

# =============================================================================
class Client(object):
  """TCP/IP client"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """Initialise attributes only"""
  # ---------------------------------------------------------------------------
  def connectToServer(self, serverHost, serverPort):
    """Connects to the server"""
    # create the data socket
    try:
      dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except Exception as ex:
      LOG_ERROR("Creation of data socket failed: " + str(ex))
      return None
    # connect the data socket to the server
    try:
      dataSocket.connect((serverHost, serverPort))
    except Exception as ex:
      LOG_ERROR("Connection to server " + str(serverPort) + "@" + serverHost + " failed: " + str(ex))
      return None
    return dataSocket

# =============================================================================
class Receiver(object):
  """TCP/IP receiver"""
  # ---------------------------------------------------------------------------
  def __init__(self, task):
    """Initialise attributes only"""
    self.task = task
    self.dataSocket = None
  # ---------------------------------------------------------------------------
  def enableReceiveSocket(self, dataSocket):
    """Enables the socket for reception"""
    if self.dataSocket != None:
      LOG_ERROR("Receive socket already open!")
      return
    self.dataSocket = dataSocket
    # register the data socket
    self.task.createFileHandler(self.dataSocket,
                                self.receiveCallback)
  # ---------------------------------------------------------------------------
  def receiveCallback(self, socket, stateMask):
    """Callback when data are received"""
    LOG_ERROR("Receiver.receiveCallback not implemented")
    sys.exit(-1)
  # ---------------------------------------------------------------------------
  def disableReceiveSocket(self):
    """Disables the receive socket"""
    # check if the receive socket is already open
    if self.dataSocket == None:
      LOG_ERROR("Receive socket not open!")
      return
    # unregister the receive socket
    self.task.deleteFileHandler(self.dataSocket)
    # close the data socket
    try:
      self.dataSocket.close()
    except Exception as ex:
      LOG_ERROR("Close of data socket failed: " + str(ex))
    self.dataSocket = None

# =============================================================================
class SingleClientReceivingServer(Server, Receiver):
  """TCP/IP server that receives data from a single client"""
  # ---------------------------------------------------------------------------
  def __init__(self, task, portNr):
    """Delegates to parent implementations"""
    Server.__init__(self, task, portNr)
    Receiver.__init__(self, task)
  # ---------------------------------------------------------------------------
  def accepted(self, clientSocket):
    """Overloaded from Server"""
    # unregister the connect socket
    self.task.deleteFileHandler(self.connectSocket)
    # enable the client socket for data reception
    self.enableReceiveSocket(clientSocket)
  # ---------------------------------------------------------------------------
  def disconnectClient(self):
    """Disonnects the client"""
    self.disableReceiveSocket()
    # register the connect socket
    self.task.createFileHandler(self.connectSocket,
                                self.connectCallback)

# =============================================================================
class SingleServerReceivingClient(Client, Receiver):
  """TCP/IP client that receives data from a single server"""
  # ---------------------------------------------------------------------------
  def __init__(self, task):
    """Delegates to parent implementations"""
    Client.__init__(self)
    Receiver.__init__(self, task)
  # ---------------------------------------------------------------------------
  def connectToServer(self, serverHost, serverPort):
    """Overloaded from Client"""
    dataSocket = Client.connectToServer(self, serverHost, serverPort)
    # use the data socket for data reception
    self.enableReceiveSocket(dataSocket)
    return dataSocket
  # ---------------------------------------------------------------------------
  def disconnectFromServer(self):
    """Disonnects from server"""
    self.disableReceiveSocket()
