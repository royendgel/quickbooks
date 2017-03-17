from collections import OrderedDict

import xmltodict
import json
import requests


# Making a code that writes code

class QuickBooksDocumentedAPI:
    def __init__(self):
        self.base_url = 'https://developer-static.intuit.com/qbsdk-current/common/newosr/index.html'
        self.error_url = 'https://developer-static.intuit.com/qbsdk-current/common/newosr/qbsdk/error.xml'
        self.requests_url = 'https://developer-static.intuit.com/qbsdk-current/common/newosr/qbsdk/json/requests.json'
        self.resource_url = 'https://developer-static.intuit.com/qbsdk-current/common/newosr/qbsdk/json/'
        self.methods = ['Add', 'Mod', 'Query']

    def get_main_site(self):
        return requests.get(self.base_url)

    def get_clean_resource_name(self, resource):
        """Gets a clean resource name without the
        Query, Add or Mod"""
        for method in self.methods:
            if resource.endswith(method):
                clean = resource.replace(method, "")
                return clean

    def get_resource_method(self, resource):
        """Gets the method of the resource"""
        for method in self.methods:
            if resource.endswith(method):
                return method

    def build_request_url(self, resource):

        url = "{}{}Rq.json".format(self.resource_url, resource)
        return url

    def get_resources(self):
        """Gets all resources from the api site and outputs a nice dict containing every resource."""
        rq = requests.get(self.requests_url)
        resources = {}
        for resource in rq.json()['messages']:
            clean_name = self.get_clean_resource_name(resource['name']),
            # FIXME: method_name can be empty be the filter. EVENTINFODEL does not have antything in it.
            resource_name = resource['name'][0]
            method_name = self.get_resource_method(resource['name'])
            if resource_name and method_name:

                if clean_name in resources:
                    resources[clean_name]['methods'].append(method_name)
                    resources[clean_name]['versions'].update({"version_{}".format(method_name.lower()): resource[
                        'minVerUS']})

                else:
                    resources.update({
                        clean_name: {
                            'methods': [method_name],
                            'versions': {"version_{}".format(method_name.lower()): resource['minVerUS']}
                        }
                    })

        return resources

    def get_resource_fields(self, resource):
        # fields = requests.get(self.build_request_url(resource))
        with open('CustomerAddRq.json', 'r') as f:
            fields = json.load(f)
            json.dumps(fields, indent=4)
            resource_field = OrderedDict()

            self.recurse(fields)

    def __element_walker(self, elements):
        # A nested walker
        if 'elements' in elements:
            self.__element_walker(elements['elements'])

    def recurse(self, d):
        if type(d) == type([]):
            for k in d:
                self.recurse(d[k])
        elif 'elements' in d:
            print 'xmlType'
        else:
            if 'elements' in d:
                print 'xmlType'

    def write_objects_models(self):
        """Replaces objects_models.py with a new set of objects."""
        pass

    def write_resource(self):
        """Creates a new file including all resources"""
        with open('quickbooks/resource.py', 'w+') as f:
            f.write("""# Automatically generated from script.\n\n""")
            f.write("from recources_super_classes import CreateMixin, DeleteMixin, Resource, RetriveMixin, "
                    "UpdateMixin\n\n\n")

            resources = self.get_resources()
            for resource in resources:
                resource_name = resource[0]
                resource_set = resources[resource]
                if resource_name != None:
                    methods = resource_set['methods']
                    class_mixin = []
                    class_methods_mapper = {'Add': 'CreateMixin', 'Mod': 'UpdateMixin', 'Query': 'RetriveMixin'}
                    for method in methods:
                        if method in class_methods_mapper:
                            class_mixin.append(class_methods_mapper[method])

                    methods = ", ".join('"{0}"'.format(method.lower()) for method in methods)
                    class_mixin = ", ".join(class_mixin)
                    f.write("""class {}({}):\n""".format(resource_name, class_mixin))
                    f.write("""    methods = [{}]\n""".format(methods))
                    versions = resource_set['versions']
                    for version in versions:
                        f.write("""    {} = {}\n""".format(version, versions[version]))

                f.write("\n\n")  # End of the line some white spaces

    def write_code(self):
        """Rewrites the whole software with new objects and resources."""
        pass

    def write_test_code(self):
        """Creates a new file including all tests"""
        with open('tests/generated_tests.py', 'w+') as f:
            f.write("""# Automatically generated from script.\n\n""")
            f.write("import unittest\n\n\n")

            resources = self.get_resources()
            for resource in resources:
                resource_name = resource[0]
                resource_set = resources[resource]
                if resource_name != None:
                    methods = resource_set['methods']
                    f.write("""class {}TestCase(unittest.TestCase):\n""".format(resource_name))
                    for method in methods:
                        f.write("    def test_{}(self):\n".format(method.lower()))
                        f.write("        pass")
                        if method != methods[-1]:
                            f.write('\n\n')

                    f.write("\n\n\n")  # End of the line some white spaces


if __name__ == '__main__':
    qb = QuickBooksDocumentedAPI()
    # print qb.get_main_site()
    # qb.get_resources()
    qb.get_resource_fields('CustomerAdd')
    # qb.write_objects_models()
    # qb.write_resource()
    # qb.write_test_code()
