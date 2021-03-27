# -*- encoding: utf-8 -*-
import datetime
from odoo.http import request
from odoo import api, fields, models, _


class AccountMove(models.Model):
    _inherit = "account.move"

    journal_entry_created = fields.Boolean(
        string="Journal Entry Created by script",
        default=False, readonly=True)
    @api.model
    def create_journal_entry(self, date, ref, journal_id, debit_account_code, credit_account_code,amount
                             ,tax_account_code,discount_account_code,taswya_account_code,
                             tax_amount,discount_amount,taswya_amount,debit_or_credit_tax_dis_YN,debit_or_credit_taswya_YN):
        amount_debit=amount_credit=amount
        calc_other_amount=0
        if not date or not ref or not journal_id  or not debit_account_code or not amount or not credit_account_code:
            return 'wrong paramaters'

        debit_account_id = self.env['account.account'].search([('code','=',debit_account_code)],limit=1)
        if not len(debit_account_id):
            return 'no account by this code'+ debit_account_code
        debit_account_id=debit_account_id[0]

        credit_account_id = self.env['account.account'].search([('code', '=', credit_account_code)], limit=1)
        if not len(credit_account_id):
            return 'no account by this code' + credit_account_code
        credit_account_id = credit_account_id[0]

        vals_other_account = []
        if tax_account_code> 0 and tax_amount >0:
            tax_account_id = self.env['account.account'].search([('code', '=', tax_account_code)], limit=1)
            if not len(tax_account_id):
                return 'no account by this code' + tax_account_id
            calc_other_amount += tax_amount;
            if debit_or_credit_tax_dis_YN ==True:
                vals_other_account += (0, 0, {
                    'account_id': tax_account_id.id,
                    'debit': tax_amount,
                    'credit': 0,
                }),
            else:
                vals_other_account += (0, 0, {
                    'account_id': tax_account_id.id,
                    'debit': 0,
                    'credit': tax_amount,
                }),

        if discount_account_code > 0 and discount_amount > 0:
            discount_account_id = self.env['account.account'].search([('code', '=', discount_account_code)], limit=1)
            if not len(discount_account_id):
                return 'no account by this code' + discount_account_id
            calc_other_amount += discount_amount;
            if debit_or_credit_tax_dis_YN == True:
                vals_other_account += (0, 0, {
                    'account_id': discount_account_id.id,
                    'debit': discount_amount,
                    'credit': 0,
                }),
            else:
                vals_other_account += (0, 0, {
                    'account_id': discount_account_id.id,
                    'debit': 0,
                    'credit': discount_amount,
                }),

        vals_taswya_account = []
        if taswya_account_code > 0 and taswya_amount > 0:
            taswya_account_id = self.env['account.account'].search([('code', '=', taswya_account_code)], limit=1)
            if not len(taswya_account_id):
                return 'no account by this code' + taswya_account_id
            if debit_or_credit_taswya_YN == True:
                vals_taswya_account += (0, 0, {
                    'account_id': taswya_account_id.id,
                    'debit': taswya_amount,
                    'credit': 0,
                }),
            else:
                vals_taswya_account += (0, 0, {
                    'account_id': taswya_account_id.id,
                    'debit': 0,
                    'credit': taswya_amount,
                }),


        if debit_or_credit_tax_dis_YN == True and len(vals_other_account)>0:
            amount_debit=amount_debit-calc_other_amount

        if debit_or_credit_taswya_YN == True and len(vals_taswya_account) > 0:
            amount_debit = amount_debit - taswya_amount

        if debit_or_credit_tax_dis_YN == False and len(vals_other_account) > 0:
            amount_credit = amount_credit - calc_other_amount

        if debit_or_credit_taswya_YN == False and len(vals_taswya_account) > 0:
            amount_credit = amount_credit - taswya_amount

        vals_items = []
        vals_items += (0, 0, {
            'account_id': debit_account_id.id,
            'debit': amount_debit,
            'credit': 0,
        }),
        if debit_or_credit_tax_dis_YN == True and len(vals_other_account) > 0:
            vals_items+=vals_other_account

        if debit_or_credit_taswya_YN == True and len(vals_taswya_account) > 0:
            vals_items+=vals_taswya_account


        vals_items += (0, 0, {
                  'account_id': credit_account_id.id,
                 'debit': 0,
                 'credit': amount_credit,
        }),
        if debit_or_credit_tax_dis_YN == False and len(vals_other_account) > 0:
            vals_items += vals_other_account

        if debit_or_credit_taswya_YN == False and len(vals_taswya_account) > 0:
            vals_items+=vals_taswya_account

        print(vals_items)

        moves_create = {
            'date': date,
            'ref': ref,
            'journal_id': journal_id,
            'company_id': self.env.user.company_id.id,
            'state': 'draft',
            'journal_entry_created': True,
            'line_ids': vals_items,
        }
        move_id = self.env['account.move'].create(moves_create)
        return move_id.id

