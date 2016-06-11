#******************************************************************************
# (C) 2014, Stefan Korner, Austria                                            *
#                                                                             *
# The Space Python Library is free software; you can redistribute it and/or   *
# modify it under the terms of the GNU Lesser General Public License as       *
# published by the Free Software Foundation; either version 2.1 of the        *
# License, or (at your option) any later version.                             *
#                                                                             *
# The Space Python Library is distributed in the hope that it will be useful, *
# but WITHOUT ANY WARRANTY; without even the implied warranty of              *
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser     *
# General Public License for more details.                                    *
#******************************************************************************
# Utilities - Task Module                                                     *
#                                                                             *
# Description: A Task is a control unit that coordinates the execution of     *
#              asynchronous event processing. All processing of a Task is     *
#              within the same thread. On single-threaded python              *
#              (e.g. SuSE 8) all tasks are processed within the main thread.  *
#              On multi-threaded python (e.g. Active Python 8.5 or SUSE 10)   *
#              each Task has a dedicated thread. A Task can be                *
#              - the parent task: it is always processed in the main thread.  *
#                Access to the parent task is possible through the global     *
#                variable s_parentTask. There should be only 1 parent task    *
#                at all.                                                      *
#              - a child task: it is attached to the parent task and          *
#                processed in the main thread (single-threaded python) or in  *
#                a background thread (multi-threaded python). The child       *
#                tasks can be accessed via the global list s_childTasks.      *
#              It is also possible to mark a task as "processingTask".        *
#              This shall be used if the application has a dedicated task     *
#              that shall be globally visible via variable s_processingTask.  *
#                                                                             *
#              A Task can process the following sources:                      *
#              - socket events (e.g. TCP/IP readers) that are installed via   *
#                createFileHandler and deleteFileHandler                      *
#              - timer events that are installed via createTimeHandler        *
#              - Event objects that can be created in any parallel thread     *
#                and be pushed to the task via pushEvent                      *
#              - console events that are attached to the task via             *
#                registerConsoleHandler                                       *
#              - an idle job that is called at least all 20 ms                *
#              Note: the events shall only do small pieces of work within an  *
#              invocation, otherwise the processing of the other events will  *
#              be delayed.                                                    *
#                                                                             *
#              A Task supports the registration of Views. This can be used    *
#              either from special type of Events (StatusEvents) or in the    *
#              implementation of a derived Task class to invoke broadcasting  *
#              of notifications via notifyViews.                              *
#                                                                             *
#              The kind of sources that are processed from a Task can be      *
#              enhanced or restricted in derived classes. This is needed to   *
#              provide a transparent integration of a GUI library             *
#              (e.g. Tkinter). In this case the GUI occupies the ParentTask.  *
#******************************************************************************
import os, signal, select, socket, struct, sys, threading, time
if sys.platform == "win32":
  import msvcrt
  PLATFORM = "win32"
else:
  versionList = sys.version.split()
  if versionList[0] == "2.2.2":
    PLATFORM = "Linux_old"
  else:
    PLATFORM = "Linux_new"
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import UTIL.SYS

#############
# constants #
#############
# Task types
PARENT = 0
THREAD = 1
FAKETHREAD = 2
# for interactive events and view synchronisation (in seconds)
POLL_CYCLE = 0.020
# maximum length of RequestHandler commands
LINEBUFFERLEN =  256

####################
# global variables #
####################
s_parentTask = None
s_processingTask = None
s_childTasks = []

