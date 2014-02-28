#!/usr/bin/env python
#******************************************************************************
# (C) 2014, Stefan Korner, Austria                                            *
#                                                                             *
# The Space Python Library is free software; you can redistribute it and/or   *
# modify it under the terms of the GNU Lesser General Public License as       *
# published by the Free Software Foundation; either version 2.1 of the        *
# License, or (at your option) any later version.                             *
#                                                                             *
# The Space C++ Library is distributed in the hope that it will be useful,    *
# but WITHOUT ANY WARRANTY; without even the implied warranty of              *
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU Lesser     *
# General Public License for more details.                                    *
#******************************************************************************
# Generic Data Processor - Unit Tests                                         *
#******************************************************************************
from GDP.SYS import Error, LOG, LOG_INFO, LOG_WARNING, LOG_ERROR
import GDP.PM

def test_PMmemoryManagement():
  """main-function to test the automatic model memory allocation"""
  model = GDP.PM.Model("testmodel")
  dataElementIds = model.getDataElementIds()
  dataElementNames = model.getDataElementNames()
  if(len(dataElementIds) != 0):
    print "DataElement id dictionary not empty:", dataElementIds
    return False
  if(len(dataElementNames) != 0):
    print "DataElement name dictionary not empty:", dataElementNames
    return False
  if not PMmemoryManagementSub(model):
    return False
  dataElementIds = model.getDataElementIds()
  dataElementNames = model.getDataElementNames()
  if(len(dataElementIds) != 0):
    print "DataElement id dictionary not empty:", dataElementIds
    return False
  if(len(dataElementNames) != 0):
    print "DataElement name dictionary not empty:", dataElementNames
    return False
  return True

def PMmemoryManagementSub(model):
  """sub-function to test the automatic model memory allocation"""
  # create and test DataElement 1
  dataElement1 = model.createDataElement()
  dataElement1Id = dataElement1.getId()
  dataElement1Name = dataElement1.getName()
  dataElementIds = model.getDataElementIds()
  dataElementNames = model.getDataElementNames()
  # check IDs
  if(len(dataElementIds) != 1):
    print "DataElement id dictionary has wrong size:", dataElementIds
    return False
  if not dataElement1Id in dataElementIds:
    print "DataElement 1 id not in dictionary:", dataElementIds
    return False
  dataElement1Ref = model.getDataElementById(dataElement1Id)
  if dataElement1Ref == None:
    print "Location of DataElement 1 in id dictionary failed"
    return False
  if dataElement1Ref.getId() != dataElement1Id:
    print "Wrong DataElement 1 retrieved by name"
    return False
  # check names
  if(len(dataElementNames) != 0):
    print "DataElement name dictionary not empty:", dataElementNames
    return False
  # create and test DataElement 2
  dataElement2 = model.createDataElement(name="dataElement2")
  dataElement2Id = dataElement2.getId()
  dataElement2Name = dataElement2.getName()
  dataElementIds = model.getDataElementIds()
  dataElementNames = model.getDataElementNames()
  # check IDs
  if(len(dataElementIds) != 2):
    print "DataElement id dictionary has wrong size:", dataElementIds
    return False
  if not dataElement1Id in dataElementIds:
    print "DataElement 1 id not in dictionary:", dataElementIds
    return False
  dataElement1Ref = model.getDataElementById(dataElement1Id)
  if dataElement1Ref == None:
    print "Location of DataElement 1 in id dictionary failed"
    return False
  if dataElement1Ref.getId() != dataElement1Id:
    print "Wrong DataElement 1 retrieved by name"
    return False
  if not dataElement2Id in dataElementIds:
    print "DataElement 2 id not in dictionary:", dataElementIds
    return False
  dataElement2Ref = model.getDataElementById(dataElement2Id)
  if dataElement2Ref == None:
    print "Location of DataElement 2 in id dictionary failed"
    return False
  if dataElement2Ref.getId() != dataElement2Id:
    print "Wrong DataElement 2 retrieved by name"
    return False
  # check names
  if(len(dataElementNames) != 1):
    print "DataElement name dictionary has wrong size:", dataElementNames
    return False
  if not dataElement2Name in dataElementNames:
    print "DataElement 2 name not in dictionary:", dataElementNames
    return False
  dataElement2Ref = model.getDataElementByName(dataElement2Name)
  if dataElement2Name == None:
    print "Location of DataElement 2 in name dictionary failed"
    return False
  if dataElement2Ref.getName() != dataElement2Name:
    print "Wrong DataElement 2 retrieved by name"
    return False
  # create and test DataElement 3
  dataElement3 = model.createDataElement(name="dataElement3")
  dataElement3Id = dataElement3.getId()
  dataElement3Name = dataElement3.getName()
  dataElementIds = model.getDataElementIds()
  dataElementNames = model.getDataElementNames()
  # check IDs
  if(len(dataElementIds) != 3):
    print "DataElement id dictionary has wrong size:", dataElementIds
    return False
  if not dataElement1Id in dataElementIds:
    print "DataElement 1 id not in dictionary:", dataElementIds
    return False
  dataElement1Ref = model.getDataElementById(dataElement1Id)
  if dataElement1Ref == None:
    print "Location of DataElement 1 in id dictionary failed"
    return False
  if dataElement1Ref.getId() != dataElement1Id:
    print "Wrong DataElement 1 retrieved by name"
    return False
  if not dataElement2Id in dataElementIds:
    print "DataElement 2 id not in dictionary:", dataElementIds
    return False
  dataElement2Ref = model.getDataElementById(dataElement2Id)
  if dataElement2Ref == None:
    print "Location of DataElement 2 in id dictionary failed"
    return False
  if dataElement2Ref.getId() != dataElement2Id:
    print "Wrong DataElement 2 retrieved by name"
    return False
  if not dataElement3Id in dataElementIds:
    print "DataElement 3 id not in dictionary:", dataElementIds
    return False
  dataElement3Ref = model.getDataElementById(dataElement3Id)
  if dataElement3Ref == None:
    print "Location of DataElement 3 in id dictionary failed"
    return False
  if dataElement3Ref.getId() != dataElement3Id:
    print "Wrong DataElement 3 retrieved by name"
    return False
  # check names
  if(len(dataElementNames) != 2):
    print "DataElement name dictionary has wrong size:", dataElementNames
    return False
  if not dataElement2Name in dataElementNames:
    print "DataElement 2 name not in dictionary:", dataElementNames
    return False
  dataElement2Ref = model.getDataElementByName(dataElement2Name)
  if dataElement2Name == None:
    print "Location of DataElement 2 in name dictionary failed"
    return False
  if dataElement2Ref.getName() != dataElement2Name:
    print "Wrong DataElement 2 retrieved by name"
    return False
  if not dataElement3Name in dataElementNames:
    print "DataElement 3 name not in dictionary:", dataElementNames
    return False
  dataElement3Ref = model.getDataElementByName(dataElement3Name)
  if dataElement3Name == None:
    print "Location of DataElement 3 in name dictionary failed"
    return False
  if dataElement3Ref.getName() != dataElement3Name:
    print "Wrong DataElement 3 retrieved by name"
    return False
  # create and test DataElement 4
  dataElement4 = None
  try:
    dataElement4 = model.createDataElement(name="dataElement3")
    print "No exception raised for multiple names"
    return False
  except Error, err:
    if str(err) != "DataElement name is not unique":
      print "Wrong exception raised"
      return False
  if dataElement4 != None:
    print "DataElement 4 wrongly created"
  return True

