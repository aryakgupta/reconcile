# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from itertools import groupby
from datetime import datetime, timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.misc import formatLang

import odoo.addons.decimal_precision as dp


class SellerPlaceOrder(models.Model):
    _name = "seller.place.order"
    _description = "Seller Place Order"
    _order = 'id desc'

    _rec_name = 'order_id'
    
    market_place_id = fields.Many2one('market.place', 'Market Place')
    vendor_place_id = fields.Many2one('vendor.place', 'Vendor Place')
    shipment_id = fields.Char('Shipment ID')
    order_item_id = fields.Char('ORDER ITEM ID')
    order_id = fields.Char('Order Id')
    order_state = fields.Char('Order State')
    order_type = fields.Char('Order Type')
    sku = fields.Char('SKU')
    product = fields.Char('Product')
    invoice_no = fields.Char('Invoice No')
    invoice_date = fields.Date('Invoice Date')
    invoice_amount = fields.Float('Invoice Amount')
    seller_price_per_item = fields.Float('Seller Price Item')
    shipping_charge_per_item = fields.Float('Shipping Charge Per Item')
    quantity = fields.Float('Quantity')
    buyer_name = fields.Char('Buyer Name')
    ship_to_name = fields.Char('Ship To Name')
    address_line1 = fields.Char('Address Line1')
    address_line2 = fields.Char('Address Line2')
    state = fields.Char('State')
    pin_code = fields.Char('Pin Code')
    tracking_id = fields.Char('Tracking ID')
    
    order_date = fields.Date('Order Date')
    delivery_return_count = fields.Integer(string='Return Delivery', compute='_compute_delivery_return_count_ids')
    transaction_count = fields.Integer(string='Transaction', compute='_compute_transaction_count')    
    

    @api.multi
    def _compute_delivery_return_count_ids(self):
        seller_place_return_delivery_obj = self.env['seller.place.return.delivery']
        for order in self:
            seller_place_return_delivery_res = self.env['seller.place.return.delivery'].search([('order_id','=',order.order_id),
                                                                                                ('order_item_id','=',order.order_item_id),
                                                                                                ('market_place_id','=',order.market_place_id and order.market_place_id.id),
                                                                                                ('vendor_place_id','=',order.vendor_place_id and order.vendor_place_id.id)])
            print"seller_place_return_delivery_res>>>>>>>>>",len(seller_place_return_delivery_res)
            order.delivery_return_count = len(seller_place_return_delivery_res)

    @api.multi
    def _compute_transaction_count(self):
        seller_place_transaction_obj = self.env['seller.place.transaction']
        for order in self:
            order_item_str = False
            order_item_list = str(order.order_item_id).split("'")
            if len(order_item_list)==2:
                order_item_str = 'OI:' + str(order_item_list[1])
            if order_item_str:
                seller_place_transaction_res = self.env['seller.place.transaction'].search([('order_id','=',order.order_id),
                                                                                            ('market_place_id','=',order.market_place_id and self.market_place_id.id),
                                                                                            ('vendor_place_id','=',order.vendor_place_id and self.vendor_place_id.id),
                                                                                            ('order_item_id','=',order_item_str)])
            else:
                seller_place_transaction_res = self.env['seller.place.transaction'].search([('order_id','=',order.order_id),
                                                                                            ('market_place_id','=',order.market_place_id and self.market_place_id.id),
                                                                                            ('vendor_place_id','=',order.vendor_place_id and self.vendor_place_id.id)])            
            print"_compute_transaction_count>>>>>>>>>",len(seller_place_transaction_res)
            order.transaction_count = len(seller_place_transaction_res)                    

    @api.multi
    def action_view_return_delivery(self):
        '''
        This function returns an action that display existing delivery orders
        of given sales order ids. It can either be a in a list or in a form
        view, if there is only one delivery order to show.
        '''
        action = self.env.ref('ecommerce_reconcile.action_seller_place_return_delivery').read()[0]

        
        seller_place_return_delivery_res = self.env['seller.place.return.delivery'].search([('order_id','=',self.order_id),
                                                                                            ('order_item_id','=',self.order_item_id),
                                                                                            ('market_place_id','=',self.market_place_id and self.market_place_id.id),
                                                                                            ('vendor_place_id','=',self.vendor_place_id and self.vendor_place_id.id)])                                                                                            
        seller_place_return_delivery_ids =[]
        for seller_place_return_delivery in seller_place_return_delivery_res:
            seller_place_return_delivery_ids.append(seller_place_return_delivery.id)
        if seller_place_return_delivery_ids:
            print "seller_place_return_delivery_ids::::::>>>>>>>>>>",seller_place_return_delivery_ids
            if len(seller_place_return_delivery_res):
                action['domain'] = [('id', 'in', seller_place_return_delivery_ids)]
                action['context'] = {}
            return action        
        return True

    @api.multi
    def action_view_transaction(self):
        '''
        '''
        order_item_str = False
        order_item_list = str(self.order_item_id).split("'")
        if len(order_item_list)==2:
            order_item_str = 'OI:' + str(order_item_list[1])
        if order_item_str:
            seller_place_transaction_res = self.env['seller.place.transaction'].search([('order_id','=',self.order_id),
                                                                                        ('market_place_id','=',self.market_place_id and self.market_place_id.id),
                                                                                        ('vendor_place_id','=',self.vendor_place_id and self.vendor_place_id.id),
                                                                                        ('order_item_id','=',order_item_str)])
        else:
            seller_place_transaction_res = self.env['seller.place.transaction'].search([('order_id','=',self.order_id),
                                                                                        ('market_place_id','=',self.market_place_id and self.market_place_id.id),
                                                                                        ('vendor_place_id','=',self.vendor_place_id and self.vendor_place_id.id)])
            
        action = self.env.ref('ecommerce_reconcile.action_seller_place_transaction').read()[0]
        seller_place_transaction_ids = []
        for seller_place_transaction in seller_place_transaction_res:
            seller_place_transaction_ids.append(seller_place_transaction.id)
        print"seller_place_transaction_ids>>>>>>>>>",seller_place_transaction_ids
        if len(seller_place_transaction_ids) >=1:
            action['domain'] = [('id', 'in', seller_place_transaction_ids)]
            action['context'] = {}
            print"action>>>>>>",action
            return action
        return True
        
