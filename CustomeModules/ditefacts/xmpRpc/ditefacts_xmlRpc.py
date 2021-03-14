#!/usr/bin/env python
import xmlrpc.client
# info = xmlrpc.client.ServerProxy('http://localhost:1212').start()
import datetime

# https://www.odoo.com/documentation/12.0/webservices/odoo.html

# ********************************************* start authenticate fun *****************************************************************************************

url, db, username, password = 'http://localhost:8069','DB_Open_Academy','admin','admin'

print(url, db, username, password)
common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
common.version()
print(common)
print(common.version())
uid = common.authenticate(db, username, password, {})
print('uid',uid)
models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

print(models)
x = models.execute_kw(db, uid, password,'res.users.meal', 'action_print', [],[])
print(x)