def archivingNotifyProcedure(self, publisher):
  """notification handler for an archiving subscriber"""
  self.archivedNotifications.append(publisher)

def test_PMnotifications():
  """function to test model notifications"""
  publisher1 = GDP.PM.Publisher()
  publisher2 = GDP.PM.Publisher()
  publisher3 = GDP.PM.Publisher()
  publisherSubscriber1 = GDP.PM.PublisherSubscriber()
  publisherSubscriber2 = GDP.PM.PublisherSubscriber()
  subscriber1 = GDP.PM.Subscriber(notifyProcedure=archivingNotifyProcedure)
  subscriber1.archivedNotifications = []
  subscriber2 = GDP.PM.Subscriber(notifyProcedure=archivingNotifyProcedure)
  subscriber2.archivedNotifications = []
  subscriber3 = GDP.PM.Subscriber(notifyProcedure=archivingNotifyProcedure)
  subscriber3.archivedNotifications = []
  GDP.PM.connect(publisher1, "p1", publisherSubscriber1, "ps1")
  GDP.PM.connect(publisher2, "p2", publisherSubscriber1, "ps1")
  GDP.PM.connect(publisher2, "p2", publisherSubscriber2, "ps2")
  GDP.PM.connect(publisher3, "p3", publisherSubscriber2, "ps2")
  GDP.PM.connect(publisherSubscriber1, "ps1", subscriber1, "s1")
  GDP.PM.connect(publisherSubscriber1, "ps1", subscriber2, "s2")
  GDP.PM.connect(publisherSubscriber2, "ps2", subscriber2, "s2")
  GDP.PM.connect(publisherSubscriber2, "ps2", subscriber3, "s3")
  publisher1.publish()
  publisher2.publish()
  publisher3.publish()
  publisher1.publish()
  publisher3.publish()
  archivedNotifications1 = subscriber1.archivedNotifications
  archivedNotifications2 = subscriber2.archivedNotifications
  archivedNotifications3 = subscriber3.archivedNotifications
  if len(archivedNotifications1) != 3:
    print "Invalid amount of notifications 1:", len(archivedNotifications1)
    return False
  if archivedNotifications1[0] != publisher1 or \
     archivedNotifications1[1] != publisher2 or \
     archivedNotifications1[2] != publisher1:
    print "Invalid notification data 1:", archivedNotifications1
    return False
  if len(archivedNotifications2) != 5:
    print "Invalid amount of notifications 2:", len(archivedNotifications2)
    return False
  if archivedNotifications2[0] != publisher1 or \
     archivedNotifications2[1] != publisher2 or \
     archivedNotifications2[2] != publisher3 or \
     archivedNotifications2[3] != publisher1 or \
     archivedNotifications2[4] != publisher3:
    print "Invalid notification data 2:", archivedNotifications2
    return False
  if len(archivedNotifications1) != 3:
    print "Invalid amount of notifications 3:", len(archivedNotifications3)
    return False
  if archivedNotifications3[0] != publisher2 or \
     archivedNotifications3[1] != publisher3 or \
     archivedNotifications3[2] != publisher3:
    print "Invalid notification data 3:", archivedNotifications3
    return False
  return True