###########
# classes #
###########
# =============================================================================
class Task(threading.Thread):
  """A task is an execution unit attached to a thread."""
  # ---------------------------------------------------------------------------
  def __init__(self, isParent, isProcessing):
    """initialises whether the task is a parent or a child"""
    global s_parentTask, s_processingTask, s_childTasks
    self.running = False
    self.eventBuffer = []
    self.views = {}
    self.readDictionary = {}
    self.timerEvents = []
    self.consoleHandler = None
    self.consoleHandlerIsPolling = False
    if isProcessing:
      s_processingTask = self
    if isParent:
      s_parentTask = self
      self.taskType = PARENT
    else:
      s_childTasks.append(self)
      if PLATFORM == "Linux_old":
        # platform is single threaded
        self.taskType = FAKETHREAD
      else:
        self.taskType = THREAD
        threading.Thread.__init__(self)
  # ---------------------------------------------------------------------------
  # Task Control
  # ---------------------------------------------------------------------------
  def start(self):
    """starts the task depending on the task type"""
    if self.taskType == PARENT:
      self.run()
    elif self.taskType == THREAD:
      threading.Thread.start(self)
    else:
      # if this is a faked thread only enable the polling
      self.running = True
      self.poll()
  # ---------------------------------------------------------------------------
  def run(self):
    """processes the event loop"""
    # note: this method is not used if this is a faked thread
    self.running = True
    # enable the polling
    self.poll()
    # process the events: blocks the thread!
    while self.running:
      # --- prepare readers ---
      readers = self.readDictionary.keys()
      # --- prepare timers ---
      # clone the timers because they might be modified by handlers
      timers = list(self.timerEvents)
      # calculate the timeout for the earliest timer
      if len(timers) == 0:
        # no timer registered
        timeout = POLL_CYCLE
      else:
        # timer registered ---> take the relative time of the 1st timer event
        timeAbsoluteSec = time.time()
        nextTimeoutAbsoluteSec = timers[0][0]
        nextTimeoutRelativeSec = nextTimeoutAbsoluteSec - timeAbsoluteSec
        # don't use negative timeouts and timeouts > POLL_CYCLE
        timeout = max(0.0, nextTimeoutRelativeSec)
        timeout = min(POLL_CYCLE, timeout)
      # --- wait for an event or timeout ---
      # use sleep or select depending on the number of readers
      if len(readers) == 0:
        time.sleep(timeout)
        status = [[], [], []]
      else:
        try:
          status = select.select(readers, [], [], timeout)
        except Exception, ex:
          LOG_ERROR("Select terminated unexcepted: " + str(ex))
          sys.exit(-1)
      # --- process readers ---
      # contains only those readers which have data
      readers = status[0]
      # try to invoke for these readers the corresponding read method
      for reader in readers:
        if reader in self.readDictionary:
          # reader found --> invoke method
          readMethod = self.readDictionary[reader]
          readMethod(reader, None)
        else:
          LOG_WARNING("Reader no more in the read dictionary")
      # --- process timers ---
      timeAbsoluteSec = time.time()
      i = 0
      while i < len(timers):
        nextTimeoutAbsoluteSec = timers[i][0]
        if nextTimeoutAbsoluteSec <= timeAbsoluteSec:
          timerMethod = timers[i][1]
          timerMethod()
          i += 1
        else:
          # too early for the next timeout
          break
      # remove all processed timer events
      self.timerEvents = self.timerEvents[i:]
  # ---------------------------------------------------------------------------
  def stop(self):
    """shall be used (e.g. from outside) to terminate the task"""
    self.running = False
  # ---------------------------------------------------------------------------
  def join(self):
    """waits until the task is really stopped"""
    self.stop()
    if self.taskType == THREAD:
      threading.Thread.join(self)
  # ---------------------------------------------------------------------------
  def poll(self):
    """
    executes all pending events from the event buffer,
    invokes the console handler (if it is a polling console handler),
    invokes the the idleCallback,
    re-register the delayed execution of this method after ~20 ms
    """
    # process pending events
    while self.running and len(self.eventBuffer) > 0:
      nextEvent = self.eventBuffer.pop(0)
      nextEvent.execute()
    # poll the console hander if there is one registered
    if self.consoleHandler and self.consoleHandlerIsPolling:
      self.consoleHandler.poll()
    # poll the idle callback
    self.idleCallback()
    # re-register after 20 ms
    if self.running:
      pollCycleMs = int(POLL_CYCLE * 1000)
      self.createTimeHandler(pollCycleMs, self.poll)
  # ---------------------------------------------------------------------------
  def idleCallback(self):
    """shall be used to perform frequent processing according to the pool cycle"""
    pass
  # ---------------------------------------------------------------------------
  # File-, Time-, and Console-Handler support
  # ---------------------------------------------------------------------------
  def createFileHandler(self, socket, handler):
    """register a file descriptor handler"""
    # special implementation for faked thread, delegate to parent task
    global s_parentTask
    if self.taskType == FAKETHREAD:
      if s_parentTask:
        s_parentTask.createFileHandler(socket, handler)
      else:
        raise Error("missing parent task for file handler creation")
      return
    # normal implementation
    self.readDictionary[socket] = handler
  # ---------------------------------------------------------------------------
  def deleteFileHandler(self, socket):
    """unregister a file descriptor handler"""
    # special implementation for faked thread, delegate to parent task
    global s_parentTask
    if self.taskType == FAKETHREAD:
      if s_parentTask:
        s_parentTask.deleteFileHandler(socket)
      return
    # normal implementation
    if socket in self.readDictionary:
      del self.readDictionary[socket]
  # ---------------------------------------------------------------------------
  def createTimeHandler(self, ms, handler):
    """register a time handler"""
    # special implementation for faked thread, delegate to parent task
    global s_parentTask
    if self.taskType == FAKETHREAD:
      if s_parentTask:
        s_parentTask.createTimeHandler(ms, handler)
      else:
        raise Error("missing parent task for time handler creation")
      return
    # normal implementation: create new timer event and order it into
    # existing ordered timer events
    timeAbsoluteSec = time.time()
    timeoutAbsoluteSec = timeAbsoluteSec + (ms / 1000.0)
    timerEvent = (timeoutAbsoluteSec, handler)
    i = 0
    while i < len(self.timerEvents):
      nextTimeout = self.timerEvents[i][0]
      if nextTimeout > timeoutAbsoluteSec:
        break
      i += 1
    self.timerEvents.insert(i, timerEvent)
  # ---------------------------------------------------------------------------
  def registerConsoleHandler(self, consoleHandler):
    """registers a handler that processes the console input"""
    self.consoleHandler = consoleHandler
    if PLATFORM == "win32":
      # on windows the console handler must be polled
      self.consoleHandlerIsPolling = True
    else:
      # on UNIX the console handler use the normal file handler API
      self.consoleHandlerIsPolling = False
      self.createFileHandler(sys.stdin, consoleHandler.receiveCallback)
  # ---------------------------------------------------------------------------
  # External Event processing support
  # ---------------------------------------------------------------------------
  def pushEvent(self, event):
    """puts an event in the event buffer for execution by the poll loop"""
    self.eventBuffer.append(event)
  # ---------------------------------------------------------------------------
  def registerView(self, view):
    """registers a view for status updates"""
    self.views[view] = view
  # ---------------------------------------------------------------------------
  def unregisterView(self, view):
    """unregisters a view for status updates"""
    del self.views[view]
  # ---------------------------------------------------------------------------
  def notifyViews(self, status):
    """notifies the views with status updates"""
    for view in self.views.keys():
      view.notifyStatus(status)
  # ---------------------------------------------------------------------------
  def notifyCommand(self, argv):
    """notifies with a command (string list)"""
    pass

