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
# User Interface infrastructure - Tkinter support classes                     *
#                                                                             *
# Description: Depending on the available version of Tkinter either the       *
#              original "old" Tk widgets are created of a mix of original     *
#              and "new" Tkk widgets are used:                                *
#              - The GUI based on the old widget set provides for each view a *
#                separate window.                                             *
#              - The GUI based on the new widget set has only one application *
#                window and for each view a separate notebook tab.            *
#                Note: The usage of Tkk is completely encapsulated here.      *
#******************************************************************************
import Tkinter, tkFileDialog, tkMessageBox, tkSimpleDialog, os, sys
from UTIL.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import UTIL.SYS, UTIL.TASK
try:
  import ttk
  GUITYPE = "ttk"
except:
  GUITYPE = "Tkinter"

####################
# global variables #
####################
s_gui = None
s_windows = []
s_views = []

###########
# classes #
###########
# =============================================================================
class AppGrid(object):
  """Helper class for grid layout"""
  # ---------------------------------------------------------------------------
  def appGrid(self,
              widget,
              row=0,
              column=0,
              rowspan=1,
              columnspan=1,
              rowweight=1,
              columnweight=1,
              sticky=Tkinter.EW+Tkinter.NS):
    """Places a widget into the embedded application grid"""
    widget.grid(row=row,
                column=column,
                rowspan=rowspan,
                columnspan=columnspan,
                sticky=sticky)
    self.rowconfigure(row, weight=rowweight)
    self.columnconfigure(column, weight=columnweight)

# =============================================================================
class GUItask(UTIL.TASK.Task):
  """Tkinter based task, is the parent task (in the main thread)"""
  # ---------------------------------------------------------------------------
  def __init__(self):
    """initialise attributes"""
    UTIL.TASK.Task.__init__(self, isParent=True, isProcessing=False)
  # ---------------------------------------------------------------------------
  def run(self):
    """processes the event loop, overloaded from UTIL.TASK.Task.run"""
    self.running = True
    self.poll()
    s_gui.mainloop()
  # ---------------------------------------------------------------------------
  def poll(self):
    """overloaded from UTIL.TASK.Task.poll"""
    UTIL.TASK.Task.poll(self)
    if not self.running:
      s_gui.quit()
  # ---------------------------------------------------------------------------
  def createFileHandler(self, socket, handler):
    """
    register a file descriptor handler - only works on single threaded UNIX,
    overloaded from UTIL.TASK.Task.createFileHandler
    """
    Tkinter.tkinter.createfilehandler(socket,
                                      Tkinter.tkinter.READABLE,
                                      handler)
  # ---------------------------------------------------------------------------
  def deleteFileHandler(self, socket):
    """
    unregister a file descriptor handler - only works on single threaded UNIX,
    overloaded from UTIL.TASK.Task.deleteFileHandler
    """
    Tkinter.tkinter.deletefilehandler(socket)
  # ---------------------------------------------------------------------------
  def createTimeHandler(self, ms, handler):
    """
    register a time handler - only works on single threaded UNIX,
    overloaded from UTIL.TASK.Task.createTimeHandler
    """
    s_gui.after(ms, handler)

# =============================================================================
class GUIview(Tkinter.Frame, AppGrid, UTIL.TASK.View):
  """Frame with grid layout that consumes status updates"""
  # ---------------------------------------------------------------------------
  def __init__(self, master):
    """register the frame for the reception of status changes"""
    global s_views
    Tkinter.Frame.__init__(self, master)
    self.guiTask().registerView(self)
    s_views.append(self)
  # ---------------------------------------------------------------------------
  def destroy(self):
    """unregister from the GUI task"""
    self.guiTask().unregisterView(self)
    Tkinter.Tk.destroy(self.master)
    s_views.remove(self)
  # ---------------------------------------------------------------------------
  def guiTask(self):
    """provides the gui task"""
    return UTIL.TASK.s_parentTask
  # ---------------------------------------------------------------------------
  def modelTask(self):
    """provides the model task"""
    return UTIL.TASK.s_processingTask
  # ---------------------------------------------------------------------------
  def notifyModelTask(self, argv):
    """updated the model task"""
    # pass the command event to the event queue of the processing task
    event = UTIL.TASK.CommandEvent(argv)
    event.enable(self.modelTask())
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

