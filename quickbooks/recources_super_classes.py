import logging
from xml.sax.saxutils import escape
import xml.etree.ElementTree as ET
import xmltodict
from collections import OrderedDict
import objects_models
class Resource:
    supported_version_create = 6.0
    supported_version_update = 6.0
    supported_version_delete = 6.0
    methods = ['Create', 'Retrieve', 'Update']
    object_map = []
    method = None
    payload = None
    filters = None

    def __init__(self, quickbooks_file_location=None, connect_method='direct'):
        # This can be webconnector or direct com
        self.connect_method = connect_method
        self.mode = 3
        self.quickbooks_file_location = quickbooks_file_location
        self.app_name = 'Quickbooks Python'
        self.xml_prefix = self.get_xml_prefix()

    def get_xml_prefix(self):
        ver = '''<?xml version="1.0" encoding="utf-8"?><?qbxml version="{}"?>'''.format(13.0)
        return ver

    def version_suported(self):
        """
        iter over the SupportedQBXMLVersion and return the last value.
        """
        self.query = 'Host'
        print 'booh'
        req = self.make_request()
        print req
        for ver in ET.fromstring(req).iter("SupportedQBXMLVersion"):
            print 'gotit'
            print ver
            return ver.text

    def __create_name(self, object_name, operation, method):
        '''
    Acording to chapter 3 page # 32:
    Naming are sliced in 3 parts object, operation + Rq
    '''
        return "%s%s%s" % (object_name, operation.title(), method.title())

    def __create_object(self, mode=3):
        """
    It creates and returns a Session Object.
    """
        try:
            import win32com.client
        except ImportError:
            print("Not supported via windows.")
        session = win32com.client.Dispatch("QBXMLRP2.RequestProcessor")
        session.OpenConnection('', self.app_name)
        # This need to be mode, 3 to gues wich
        self.ticket = session.BeginSession(self.quickbooks_file_location, 3)

        return session

    def __close_connection(self, session, ticket):

        session.EndSession(ticket)
        session.CloseConnection()

    def get_resource_name(self):
        return self.__class__.__name__

    def get_request_name(self):
        return "{}{}Rq".format(self.get_resource_name(), self.method.title())

    def make_request(self):

        session = self.__create_object()
        resp = None
        try:
            resp = session.ProcessRequest(self.ticket, self.make_qbxml())
        except Exception, e:
            logging.error(e)
        finally:
            self.__close_connection(session, self.ticket)
            logging.info("Connection closed")

        return resp

    def xml_soap(self, xml):
        return escape(xml)

    def make_qbxml(self):

        """
        Outputs a valid QBXML
        if there is a payload it will be included in the output

        :param query is the full name of the object like CustomerAddRq
        :param payload is the optional payload , it is required when adding items.
        """

        if self.payload:
            qb_request = self.payload
        else:
            qb_request = None

        if self.filters:
            self.payload = self.filters

        message = OrderedDict(
            [
                ('@onError', "stopOnError"),
                (self.query, None if not self.payload else self.payload)
            ]
        )

        qbxml_query = {
            'QBXML': {
                'QBXMLMsgsRq':
                    message

            }

        }
        data_xml = self.xml_soap(xmltodict.unparse(qbxml_query, full_document=False))
        data_xml = xmltodict.unparse(qbxml_query, full_document=False)
        res = self.xml_prefix + data_xml
        return res


class CreateMixin(Resource):
    def create(self, payload, **kwargs):
        # Pull the model
        data_model = None
        class_name = self.__class__.__name__
        if hasattr(objects_models, '{}Model'.format(class_name)):
            data_model = getattr(objects_models, '{}Model'.format(class_name))

        self.method = 'add'
        self.query = self.get_request_name()
        self.filters = OrderedDict([("{}{}".format(class_name, self.method.title()), payload)])
        return self.make_request()


class RetriveMixin(Resource):
    def retrieve(self, **kwargs):
        options = {}
        for item in kwargs:
            options.update({"{}".format(item): kwargs[item]})
        if options:
            self.filters = options

        self.method = 'query'
        self.query = self.get_request_name()
        return self.make_request()

class UpdateMixin(Resource):
    def update(self):
        pass


class DeleteMixin(Resource):
    def delete(self):
        pass
