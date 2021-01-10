# -*- coding: utf-8 -*-
{
    'name': "Text validation for surveys",

    'summary': """
        Allow to create scored text questions in surveys""",

    'description': """
    """,

    'author': "Reem Elfalah",
    'website': "http://www.streamline.com.ly",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'survey'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