# =============================================================================
class GUIwinView(GUIview):
  """GUI window contents"""
  # ---------------------------------------------------------------------------
  def __init__(self, master, viewMnemo, viewName):
    """register the window view"""
    GUIview.__init__(self, master)
    self.viewMnemo = viewMnemo
    self.viewName = viewName
    # with old Tkinter there are separate windows with dedicated menues
    if GUITYPE == "Tkinter":
      self.master.protocol("WM_DELETE_WINDOW", self.quitCallback)
      self.master.title(self.getAppMnemo() + " " + self.viewName + " " + self.getAppName() + " " + self.getVersion())
      # menu bar
      self.menubar = Tkinter.Menu(self)
      # file menu
      self.filemenu = Tkinter.Menu(self.menubar, tearoff=0)
      self.filemenu.add_command(label="Save " + viewMnemo + " Log", command=self.saveLogCallback)
      self.filemenu.add_command(label="Quit", command=self.quitCallback)
      self.menubar.add_cascade(label="File", menu=self.filemenu)
      # edit menu
      self.editmenu = Tkinter.Menu(self.menubar, tearoff=0)
      self.editmenu.add_command(label="Clear " + viewMnemo + " Log", command=self.clearLogCallback)
      self.menubar.add_cascade(label="Edit", menu=self.editmenu)
      # command menu
      self.commandmenu = Tkinter.Menu(self.menubar, tearoff=0)
      self.menubar.add_cascade(label="Command", menu=self.commandmenu)
      self.fillCommandMenuItems()
      # help menu
      self.helpmenu = Tkinter.Menu(self.menubar, tearoff=0)
      self.helpmenu.add_command(label="Help", command=self.helpCallback)
      self.helpmenu.add_command(label="About", command=self.aboutCallback)
      self.helpmenu.add_command(label="DumpConfiguration", command=self.dumpConfigurationCallback)
      self.menubar.add_cascade(label="Help", menu=self.helpmenu)
      self.master.config(menu=self.menubar)
    else:
      # prepare a command menu which is attached later on to the notebook win.
      self.commandmenu = None
  # ---------------------------------------------------------------------------
  def fillCommandMenuItems(self):
    """fill the command menu bar, shall be implemented in derived class"""
    pass
  # ---------------------------------------------------------------------------
  def addCommandMenuItem(self, label, command, enabled=True):
    """add an item to the command menu"""
    if enabled:
      self.commandmenu.add_command(label=label, command=command, state=Tkinter.NORMAL)
    else:
      self.commandmenu.add_command(label=label, command=command, state=Tkinter.DISABLED)
  # ---------------------------------------------------------------------------
  def enableCommandMenuItem(self, index):
    """config an item to the command menu"""
    self.commandmenu.entryconfig(index=index, state=Tkinter.NORMAL)
  # ---------------------------------------------------------------------------
  def disableCommandMenuItem(self, index):
    """config an item to the command menu"""
    self.commandmenu.entryconfig(index=index, state=Tkinter.DISABLED)
  # ---------------------------------------------------------------------------
  def saveLogCallback(self):
    """Saves the log to a file"""
    fileName = tkFileDialog.asksaveasfilename(title="Save " + self.viewMnemo + " Log to File")
    if fileName != "":
      try:
        logFile = open(fileName, "w")
        logFile.write(self.messageLogger.text.get(1.0, Tkinter.END))
        LOG_INFO("Log file saved to " + fileName, self.viewMnemo)
      except:
        LOG_WARNING("Can not write log to " + fileName, self.viewMnemo)
  # ---------------------------------------------------------------------------
  def clearLogCallback(self):
    """Clears the log"""
    self.messageLogger.text.delete(1.0, Tkinter.END)
  # ---------------------------------------------------------------------------
  def quitCallback(self):
    """Called when the Quit menu entry is selected"""
    try:
      if tkMessageBox.askyesno(title="Quit Dialog",
                               message="Terminate " + self.getAppName() + "?"):
        self.notifyModelTask(["QUIT"])
    except:
      pass
  # ---------------------------------------------------------------------------
  def helpCallback(self):
    """Called when the Help menu entry is selected"""
    self.notifyModelTask(["HELP"])
  # ---------------------------------------------------------------------------
  def aboutCallback(self):
    """Called when the About menu entry is selected"""
    try:
      tkMessageBox.showinfo(title="About Dialog",
        message=self.viewName + " " + self.getAppName() + " " + self.getVersion() + "\n" +
                "\n" +
                "(C) Stefan Korner, Austria")
    except:
      pass
  # ---------------------------------------------------------------------------
  def dumpConfigurationCallback(self):
    """Called when the DumpConfiguration menu entry is selected"""
    self.notifyModelTask(["DUMPCONFIGURATION"])

