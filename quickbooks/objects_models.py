BillModel = [
    ('VendorRef', [
        'ListID',
        'FullName',
    ]),
    ('VendorAddress', [
        'Addr1',
        'Addr2',
        'Addr3',
        'Addr4',
        'Addr5',
        'City',
        'State',
        'PostalCode',
        'Country',
        'Note'
    ]),
    ('APAccountRef', [
        'ListID',
        'FullName'

    ]),
    'TxnDate',
    'DueDate',
    'RefNumber',
    ('TermsRef', [
        'ListID',
        'FullName'

    ]),
    'Memo',
    'ExchangeRate',
    'ExternalGUID',
    'LinkToTxnID',
    ('ExpenseLineAdd', [
        ('AccountRef', [
            'ListID',
            'FullName'

        ]),
        'Amount',
        'Memo',
        ('CustomerRef', [
            'ListID',
            'FullName'

        ]),
        ('ClassRef', [
            'ListID',
            'FullName'

        ]),
        'BillableStatus',
        ('SalesRepRef', [
            'ListID',
            'FullName'
        ]),
        ('DataExt', [
            'OwnerID',
            'DataExtName',
            'DataExtValue'
        ])
    ]),
    ('ItemLineAdd', [
        ('ItemRef', [
            'ListID',
            'FullName'
        ]),
        ('InventorySiteRef', [
            'ListID',
            'FullName'
        ]),
        ('InventorySiteLocationRef', [
            'ListID',
            'FullName'
        ]),
        'SerialNumber',
        'LotNumber',
        'Desc',
        'Quantity',
        'UnitOfMeasure',
        'Cost',
        'Amount',
        ('CustomerRef', [
            'ListID',
            'FullName'
        ]),
        ('ClassRef', [
            'ListID',
            'FullName'
        ]),
        'BillableStatus',
        ('OverrideItemAccountRef', [
            'ListID',
            'FullName'
        ]),
        ('LinkToTxn', [
            'TxnID',
            'TxnLineID'
        ]),
        ('SalesRepRef', [
            'ListID',
            'FullName'
        ]),
        ('DataExt', [
            'OwnerID',
            'DataExtName',
            'DataExtValue'
        ])

    ]),
    ('ItemGroupLineAdd', [
        ('ItemGroupRef', [
            'ListID',
            'FullName'
        ]),
        'Quantity',
        'UnitOfMeasure',
        ('InventorySiteRef', [
            'ListID',
            'FullName'
        ]),
        ('InventorySiteLocationRef', [
            'ListID',
            'FullName'
        ]),
        ('DataExt', [
            'OwnerID',
            'DataExtName',
            'DataExtValue'

        ])

    ])

]

CustomerModel = [
    'Name',
    'IsActive',
    ('ParentRef', [
        'ListID',
        'FullName'
    ]),
    'AccountType',
    'AccountNumber',
    'BankNumber',
    'Desc',
    'OpenBalance',
    'OpenBalanceDate',
    'TaxLineID',
    ('CurrencyRef', [
        'ListID',
        'FullName'
    ]),
]

ARRefundCreditCardAdd = [
    
]