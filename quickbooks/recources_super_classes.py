class Resource:
    supported_version_create = 6.0
    supported_version_update = 6.0
    supported_version_delete = 6.0
    methods = ['Create', 'Retrieve', 'Update']
    object_map = []


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