# =============================================================================
class NotebookWindow(Tkinter.Tk):
  """
  Application window with a notebook for embedded views.
  An object of this class is only created if there is a new Tkinter (ttk)
  """
  # ---------------------------------------------------------------------------
  def __init__(self):
    """Creates the application window with a menu bar and a notebook"""
    Tkinter.Tk.__init__(self)
    self.protocol("WM_DELETE_WINDOW", self.quitCallback)
    self.title(self.getAppMnemo() + " " + self.getAppName() + " " + self.getVersion())
    # create the menu bar with an empty file menu
    # - the menu entries in the file menu are added later
    # - the command menus for the embedded views are added later
    # - the help menu is added later
    self.menubar = Tkinter.Menu(self)
    # file menu
    self.filemenu = Tkinter.Menu(self.menubar, tearoff=0)
    self.menubar.add_cascade(label="File", menu=self.filemenu)
    # edit menu
    self.editmenu = Tkinter.Menu(self.menubar, tearoff=0)
    self.menubar.add_cascade(label="Edit", menu=self.editmenu)
    self.config(menu=self.menubar)
    # create the notebook
    if GUITYPE == "ttk":
      self.notebook = ttk.Notebook(self)
      self.notebook.grid(column=0, row=0, sticky=(Tkinter.N, Tkinter.W, Tkinter.E, Tkinter.S))
  # ---------------------------------------------------------------------------
  def finaliseCreation(self):
    """finalise the creation of the notebook window"""
    global s_views
    for tab in self.notebook.tabs():
      tabPos = self.notebook.index(tab)
      view = s_views[tabPos]
      # set the correct view name for the tab
      viewName = view.viewName
      self.notebook.tab(tab, text=viewName)
      # create the save log menu item
      viewMnemo = view.viewMnemo
      self.filemenu.add_command(label="Save " + viewMnemo + " Log", command=view.saveLogCallback)
      # create the clear log menu item
      self.editmenu.add_command(label="Clear " + viewMnemo + " Log", command=view.clearLogCallback)
      # create the command menu
      commandmenu = Tkinter.Menu(self.menubar, tearoff=0)
      view.commandmenu = commandmenu
      view.fillCommandMenuItems()
      self.menubar.add_cascade(label=viewMnemo, menu=commandmenu)
    # finalise the file menu
    self.filemenu.add_command(label="Quit", command=self.quitCallback)
    # create the help menu
    helpmenu = Tkinter.Menu(self.menubar, tearoff=0)
    helpmenu.add_command(label="Help", command=self.helpCallback)
    helpmenu.add_command(label="About", command=self.aboutCallback)
    helpmenu.add_command(label="DumpConfiguration", command=self.dumpConfigurationCallback)
    self.menubar.add_cascade(label="Help", menu=helpmenu)
  # ---------------------------------------------------------------------------
  def createTab(self, shortTitle):
    """creates a tab for the notebook"""
    if GUITYPE == "ttk":
      tab = ttk.Frame()
      self.notebook.add(tab, text=shortTitle)
      return tab
  # ---------------------------------------------------------------------------
  def quitCallback(self):
    """Called when the Quit menu entry is selected"""
    try:
      if tkMessageBox.askyesno(title="Quit Dialog",
                               message="Terminate " + self.getAppName() + "?"):
        self.notifyModelTask(["QUIT"])
    except:
      pass
  # ---------------------------------------------------------------------------
  def helpCallback(self):
    """Called when the Help menu entry is selected"""
    self.notifyModelTask(["HELP"])
  # ---------------------------------------------------------------------------
  def aboutCallback(self):
    """Called when the About menu entry is selected"""
    try:
      tkMessageBox.showinfo(title="About Dialog",
        message=self.getAppName() + " " + self.getVersion() + "\n" +
                "\n" +
                "(C) Stefan Korner, Austria")
    except:
      pass
  # ---------------------------------------------------------------------------
  def dumpConfigurationCallback(self):
    """Called when the DumpConfiguration menu entry is selected"""
    self.notifyModelTask(["DUMPCONFIGURATION"])
  # ---------------------------------------------------------------------------
  def modelTask(self):
    """provides the model task"""
    return UTIL.TASK.s_processingTask
  # ---------------------------------------------------------------------------
  def notifyModelTask(self, argv):
    """updated the model task"""
    # pass the command event to the event queue of the processing task
    event = UTIL.TASK.CommandEvent(argv)
    event.enable(self.modelTask())
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

