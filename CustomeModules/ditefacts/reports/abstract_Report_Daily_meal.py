# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import calendar
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from odoo import api,  models, _

class dailyMealReport(models.AbstractModel):
    _name = 'report.ditefacts.call_dailymealreport'
    _description = 'daily Meal Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        date_start = data['form']['date_start']
        date_end = data['form']['date_end']
        docs = self.env['res.users.meal'].browse([23,29])
        print(docs)
        return {
            'doc_ids': self.ids,
            'doc_model': data['model'],
            'date_start': date_start,
            'date_end': date_end,
            'docs': docs,
        }
