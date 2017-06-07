import json
import os
from collections import OrderedDict

from quickbooks import Customer
from quickbooks.objects_models import CustomerAddModel
import xmltodict
pt = os.path.abspath(os.path.join("..", 'client files', 'qbfile', 'Exploitatie 1998 tm 2014.QBW'))
print pt

class MergeCompanyFile:
    def __init__(self, source, target):
        self.tatget = target
        self.source = source

    def preflight(self):
        """Check if data is correct and performs some query to target"""
        pass

    def pull_data(self):
        """Pull data from source"""
        pass

    def push_data(self):
        """Insert data into the target"""
        pass

    def control_data(self):
        """Check if everything is ok, be comparing the number of items in list"""
        pass

    def make_report(self):
        """Make report about the process"""
        pass


with open('Customer.xml', 'r') as f:
    transaction_xml = xmltodict.parse(f.read())

data = OrderedDict()


def data_conditioner(data, new_data):
    for key in data:
        transaction = OrderedDict()
        if key:
            xml_name = key['xmlName']
        elif not key:
            pass
        else:
            print 'whot'
        if key:
            if 'elements' in key:
                pass
                new_data.update([(xml_name, data_conditioner(data=key['elements'], new_data=OrderedDict()))])
            else:
                new_data.update([(xml_name, None)])
    return new_data


result = data_conditioner(data=CustomerAddModel['elements'], new_data=data)

data_to_push = OrderedDict()


def condition_push(transactions, data_to_push, model):
    a = []
    for ret in transactions:
        transaction_data = []
        if ret:
            trans = OrderedDict()  # The ordereddict for the current dict
            if isinstance(ret, type(OrderedDict())):
                for key in ret:
                    if str(key).endswith('Ref'):
                        pass
                    elif key in model:
                        res = ret[key]
                        if isinstance(res, type(OrderedDict())):
                            pass
                            dt = (key, condition_push(res, OrderedDict(), model[key]))
                            trans.update([(key, res)])
                            # print key
                            # return trans
                        else:
                            dt = (key, res)
                            # print dt
                            trans.update([dt])

                    else:

                        pass
            else:
                pass
                dt = (ret, transactions[ret])
                trans.update([dt])

            if trans:
                pass
                transaction_data.append(trans)

        a.append(transaction_data)
    return a

a = condition_push(transaction_xml['QBXML']['QBXMLMsgsRs']['CustomerQueryRs']['CustomerRet'], data_to_push, result)

# print json.dumps(a, indent=4)
c = Customer(quickbooks_file_location=pt)
# print a[0]
# xmltodict.unparse(json.dumps(a[0]))
for customer in a:
 print c.create(payload=customer)

