
from odoo import models, fields,api
class create_users_meal_wizard(models.TransientModel):
    _name = 'create.users.meal'
    # lock_confirmed_po = fields.Boolean("Lock Confirmed Orders", default=lambda self: self.env.company.po_lock == 'lock')
    name = fields.Char(string="Meal Name")
    meal_date = fields.Datetime(string="Meal Date")
    user_id = fields.Many2one('res.users', string="Meal User", required=True)
    notes = fields.Text('notes')

    def Create_User_Meal(self):
        vals = {
            'name': self.name,
            'meal_date': self.meal_date,
            'user_id': self.user_id.id,
            'notes': self.notes,
        }

        record_id= self.env['res.users.meal'].create(vals)
        self.env['res.users.mealitem'].create({
            'meal_id': record_id.id,
            'item_id': '15',
            'servings': '5',
            'notes': 'ahmed Fahmy ',
            'calories': '30 ',
        })
        record_id.message_post(
            subject='Create By Wizerd', body='Create By Code in View Wizerd')

        return record_id
