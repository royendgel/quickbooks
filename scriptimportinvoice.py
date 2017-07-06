import os
import glob
import logging
from xml.sax.saxutils import escape
import xml.etree.ElementTree as ET
import xmltodict

# preflight Check if we can reach all of trans types
def get_all_queries(source, target):
    from datetime import datetime
    startTime = datetime.now()
    from quickbooks import resource


    company = source
    base_dir = os.path.join("..", 'data')
    file_dir_name = company.split('\\')[-1].split('.')[0]
    xml_files = glob.glob(os.path.join(base_dir, file_dir_name, '*.xml'))
    query_resources = []
    query_files = []
    exclude = []
    trans= [
    'Check',
    'Deposit',
    'Invoice',
    'JournalEntry',
    'ReceivePayment',
    'Transfer',
    ]


    for entry in xml_files:
        res_name = entry.split('\\')[-1].split('.')[0]
        if res_name not in exclude:
            if hasattr(resource, res_name):
                if 'add' in  getattr(resource, res_name).methods:
                    query_resources.append(res_name)
                    query_files.append(entry)

    for q in query_files:
        res_name = q.split('\\')[-1].split('.')[0]
        print("Creating entries for: {}".format(q))
        with open(q, 'r') as f:
            document = xmltodict.parse(f)
            for key in document['QBXML']['QBXMLMsgsRs']["{}QueryRs".format(res_name)]["{}Ret".format(res_name)]:
                for k in key:
                    pass
                result = getattr(resource, res_name)(quickbooks_file_location=target).create(payload=key)
        break
        # print result

    print datetime.now() - startTime

get_all_queries(source=os.path.join("..", 'client files', 'qbfile', 'Exploitatie  2015 tot heden.qbw') ,target=os.path.abspath(os.path.join("..", 'client files', 'qbfile', 'Exploitatie 1998 tm 2014.QBW')))