class SellerPlaceReturn(models.Model):
    _name = "seller.place.return.delivery"
    _description = "Seller Place Return Delivery"
    _order = 'id desc'

    _rec_name = 'order_id'
    
    market_place_id = fields.Many2one('market.place', 'Market Place')
    vendor_place_id = fields.Many2one('vendor.place', 'Vendor Place')
    return_approval_date = fields.Date('Return Approval Date')
    return_requested_date = fields.Date('Return Requested Date')
    return_delivery_promise_date = fields.Date('Return Delivery Promise Date')
    picked_up_date = fields.Date('Picked Up Date')
    completed_date = fields.Date('Completed Date')
    return_id = fields.Char('Return ID')
    tracking_id = fields.Char('Tracking ID')
    order_item_id = fields.Char('ORDER ITEM ID')
    order_id = fields.Char('Order Id')    
    return_type = fields.Char('Return Type')
    return_sub_type = fields.Char('Return Type')
    replacement_order_item_id = fields.Char('Replacement Order Item ID')
    return_status = fields.Char('Return Status')
    return_reason = fields.Char('Return Reason')
    return_subreason = fields.Char('Return Sub-reason')
    comments = fields.Char('Comments')
    sku = fields.Char('SKU')
    product = fields.Char('Product')
    total_price = fields.Float('Total Price')
    quantity = fields.Float('Quantity')
    vendor_name = fields.Char('Vendor Name')
    
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('de-active', 'De-Active'),
        ], string='Status', readonly=True, copy=False, default='draft')
    
