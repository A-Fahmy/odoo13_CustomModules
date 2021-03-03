# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class Ditefacts(http.Controller):
    @http.route('/ditefacts/res_meal_onboarding', auth='user', type='json')
    def res_meal_onboarding(self):
        """ Returns the `banner` for the sale onboarding panel.
            It can be empty if the user has closed it or if he doesn't have
            the permission to see it. """

        company = request.env.company
        if not request.env.is_admin() or \
                company.sale_quotation_onboarding_state == 'closed':
            return {}

        return {
            'html': request.env.ref('sale.sale_quotation_onboarding_panel').render({
                'company': company,
                'state': company.get_and_update_sale_quotation_onboarding_state()
            })
        }

    # @http.route('/ditefacts/ditefacts/', auth='public')
    # def index(self, **kw):
    #     return "Hello, world"
    #
    # @http.route('/ditefacts/ditefacts/objects/', auth='public')
    # def list(self, **kw):
    #     return http.request.render('ditefacts.listing', {
    #         'root': '/ditefacts/ditefacts',
    #         'objects': http.request.env['ditefacts.ditefacts'].search([]),
    #     })
    #
    # @http.route('/ditefacts/ditefacts/objects/<model("ditefacts.ditefacts"):obj>/', auth='public')
    # def object(self, obj, **kw):
    #     return http.request.render('ditefacts.object', {
    #         'object': obj
    #     })