# =============================================================================
class ProcessingTask(Task):
  """A task that performs the processing of the application."""
  # ---------------------------------------------------------------------------
  def __init__(self, isParent):
    """initialises whether the task is a parent or a child"""
    Task.__init__(self, isParent=isParent, isProcessing=True)
  # ---------------------------------------------------------------------------
  def getAppMnemo(self):
    """Application Mnemonic"""
    return UTIL.SYS.s_configuration.SYS_APP_MNEMO
  # ---------------------------------------------------------------------------
  def getAppName(self):
    """Application Name"""
    return UTIL.SYS.s_configuration.SYS_APP_NAME
  # ---------------------------------------------------------------------------
  def getVersion(self):
    """Application Version, should be in line with the User Manual"""
    return UTIL.SYS.s_configuration.SYS_APP_VERSION
  # ---------------------------------------------------------------------------
  def logMethod(self, methodName, subsystem=None):
    """Logs a method name"""
    LOG_INFO(self.getAppMnemo() + "." + methodName, subsystem)
  # ---------------------------------------------------------------------------
  def notifyCommand(self, argv):
    """Callback for processing the input arguments"""
    if len(argv) > 0:
      # decode the command
      cmd = argv[0].upper()
      if cmd == "H" or cmd == "HELP":
        self.helpCmd(argv)
      elif cmd == "Q" or cmd == "QUIT":
        self.quitCmd(argv)
      else:
        LOG_WARNING("Invalid command " + argv[0])
        self.helpCmd([])
    return 0
  # ---------------------------------------------------------------------------
  def helpCmd(self, argv):
    """Decoded help command"""
    LOG_INFO("Available commands:")
    LOG("")
    LOG("h | help ........provides this information")
    LOG("q | quit ........terminates the application")
    LOG("")
  # ---------------------------------------------------------------------------
  def quitCmd(self, argv):
    """Decoded quit command"""
    global s_parentTask
    s_parentTask.stop()

