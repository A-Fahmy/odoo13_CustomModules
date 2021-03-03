# -*- coding: utf-8 -*-

from odoo import models, fields, api


class usersmealSummaryReportWizard(models.TransientModel):
    _name = 'wizard.users.meal.by.date'

    date_start = fields.Date(string='Start Date', required=True, default=fields.Date.today)
    date_end = fields.Date(string='End Date', required=True, default=fields.Date.today)

    def get_report(self):
        data = {
            'model': self._name,
            'ids': self.ids,
            'form': {
                'date_start': self.date_start, 'date_end': self.date_end,
            },
        }

        # ref `module_name.report_id` as reference.

        return self.env.ref('ditefacts.report_users_meal_bydate').report_action(self, data=data)