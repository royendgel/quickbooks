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
    qbxml = None

    def __init__(self, quickbooks_file_location=None, connect_method='direct'):
        # This can be webconnector or direct com
        self.connect_method = connect_method
        self.mode = 3
        self.quickbooks_file_location = quickbooks_file_location
        self.app_name = 'Quickbooks Python'
        self.xml_prefix = self.get_xml_prefix()

    def get_xml_prefix(self):
        ver = '''<?xml version="1.0" encoding="utf-8"?><?qbxml version="{}"?>'''.format(12.0)
        return ver

    def version_suported(self):
        """
        iter over the SupportedQBXMLVersion and return the last value.
        """
        self.query = 'Host'
        req = self.make_request()
        for ver in ET.fromstring(req).iter("SupportedQBXMLVersion"):
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
        # data_xml = self.xml_soap(xmltodict.unparse(qbxml_query, full_document=False))
        data_xml = xmltodict.unparse(qbxml_query, full_document=False)
        res = self.xml_prefix + data_xml
        self.qbxml = res
        return res


    def order_elements(self, order_dict, elements, new_dict):
        """
        This is a copy of order_extra_elements, this gives the opportunity to loop recursive without making
        the code unreadable
        :param order_dict: The model, having the structure of the data
        :param elements: Elements / payload
        :return: modified payload with extra elements

        Loop through the original data model and original payload(elements)
        Make a new ordereddict and add every key in the correct possition
        """

        # Loop through the original data model and check if that key is in the payload.
        # Begins with an 'elements' key and there is a list with odereddicts in it.
        model_elements = order_dict['elements']
        a = len(elements)
        def is_ini_it(elements, element):
            for item in elements:
                for key in item.keys():
                    if key == element:
                        return True
            return False

        for model_element in model_elements: # model_elements is a list
            if isinstance(model_element, type(OrderedDict())):
                if model_element:
                    name = model_element['xmlName']
                    if name == 'OR':
                        for item in model_element['elements']:
                            item_name = item['xmlName']
                            # print item_name
                            # print item['xmlName'] in elements
                            # print elements
                            if is_ini_it(elements, item_name):
                                new_dict.update([(item_name, elements[0][item_name])])

                    else:
                        if name in elements[0]:
                            if  elements[0][name] != 'None':
                                cont = elements[0][name]
                                if isinstance(elements[0][name], type(unicode())):
                                    cont= escape(elements[0][name].encode('utf-8').decode('utf-8'))
                                # print type(elements[0][name])
                                new_dict.update([(name, cont)])
                            else:
                                pass
                                # print name


        return new_dict






    def order_extra_elements(self, elements, extra=None):
        """
        :param elements: The original payload
        :param extra: The extra parameters that need to be added
        :return: modified payload with extra elements
        """
        """Loop through the elements and adds the extra element on the right position"""
        model_name = "{}AddModel".format(self.__class__.__name__)
        if hasattr(objects_models, model_name):
            # append the extra element to the elements list, this will break the original payload.
            if extra:
                elements[0].update(extra)
            new_dict = OrderedDict()
            return self.order_elements(getattr(objects_models, model_name), elements, new_dict)


        return False



class CreateMixin(Resource):
    def create(self, payload, **kwargs):
        # Pull the model
        data_model = None
        if 'extra' in kwargs:
            """Overide the payload with the extra key in it"""
            if kwargs['extra']:
                # print payload
                payload = self.order_extra_elements(payload, kwargs['extra'])
            else:
                payload = self.order_extra_elements(payload)

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