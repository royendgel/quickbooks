Quickbooks Desktop  Python wrapper
==================================

This supports all transaction type! 

###Requirements:

- Windows (32 bit recommended) if you want to work without the qwc
- win32com IMPORTANT ! if you want to work directly without qwc `pip install pywin32`
- Quickbooks > Pro Version, Enterprise edition
- Administrator account
- Python (32BIT not 64BIT)
- xmltodict



To install :
- clone this repo

install win32com

in your code write this:

```
from quickbooks import Quickbooks

Quickbooks(qb_file='path_to_your_file').get_all()


from quickbooks import Customer

# Retrieve all customer
Customer.retrieve()

# Retrieve customers based on filter
Customer.filter(date='2016-02-02')

# Add Customer
 Customer.create('name')
```