# =============================================================================
class ScrolledListbox(Tkinter.Frame):
  """Tkinter.Listbox with scroll bars, implemented as Tkinter.Frame"""
  # ---------------------------------------------------------------------------
  def __init__(self, master, selectmode):
    """Attaches the scrollbars to the embedded listbox"""
    Tkinter.Frame.__init__(self, master, relief=Tkinter.GROOVE, borderwidth=1)
    # listbox
    self.listbox = Tkinter.Listbox(self, selectmode=selectmode)
    self.listbox.grid(row=0, column=0, sticky=Tkinter.EW+Tkinter.NS)
    self.rowconfigure(0, weight=1)
    self.columnconfigure(0, weight=1)
    # horizontal scrollbar
    self.hscrollbar = Tkinter.Scrollbar(self,
                                        orient=Tkinter.HORIZONTAL,
                                        command=self.listbox.xview)
    self.hscrollbar.grid(row=1, column=0, sticky=Tkinter.EW)
    # vertival scrollbar
    self.vscrollbar = Tkinter.Scrollbar(self,
                                        orient=Tkinter.VERTICAL,
                                        command=self.listbox.yview)
    self.vscrollbar.grid(row=0, column=1, sticky=Tkinter.NS)
    self.listbox.config(xscrollcommand=self.hscrollbar.set,
                        yscrollcommand=self.vscrollbar.set)
  # ---------------------------------------------------------------------------
  def list(self):
    """Helper for direct access of the embedded listbox"""
    return self.listbox

# =============================================================================
class ScrolledText(Tkinter.Frame):
  """Tkinter.Text with scroll bars, implemented as Tkinter.Frame"""
  # ---------------------------------------------------------------------------
  def __init__(self, master):
    Tkinter.Frame.__init__(self, master, relief=Tkinter.GROOVE, borderwidth=1)
    # listbox
    self.text = Tkinter.Text(self)
    self.text.grid(row=0, column=0, sticky=Tkinter.EW+Tkinter.NS)
    self.rowconfigure(0, weight=1)
    self.columnconfigure(0, weight=1)
    # horizontal scrollbar
    self.hscrollbar = Tkinter.Scrollbar(self,
                                        orient=Tkinter.HORIZONTAL,
                                        command=self.text.xview)
    self.hscrollbar.grid(row=1, column=0, sticky=Tkinter.EW)
    # vertival scrollbar
    self.vscrollbar = Tkinter.Scrollbar(self,
                                        orient=Tkinter.VERTICAL,
                                        command=self.text.yview)
    self.vscrollbar.grid(row=0, column=1, sticky=Tkinter.NS)
    self.text.config(xscrollcommand=self.hscrollbar.set,
                     yscrollcommand=self.vscrollbar.set)
  # ---------------------------------------------------------------------------
  def text(self):
    """Helper for direct access of the text widget"""
    return self.text

