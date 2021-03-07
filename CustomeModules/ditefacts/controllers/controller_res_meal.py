from odoo import http
from odoo.http import request
from odoo.addons.website_sale.controllers.main import WebsiteSale

class WebsiteSale_inherits(WebsiteSale):
    @http.route([
        '''/shop''',
        '''/shop/page/<int:page>''',
        '''/shop/category/<model("product.public.category"):category>''',
        '''/shop/category/<model("product.public.category"):category>/page/<int:page>'''
    ], type='http', auth="public", website=True)
    def shop(self, page=0, category=None, search='', ppg=False, **post):
        res=super(WebsiteSale_inherits, self).shop(page=0, category=None, search='', ppg=False, **post)
        print('ahmed Fahmy shop',res)
        return res

class Ditefacts_Res_Meals(http.Controller):

    @http.route('/Ditefacts/Res_Meals/', website=True, type='http', auth='public')
    def Get_All_Res_Meals(self, **kw):
        Get_Res_Meals=request.env['res.users.meal'].sudo().search([])
        print('Get_All_Res_Meals ')
        return request.render('ditefacts.desing_controller_res_meal', {
            'docs': Get_Res_Meals
        })

    @http.route(['/Ditefacts/Res_Meals/form'], type='http', auth="public", website=True)
    def Res_Meals_form(self, **post):
        Get_res_users = request.env['res.users'].search([])

        return request.render("ditefacts.tmp_res_meal_form", {
            'notes': ' exmple Defulte value Notes',
            'Doc_res_users': Get_res_users
        })
    @http.route(['/Ditefacts/Res_Meals/form/submit'], type='http', auth="public", website=True)
    def Res_Meals_form_submit(self, **post):
        # dic = {
        #     'name': post.get('name'),
        #     'meal_date': post.get('meal_date'),
        #     'notes': post.get('notes')
        # }
        # request.env['res.users.meal'].call_action_from_api(dic)

        #  exmple create 1
        # requst_Res_Meals = request.env['res.users.meal'].create(post)

        # exmple create 2
        requst_Res_Meals = request.env['res.users.meal'].create({
            'name': post.get('name'),
            'meal_date': post.get('meal_date'),
            'notes': post.get('notes')
        })
        vals = {
            'docs': requst_Res_Meals,
        }
        request.env['res.users.meal'].call_action_from_api(vals)
        return request.render("ditefacts.tmp_res_meals_form_success", vals)






