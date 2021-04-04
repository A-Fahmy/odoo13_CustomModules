# -*- coding: utf-8 -*-

from odoo import models, fields, api


class dailyMealReportWizard(models.TransientModel):
    _name = 'wizard.daily.meal.report'
    date_start = fields.Date(string='Start Date', required=True, default=fields.Date.today)
    date_end = fields.Date(string='End Date', required=True, default=fields.Date.today)
    user_id = fields.Many2one('res.users', string="Meal User")
    user_ids = fields.Many2many('res.users', string="Meal Users")


    def get_report(self):
        data = {
            'model': self._name,
            'ids': self.ids,
            'form': {
                'date_start': self.date_start,
                'date_end': self.date_end,
                'user_id': self.user_id.id,
                'user_name': self.user_id.name,
                'user_ids': [tuple(self.user_ids.ids)],

            },
        }

        # ref `module_name.report_id` as reference.
        # params = [tuple(self.user_ids.ids)]
        # print(params)

        return self.env.ref('ditefacts.report_dailyMealReport').report_action(self, data=data)