# =============================================================================
class MessageLogger(ScrolledText, UTIL.SYS.Logger):
  """Scrolled text which implements a GUI based UTIL.SYS.Logger"""
  # ---------------------------------------------------------------------------
  def __init__(self, master, subsystem=None):
    """Registers the scrolled text as child logger"""
    ScrolledText.__init__(self, master)
    self.subsystem = subsystem
    UTIL.SYS.s_logger.registerChildLogger(self, subsystem)
    # Defines the tags used for the different error severities
    self.text.tag_config("log", foreground="black", background="white")
    self.text.tag_config("info", foreground="black", background="green")
    self.text.tag_config("warn", foreground="black", background="yellow")
    self.text.tag_config("err", foreground="black", background="red")
  # ---------------------------------------------------------------------------
  def __del__(self):
    """Unregisters the scrolled text as child logger"""
    UTIL.SYS.s_logger.unregisterChildLogger(self.subsystem)
  # ---------------------------------------------------------------------------
  def insertLine(self, text, style):
    """Appends a line at the end of the message window"""
    # this message is probably called in a background thread (e.g. processing
    # task) and must be passed to the gui task
    event = LogEvent(self, text, style)
    event.enable(UTIL.TASK.s_parentTask)
  # ---------------------------------------------------------------------------
  def insertLineCallback(self, text, style):
    """Appends a line at the end of the message window"""
    # this message must be invoked in the gui task
    self.text.insert(Tkinter.END, text + "\n", style)
    self.text.yview_moveto(1)
  # ---------------------------------------------------------------------------
  def _log(self, message, subsystem):
    """logs a message"""
    self.insertLine(message, "log")
  # ---------------------------------------------------------------------------
  def _logInfo(self, message, subsystem):
    """logs an info message"""
    self.insertLine(message, "info")
  # ---------------------------------------------------------------------------
  def _logWarning(self, message, subsystem):
    """logs a warning message"""
    self.insertLine(message, "warn")
  # ---------------------------------------------------------------------------
  def _logError(self, message, subsystem):
    """logs an error message"""
    self.insertLine(message, "err")
  # ---------------------------------------------------------------------------
  def close(self):
    """Delegates the closing of the logger to the original implementation"""
    if self.originalLogger != None:
      return self.originalLogger.close()
    return True

# =============================================================================
class LogEvent(UTIL.TASK.TaskEvent):
  """event that forces a logging in the gui task"""
  # ---------------------------------------------------------------------------
  def __init__(self, messageLogger, text, style):
    """initialize the message fields"""
    self.messageLogger = messageLogger
    self.text = text
    self.style = style
    UTIL.TASK.TaskEvent.__init__(self)
  # ---------------------------------------------------------------------------
  def execute(self):
    """executes the event, overloaded from TaskEvent.execute"""
    self.messageLogger.insertLineCallback(self.text, self.style)

# =============================================================================
class SubFrame(Tkinter.Frame, AppGrid):
  """Maintains a frame with grid layout"""
  # ---------------------------------------------------------------------------
  def __init__(self, master):
    """Initialise the frame"""
    Tkinter.Frame.__init__(self, master, relief=Tkinter.GROOVE, borderwidth=1)

# =============================================================================
class ValueField:
  """Combines a fixed label field and a dynamic value field managed by a StringVar"""
  # ---------------------------------------------------------------------------
  def __init__(self, master, row=0, column=0, label="", width=40, fieldColumnspan=1):
    """Creates the static and dynamic label fields and places the widgets on the grid"""
    self.stringVar = Tkinter.StringVar()
    self.label = Tkinter.Label(master, text=label, anchor=Tkinter.W)
    master.appGrid(self.label, row=row, column=column, rowweight=0, columnweight=0)
    self.field = Tkinter.Label(master,
                               textvariable=self.stringVar,
                               anchor=Tkinter.W,
                               width=width,
                               relief=Tkinter.GROOVE)
    master.appGrid(self.field,
                   row=row,
                   column=column+1,
                   rowweight=0,
                   columnweight=1,
                   columnspan=fieldColumnspan)
  # ---------------------------------------------------------------------------
  def set(self, value):
    """Set a new value for the dynamic label field"""
    self.stringVar.set(str(value))
  # ---------------------------------------------------------------------------
  def setBackground(self, color):
    """Change the background color of the dynamic label field"""
    self.field.config(background=color)
  # ---------------------------------------------------------------------------
  def get(self):
    """Returns the contents of the dynamic label field"""
    return self.stringVar.get()

# =============================================================================
class InputField:
  """Combines a fixed label field and an entry field"""
  # ---------------------------------------------------------------------------
  def __init__(self, master, appGridMaster=None, row=0, column=0, label="", initVal=""):
    """Creates the label and entry field and places the widgets on the grid"""
    if appGridMaster == None:
      appGridMaster = master
    self.label = Tkinter.Label(master, text=label, anchor=Tkinter.W)
    appGridMaster.appGrid(self.label, row=row, column=column, rowweight=0)
    self.field = Tkinter.Entry(master, width=40)
    appGridMaster.appGrid(self.field, row=row, column=column+1, rowweight=0)
    self.field.insert(0, initVal)
  # ---------------------------------------------------------------------------
  def get(self):
    """Returns the contents of the embedded entry field"""
    return self.field.get()