# =============================================================================
class ConsoleHandler(object):
  """generic keyboard handler that can be registers in the ModelTask"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    self.inputLine = ""   # not used on UNIX
  # ---------------------------------------------------------------------------
  def receiveCallback(self, socket, stateMask):
    """Callback when data are received on sys.stdin (UNIX only)"""
    # due to the line buffering of the UNIX shell
    # it is possible to read a full line
    inputLine = sys.stdin.readline()
    # skip the last character in the string, which is "\n"
    inputLine = inputLine[:-1]
    self.processBuffer(inputLine)
  # ---------------------------------------------------------------------------
  def poll(self):
    """Poll for data on msvcrt (Windows only)"""
    completeLineRead = False
    while msvcrt.kbhit():
      nextChar = msvcrt.getche()
      if nextChar == "\r":
        completeLineRead = True
        print ""
        break
      self.inputLine += nextChar
    if completeLineRead:
      self.processBuffer(self.inputLine)
      self.inputLine = ""
  # ---------------------------------------------------------------------------
  def processBuffer(self, buffer):
    """Callback when a line is read from the console"""
    # split the buffer into tokens
    argv = buffer.split()
    # delegate the processing to the processing task
    return UTIL.TASK.s_processingTask.notifyCommand(argv)

# =============================================================================
class RequestHandler(ConsoleHandler):
  """
  Handles the requests invoked by the ART framework
  Goes into background if the commandline switch
  '-bg' or '-background' is used.
  Opens a TCP/IP port if the commandline switch
  '-p <portNr>' or '-port <portNr>' is used.
  """
  # ---------------------------------------------------------------------------
  def __init__(self, argv):
    """Initialise the test driver and fork on demand"""
    ConsoleHandler.__init__(self)
    self.foreground = True
    self.helpRequested = False
    self.portNr = 0
    self.connectSocket = None
    self.clientSocket = None
    self.tcpLineBuffer = ""

    argc = len(argv)
    i = 0;
    for arg in argv:
      LOG("argv[" + str(i) + "] = " + arg)
      i += 1
    # parse command line arguments
    logFileName = None
    i = 0
    while i < argc:
      cmdSwitch = argv[i]
      if (cmdSwitch == "-bg") or (cmdSwitch == "-background"):
        # shall be evaluated in the main program
        self.foreground = False
      elif (cmdSwitch == "-h") or (cmdSwitch == "-help"):
        # shall be evaluated in the main program
        self.helpRequested = True
      elif (cmdSwitch == "-l") or (cmdSwitch == "-logfile"):
        # logfile switch ---> next argument is the logfile name
        i += 1
        if i < argc:
          logFileName = argv[i]
        else:
          LOG_ERROR("no logfile name specified for switch " + cmdSwitch)
          sys.exit(-1)
      elif (cmdSwitch == "-p") or (cmdSwitch == "-port"):
        # port switch ---> next argument is the port number
        i += 1
        if i < argc:
          self.portNr = int(argv[i]);
        else:
          LOG_ERROR("no port number specified for switch " + cmdSwitch)
          sys.exit(-1)
      i += 1

    # checks if the process shall go into background
    if not self.foreground:
      # bring the process into background via fork

      # ignore the SIGCHLD signal before forking,
      # otherwise is inherited by the parent
      signal.signal(signal.SIGCHLD, signal.SIG_IGN)

      # start the process
      process_ID = os.fork()
      if process_ID != 0:
        # this is the parent ---> terminate
        sys.exit(0);
    # enalble the log file only if the process is in foreground or the child
    if logFileName != None:
      UTIL.SYS.s_logger.enableFileLogging(logFileName)
  # ---------------------------------------------------------------------------
  def openConnectPort(self, hostName=None):
    """Open the test driver TCP/IP connect port (TECO connect port)"""
    # check if the port is already open
    if self.connectSocket != None:
      LOG_ERROR("connect port already open!")
      return False

    # create the server socket
    try:
      connectSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except:
      LOG_ERROR("can't create server socket!")
      return False

    # set the socket linger
    try:
      connectSocket.setsockopt(socket.SOL_SOCKET,
                               socket.SO_LINGER,
                               struct.pack('ii', 1, 10))
    except:
      LOG_ERROR("can't set socket linger!")
      connectSocket.close()
      return False

    # set the socket reuse address
    try:
      connectSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    except:
      LOG_ERROR("can't set socket reuse address!")
      connectSocket.close()
      return False

    # bind the server socket
    if hostName == None:
      hostName = socket.gethostname()
    try:
      connectSocket.bind((hostName, self.portNr))
    except:
      LOG_ERROR("bind the server socket!")
      connectSocket.close()
      return False

    # listen on the server socket
    try:
      connectSocket.listen(5)
    except:
      LOG_ERROR("listen on the server socket!")
      connectSocket.close()
      return False

    self.connectSocket = connectSocket
    return True
  # ---------------------------------------------------------------------------
  def closeConnectPort(self):
    """Close the test driver TCP/IP connect port"""
    LOG_INFO("RequestHandler.closeConnectPort")
    # check if the port is already open
    if self.connectSocket == None:
      LOG_ERROR("connect port not open!")
      return False

    try:
      self.connectSocket.close()
    except:
      LOG_ERROR("close of connect port failed!")
      self.connectSocket = None
      return False
    self.connectSocket = None
    return True
  # ---------------------------------------------------------------------------
  def closeClientPort(self):
    """Close the test driver TCP/IP client port"""
    LOG_INFO("RequestHandler.closeClientPort")
    # check if the port is already open
    if self.clientSocket == None:
      LOG_ERROR("data port not open!")
      return False

    try:
      self.clientSocket.close()
    except:
      LOG_ERROR("close of data port failed!")
      self.clientSocket = None
      return False
    self.clientSocket = None
    return True
  # ---------------------------------------------------------------------------
  def tcpConnectCallback(self, socket, stateMask):
    """Callback when a TCP/IP client (e.g. TECO) has connected"""
    # accept the client connection
    try:
      clientSocket,clientHost = self.connectSocket.accept()
    except:
      LOG_ERROR("accept of the client connection failed!")
      return
    self.clientSocket = clientSocket;

    # delegate the remaing processing
    self.connected()
  # ---------------------------------------------------------------------------
  def tcpDataCallback(self, socket, stateMask):
    """Callback when a TCP/IP client (e.g. TECO) has send a command"""
    # read the next set of byte from stdin
    tcpLineBuffer = self.tcpLineBuffer
    try:
      tcpLineBuffer += self.clientSocket.recv(LINEBUFFERLEN);
      LOG("tcpLineBuffer: " + tcpLineBuffer)
    except:
      # read failed
      self.disconnected()
      return

    # handle the input: extract the lines from the line buffer
    lines = tcpLineBuffer.split("\n")
    # the last line has to be handled in a special way and can not be
    # processed directly
    lastLine = lines[-1]
    lines = lines[:-1]
    if lastLine == "":
      # read of the data was complete (incl. "\n")
      pass
    else:
      # last line was cutt off and the rest should come with the next read
      self.tcpLineBuffer = lastLine

    for line in lines:
      # remove a terminating "\r" for clients like telnet
      if line[-1] == "\r":
        line = line[:-1]
      # terminate the client connection if exit has been entered (case insensitive)
      upperLine = line.upper()
      if (upperLine == "X") or (upperLine == "EXIT"):
        LOG("exit requested")
        # set the OK response back to the TECO
        retString = "OK 0\n"
        try:
          self.clientSocket.send(retString)
        except:
          LOG_ERROR("send of OK response failed!")
        # terminate the client connection
        self.disconnected();
        return
      # delegate the input
      pstatus = self.processBuffer(line);
      if pstatus == 0:
        # send the OK response back to the TECO
        retString = "OK 0\n";
        try:
          self.clientSocket.send(retString)
        except:
          LOG_ERROR("send of OK response failed!")
      else:
        LOG_WARNING("return status = " + str(pstatus))
        # set the Error response back to the TECO:
        retString = "Error: execution failed (see log)!\n"
        try:
          self.clientSocket.send(retString)
        except:
          LOG_ERROR("send of Error response failed!")
  # ---------------------------------------------------------------------------
  def connected(self):
    """Client (TECO) has connected: register/unregister file descriptors"""
    # unregister the connect socket
    UTIL.TASK.s_processingTask.deleteFileHandler(self.connectSocket)
    # register the client socket
    UTIL.TASK.s_processingTask.createFileHandler(self.clientSocket,
                                                 self.tcpDataCallback)
  # ---------------------------------------------------------------------------
  def disconnected(self):
    """Client (TECO) has disconnected: register/unregister file descriptors"""
    clientSocket = self.clientSocket
    # close the client port
    self.closeClientPort()
    # unregister the client socket
    UTIL.TASK.s_processingTask.deleteFileHandler(clientSocket)
    # register the connect socket
    UTIL.TASK.s_processingTask.createFileHandler(self.connectSocket,
                                                 self.tcpConnectCallback)

# =============================================================================
class TaskEvent(object):
  """events that are executed from a task"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """initialize an event for a specific task"""
    self.task = None
  # ---------------------------------------------------------------------------
  def enable(self, task):
    """enables the event for execution"""
    self.task = task
    task.pushEvent(self)
  # ---------------------------------------------------------------------------
  def execute(self):
    """executes the event, shall be overloaded in derived class"""
    pass

# =============================================================================
class ViewEvent(TaskEvent):
  """status event that automatically notifies all views"""
  # ---------------------------------------------------------------------------
  def __init__(self, status):
    """initialize the status"""
    self.status = status
    TaskEvent.__init__(self)
  # ---------------------------------------------------------------------------
  def execute(self):
    """executes the event, overloaded from TaskEvent.execute"""
    self.task.notifyViews(self.status)

# =============================================================================
class CommandEvent(TaskEvent):
  """command event that forces an execution in the task"""
  # ---------------------------------------------------------------------------
  def __init__(self, argv):
    """initialize the status"""
    self.argv = argv
    TaskEvent.__init__(self)
  # ---------------------------------------------------------------------------
  def execute(self):
    """executes the event, overloaded from TaskEvent.execute"""
    self.task.notifyCommand(self.argv)

# =============================================================================
class View(object):
  """consumer of status updates"""
  # ---------------------------------------------------------------------------
  def notifyStatus(self, status):
    """reception of status updates"""
    pass
