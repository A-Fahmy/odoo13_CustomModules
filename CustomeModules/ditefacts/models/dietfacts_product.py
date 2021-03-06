# -*- coding: utf-8 -*-

from odoo import models, fields,exceptions, api,_
from lxml import etree
#
#

class dietfacts_res_users(models.Model):
    # _name = 'product.template'
    _inherit = 'res.users'


    # def name_get(self):
    #     result = []
    #     for rec in self:
    #         name = str(rec.id) + '-' + rec.name
    #         result.append((rec.id, name))
    #     return result

    @api.model
    def _name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []
        domain = []
        if name:
            domain = ['|', ('name', operator, name), ('id', operator, name)]

        # domain = ['|', '|', '|', ('name', operator, name), ('email', operator, name),
        #           ('school_number', operator, name), ('school_type', operator, name)]
        return super(dietfacts_res_users, self).search(domain,limit=limit).name_get()


    # @api.model
    # def default_get(self, fields):
    #     res = super(dietfacts_res_users, self).default_get(fields)
    #     warehouse = None
    #     if 'warehouse_id' not in res and res.get('company_id'):
    #         warehouse = self.env['stock.warehouse'].search([('company_id', '=', res['company_id'])], limit=1)
    #     if warehouse:
    #         res['warehouse_id'] = warehouse.id
    #         res['location_id'] = warehouse.lot_stock_id.id
    #     return res

    @api.model
    def default_get(self, fields):
        res = super(dietfacts_res_users, self).default_get(fields)
        res['login'] = 'ahmed Fahmy'
        return res

class dietfacts_res_partner(models.Model):
    _inherit = 'res.partner'
    company_type = fields.Selection(selection_add=[('code', 'Fahmy')])
    name_ditefact = fields.Char(string="Meal Name")


class dietfacts_sale_order(models.Model):
    _inherit = 'sale.order'
    dietfact_id = fields.Char(string="Diet Fact ID")
    def action_confirm(self):
        print('ahmed')
        super(dietfacts_sale_order, self).action_confirm()



class dietfacts_product_Templete(models.Model):
    # _name = 'product.template'
    _inherit = 'product.template'
    calories = fields.Integer(string="calories")
    servingsize = fields.Float(string="serving size")
    lastupdate = fields.Date(string="last update")
    dietitem = fields.Boolean(string="diet item")
    nutrient_ids = fields.One2many('product.template.nutrient', 'product_id', string="Nutrient")

class dietfacts_Product_Template_Attribute_Line(models.Model):
    _inherit = 'product.template.attribute.line'
    notes = fields.Text('notes')

