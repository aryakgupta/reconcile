# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Ecommerce Reconcile',
    'version': '1.0',
    'category': 'Sales',
    'sequence': 15,
    'summary': 'Ecommerce Reconcile',
    'description': """
Manage FK Reconcile
==================================

    """,
    'website': 'https://www.odoo.com/page/crm',
    'depends': [],
    'data': [
        'views/seller_config_view.xml',
        'views/seller_reconcile_view.xml',
        'views/amazon_seller_reconcile_view.xml',
        'views/paytm_seller_reconcile_view.xml',
        'views/shopcluse_seller_reconcile_view.xml',
        'wizard/import_order_views.xml',
        'wizard/message_wizard_view.xml',
        'wizard/sale_report_view.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}
