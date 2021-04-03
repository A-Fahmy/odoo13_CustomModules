# -*- coding: utf-8 -*-

from odoo import models, fields, api


class dailyMealReportWizard(models.TransientModel):
    _name = 'wizard.daily.meal.report'
    date_start = fields.Date(string='Start Date', required=True, default=fields.Date.today)
    date_end = fields.Date(string='End Date', required=True, default=fields.Date.today)
    user_id = fields.Many2one('res.users', string="Meal User")


    def get_report(self):
        data = {
            'model': self._name,
            'ids': self.ids,
            'form': {
                'date_start': self.date_start, 'date_end': self.date_end,
            },
        }

        # ref `module_name.report_id` as reference.

        return self.env.ref('ditefacts.report_dailyMealReport').report_action(self, data=data)