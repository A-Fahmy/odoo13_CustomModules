# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import calendar

from datetime import datetime, timedelta

from odoo import models, fields, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT

class res_users_meal_Report(models.AbstractModel):
    _name ='report.ditefacts.desing_report_users_meal_bydate_view'
    _description = 'report Res Users Meal By Date'

    @api.model
    def _get_report_values(self, docids, data=None):
        date_start = data['form']['date_start']
        date_end = data['form']['date_end']
        activities = []

        # cr.execute("""UPDATE roster_days_allocation SET roster_allocation_connection = (SELECT MAX(ra.id) FROM roster_allocation ra, roster_substitution rs
        #                             WHERE ra.emp_id=rs.sub_employee)
        #               WHERE allocation_start_day = %s AND roster_time_list = %s""", (sub_day, ros_time))

        self.env.cr.execute('select product_id, order_id from  sale_order_line where order_id=37')
        result = self.env.cr.fetchall()
        print(result)

        sql = "select meal_date,10 as totalcalories, 11  as total_res_user from res_users_meal"
        self.env.cr.execute(sql)
        for activity in self.env.cr.dictfetchall():
            activities.append({
                'meal_date': activity.get('meal_date'),
                'totalcalories': activity.get('totalcalories'),
                'total_res_user': activity.get('total_res_user'),
                'company': self.env.user.company_id
            })

        print(activities)


        res = self.env['res.users.meal']
        start_date = datetime.strptime(date_start, DATE_FORMAT)
        end_date = datetime.strptime(date_end, DATE_FORMAT)
        delta = timedelta(days=1)

        docs = []
        while start_date <= end_date:
            date = start_date
            start_date += delta

            print(date, start_date)
            res_users = res.search([
                ('meal_date', '>=', date.strftime(DATETIME_FORMAT)),
                ('meal_date', '<', start_date.strftime(DATETIME_FORMAT)),
            ])

            total_res_user = len(res_users)
            totalcalories = sum(r.totalcalories for r in res_users)

            docs.append({
                'meal_date': date.strftime("%Y-%m-%d"),
                'total_res_user': total_res_user,
                'totalcalories': totalcalories,
                'company': self.env.user.company_id
            })
        return {
            'doc_ids': data['ids'],
            'doc_model': data['model'],
            'date_start': date_start,
            'date_end': date_end,
            'docs': activities,
        }