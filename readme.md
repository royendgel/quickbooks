Quickbooks Python
==================

Use this to connect to your quickbooks and read data.

###Requirements:

- Windows (32 bit recommended)
- win32com IMPORTANT !
- Quickbooks > Pro Version, Enterprise edition
- Administrator account
- Python (32BIT not 64BIT)


###Optional

- xmltodict

To install :
- clone this repo

install win32com
go into the folder and run python setup.py install

in your code write this:

```
from quickbooks import Quickbooks

Quickbooks(qb_file='path_to_your_file').get_all()
```

it does more than that read the source.

This is it, I will add more when my client ask me more ;)

Please note this will take longtime to load all your data.

Plan :
- Want to be able to create, remove and modify data
- Insert everything into database
- save the state so the next time I can get increment data (Faster)
- Make it work with qbwc (Should be easy I have a working version)
- implement in django and admin
