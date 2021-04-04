# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import calendar
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from odoo import api,  models, _
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from datetime import datetime, timedelta
class dailyMealReport(models.AbstractModel):
    _name = 'report.ditefacts.call_dailymealreport'
    _description = 'daily Meal Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        date_start = data['form']['date_start']
        date_end = data['form']['date_end']
        user_id = data['form']['user_id']
        user_name = data['form']['user_name']
        user_ids = data['form']['user_ids'][0]

        start_date = datetime.strptime(date_start, DATE_FORMAT)
        end_date = datetime.strptime(date_end, DATE_FORMAT)
        domain = ['&', ('meal_date', '>=', start_date.strftime(DATETIME_FORMAT)), ('meal_date', '<', end_date.strftime(DATETIME_FORMAT))]
        if user_id and user_id>0:
            domain = domain + [('user_id', '=', user_id)]
            # domain = domain + [('user_id', 'in', user_ids)]

        docs = self.env['res.users.meal'].search(domain)
        # docs = self.env['res.users.meal'].browse([23,29])
        print(docs)
        return {
            'doc_ids': self.ids,
            'doc_model': data['model'],
            'date_start': date_start,
            'date_end': date_end,
            'user_id': user_id,
            'user_name': user_name,
            'docs': docs,
        }