class SellerPlaceTransaction(models.Model):
    _name = "seller.place.transaction"
    _description = "Seller Place Return Delivery"
    _order = 'id desc'

    _rec_name = 'order_id'
    
    market_place_id = fields.Many2one('market.place', 'Market Place')
    vendor_place_id = fields.Many2one('vendor.place', 'Vendor Place')
    settlement_ref_no = fields.Char('Settlement Ref No.')
    order_type = fields.Char('Order Type')
    sku = fields.Char('SKU')
    order_id = fields.Char('Order Id')
    order_item_id = fields.Char('ORDER ITEM ID')
    settlement_value = fields.Float('Settlement Value')
    order_date = fields.Date('Order Date')    
    dispatch_date = fields.Date('Dispatch Date')    
    delivery_date = fields.Date('Delivery Date')
    settlement_date = fields.Date('Settlement Date')    
    order_status = fields.Char('Order Status')
    quantity = fields.Float('Quantity')
    order_item_value = fields.Float('Order Item Value')
    sale_transaction_amount = fields.Float('Sale Transaction Amount')
    discount_transaction_amount = fields.Float('Discount Transaction Amount')
    refund = fields.Float('Refund')
    protection_fund = fields.Float('Protection Fund')
    total_marketplace_fee = fields.Float('Total Marketplace Fee')
    service_tax = fields.Float('Service Tax')
    sb_cess_tax = fields.Float('Sb Cess Tax')
    kk_cess_tax = fields.Float('KK Cess Tax')
    settlement_value = fields.Float('Settlement Value')
    commission_rate = fields.Char('Commission Rate')
    commission = fields.Float('Commission')
    payment_rate = fields.Char('Payment Rate')
    payment_fee = fields.Float('Payment Fee')
    fee_discount = fields.Float('Fee Discount')
    cancellation_fee = fields.Float('Cancellation Fee')
    fixed_fee = fields.Float('Fixed Fee')
    admonetaisation_fee = fields.Float('Admonetaisation Fee')
    shipping_fee = fields.Float('Shipping Fee')
    reverse_shipping_fee = fields.Float('Reverse Shipping Fee')
    shipping_fee_reversal = fields.Float('Shipping Fee Reversal')
    invoice_amount = fields.Float('Invoice Amount (Invoice to Buyer)')
    invoice_id = fields.Char('Invoice ID')
    invoice_date = fields.Date('Invoice Date (Invoice to Buyer)')
    dead_weight = fields.Char('Dead Weight (In Kgs)')
    volumetric_weight = fields.Char('Volumetric Weight(In Kgs)')
    
    order_count = fields.Integer(string='Orders', compute='_compute_order_count')    
    
    @api.multi
    def _compute_order_count(self):
        seller_place_order_obj = self.env['seller.place.order']
        for order in self:
            order_item_str = False
            order_item_list = str(order.order_item_id).split("OI:")
            if len(order_item_list)==2:
                order_item_str = "'" + str(order_item_list[1])
            if order_item_str:
                seller_place_order_res = seller_place_order_obj.search([('order_id','=',order.order_id),
                                                                              ('market_place_id','=',order.market_place_id and order.market_place_id.id),
                                                                              ('vendor_place_id','=',order.vendor_place_id and order.vendor_place_id.id),
                                                                              ('order_item_id','=',order_item_str)])
            else:
                seller_place_order_res = seller_place_order_obj.search([('order_id','=',order.order_id),
                                                                        ('market_place_id','=',order.market_place_id and order.market_place_id.id),
                                                                        ('vendor_place_id','=',order.vendor_place_id and order.vendor_place_id.id)])            
            print"seller_place_order_res>>>>>>>>>",len(seller_place_order_res)
            order.order_count = len(seller_place_order_res)                    

    @api.multi
    def action_view_order(self):
        '''
        '''
        seller_place_order_obj = self.env['seller.place.order']
        action = self.env.ref('ecommerce_reconcile.action_seller_place_order').read()[0]
        order_item_str = False
        order_item_list = str(self.order_item_id).split("OI:")
        if len(order_item_list)==2:
            order_item_str = "'" + str(order_item_list[1])
        if order_item_str:
            seller_place_order_res = seller_place_order_obj.search([('order_id','=',self.order_id),
                                                                    ('market_place_id','=',self.market_place_id and self.market_place_id.id),
                                                                    ('vendor_place_id','=',self.vendor_place_id and self.vendor_place_id.id),
                                                                    ('order_item_id','=',order_item_str)])
        else:
            seller_place_order_res = seller_place_order_obj.search([('order_id','=',order.order_id),
                                                                    ('market_place_id','=',self.market_place_id and self.market_place_id.id),
                                                                    ('vendor_place_id','=',self.vendor_place_id and self.vendor_place_id.id)])
        
        seller_place_order_ids =[]
        for seller_place_order in seller_place_order_res:
            seller_place_order_ids.append(seller_place_order.id)
        if seller_place_order_ids:
            print "seller_place_order_ids::::::>>>>>>>>>>",seller_place_order_ids
            if len(seller_place_order_ids):
                action['domain'] = [('id', 'in', seller_place_order_ids)]
                action['context'] = {}
            return action        
        return True