# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import calendar

from datetime import timedelta
from dateutil.relativedelta import relativedelta
from odoo import api,  models, _

class res_users_meal_Report(models.AbstractModel):
    _name = 'report.ditefacts.call_report_res_users_meal_view2'
    _description = 'report Res Users Meal'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['res.users.meal'].browse(docids[0])
        recuserslist = self.env['res.users'].sudo().search([('id', '=', docs.user_id.id)])
        userslist = []
        for record in recuserslist:
            vals = {
                'id': record.id,
                'name': record.name,
                'login': record.login,
            }
            userslist.append(vals)
        print(userslist)
        return {
            'doc_ids': self.ids,
            'doc_model': 'res.users.meal',
            'docs': docs,
            'userslist': userslist,
        }