# =============================================================================
class CheckbuttonField(object):
  """Combines a fixed label field and an checkbutton field"""
  # ---------------------------------------------------------------------------
  def __init__(self, master, appGridMaster=None, row=0, column=0, label="", selectcolor="#C0C0C0"):
    """Creates the label and checkbutton and places the widgets on the grid"""
    if appGridMaster == None:
      appGridMaster = master
    self.stringVar = Tkinter.StringVar()
    self.label = Tkinter.Label(master, text=label, anchor=Tkinter.W)
    appGridMaster.appGrid(self.label, row=row, column=column, rowweight=0)
    self.button = Tkinter.Checkbutton(master,
                                      variable=self.stringVar,
                                      selectcolor=selectcolor,
                                      anchor=Tkinter.W)
    appGridMaster.appGrid(self.button, row=row, column=column+1)
  # ---------------------------------------------------------------------------
  def get(self):
    """Returns the status of the embedded checkbutton as boolean"""
    return (self.stringVar.get() == "1")

# =============================================================================
class RadiobuttonsField:
  """Combines fixed label fields and an radiobutton fields"""
  # ---------------------------------------------------------------------------
  def __init__(self, master, appGridMaster=None, row=0, column=0, labels=["?"]):
    """Creates the labels and radiobuttons and places the widgets on the grid"""
    if appGridMaster == None:
      appGridMaster = master
    self.intVar = Tkinter.IntVar(0)
    self.firstButton = None
    self.nrButtons = 0
    for buttonTxt in labels.split("|"):
      label = Tkinter.Label(master, text=buttonTxt, anchor=Tkinter.W)
      appGridMaster.appGrid(label, row=(row+self.nrButtons), column=column, rowweight=0)
      button = Tkinter.Radiobutton(master,
                                   variable=self.intVar,
                                   value=self.nrButtons,
                                   anchor=Tkinter.W)
      if self.firstButton == None:
        self.firstButton = button
      appGridMaster.appGrid(button, row=(row+self.nrButtons), column=column+1)
      self.nrButtons += 1
  # ---------------------------------------------------------------------------
  def get(self):
    """Returns the status of the embedded checkbutton as boolean"""
    return (self.intVar.get())

# =============================================================================
class InputDialog(tkSimpleDialog.Dialog, AppGrid):
  """Input dialog with text field and checkbox entries"""
  # ---------------------------------------------------------------------------
  def __init__(self, master, title, fieldsSpec=[], prompt=""):
    """Stores the parameters, the initialisation is done in the body method"""
    self.prompt = prompt
    self.fieldsSpec = fieldsSpec
    self.fields = []
    tkSimpleDialog.Dialog.__init__(self, master, title=title)
  # ---------------------------------------------------------------------------
  def body(self, master):
    """Initialise the dialog fields"""
    row=0
    if self.prompt != "":
      label = Tkinter.Label(master, text=self.prompt)
      label.grid(row=row, column=0, columnspan=2)
      row += 1
      label = Tkinter.Label(master)
      label.grid(row=row, column=0, columnspan=2)
      row += 1
    firstField = None
    for fieldSpec in self.fieldsSpec:
      isCheckbutton = False
      isRadiobuttons = False
      labelText = ""
      initVal = ""
      if len(fieldSpec) > 0:
        isCheckbutton = (fieldSpec[0] == "Checkbutton")
        isRadiobuttons = (fieldSpec[0] == "Radiobuttons")
      if len(fieldSpec) > 1:
        labelText = str(fieldSpec[1])
      if len(fieldSpec) > 2:
        initVal = str(fieldSpec[2])
      if isCheckbutton:
        field = CheckbuttonField(master=master,
                                 appGridMaster=self,
                                 row=row,
                                 label=labelText)
        if firstField == None:
          firstField = field.button
        row += 1
      elif isRadiobuttons:
        field = RadiobuttonsField(master=master,
                                  appGridMaster=self,
                                  row=row,
                                  labels=labelText)
        if firstField == None:
          firstField = field.firstButton
        row += field.nrButtons
      else:
        field = InputField(master=master,
                           appGridMaster=self,
                           row=row,
                           label=labelText,
                           initVal=initVal)
        if firstField == None:
          firstField = field.field
        row += 1
      self.fields.append(field)
    return firstField
  # ---------------------------------------------------------------------------
  def apply(self):
    """Called when the OK button is pressed"""
    values = []
    for field in self.fields:
      values.append(field.get())
    self.result = values