class dietfacts_res_users_meal(models.Model):
    _name = 'res.users.meal'
    _inherit = ['mail.thread.cc', 'mail.activity.mixin']
    # _rec_name = 'meal_date'
    _rec_name = 'name_seq'
    _order = 'name_seq asc'

    # // exmple  Make Defulte Value in one2meny and one2one
    @api.model
    def default_get(self, fields_list):
        print(fields_list)
        res = super(dietfacts_res_users_meal, self).default_get(fields_list)
        # vals = [(0, 0, {'item_id': 20, 'servings': 12}),
        #         (0, 0, {'item_id': 22, 'servings': 19})]
        # res.update({'item_ids': vals})
        res['user_id']= 2
        res['gender'] = 'male'
        return res


    # // Add Field in desing file xml by code
    # @api.model
    # def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
    #
    #     res = super(school_student, self).fields_view_get(view_id=view_id, view_type=view_type, toolbar=toolbar,
    #                                                       submenu=submenu)
    #
    #     if view_type == "form":
    #         doc = etree.XML(res['arch'])
    #         name_field = doc.xpath("//field[@name='name']")
    #         if name_field:
    #             # Added one label in form view.
    #             name_field[0].addnext(
    #                 etree.Element('label', {'string': 'Hello this is custom label from fields_view_get method'}))
    #
    #         # override attribute
    #         address_field = doc.xpath("//field[@name='school_address']")
    #         if address_field:
    #             address_field[0].set("string", "Hello This is School Address.")
    #             address_field[0].set("nolabel", "0")
    #
    #         res['arch'] = etree.tostring(doc, encoding='unicode')
    #
    #     if view_type == 'tree':
    #         doc = etree.XML(res['arch'])
    #         school_field = doc.xpath("//field[@name='school_id']")
    #         if school_field:
    #             # Added one field in tree view.
    #             school_field[0].addnext(etree.Element('field', {'string': 'Total Fees',
    #                                                             'name': 'total_fees'}))
    #         res['arch'] = etree.tostring(doc, encoding='unicode')
    #     return res


    def _set_defult_notes(self):
        return " Create Notes"


    def _get_user_id_Count(self):
        _count = self.env['res.users.meal'].search_count([('user_id', '=', self.user_id.id)])
        self.user_id_Count_in_model=_count

    def action_delete_one2many(self):
        # // exmple Delete and Create one 2 many
        CurrentRecord = self.env['sale.order'].sudo().search([('dietfact_id', '=', self.name_seq)])
        vals_itemstest=[]
        if self.item_ids:
            # // Create one Record from self.item_ids
            # for record in self.item_ids:
            #     vals_itemstest = [(0, 0, {
            #         'product_id': record.item_id.id,
            #         'price_unit': 5,
            #         'product_uom_qty': record.servings,
            #     })]
            # // Create all  Record from self.item_ids
            for record in self.item_ids:
                vals_itemstest += [(0, 0, {
                    'product_id': record.item_id.id,
                    'price_unit': 5,
                    'product_uom_qty': record.servings,
                })]
        vals = {
            'partner_id': 14,
            'date_order': self.meal_date,
            'state': 'draft',
            'dietfact_id': self.name_seq,
            'order_line': vals_itemstest,
        }
        print(vals_itemstest)

        if CurrentRecord.exists():
            print('fahmy')
            CurrentRecord.order_line=[(5, 0, 0)]
            CurrentRecord.write(vals)
            record_id = CurrentRecord
        else:
            print('xxxxx')
            record_id = self.env['sale.order'].create(vals)


        # for record in self:
        #     record.item_ids=[(5, 0, 0)]





    def action_confirm(self):
         for rec in self:
             rec.state="confirm"
         self.write({'notes_create': 'notes write'})

         return {
                'effect': {
                    'fadeout': 'slow',
                    'message': 'Confirm Done',
                    'type': 'rainbow_man',
                }
            }

    def action_done(self):
         for rec in self:
             print('fahmy')
             rec.state="done"

    def action_delete_record(self):
         # for rec in self:
         self.search([('id', '=', self.id)]).unlink()
         action_vals = {
              'name': _('users'),
             # 'domain': [('id', 'in', payments.ids), ('state', '=', 'posted')],
             # 'domain': [('id', '=', self.user_id.id), ('phone', '!=', False)],
             'res_model': 'res.users.meal',
             'view_id': False,
             'view_mode': 'tree,form',
             'type': 'ir.actions.act_window',
         }
         print('xxxx')
         return action_vals






    def action_Create_quotationByCreate_H_and_D_One_Action(self):
        for record in self.item_ids:
            vals_itemstest = [(0, 0, {
                'product_id': record.item_id.id,
                'price_unit': 5,
                'product_uom_qty': record.servings,
            })]

        vals = {
            'partner_id': 14,
            'date_order': self.meal_date,
            'state': 'draft',
            'dietfact_id': self.name_seq,
            'order_line': vals_itemstest,
        }
        record_id = self.env['sale.order'].create(vals)

        print(record_id)

        return record_id
    #region check_Call AccountMove
    # def action_print(self):
    #     date='2021-3-28'
    #     ref='Journal Entry For testing1'
    #     journal_id=1
    #     debit_account_code=101501
    #     credit_account_code=101401
    #     amount=150
    #     tax_account_code=101701
    #     discount_account_code =110100
    #     taswya_account_code = 450000
    #     tax_amount = 30
    #     discount_amount = 50
    #     taswya_amount = 15
    #     debit_or_credit_tax_dis_YN = True
    #     debit_or_credit_taswya_YN = True
    #
    #
    #
    #     return self.env['account.move'].create_journal_entry(date,ref,journal_id,debit_account_code,credit_account_code,amount
    #                                                          ,tax_account_code,discount_account_code,taswya_account_code
    #                                                          ,tax_amount,discount_amount,taswya_amount,debit_or_credit_tax_dis_YN,debit_or_credit_taswya_YN)
    #endregion

    def action_print(self):
        self._update_cron()
        return self.env.ref('ditefacts.report_res_users_meal').report_action(self)

    def action_print_excel(self):
        return self.env.ref('ditefacts.report_res_users_meal_excel').report_action(self)

    @api.model
    def action_printxml(self):
        print('ahmed fahmy')
        return True

    def action_Create_quotation(self):

         # // exmple Create View in odoo

        # self.env.cr.execute('select product_id, order_id from  sale_order_line where order_id=37')
        # result = self.env.cr.fetchall()
        # print(result)
         
          # // exmple filter in odoo
         
        # var_filter= self.env['sale.order'].search([]).filtered(lambda m: m.id == 20)
        # print(var_filter)

          # // exmple mapped in odoo
         
        # var_mapped = self.env['sale.order'].search([]).mapped()
        # print(var_mapped)

          # // exmple sorted in odoo
         
        # var_sorted = self.env['sale.order'].search([]).sorted(key='id', reverse=True).mapped()
        # print(var_sorted)

        # CurrentRecord = self.env['sale.order'].browse(48)



        CurrentRecord = self.env['sale.order'].sudo().search([('dietfact_id', '=', self.name_seq)])
        vals = {
            'partner_id': 14,
            'date_order': self.meal_date,
            'state': 'draft',
            'dietfact_id': self.name_seq,
        }


        if CurrentRecord.exists():
               CurrentRecord.write(vals)
               record_id=CurrentRecord

        else:
              record_id = self.env['sale.order'].create(vals)

        # // org
        print(record_id)
        if self.item_ids:
            for record in self.item_ids:
                vals_items={
                    'order_id': record_id.id,
                    'product_id': record.item_id.id,
                    'price_unit': 5,
                    'product_uom_qty': record.servings,
                }
                if  CurrentRecord.exists():
                    checkItem=self.env['sale.order.line'].sudo().search([('product_id', '=', record.item_id.id),('order_id', '=', CurrentRecord.id)])
                    if checkItem.exists():
                        checkItem.write(vals_items)
                    else:
                        self.env['sale.order.line'].create(vals_items)
                else:
                    self.env['sale.order.line'].create(vals_items)

        return record_id

    name = fields.Char(string="Meal Name")
    # meal_date = fields.Datetime(string="Meal Date", groups="base.group_no_one")  // show field only in developer mode
    meal_date = fields.Datetime(string="Meal Date")
    user_id = fields.Many2one('res.users', string="Meal User", required=True)
    user_ids = fields.Many2many('res.users', string="Meal Users")
    # // Create Field Many2many with Determine the name Tables and Fields Name Relations
    # user_ids = fields.Many2many('res.users','res_Meal_Res_User_rel','field_meal_id','field_user_id', string="Meal Users")

    notes = fields.Text('notes',default=_set_defult_notes,)
    item_ids = fields.One2many('res.users.mealitem', 'meal_id', string="meal item")
    color = fields.Integer()
    totalcalories = fields.Integer(string="Total Meal Calories", Store=True,  compute='_calccalories')
    larg_Meal = fields.Boolean(string="Larg Meal", compute='_largMeal')
    name_seq = fields.Char(string='No Reference', required=True, copy=False, readonly=True,
                        index=True, default=lambda self: _('New'))

    user_id_Count_in_model = fields.Integer(string="count in Model", compute='_get_user_id_Count')


    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], default="male", string="gender", tracking=True,track_visibility='always')

    age_group = fields.Selection([
        ('major', 'Major'),
        ('minor', 'Minor'),
    ],  string="Age Group", compute='_set_age_group')
    age_user_id = fields.Integer(string='age',track_visibility='always', group_operator=False)
    notes_create = fields.Text('notes Test')
    state = fields.Selection([('draft', 'Draft'), ('confirm', 'Confirm'), ('done', 'Done'), ('cancel', 'Cancel')], string='Status', required=True,
                             default='draft')
    active = fields.Boolean('Active', default=True)
    res_mail_by_userid= fields.Many2one('res.users.meal', string="Res Mail by Userid")
    company_id = fields.Many2one('res.company', string='Company', required=True, default=lambda self: self.env.user.company_id)
    email_id = fields.Char(string="Email",copy=False)

    @api.onchange('user_id')
    def _onchange_user_id(self):
        domain = []
        if self.user_id:
            domain = [('user_id', '=', self.user_id.id)]
        return {'domain': {'res_mail_by_userid': domain}}

    @api.onchange('res_mail_by_userid')
    def _res_mail_by_userid(self):
        for rec in self:
            vals_items =[(5, 0, 0)]
            # vals_items = [] // For Append in field one2many
            if rec.res_mail_by_userid:
                get_meal_items = self.env['res.users.mealitem'].search([('meal_id', '=', rec.res_mail_by_userid.id)])
                # get_meal_items = self.env['res.users.mealitem'].browse(get_meal_itemstest.ids)
                if get_meal_items:
                    mealitem_lines=[(5, 0, 0)]
                    for r in get_meal_items:
                        vals_items += [(0, 0, {
                            'meal_id': 1,
                            'item_id': r.item_id.id,
                            'servings': r.servings,
                            'notes': r.notes,
                            'calories': r.calories,
                        })]
                        mealitem_lines.append(vals_items)
                print(get_meal_items)
                   # //  this is done after fill vals_items
                return {'value': {'item_ids': vals_items}}
                    # // this is done for return get_meal_items
                # return {'value': {'item_ids': get_meal_items}}

    @api.depends('age_user_id')
    def _set_age_group(self):
        for r in self:
            r.age_group='minor'
            if r.age_user_id:
                if r.age_user_id < 18:
                    r.age_group = 'minor'
                else:
                    r.age_group = 'major'

    @api.constrains('age_user_id')
    def _Check_age(self):
        for r in self:
            if r.age_user_id <= 5:
                raise exceptions.ValidationError("the Age Must be Greater then 5")

    def action_get_users_view(self):
        check_empty = self.env['res.users'].sudo().search([('id', '=', self.user_id.id),('phone', '!=', False)]).id
        if check_empty == False:
            raise exceptions.ValidationError("No Data")
            return
        else:
            action_vals= {
                'name': _('users'),
                # 'domain': [('id', 'in', payments.ids), ('state', '=', 'posted')],
                'domain': [('id', '=', self.user_id.id) , ('phone', '!=', False)],
                'res_model': 'res.users',
                'view_id': False,
                'view_mode': 'tree,form',
                'type': 'ir.actions.act_window',
            }
            # if len(check_empty) > 0:
            #     action_vals.update({'id': check_empty, 'view_mode': 'form'})
            # else:
            #     action_vals['view_mode'] = 'tree,form'
            return action_vals
        return action_vals

    @api.model
    def _update_cron(self):
        try:
            # Enabled/Disable cron based on the number of 'done' server of type pop or imap

            # cron = self.env.ref('base_automation.ir_cron_data_base_automation_check', raise_if_not_found=False)
            # return cron and cron.toggle(model=self._name, domain=[('trigger', '=', 'on_time')])

            cron = self.env.ref('ditefacts.Cron_action_test_ditemeal',raise_if_not_found=False)
            # cron.toggle()
        except ValueError:
            pass

    @api.model
    def _cron_job_action_test_ditemeal(self):
        print('xxxxxx')
        # ''' This method is called from a cron job.
        # It is used to post entries such as those created by the module
        # account_asset.
        # '''
        # records = self.search([
        #     ('state', '=', 'draft'),
        #     ('date', '<=', fields.Date.today()),
        #     ('auto_post', '=', True),
        # ])
        # records.post()
        print('cron_job_action_test_ditemeal')

    @api.model
    def _Call_Function_by_server_action(self):
        print('Call_Function_by_server_action')
        action_vals = {
            'name': _('open Res Meal after Call Function by server action'),
            'res_model': 'res.users.meal',
            'view_id': False,
            'view_mode': 'tree,form',
            'type': 'ir.actions.act_window',
        }
        return action_vals

    @api.depends('item_ids', 'item_ids.servings')
    def _calccalories(self):
        for facts in self:
            facts.totalcalories=0
            if facts.item_ids:
                currentcalories=0
                for r in facts.item_ids:
                    if not r.calories and not r.servings:
                        continue
                    currentcalories += (r.calories*r.servings)
                facts.totalcalories=currentcalories

    @api.depends('totalcalories')
    def _largMeal(self):
        for r in self:
            self.larg_Meal = False
            if not r.totalcalories:
                r.larg_Meal = False
            elif r.totalcalories > 100:
                r.larg_Meal = True

    # // override function Create
    @api.model
    def create(self, vals):
        if vals.get('name_seq', _('New')) == _('New'):
              vals['name_seq'] = self.env['ir.sequence'].next_by_code('Ditefacts.Sequence') or _('New')
        vals['notes_create']='Fahmy Fahmy'

        result = super(dietfacts_res_users_meal, self).create(vals)
        result.notes='Mazen'
        print(result)
        return result

    # // override function write
    def write(self, vals):
        # vals['notes']='Mazen'
        res = super(dietfacts_res_users_meal, self)._write(vals)
        print(res)
        return res

    def copy(self, default = {}):
        #default['active'] = False
        default['name'] = "copy ("+self.name+")"
        rtn = super(dietfacts_res_users_meal, self).copy(default=default)
        rtn.total_fees = 500
        return rtn

    # def unlink(self):
    #     print("self statement ",self)
    #     # for stud in self:
    #     #     if stud.total_fees > 0:
    #     #         raise UserError(_("You can't delete this %s student profile"%stud.name))
    #     rtn = super(dietfacts_res_users_meal, self).unlink()
    #     print("Return statement ",rtn)
    #     return rtn

    def call_action_from_api(self,vals):
        # print(vals['name'])

        get_docs=vals['docs']
        print(get_docs.name)
        print(' the  call action from api after create')

    def action_send_card(self):
        # sending the patient report to patient via email
        template_id = self.env.ref('ditefacts.res_meal_card_email_template').id
        template = self.env['mail.template'].browse(template_id)
        template.send_mail(self.id, force_send=True)





