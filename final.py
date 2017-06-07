import codecs
import glob
import json
import os
from collections import OrderedDict

import re
from time import sleep

from quickbooks import Customer
from quickbooks.objects_models import CustomerAddModel
import xmltodict
company_target = os.path.abspath(os.path.join("..", 'client files', 'qbfile', 'qb981413_2.QBW'))
# company_target = os.path.abspath(os.path.join("..", 'client files', 'qbfile', 'Exploitatie 1998 tm 2014.QBW'))
company_source = os.path.abspath(os.path.join("..", 'client files', 'qbfile', 'Exploitatie  2015 tot heden'))
log_file = 'C:\\ProgramData\\Intuit\QuickBooks\\qbsdklog.txt'

force_allow = ['AccountRef', 'DepositToAccountRef', 'CustomerRef']
xml_files_ordered = ['Customer', 'Account', 'Check', ] # push some elements to the top, example account need to be before check


def get_log(log_file):
    with open(log_file, 'r',) as f:
        line_n = 0
        lines = []
        answer = None
        lines = f.readlines()
        for line in lines:
            line_n += 1


            occurence = line.find('================')
            if occurence != -1:
                answer = line_n
        if answer:
            return "".join(lines[answer:len(lines)])
    return False


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


def condition_push(transactions, data_to_push, model):
    a = []
    for ret in transactions:

        transaction_data = []
        if ret:
            trans = OrderedDict()  # The ordereddict for the current dict
            if isinstance(ret, type(OrderedDict())):
                for key in ret:
                    if str(key).endswith('Ref') and key not in force_allow:
                        pass
                    elif str(key).endswith('Ref'):
                        res = ret[key]
                        dt = (key, condition_push(res, OrderedDict(), model[key]))
                        trans.update([(key, res)])
                    elif key in model:
                        res = ret[key]
                        if isinstance(res, type(OrderedDict())):
                            dt = (key, condition_push(res, OrderedDict(), model[key]))
                            trans.update([(key, res)])
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

base_dir = os.path.join("..", 'data')
file_dir_name = company_source.split('\\')[-1].split('.')[0]
xml_files = glob.glob(os.path.join(base_dir, file_dir_name, '*.xml'))
query_resources = []
query_files = []
exclude = ['Company', 'Entity', 'CustomerMsg','Preferences', 'PriceLevel', 'ShipMethod','Template', 'Item',
           'SalesTaxPayable', 'Terms','Transaction']
transactions_list = []
trans= [
'Check',
'Deposit',
'Invoice',
'JournalEntry',
'ReceivePayment',
'Transfer',
]

from quickbooks import objects_models
from quickbooks import resource


def replace_ref(ref, new_ref, filenames):
    for filename in filenames:
        print 'replacing: {} ==> {} in {}'.format(ref, new_ref,  filename)

        with open(filename, 'r') as fr:
            contents = fr.read().replace(ref, new_ref)
        with open(filename, 'w') as fw:
            fw.write(contents)
            print 'done'

def get_refs(obj):
    print obj.retrieve()

def find_ref(js, ref_n, previous=[]):
    transaction_name = None
    full_name = None
    if not previous:
        previous = [1,]
    for j in js:

        if isinstance(js[j], type(OrderedDict())):
            previous.append(j)

            return find_ref(js[j], ref_n, previous)
        elif ref == js[j]:
            # print previous
            transaction_name = previous[-1].replace('Ref', '')
    return transaction_name, js['FullName']



xml_files = [xml_files.pop(xml_files.index(x)) for x in [(lambda xml: xml)(xml) for order in xml_files_ordered for xml in xml_files if order in xml]] + xml_files

# xml_files = [xml for xml in xml_files if exclude not in xml]
for x in xml_files:
    for a in exclude:
        if a in x:
            xml_files.pop(xml_files.index(x))
        else:
            print a, x
ordering = ["{} => {}".format(xml_files.index(x), x.split('\\')[-1].split('.')[0]) for x in xml_files]
print "\n".join(ordering)


for xml_file in xml_files[18:]:
    extra = None
    xml_name = xml_file.split('\\')[-1].split('.')[0]

    if xml_name:
        with codecs.open(xml_file, 'r', 'utf-8') as f:
            transaction_xml = xmltodict.parse(f.read())
            data = OrderedDict()
            result = data_conditioner(data=getattr(objects_models, "{}AddModel".format(xml_name))['elements'], new_data=data)
            data_to_push = OrderedDict()

            transactions = condition_push(transaction_xml['QBXML']['QBXMLMsgsRs']['{}QueryRs'.format(xml_name)]['{}Ret'.format(xml_name)], data_to_push, result)
            resource_object = getattr(resource, xml_name)(quickbooks_file_location=company_target)
            for transaction in transactions:
                print xml_name
                # modify this and add isautoapply
                if xml_name == 'ReceivePayment':
                    extra = OrderedDict([('IsAutoApply', 1)])



                res = resource_object.create(payload=transaction, extra=extra)
                if res:
                    res = xmltodict.parse(res)
                    if 'QBXML' in res:

                        result_tag = res['QBXML']['QBXMLMsgsRs']['{}AddRs'.format(xml_name)]
                        status = result_tag['@statusCode']
                        severity = result_tag['@statusSeverity']
                        message = result_tag['@statusMessage']

                        if int(status) == 3180:
                            print 'Duplicate'
                        elif int(status) ==3100:
                            print "Already in use"
                        elif int(status) ==3153:
                            print "Element may not be used : {}".format(message)
                        elif int(status) ==3240:
                            # Quickbooks has consistency with fullName in refs

                            ref = re.match('Object "(.*?)"',message).groups()[0]

                            js = xmltodict.parse(resource_object.qbxml)
                            ref_result = find_ref(js, ref)
                            transaction_name = ref_result[0]
                            if transaction_name:
                                print "Transaction name : {}".format(transaction_name)
                                tr = getattr(resource, transaction_name)(company_target)
                                res = xmltodict.parse(tr.retrieve(FullName=ref_result[1]))

                                try:
                                    if 'QBXML' in res:
                                        if 'QBXMLMsgsRs' in res['QBXML']:
                                            list_id = res['QBXML']['QBXMLMsgsRs']\
                                                ['{}QueryRs'.format(transaction_name)]['{}Ret'.format(transaction_name)]['ListID']

                                            replace_ref(ref, list_id, xml_files)
                                except Exception as e:
                                    print e
                                    print res

                        else:
                            print status, severity, message
                        if int(status) ==3100 or int(status) ==3100:
                            pass
                else:
                    log_str = get_log(log_file)
                    print log_str
                    print resource_object.qbxml
                    print 'sleeping so you can debug... '
                    # sleep(15)