# =============================================================================
class MenuButtons(SubFrame):
  """Maintains application buttons"""
  # ---------------------------------------------------------------------------
  def __init__(self, master, fieldsSpec=[]):
    """Initialise the buttons"""
    SubFrame.__init__(self, master)
    self.buttons = {}
    column = 0
    for fieldSpec in fieldsSpec:
      if len(fieldSpec) == 0:
        # ignore buttons without a label
        continue
      label = str(fieldSpec[0])
      if len(fieldSpec) == 1:
        button = Tkinter.Button(self,
                                text=label)
      elif len(fieldSpec) == 2:
        button = Tkinter.Button(self,
                                text=label,
                                command=fieldSpec[1])
      elif len(fieldSpec) == 3:
        button = Tkinter.Button(self,
                                text=label,
                                command=fieldSpec[1],
                                foreground=str(fieldSpec[2]))
      elif len(fieldSpec) == 4:
        button = Tkinter.Button(self,
                                text=label,
                                command=fieldSpec[1],
                                foreground=str(fieldSpec[2]),
                                background=str(fieldSpec[3]))
      else:
        button = Tkinter.Button(self,
                                text=label,
                                command=fieldSpec[1],
                                foreground=str(fieldSpec[2]),
                                background=str(fieldSpec[3]),
                                state=fieldSpec[4])
      self.appGrid(button, column=column, columnweight=0)
      self.buttons[label] = button
      column += 1
    # add a label as filler
    filler = Tkinter.Label(self)
    self.appGrid(filler, column=column, sticky=Tkinter.EW)
  # ---------------------------------------------------------------------------
  def setState(self, label, state):
    """
    Sets the state of a button:
    Tkinter.ENABLED....active
    Tkinter.DISABLED...disabled
    """
    if label in self.buttons:
      self.buttons[label].config(state=state)

# =============================================================================
class Checkbuttons(SubFrame):
  """Maintains a set of check buttons"""
  # ---------------------------------------------------------------------------
  def __init__(self, master, fieldsSpec=[]):
    """Initialise the buttons"""
    SubFrame.__init__(self, master)
    self.buttons = {}
    column = 0
    for fieldSpec in fieldsSpec:
      if len(fieldSpec) == 0:
        # ignore buttons without a label
        continue
      label = str(fieldSpec[0])
      if len(fieldSpec) > 3:
        button = CheckbuttonField(self, column=column, label=label, selectcolor=fieldSpec[3])
      else:
        button = CheckbuttonField(self, column=column, label=label)
      if len(fieldSpec) > 1:
        button.button.config(command=fieldSpec[1])
      if len(fieldSpec) > 2:
        button.stringVar.set(str(int(fieldSpec[2])))
      self.buttons[label] = button
      column += 2
  # ---------------------------------------------------------------------------
  def getButtonPressed(self, label):
    """Returns the state True / False of a check button"""
    if label in self.buttons:
      return self.buttons[label].get()
    return False
  # ---------------------------------------------------------------------------
  def setButtonPressed(self, label, state):
    """
    Sets the state of a check button:
    True....button pressed
    False...button unpressed
    """
    if label in self.buttons:
      self.buttons[label].stringVar.set(str(int(state)))

#############
# functions #
#############
# these functions encapsulate platform specific creation of windows:
# - on old Tkinter each GUIview gets its separate window
# - on new Tkinter (ttk) each GUIview gets a notebook tab
# -----------------------------------------------------------------------------
def createGUI():
  """create the GUI layer"""
  global s_gui
  if GUITYPE == "Tkinter":
    s_gui = Tkinter.Tk()
  else:
    s_gui = NotebookWindow()
# -----------------------------------------------------------------------------
def createWindow():
  """creates a window for a frame"""
  global s_gui, s_windows
  if GUITYPE == "Tkinter":
    if len(s_windows) == 0:
      # use the main window
      window = s_gui
    else:
      # create a child window
      window = Tkinter.Toplevel()
  else:
    # create a tab for the notebook window
    title = "win" + str(len(s_windows))
    window = s_gui.createTab(title)
  s_windows.append(window)
  return window
# -----------------------------------------------------------------------------
def finaliseGUIcreation():
  """finalise the creation of the GUI layer"""
  if GUITYPE == "ttk":
    s_gui.finaliseCreation()
