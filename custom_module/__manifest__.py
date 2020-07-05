# -*- coding: utf-8 -*-
{
    'name': "CustomModule",

    'summary': """
        This module will be used as base module to edit odoo src code to better fit the business requirment""",

    'description': """
        Inherit : Views - Controllers - Models
        Add functionality if necessary.
        Simple Edit on Views. 
        Website pages.
    """,

    'author': "YasinAbu",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Customisation',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','website','portal','website_slides'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/account_inherit.xml',
        'views/homepage.xml',
        'views/portal_my_home_inherit.xml',
        'views/website_slides_share_inherit.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
