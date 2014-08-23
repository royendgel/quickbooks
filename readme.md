Quickbooks Python
==================

Use this to connect to your quickbooks and read data.

###Requirments:

- Windows #ARGGGHH !
- win32com
- Quickbooks > Pro Version, Enterprise edition
- Administrator account

To install :
- clone this repo

install win32com
go into the folder and run python setup.py install

in your code write this:

```
import quickbooks

quickbooks(qb_file='path_to_your_file').get_all()
```

it does more than that read the source.

This is it, I will add more when my client ask me more ;)

Plan :
- Want to be able to create, remove and modify data
- Insert everything into database
- save the state so the next time I can get increment data (Faster)
- Make it work with qbwc (Should be easy I have a working version)
- implement in django and admin
