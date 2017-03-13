from collections import OrderedDict
from xml.sax.saxutils import escape

import os
import logging
import xml.etree.ElementTree as ET

import xmltodict

from quickbooks.objects_models import BillModel, CustomerModel
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
        self.xml_prefix = '''<?xml version="1.0" encoding="utf-8"?><?qbxml version="2.0"?>'''

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

    def make_qbxml(self, query=None, payload=None):

        """
        Outputs a valid QBXML
        if there is a payload it will be included in the output

        :param query is the full name of the object like CustomerAddRq
        :param payload is the optional payload , it is required when adding items.
        """

        if payload:
            qb_request = payload
        else:
            qb_request = None

        qbxml_query = {
            'QBXML': {
                'QBXMLMsgsRq':
                    {
                        '@onError': "stopOnError",
                        query: qb_request
                    }

            }

        }
        data_xml = self.xml_soap(xmltodict.unparse(qbxml_query, full_document=False))
        data_xml = xmltodict.unparse(qbxml_query, full_document=False)
        res = self.xml_prefix + data_xml

        return res

    def make_request(self, query='CustomerQuery', payload=None):

        session = self.__create_object()
        resp = None
        try:
            q = self.rc.create_name(object_name=query, operation='', method='')
            resp = session.ProcessRequest(self.ticket, self.make_qbxml(query=q, payload=payload))
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
        for items in response[response.keys()[-1]]:
            # Get keys for each item
            for item in items:
                if item not in keys:
                    keys.append(items[item])

    def __payload_generator(self, payload, object_name):
        data = {
            '@requestID': "15",
            "{}Add".format(object_name.title()): payload
        }
        return data

    def xml_soap(self, xml):
        return escape(xml)

    def build_params(self, data, params):
        ord_payload = OrderedDict()
        for param in params:

            # If the item is a tuple we know it's a nested item
            # It is very important to mantain the same position ALWAYS !!
            if isinstance(param, tuple):
                # The first item is the key
                if param[0] in data:
                    nested_param = OrderedDict()
                    # The second item contains the childrens
                    for p in param[1]:
                        nested_param.update([(p, data[param[0]][p])])
                    # Need to append this to the ordereddict so it can stay in place.
                    ord_payload.update([(param[0], nested_param)])
            else:
                ord_payload[param] = data[param].decode('utf-8')

        return ord_payload

    def add_customer(self, data):

        rq = 'Customer'

        params = [
            'Name',
            'CompanyName',
            'FirstName',
            'LastName',
            ('BillAddress', [
                'Addr1',
                'Addr2',
                'Addr3',
                'City',
                'State',
                'PostalCode',
                'Country',
            ]),
            'Phone',
            'AltPhone',
            'Fax',
            'Email',
            'Contact'
        ]

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_account(self, data):

        rq = 'Account'

        params = CustomerModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_bill(self, data):

        rq = 'Bill'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_invoice(self, data):

        rq = 'Invoice'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_receive_payment(self, data):

        rq = 'ReceivePayment'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_vendor(self, data):

        rq = 'Vendor'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_worker_comp_code(self, data):

        rq = 'WorkerCompCode'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_vendor_type(self, data):

        rq = 'VendorType'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_vendor_credit(self, data):

        rq = 'VendorCredit'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_vehicle(self, data):

        rq = 'Vehicle'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_vehicle_mileage(self, data):

        rq = 'VehicleMileage'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_unit_of_measure_set(self, data):

        rq = 'UnitOfMeasureSet'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_txn_display(self, data):

        rq = 'UnitOfMeasureSet'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_transfer(self, data):

        rq = 'Transfer'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_transfer_inventory(self, data):

        rq = 'TransferInventory'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_todo(self, data):

        rq = 'ToDo'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_time_tracking(self, data):

        rq = 'TimeTracking'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_standard_terms(self, data):

        rq = 'StandardTerms'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_ship_method(self, data):

        rq = 'ShipMethod'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_sales_tax_payment_check(self, data):

        rq = 'SalesTaxtPaymentCheck'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_sales_tax_code(self, data):

        rq = 'SalesTaxCode'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_sales_rep(self, data):

        rq = 'SalesRep'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_sales_receipt(self, data):

        rq = 'SalesReceiptAdd'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_sales_order(self, data):

        rq = 'SalesOrder'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_purchase_order(self, data):

        rq = 'PurchaseOrder'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_price_level(self, data):

        rq = 'PriceLevel'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_payroll_item_wage(self, data):

        rq = 'PayrollItemWage'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_payment_method(self, data):

        rq = 'PaymentMethod'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_other_name(self, data):

        rq = 'OtherName'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_list_display(self, data):

        rq = 'ListDisplay'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_lead(self, data):

        rq = 'Lead'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_journal_entry(self, data):

        rq = 'JournalEntry'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_job_type(self, data):

        rq = 'JobType'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

    def add_item_subtotal(self, data):

        rq = 'ItemSubTotal'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_item_service(self, data):

        rq = 'ItemService'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_item_tax(self, data):

        rq = 'ItemTax'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_item_sales_tax_group(self, data):

        rq = 'ItemSalesTaxGroup'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_item_receipt(self, data):

        rq = 'ItemReceipt'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_item_paymentp(self, data):

        rq = 'ItemPayment'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_item_other_charge(self, data):

        rq = 'ItemOtherCharge'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_item_non_inventory(self, data):

        rq = 'ItemNonInventory'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_item_non_inventory(self, data):

        rq = 'ItemNonInventory'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_item_inventory_assembly(self, data):

        rq = 'ItemIventoryAssembly'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_inventory(self, data):

        rq = 'ItemIventory'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_group(self, data):

        rq = 'ItemGroup'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

    def add_item_fixed_asset(self, data):

        rq = 'ItemFixedAsset'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_item_discount(self, data):

        rq = 'ItemDiscount'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_inventory_site(self, data):

        rq = 'InventorySite'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_inventory_adjustment(self, data):

        rq = 'InventoryAdjustment'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_employee(self, data):

        rq = 'Employee'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_deposit(self, data):

        rq = 'Deposit'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_data_driven_terms(self, data):

        rq = 'DataDrivenTerms'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_data_ext_def(self, data):

        rq = 'DataExtDef'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_customer_type(self, data):

        rq = 'CustomerType'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_currency(self, data):

        rq = 'Currency'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_credit_memo(self, data):

        rq = 'CreditMemo'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_credit_card_credit(self, data):

        rq = 'CreditCardCredit'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_credit_card_charge(self, data):

        rq = 'CreditCardCharge'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_class(self, data):

        rq = 'Class'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_check(self, data):

        rq = 'Check'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_charge(self, data):

        rq = 'Charge'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_build_assembly(self, data):

        rq = 'BuildAssembly'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_billing_rate(self, data):

        rq = 'BillingRate'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_bill_payment_credit_card(self, data):

        rq = 'BillPaymentCreditCard'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_bill_payment_check(self, data):

        rq = 'BillPaymentCheck'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)

    def add_ar_refund_credit_card(self, data):

        rq = 'ArRefundCreditCard'

        params = BillModel

        payload = self.__payload_generator(payload=OrderedDict(
            self.build_params(data=data, params=params)
        ), object_name=rq)

        self.make_request(self.rc.create_name(rq, operation='add', method='rq'), payload=payload)
