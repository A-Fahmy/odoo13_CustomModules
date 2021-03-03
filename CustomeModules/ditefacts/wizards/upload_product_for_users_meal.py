
from odoo import models, fields,api
class upload_product_for_users_meal_wizard(models.TransientModel):
    _name = 'upload.product.for.users.meal'
    product_catid = fields.Many2one('Product Category', string="Product Category")
    item_ids = fields.Many2many('res.users.mealitem', string="Attendees")

    @api.model
    def default_get(self, fields_list):
        res = super(upload_product_for_users_meal_wizard, self).default_get(fields_list)
        vals = [(0, 0, {'item_id': 20, 'servings': 12}),
                (0, 0, {'item_id': 22, 'servings': 19})]
        res.update({'item_ids': vals})
        return res

    def action_upload_done(self):
        print('ahmed fahmy')
        # action_vals = {
        #     'name': _('users'),
        #     # 'domain': [('id', 'in', payments.ids), ('state', '=', 'posted')],
        #     # 'domain': [('id', '=', self.user_id.id), ('phone', '!=', False)],
        #     'res_model': 'res.users.meal',
        #     'view_id': False,
        #     'view_mode': 'tree,form',
        #     'type': 'ir.actions.act_window',
        # }
        context = dict(self.env.context)
        context['form_view_initial_mode'] = 'edit'
        print(self.item_ids)
        return {
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'res.users.meal',
            'res_id': False,
            'target': 'current',
            'res_item_ids': self.item_ids,
            'context': context,
            # 'context': {'default_item_ids': self.item_ids}

        }






