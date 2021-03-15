from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale
class DiteFact_ORM(http.Controller):

    # Sample Controller Created

    # exmple path json in postman
    # {
    #     "jsonrpc": "2.0",
    #     "params":
    #         {
    #             "id": "129",
    #             "name": "DB_Open_Academy ahmed",
    #             "notes": "admin"
    #         }
    # }

    @http.route('/update_Meals', type='json', auth='user')
    def update_Meals(self, **rec):
        if request.jsonrequest:
            if rec['id']:
                print("rec...", rec)
                record= request.env['res.users.meal'].sudo().search([('id', '=', rec['id'])])
                if record:
                    record.sudo().write(rec)
                args = {'success': True, 'message': 'Meals Updated'}
        return args

    @http.route('/create_Meals', type='json', auth='user')
    def create_Meals(self, **rec):
        if request.jsonrequest:
            print("rec", rec)
            if rec['name']:
                vals = {
                    'name': rec['name'],
                    'notes': rec['notes']
                }
                new_record = request.env['res.users.meal'].sudo().create(vals)
                print("New Meals Is", new_record)
                args = {'success': True, 'message': 'Success', 'id': new_record.id}
        return args

    @http.route('/get_Meals', type='json', auth='user')
    def get_Meals(self):
        print("Yes here entered")
        record = request.env['res.users.meal'].search([])
        meals = []
        for rec in record:
            vals = {
                'id': rec.id,
                'name': rec.name,
                'meal_date': rec.meal_date,
                'sequence': rec.name_seq,
            }
            meals.append(vals)
        print("Meals List--->", meals)
        data = {'status': 200, 'response': meals, 'message': 'Done All Melas Returned'}
        return data

    # this is code call function by send json in postman
    # {
    #     "jsonrpc": "2.0",
    #     "params":
    #         {
    #             "id": "129",
    #             "name": "DB_Open_Academy ahmed",
    #             "notes": "admin"
    #         }
    # }
    @http.route('/get_Meals_by_Parametrs', type='json', auth='user')
    def get_Meals_by_Parametrs(self, id, name, notes):
        print(id)
        record = request.env['res.users.meal'].sudo().search([('id', '=', id)])
        meals = []
        for rec in record:
            vals = {
                'id': rec.id,
                'name': rec.name,
                'meal_date': rec.meal_date,
                'sequence': rec.name_seq,
            }
            meals.append(vals)
        print("Meals List--->", meals)
        data = {'status': 200, 'response': meals, 'message': 'Done All Melas Returned'}
        return data






