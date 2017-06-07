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
        """Runs through the elements in resources, this elements can be nested
        This function should handle all depths.
        """
        url = self.build_request_url(resource)
        # print url
        fields = requests.get(url)
        elements = json.JSONDecoder(object_pairs_hook=OrderedDict).decode(fields.content)
        # print json.dumps(elements, indent=4)
        safe_items = ['elements', 'xmlName']
        delete_keys = ['Width', 'TopLeftX', 'supports', 'US', 'OE', 'CA', 'UK', 'AU', 'fcName', 'xmlNameHtml',
                       'Height', 'fcNameHtml', 'MasterImage', 'xmlType', 'fcType', 'required', 'TopLeftY', ]
        data = OrderedDict()

        new_data = self.build_new_ordered_dict(self.recursive(elements['elements']))
        return self.finisher(new_data)

    def recursive(self, data):

        if isinstance(data, type([])):
            for item in data:
                if item:
                    if isinstance(item, type(OrderedDict())):
                        self.recursive(item)

            if 'elements' in data:
                self.recursive(data)

        elif isinstance(data, type(OrderedDict())):
            safe_items = ['elements', 'xmlName']

            # Let's delete what we don't want !
            for item in data:
                if item not in safe_items:
                    del data[item]

                elif item in safe_items:
                    if item == 'elements':
                        for element in data['elements']:
                            if isinstance(element, type(OrderedDict())):
                                self.recursive(element)
                    elif item == 'xmlName':
                        pass

                    else:
                        pass

                else:
                    if not isinstance(data[item], type(unicode())):
                        self.recursive(data[item])
                    else:
                        pass

        return data

    def finisher(self, data):

        if isinstance(data, type([])):
            for item in data:
                if item:
                    if isinstance(item, type(OrderedDict())):
                        self.finisher(self.build_new_ordered_dict(item))

            if 'elements' in data:
                self.finisher(self.build_new_ordered_dict(data))

        elif isinstance(data, type(OrderedDict())):
            for item in data:
                if item == 'elements':
                    for element in data[item]:
                        if isinstance(element, type(OrderedDict())):
                            self.build_new_ordered_dict(element)
                            # self.finisher(self.build_new_ordered_dict(element))

        return data

    def build_new_ordered_dict(self, data):
        new_dict = OrderedDict()
        for item in data:
            if 'elements' in data:
                for el in data['elements']:
                    if el:
                        new_dict.update([(el['xmlName'], el)])
            elif isinstance(item, type(OrderedDict())):
                new_dict.update(item)
            elif item == 'xmlName':
                # print data[item]
                new_dict.update([(data[item], '')])
            else:
                # print data[item]
                pass

        return new_dict

    def write_objects_models(self):
        """Replaces objects_models.py with a new set of objects."""
        all_resources = self.get_resources()
        # all_resources = [('Check', None)]
        # print all_resources
        from quickbooks import resource
        data = []
        for entry in all_resources:
            if hasattr(resource, entry[0]):
                for method in self.methods:
                    try:
                        res = "{}{}".format(entry[0], method.title())
                        fields = self.get_resource_fields(res)
                        #     # data.append("{}Model={}".format(entry[0], json.dumps(fields, indent=4)))
                        data.append("{}{}Model={}".format(entry[0], method.title(), fields))
                    except Exception as e:
                        print e
        with open('quickbooks/objects_models.py', 'w+') as f:
            f.write("from collections import OrderedDict\n")
            for entry in data:
                f.write(entry)
                f.write("\n")

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

                f.write("\n\n")  # End of the line some blank lines

    def write_resource_list(self):
        """Creates a new file including all resources"""
        with open('quickbooks/resource_list.py', 'w+') as f:
            f.write("""# Automatically generated from script.\n\n""")
            resources = self.get_resources()
            f.write("resource_list = [")
            for resource in resources:
                resource_name = resource[0]
                f.write("""'{}',\n""".format(resource_name))
            f.write("]")

            f.write("\n\n")  # End of the line some blank lines

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
    # qb.get_resource_fields('CustomerAdd')
    # qb.write_objects_models()
    # qb.write_resource()
    # qb.write_test_code()
    # qb.write_resource_list()
    qb.write_objects_models()
