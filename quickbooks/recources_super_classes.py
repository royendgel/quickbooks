class Resource:
    supported_version_create = 6.0
    supported_version_update = 6.0
    supported_version_delete = 6.0
    methods = ['Create', 'Retrieve', 'Update']
    object_map = []

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
        try:
            import win32com.client
        except ImportError:
            print("Not supported via windows.")
        session = win32com.client.Dispatch("QBXMLRP2.RequestProcessor")
        session.OpenConnection('', self.app_name)
        # This need to be mode, 3 to gues wich
        self.ticket = session.BeginSession(self.qb_file, 3)

        return session

    def __close_connection(self, session, ticket):

        session.EndSession(ticket)
        session.CloseConnection()




class CreateMixin(Resource):
    def __init__(self):
        pass

    def create(self):
        pass


class RetriveMixin(Resource):
    def __init__(self):
        pass

    def retrieve(self):
        pass


class UpdateMixin(Resource):
    def __init__(self):
        pass

    def update(self):
        pass


class DeleteMixin(Resource):
    def __init__(self):
        pass

    def delete(self):
        pass