class dietfacts_res_users_mealitems(models.Model):
    _name = 'res.users.mealitem'

    meal_id = fields.Many2one('res.users.meal', string="Meal id")
    item_id = fields.Many2one('product.template', string="meal items")
    servings = fields.Float(string="serving")
    notes = fields.Text('meal item notes')
    calories = fields.Integer(related='item_id.calories', string='Calories Per Serving', Store=True, readonly=False)
    # calories2 = fields.Integer(string='Calories Per Serving2')
    sequence = fields.Integer(string="sequence")

    @api.onchange('servings')
    def _onchange_servings(self):
        if self.item_id.id > 0 and self.calories <= 0 :
            self.calories = self.servings


    def open_one2many_line(self):
        context = self.env.context
        print(context.get('default_active_id'))


class dietfacts_product_nutrient(models.Model):
    _name = 'product.nutrient'
    name = fields.Char(string="Nutrient Name")
    uom_id = fields.Many2one('uom.uom', string="Unit of Measure")
    description = fields.Text('description')

class dietfacts_product_template_nutrient(models.Model):
    _name = 'product.template.nutrient'
    nutrient_id = fields.Many2one('product.nutrient', string="Nutrient")
    product_id = fields.Many2one('product.template', string="Diet Item")
    value = fields.Float(string="Value")
    dailypercentage = fields.Float(string="Daily Percentage")
    # unitofmeasure = fields.Integer(related='nutrient_id.uom.id.name', string='Unit Of Measure',  readonly=True)

