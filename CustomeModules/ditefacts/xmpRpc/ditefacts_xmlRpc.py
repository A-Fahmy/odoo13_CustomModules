#!/usr/bin/env python
import xmlrpc.client
# info = xmlrpc.client.ServerProxy('http://localhost:1212').start()
import datetime

# https://www.odoo.com/documentation/12.0/webservices/odoo.html

# ********************************************* start authenticate fun *****************************************************************************************

# url, db, username, password = 'http://localhost:8069','DB_Open_Academy','admin','admin'
url, db, username, password = 'http://149.56.255.81:1110','Nour_live2021','mohamedhamdy635@gmail.com','admin'

print(url, db, username, password)
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
common.version()
print(common)
print(common.version())
uid = common.authenticate(db, username, password, {})
print('uid',uid)
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

# print(models)
# x = models.execute_kw(db, uid, password,'res.users.meal', 'action_printxml', [],[])
# print(x)
amount=150
par_dict = {
   'date':'2021-3-28',
   'ref': 'Journal Entry For testing1',
   'journal_id': 1,
   'debit_account_code': 102030103,
   'credit_account_code': 401010001,
   'amount': amount,
   'tax_account_code': 206010290,
   'discount_account_code': 102010003,
   'taswya_account_code': 206010001,
   'tax_amount': 30,
   'discount_amount': 50,
   'taswya_amount': 15,
   'debit_or_credit_tax_dis_YN': True,
   'debit_or_credit_taswya_YN': True,
}
res = models.execute_kw(db, uid, password,'account.move', 'create_journal_entry', [],par_dict)
print(res)



