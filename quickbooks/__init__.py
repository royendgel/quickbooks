import os
import logging
# Using this instead of my favorite lxml
import xml.etree.ElementTree as ET
from request_creator import RequestCreator
import win32com.client

class Quickbooks:
  def __init__(self, qb_file=None, stop_on_error=True):
    # Absolute path to your quickbooks
    self.qb_file = qb_file
    self.app_name = "Quickbooks Python"
    self.ticket = None
    self.rc = RequestCreator()

    # This are important for me. using upto version 6 of the SDK.
    # You can check the version suported very easy by doing:
    # self.verion_suported() it will return the value.
    self.queries = [
      "Customer",
      "Account",
      "Invoice",
      "Bill",
      "Check",
      "Host",
      "Invoice",
      "ReceivePayment",
      "SalesReceipt",
      "Vendor",
      "ToDo",
      "Terms",
      "Template",
      "StandardTerms",
      "SalesOrder",
      "ItemSalesTax",
      "ItemReceipt",
      "Item",
      "Estimate",
      "Class",
    ]

  def version_suported(self):
    """
    iter over the SupportedQBXMLVersion and return the last value.
    """
    for ver in ET.fromstring(self.get('Host')).iter("SupportedQBXMLVersion"):
      version = ver.text

    return  version

  def __create_name(self, object_name, operation, method):
    '''
    Acording to chapter 3 page # 32:
    Naming are sliced in 3 parts object, operation + Rq
    '''
    return "%s%s%s" %(object_name, operation.title(), method.title())

  def __create_object(self, mode=2):
    """
    It creates and returns a Session Object.
    """
    session = win32com.client.Dispatch("QBXMLRP2.RequestProcessor")
    session.OpenConnection('', self.app_name)
    self.ticket = session.BeginSession(self.qb_file, 2)

    return session

  def __close_connection(self, session, ticket):
    session.EndSession(ticket)
    session.CloseConnection()

  def make_request(self, query='CustomerQuery'):

    session = self.__create_object()
    resp = None
    try:
      q = self.rc.create_name(object_name=query, operation='', method='')
      qbxml_query = """
      <?qbxml version="6.0"?>
      <QBXML>
         <QBXMLMsgsRq onError="stopOnError">
            <%s></%s>
         </QBXMLMsgsRq>
      </QBXML>
      """ %(q, q)
      resp = session.ProcessRequest(self.ticket, qbxml_query)
    except Exception, e:
      print e
    finally:
      self.__close_connection(session, self.ticket)

    return resp

  def get_all(self, filedir=None):
    '''
    Make a loop into the queries list.
    Saves the file in a directory or prints it.
    if the filedir is not None it will save it otherwise print it.
    '''

    for req in self.queries:
      print 'extracting %s' %(req)
      resp = self.make_request(query=self.rc.create_name(req, \
      operation='query', method='rq'))

      # Make sure you have write access to the dir
      if filedir is not None and os.path.isdir(filedir):
        with open(os.path.join(filedir, req.lower() + ".xml"), 'w+') as f:
          f.write(resp)
      else:
        print resp

    print "Finished..!"

  def get(self, query):
    q = self.rc.create_name(query, operation='query', method='rq')
    return self.make_request(q)
