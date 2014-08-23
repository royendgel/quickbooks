import os
import win32com.client

class Quickbooks(object):
  def __init__(self, qb_file=None):
    # Absolute path to your quickbooks
    self.qb_file = qb_file
    self.app_name = "Quickbooks Python"
    self.ticket = None

    # This are important for me.
    self.queries = [
      "CustomerQuery",
      "AccountQuery",
      "InvoiceQuery",
      "BillQuery",
      "CheckQuery",
      "HostQuery",
      "InvoiceQuery",
      "ReceivePaymentQuery",
      "SalesReceiptQuery",
      "VendorQuery",
      "TransferInventoryQuery",
      "ToDoQuery",
      "TermsQuery",
      "TemplateQuery",
      "StandardTermsQuery",
      "SalesOrderQuery",
      "ItemSalesTaxQuery",
      "ItemReceiptQuery",
      "ItemQueryRq",
      "EstimateQuery",
      "ClassQuery",
    ]

  def __create_object(self, mode=2):
    """
    It creates and returns a Session Object.
    """
    session = win32com.client.Dispatch("QBXMLRP2.RequestProcessor")
    session.OpenConnection('', self.app_name)
    self.ticket = session.BeginSession(self.qb_file, mode)

    return session

  def __close_connection(self, session, ticket):
    session.EndSession(ticket)
    session.CloseConnection()

  def make_request(self, qb_query=None, query='CustomerQueryRq'):

    session = self.__create_object()
    qbxml_query = """
    <?qbxml version="6.0"?>
    <QBXML>
       <QBXMLMsgsRq onError="stopOnError">
          <%s></%s>
       </QBXMLMsgsRq>
    </QBXML>
    """ %(query, query)
    resp = session.ProcessRequest(self.ticket, qbxml_query)
    self.__close_connection(session, self.ticket)
    return resp

  def get_all(self, filedir):
    '''
    Make a loop into the queries list.
    Saves the file in a directory or prints it.
    if the filedir is not None it will save it otherwise print it.
    '''

    for req in self.queries:
      print 'extracting %s' %(req)
      resp = self.make_request(query=req + "Rq")
      # Make sure you have write access to the dir
      if filedir is not None and os.path.isdir(filedir):
        with open(os.path.join(filedir, req.lower() + ".xml"), 'w+') as f:
          f.write(resp)
      else:
        print resp

    return "Finished..!"