def loggingNotifyProcedure(self, publisher):
  """notification handler for a logging subscriber"""
  print str(self.name) + ".notify(...)"

def archivingNotifyProcedure2(self, publisher):
  """notification handler for an archiving subscriber"""
  self.archivedNotifications.append(publisher)
  print str(self.name) + ".notify(...)"

def test_PMdataElementNotifications():
  """function to test notifications of DataElements"""
  model = GDP.PM.Model("testmodel")
  publisher1 = model.createDataElement(name="publisher1", notifyProcedure=loggingNotifyProcedure)
  publisher2 = model.createDataElement(name="publisher2", notifyProcedure=loggingNotifyProcedure)
  publisher3 = model.createDataElement(name="publisher3", notifyProcedure=loggingNotifyProcedure)
  publisherSubscriber1 = model.createDataElement(name="publisherSubscriber1", notifyProcedure=loggingNotifyProcedure)
  publisherSubscriber2 = model.createDataElement(name="publisherSubscriber2", notifyProcedure=loggingNotifyProcedure)
  subscriber1 = model.createDataElement(name="subscriber1", notifyProcedure=archivingNotifyProcedure2)
  subscriber1.archivedNotifications = []
  subscriber2 = model.createDataElement(name="subscriber2", notifyProcedure=archivingNotifyProcedure2)
  subscriber2.archivedNotifications = []
  subscriber3 = model.createDataElement(name="subscriber3", notifyProcedure=archivingNotifyProcedure2)
  subscriber3.archivedNotifications = []
  GDP.PM.connect(publisher1, "p1", publisherSubscriber1, "ps1")
  GDP.PM.connect(publisher2, "p2", publisherSubscriber1, "ps1")
  GDP.PM.connect(publisher2, "p2", publisherSubscriber2, "ps2")
  GDP.PM.connect(publisher3, "p3", publisherSubscriber2, "ps2")
  GDP.PM.connect(publisherSubscriber1, "ps1", subscriber1, "s1")
  GDP.PM.connect(publisherSubscriber1, "ps1", subscriber2, "s2")
  GDP.PM.connect(publisherSubscriber2, "ps2", subscriber2, "s2")
  GDP.PM.connect(publisherSubscriber2, "ps2", subscriber3, "s3")
  publisher1.publish()
  print ""
  publisher2.publish()
  print ""
  publisher3.publish()
  print ""
  publisher1.publish()
  print ""
  publisher3.publish()
  archivedNotifications1 = subscriber1.archivedNotifications
  archivedNotifications2 = subscriber2.archivedNotifications
  archivedNotifications3 = subscriber3.archivedNotifications
  if len(archivedNotifications1) != 3:
    print "Invalid amount of notifications 1:", len(archivedNotifications1)
    return False
  if archivedNotifications1[0] != publisher1 or \
     archivedNotifications1[1] != publisher2 or \
     archivedNotifications1[2] != publisher1:
    print "Invalid notification data 1:", archivedNotifications1
    return False
  if len(archivedNotifications2) != 5:
    print "Invalid amount of notifications 2:", len(archivedNotifications2)
    return False
  if archivedNotifications2[0] != publisher1 or \
     archivedNotifications2[1] != publisher2 or \
     archivedNotifications2[2] != publisher3 or \
     archivedNotifications2[3] != publisher1 or \
     archivedNotifications2[4] != publisher3:
    print "Invalid notification data 2:", archivedNotifications2
    return False
  if len(archivedNotifications1) != 3:
    print "Invalid amount of notifications 3:", len(archivedNotifications3)
    return False
  if archivedNotifications3[0] != publisher2 or \
     archivedNotifications3[1] != publisher3 or \
     archivedNotifications3[2] != publisher3:
    print "Invalid notification data 3:", archivedNotifications3
    return False
  return True

print "***** test_PMmemoryManagement() start"
retVal = test_PMmemoryManagement()
print "***** test_PMmemoryManagement() done:", retVal
print "***** test_PMnotifications() start"
retVal = test_PMnotifications()
print "***** test_PMnotifications() done:", retVal
print "***** test_PMdataElementNotifications() start"
retVal = test_PMdataElementNotifications()
print "***** test_PMdataElementNotifications() done:", retVal

