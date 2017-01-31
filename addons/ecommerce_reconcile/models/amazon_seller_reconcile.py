# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from itertools import groupby
from datetime import datetime, timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.misc import formatLang

import odoo.addons.decimal_precision as dp



class AmazonSellerPlaceOrder(models.Model):
    _name = "amazon.seller.place.order"
    _description = "Seller Place Order"
    _order = 'id desc'

    _rec_name = 'order_id'
    
    market_place_id = fields.Many2one('market.place', 'Market Place')
    vendor_place_id = fields.Many2one('vendor.place', 'Vendor Place')
    order_date = fields.Date('Date')
    order_id = fields.Char('Order Id')
    sku = fields.Char('SKU')
    transaction_type = fields.Char('Transaction type')
    payment_type = fields.Char('Payment Type')
    payment_detail = fields.Char('Payment Detail')
    amount = fields.Float('Amount')
    quantity = fields.Float('Quantity')
    product_title = fields.Char('Product Title')
    
