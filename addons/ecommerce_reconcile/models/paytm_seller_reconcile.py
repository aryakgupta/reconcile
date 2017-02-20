# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from itertools import groupby
from datetime import datetime, timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.misc import formatLang

import odoo.addons.decimal_precision as dp



class PaytmSellerPlaceOrder(models.Model):
    _name = "paytm.seller.place.order"
    _description = "Paytm Seller Place Order"
    _order = 'id desc'

    _rec_name = 'order_id'
    
    market_place_id = fields.Many2one('market.place', 'Market Place')
    vendor_place_id = fields.Many2one('vendor.place', 'Vendor Place')
    order_date = fields.Date('Date')
    order_id = fields.Char('Order Id')
    item_id = fields.Char('Item Id')
    item_name = fields.Char('Item Name')
    merchant_id = fields.Char('Merchant Id')
    item_sku = fields.Char('Item SKU')
    item_product_id = fields.Char('Item Product ID')
    item_status = fields.Char('item status')
    updation_date = fields.Date('Updation Date')
    item_mrp = fields.Float('Item MRP')
    item_price = fields.Float('Item Price')
    quantity = fields.Float('Quantity')
    shipping_amount = fields.Float('Shipping Amount')
    estimated_shipping_date = fields.Date('Estimated Shipping Date')
    fulfillment_service_id = fields.Char('Fulfillment Service ID')
    sla_extended = fields.Char('SLA Extended')
    customer_firstname = fields.Char('Customer First Name')
    customer_lastname = fields.Char('Customer Last Name')
    customer_email = fields.Char('Customer Email')
    phone = fields.Char('Phone')
    address = fields.Char('Address')
    city = fields.Char('City')
    state = fields.Char('State')
    pincode = fields.Char('Pincode')
    invoice_id = fields.Char('Invoice ID')
    attributes = fields.Char('Attributes')
    replacement_flag = fields.Char('Replacement Fxlag')
    paytm_warehouse_id = fields.Char('Warehouse ID')
    
    

class PaytmSellerPlacePayment(models.Model):
    _name = "paytm.seller.place.payment"
    _description = "Paytm Seller Place Payment"
    _order = 'id desc'

    _rec_name = 'order_id'
    
    market_place_id = fields.Many2one('market.place', 'Market Place')
    vendor_place_id = fields.Many2one('vendor.place', 'Vendor Place')
    order_date = fields.Date('Date')
    order_id = fields.Char('Order Id')
    order_item_id = fields.Char('Order Item ID')
    return_date = fields.Char('Return Date')
    product_id = fields.Char('Product ID')
    product_name = fields.Char('Product Name')
    merchant_sku = fields.Char('Merchant SKU')
    order_item_status = fields.Char('Order Item Status')
    settlement_date = fields.Date('Settlement Date')
    payment_type = fields.Char('Payment Type')
    payment_status = fields.Char('Payment Status')
    adjustment_reason = fields.Char('Adjustment Reason')
    total_price = fields.Float('Total Price')
    marketplace_commission = fields.Float('Marketplace Commission')
    logistics_charges = fields.Float('Logistics Charges')
    pg_commission = fields.Float('PG Commission')
    penalty = fields.Float('Penalty')
    adjustment_amount = fields.Float('Adjustment Amount')
    adjustment_taxes = fields.Float('Adjustment Taxes')
    net_adjustments = fields.Float('Net Adjustments')
    service_tax = fields.Float('Service Tax')
    payable_amount = fields.Float('Payable Amount')
    payout_wallet = fields.Float('Payout - Wallet')
    payout_pg = fields.Float('Payout - PG')
    payout_cod = fields.Float('Payout - COD')
    wallet_utr = fields.Char('Wallet UTR')
    pg_utr = fields.Char('PG UTR')
    cod_utr = fields.Char('COD UTR')
    operator_reference_number = fields.Char('Operator Reference Number')
        
