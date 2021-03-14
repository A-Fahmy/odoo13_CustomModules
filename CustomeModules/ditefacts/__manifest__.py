# -*- coding: utf-8 -*-
{
    'name': "ditefacts",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "ahmed Fahmy",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'sale',
    ],
    # always loaded
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'data/data.xml',
        'data/cron.xml',
        'views/views.xml',
        'views/templates.xml',
        'views/dietfacts_saleorder.xml',
        'wizards/upload_product_for_users_meal.xml',
        'views/res_users_meal.xml',
        'views/dietfacts_product.xml',
        'data/mail_template.xml',
        'wizards/create_users_meal.xml',
        'wizards/report_users_meal_bydate.xml',
        'reports/Desing_report_users_meal_bydate.xml',
        'views/dietfacts_nutrient.xml',
        'views/view_controller_res_meal.xml',
        'views/create_res_meal_controller_byCode.xml',
        'reports/report_res_users_meal.xml',
        'reports/report_quotation_inherit.xml',





    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
