import os
import logging
import xml.etree.ElementTree as ET

import xmltodict

from request_creator import RequestCreator

logging.getLogger(__name__)


class Quickbooks:
    def __init__(self, qb_file=None, version=6.0, stop_on_error=True):
        # Absolute path to your quickbooks
        self.qb_file = qb_file
        self.app_name = "Quickbooks Python"
        self.ticket = None
        self.rc = RequestCreator()
        self.version = version

        # This are important for me. using upto version 6 of the SDK.
        # You can check the version suported very easy by doing:
        # self.verion_suported() it will return the value.
        self.__queries = [
            ("Account", 6.0),
            ("Bill", 6.0),
            ("Check", 6.0),
            ("Class", 6.0),
            ("Customer", 6.0),
            ("Host", 6.0),
            ("Invoice", 6.0),
            ("Item", 6.0),
            ("ItemReceipt", 6.0),
            ("ItemSalesTax", 6.0),
            ("ReceivePayment", 6.0),
            ("SalesOrder", 6.0),
            ("SalesReceipt", 6.0),
            ("StandardTerms", 6.0),
            ("Template", 6.0),
            ("Terms", 6.0),
            ("ToDo", 6.0),
            ("Vendor", 6.0),
            ('BillPaymentCheck', 6.0),
            ('BuildAssembly', 6.0),
            ('Charge', 6.0),
            ('Check', 6.0),
            ('Credit', 6.0),
            ('CreditCardCharge', 6.0),
            ('CreditCardCredit', 6.0),
            ('Deposits', 6.0),
            ('Employee', 6.0),
            ('Estimate', 6.0),
            ('Estimates', 6.0),
            ('Invoices', 6.0),
            ('ItemPayment', 6.0),
            ('ItemReceipt', 6.0),
            ('JournalEntry', 6.0),
            ('PriceLevel', 6.0),
            ('Purchase', 6.0),
            ('ReceivePayment', 6.0),
            ('Sales', 6.0),
            ('SalesReceipt', 6.0),
            ('Statement', 6.0),
            ('TimeTracking', 6.0),
            ('VendorCredit', 6.0),
        ]
        self.queries = [query[0] for query in self.__queries]

    def version_suported(self):
        """
        iter over the SupportedQBXMLVersion and return the last value.
        """
        for ver in ET.fromstring(self.get('Host')).iter("SupportedQBXMLVersion"):
            return ver.text

    def __create_name(self, object_name, operation, method):
        '''
    Acording to chapter 3 page # 32:
    Naming are sliced in 3 parts object, operation + Rq
    '''
        return "%s%s%s" % (object_name, operation.title(), method.title())

    def __create_object(self, mode=2):
        """
    It creates and returns a Session Object.
    """
        import win32com.client
        session = win32com.client.Dispatch("QBXMLRP2.RequestProcessor")
        session.OpenConnection('', self.app_name)
        # This need to be mode, 3 to gues wich
        self.ticket = session.BeginSession(self.qb_file, 3)

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
      """ % (q, q)
            resp = session.ProcessRequest(self.ticket, qbxml_query)
        except Exception, e:
            logging.error(e)
        finally:
            self.__close_connection(session, self.ticket)
            logging.info("Connection closed")

        return resp

    def get_all(self, filedir=None):
        '''
        Make a loop into the queries list.
        Saves the file in a directory or prints it.
        if the filedir is not None it will save it otherwise print it.
        '''

        for req in self.queries:
            logging.info("extracting {}".format(req))
            resp = self.make_request(query=self.rc.create_name(
                req, operation='query', method='rq'))

            #   Make sure you have write access to the dir
            if filedir is not None and os.path.isdir(filedir):
                filename = os.path.join(filedir, req.lower() + ".xml")
                with open(filename, 'w+') as f:
                    logging.DEBUG("Writing to file {}").format(filename)
                    f.write(resp)
            else:
                logging.debug(resp)

        logging.debug(resp)

    def get(self, query):

        q = self.rc.create_name(query, operation='query', method='rq')

        return self.make_request(q)

    def extract_data(self, data, query):
        query_rs = "{}QueryRs".format(query)
        xml = xmltodict.parse(data)
        response = xml['QBXML']['QBXMLMsgsRs'][query_rs]

        keys = []

        # Get the last key in the dict, that will be the items
        for items in response[response.keys()[-1]][:5]:
            # Get keys for each item
            for item in items:
                if item not in keys:
                    keys.append(items[item])
        print(keys)
        print len(keys)
