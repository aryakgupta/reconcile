# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from itertools import groupby
from datetime import datetime, timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.misc import formatLang

import odoo.addons.decimal_precision as dp



class ShopcluesSellerPlaceOrder(models.Model):
    _name = "shopclues.seller.place.order"
    _description = "Seller Place Order"
    _order = 'id desc'

    _rec_name = 'order_id'
    
    market_place_id = fields.Many2one('market.place', 'Market Place')
    vendor_place_id = fields.Many2one('vendor.place', 'Vendor Place')
    order_date = fields.Date('Date')
    shipment_date = fields.Date('Shipment Date')
    order_id = fields.Char('Order Id')
    sku = fields.Char('SKU')
    order_status = fields.Char('Order Status')
    product_details = fields.Char('Product Details')
    buyer_name = fields.Char('Buyer Name')
    shipping_city = fields.Char('Shipping City')
    shipping_state = fields.Char('Shipping State')
    shipping_pincode = fields.Char('Shipping Pincode')
    quantity = fields.Float('Item Count')
    payment_type = fields.Char('Payment Type')
    payment_details = fields.Char('Payment Details')
    order_subtotal = fields.Float('Order SubTotal')
    collectable_amount = fields.Float('Collectable Amount')
    merchant_sku = fields.Char('Merchant SKU')
    shipment_id = fields.Char('Shipment ID')
    tracking_no = fields.Char('Tracking No')
    carrier_name = fields.Char('Carrier Name')
    merchant_name = fields.Char('Merchant Name')
    merchant_type = fields.Char('Merchant Type')
    merchant_city = fields.Char('Merchant City')
    regular_selling_price = fields.Float('Regular Selling Price')
    total_merchnat_discount_permotions = fields.Float('Total Merchnat discount and permotions')
    invoice_value = fields.Float('Invoice Value')
    shipping_cost = fields.Float('Shipping Cost')
    weight = fields.Char('Weight(Grams)')
    sku_id = fields.Char('SKU ID')
    

class ShopcluesSellerPlacePayment(models.Model):
    _name = "shopclues.seller.place.payment"
    _description = "Shopclues Seller Place Payment"
    _order = 'id desc'

    _rec_name = 'order_id'
    
    market_place_id = fields.Many2one('market.place', 'Market Place')
    vendor_place_id = fields.Many2one('vendor.place', 'Vendor Place')
    order_date = fields.Date('Date')
    order_id = fields.Char('Order Id')
    product_id = fields.Char('Product ID')
    merchant_reference_no  = fields.Char('Merchant Reference No')
    product = fields.Char('Product')
    status = fields.Char('Status')
    billing_type = fields.Char('Billing Type')
    net_payout = fields.Char('Net Payout')
    shipping_cost = fields.Float('Shipping Cost (A)')
    selling_price = fields.Float('Selling Price (B)')
    merchant_Order_total = fields.Float('Merchant Order Total (C=A+B)')
    remote_address_shipping = fields.Char('Remote Address Shipping')
    order_total = fields.Float('Order Total')
    deal_price = fields.Float('Deal Price')
    unit_target_payout = fields.Char('Unit Target Payout(If any)')
    selling_service_fee_before_tax = fields.Float('Selling Service Fee ( Before tax )')
    selling_service_fee_after_tax = fields.Float('Selling Service Fee ( After tax )')
    fullfillment_service_fee_before_tax = fields.Float('Fullfillment Service Fee ( Before tax )')
    fullfillment_service_fee_after_tax = fields.Float('Fullfillment Service Fee (After Tax)')
    total_service_fee = fields.Float('Total Service Fee')
    service_tax_rate = fields.Float('Service Tax Rate')
    tp_selling_fee = fields.Float('TP Selling Fee')
    weight = fields.Float('Weight (in Grams)')
    customer_name = fields.Char('Customer Name')
    state = fields.Char('State')
    invoice = fields.Char('Invoice')