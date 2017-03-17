class Resource:
    supported_version_create = 6.0
    supported_version_update = 6.0
    supported_version_delete = 6.0
    methods = ['Create', 'Retrieve', 'Update']
    object_map = []


class CreateMixin:
    def create(self):
        pass


class RetriveMixin:
    def retrieve(self):
        pass


class UpdateMixin:
    def update(self):
        pass


class DeleteMixin:
    def delete(self):
        pass
