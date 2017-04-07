# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import time

from odoo import api, fields, models, _
import odoo.addons.decimal_precision as dp
from odoo.exceptions import UserError
import csv
import logging
import os
import base64
from odoo.exceptions import UserError


_logger = logging.getLogger("Import Orders")


class OrderImport(models.TransientModel):
    _inherit = "bulk.order.import"

    @api.multi
    def do_remove_shopclues_exisit_order(self, data_lines):
        """
            This method will delete exisitin
        """
        shopcluse_seller_place_order_obj = self.env['shopclues.seller.place.order']
        for data in data_lines:
            order_id = data['Order No.']
            order_date = data['Order Date']    
            market_place_id =  self.market_place_id.id
            vendor_place_id =  self.vendor_place_id.id  
            shopcluse_seller_place_order_res = shopcluse_seller_place_order_obj.search([('order_id','=',order_id),
                                                                                  ('order_date','=',order_date),
                                                                                  ('market_place_id','=',market_place_id),
                                                                                  ('vendor_place_id','=',vendor_place_id)])
            if shopcluse_seller_place_order_res:
                shopcluse_seller_place_order_res.unlink()
        return True
            
    @api.multi
    def do_upload_shopclues_order(self):
        shopcluse_seller_place_order_obj = self.env['shopclues.seller.place.order']
        message_wiz_obj = self.env['message.wiz']
        print">>>>do_upload_order called"
        if not self.csv_file or self.csv_file == "":
            _logger.warning("Import can not be started. Configure your .csv file path.")
            raise UserError(_('!Please select file.'))
            return True
        fields = data_lines = False
        try:
            fields, data_lines = self._read_csv_data()
        except:
            _logger.warning("Can not read source file(csv) '%s', Invalid file path or File not reachable on file system."%(self.csv_file))
            return True            
        if not data_lines:
            _logger.info("File '%s' has not data or it has been already imported, please update the file."%(csv_file))
            return True
        #_logger.info("Starting update Product Process from file '%s'."%(csv_file))
        print"data_lines>>>>>>",data_lines  
        for data in data_lines:
            try:
                if data['Order No.'] and data['Order Date'] and data['Order Time'] and data['Occasion'] and \
                    data['Priority Level'] and data['Order Status'] and data['Product Details'] and data['Product Options'] and \
                    data['Buyer Name'] and data['Shipping Address'] and data['Shipping City'] and data['Shipping State'] and \
                    data['Shipping Pincode'] and data['Item Count'] and data['Payment Type'] and data['Payment Details'] and \
                    data['Order SubTotal'] and data['Collectible Amount'] and data['Merchant SKU'] and data['Shipment ID'] and \
                    data['Tracking No'] and data['Carrier Name'] and data['Shipment Date'] and data['Merchant City'] and \
                    data['Merchant Name'] and data['Merchant Type'] and data['Merchant City'] and data['Servicable By'] and \
                    data['Last Cause'] and data['Cause Date'] and data['Notes'] and data['User'] and \
                    data['Last Tag'] and data['Tag Date'] and data['Notes'] and data['User'] and \
                    data['Last Email'] and data['Regular Selling Price'] and data['Total Merchnat discount and permotions'] and \
                    data['InvoiceValue'] and data['Shipping Cost'] and data['Weight(Grams)'] and data['SKU ID']:
                    print"KKKKKKKKKKK"
            except:
                raise UserError(_('Selected file format is incorrect. !Please select correct file for Shopclues order and try again.'))
        record_count = 0
        self.do_remove_shopclues_exisit_order(data_lines)
        for data in data_lines:
            seller_place_order_dic ={}
            seller_place_order_dic['market_place_id'] =  self.market_place_id.id
            seller_place_order_dic['vendor_place_id'] =  self.vendor_place_id.id
            seller_place_order_dic['order_id'] = data['Order No.']
            if data['Order Date']:
                seller_place_order_dic['order_date'] = data['Order Date']
            if data['Shipment Date']:
                shipment_date_data = data['Shipment Date'].split()
                if shipment_date_data:
                    seller_place_order_dic['shipment_date'] = shipment_date_data[0]
            seller_place_order_dic['order_status'] = data['Order Status']
            seller_place_order_dic['product_details'] = data['Product Details']
            seller_place_order_dic['buyer_name'] = data['Buyer Name']
            seller_place_order_dic['shipping_city'] = data['Shipping City']
            seller_place_order_dic['shipping_state'] = data['Shipping State']
            seller_place_order_dic['shipping_pincode'] = data['Shipping Pincode']
            seller_place_order_dic['quantity'] = data['Item Count']
            seller_place_order_dic['payment_type'] = data['Payment Type']
            seller_place_order_dic['payment_details'] = data['Payment Details']
            seller_place_order_dic['order_subtotal'] = data['Order SubTotal']
            seller_place_order_dic['collectable_amount'] = data['Collectible Amount']
            seller_place_order_dic['merchant_sku'] = data['Merchant SKU']
            seller_place_order_dic['shipment_id'] = data['Shipment ID']
            seller_place_order_dic['tracking_no'] = data['Tracking No']
            seller_place_order_dic['carrier_name'] = data['Carrier Name']
            seller_place_order_dic['merchant_name'] = data['Merchant Name']
            seller_place_order_dic['merchant_type'] = data['Merchant Type']
            seller_place_order_dic['merchant_city'] = data['Merchant City']
            seller_place_order_dic['regular_selling_price'] = data['Regular Selling Price']
            seller_place_order_dic['total_merchnat_discount_permotions'] = data['Total Merchnat discount and permotions']
            seller_place_order_dic['invoice_value'] = data['InvoiceValue']
            seller_place_order_dic['shipping_cost'] = data['Shipping Cost']
            seller_place_order_dic['weight'] = data['Weight(Grams)']
            seller_place_order_dic['sku_id'] = data['SKU ID']
            print"seller_place_order_dic>>>>>>>>.",seller_place_order_dic
            shopcluse_seller_place_order_obj.create(seller_place_order_dic)
            record_count = record_count + 1
        if record_count:
            text = '%s Orders created successfully.'%record_count
        else:
            text = 'No Record created.'
        partial = message_wiz_obj.create({'text':text}) 
        return{'name':_("Bulk Shopclues Seller Order Window"),
                 'view_mode': 'form',
                 'view_id': False,
                 'view_type': 'form',
                 'res_model': 'message.wiz',
                 'res_id': partial.id,
                 'type': 'ir.actions.act_window',
                 'nodestroy': True,
                 'target': 'new',
                 'domain': '[]',
             } 
        return True

                
    @api.multi
    def action_upload_shopclues_order(self):
        print"action_upload_paytm_order>>>>>>>>>>>callled"
        seller_place_config_obj = self.env['seller.place.config']
        auth_res = seller_place_config_obj.get_authentication(self.market_place_id.id, self.vendor_place_id.id, self.password)
        if auth_res:
            res = self.do_upload_shopclues_order()
        else:
            raise UserError(_('Credential invalid.!Please contact to Administrator.'))
        return res    


    @api.multi
    def do_remove_shopclues_exisit_payment(self, data_lines):
        """
            This method will delete existing payment data.
        """
        return True
        shopcluse_seller_place_payment_obj = self.env['shopclues.seller.place.payment']
        for data in data_lines:
            order_id = data['Order ID']
            order_date = data['Order Date']    
            market_place_id =  self.market_place_id.id
            vendor_place_id =  self.vendor_place_id.id  
            shopclues_seller_place_payment_res = shopcluse_seller_place_payment_obj.search([('order_id','=',order_id),
                                                                                  ('order_date','=',order_date),
                                                                                  ('market_place_id','=',market_place_id),
                                                                                  ('vendor_place_id','=',vendor_place_id)])
            if shopclues_seller_place_payment_res:
                shopclues_seller_place_payment_res.unlink()
        return True
            
    @api.multi
    def do_upload_shopclues_payment(self):
        shopcluse_seller_place_payment_obj = self.env['shopclues.seller.place.payment']
        message_wiz_obj = self.env['message.wiz']
        print">>>>do_upload_paytm_payment called"
        if not self.csv_file or self.csv_file == "":
            _logger.warning("Import can not be started. Configure your .csv file path.")
            raise UserError(_('!Please select file.'))
            return True
        fields = data_lines = False
        try:
            fields, data_lines = self._read_csv_data()
        except:
            _logger.warning("Can not read source file(csv) '%s', Invalid file path or File not reachable on file system."%(self.csv_file))
            return True            
        if not data_lines:
            _logger.info("File '%s' has not data or it has been already imported, please update the file."%(csv_file))
            return True
        #_logger.info("Starting update Product Process from file '%s'."%(csv_file))
        print"data_lines>>>>>>",data_lines  
        for data in data_lines:
            try:
                if data['Order ID'] and data['Product ID'] and data['Merchant Reference No'] and data['Product'] and \
                    data['Status'] and data['Billing Type'] and data['Net Payout'] and data['Shipping Cost (A)'] and \
                    data['Selling Price (B)'] and data['Merchant Order Total (C=A+B)'] and data['Remote Address Shipping'] and data['Order Total'] and \
                    data['Deal Price'] and data['Unit Target Payout(If any)'] and data['Selling Service Fee ( Before tax )'] and data['Selling Service Fee ( After tax )'] and \
                    data['Fullfillment Service Fee ( Before tax )'] and data['Fullfillment Service Fee (After Tax)'] and data['Total Service Fee'] and data['Service Tax Rate'] and \
                    data['TP Selling Fee'] and data['Weight (in Grams)'] and data['Order Date'] and data['Customer Name'] and \
                    data['Address'] and data['State'] and data['Billing Cycle'] and data['Invoice']:
                    print"KKKKKKKKKKK"
            except:
                raise UserError(_('Selected file format is incorrect. !Please select correct file format for Shopclues payment sheet and try again.'))
        record_count = 0
        self.do_remove_shopclues_exisit_payment(data_lines)
        for data in data_lines:
            seller_place_payment_dic ={}
            seller_place_payment_dic['market_place_id'] =  self.market_place_id.id
            seller_place_payment_dic['vendor_place_id'] =  self.vendor_place_id.id
            seller_place_payment_dic['order_id'] = data['Order ID']
            if data['Order Date']:
                seller_place_payment_dic['order_date'] = data['Order Date']            
            seller_place_payment_dic['product_id'] = data['Product ID']
            seller_place_payment_dic['merchant_reference_no'] = data['Merchant Reference No']
            seller_place_payment_dic['product'] = data['Product']
            seller_place_payment_dic['status'] = data['Status']
            seller_place_payment_dic['billing_type'] = data['Billing Type']
            seller_place_payment_dic['net_payout'] = data['Net Payout']
            seller_place_payment_dic['shipping_cost'] = data['Shipping Cost (A)']
            seller_place_payment_dic['selling_price'] = data['Selling Price (B)']
            seller_place_payment_dic['merchant_Order_total'] = data['Merchant Order Total (C=A+B)']
            seller_place_payment_dic['remote_address_shipping'] = data['Remote Address Shipping']
            seller_place_payment_dic['order_total'] = data['Order Total']
            seller_place_payment_dic['deal_price'] = data['Deal Price']
            seller_place_payment_dic['unit_target_payout'] = data['Unit Target Payout(If any)']
            seller_place_payment_dic['selling_service_fee_before_tax'] = data['Selling Service Fee ( Before tax )']
            seller_place_payment_dic['selling_service_fee_after_tax'] = data['Selling Service Fee ( After tax )']
            seller_place_payment_dic['fullfillment_service_fee_before_tax'] = data['Fullfillment Service Fee ( Before tax )']
            seller_place_payment_dic['fullfillment_service_fee_after_tax'] = data['Fullfillment Service Fee (After Tax)']
            seller_place_payment_dic['total_service_fee'] = data['Total Service Fee']
            seller_place_payment_dic['service_tax_rate'] = data['Service Tax Rate']
            seller_place_payment_dic['tp_selling_fee'] = data['TP Selling Fee']
            seller_place_payment_dic['weight'] = data['Weight (in Grams)']
            seller_place_payment_dic['customer_name'] = data['Customer Name']
            seller_place_payment_dic['state'] = data['State']
            seller_place_payment_dic['invoice'] = data['Invoice']
            shopcluse_seller_place_payment_obj.create(seller_place_payment_dic)
            record_count = record_count + 1
        if record_count:
            text = '%s Orders created successfully.'%record_count
        else:
            text = 'No Record created.'
        partial = message_wiz_obj.create({'text':text}) 
        return{'name':_("Bulk Shopclues Seller Payment Window"),
                 'view_mode': 'form',
                 'view_id': False,
                 'view_type': 'form',
                 'res_model': 'message.wiz',
                 'res_id': partial.id,
                 'type': 'ir.actions.act_window',
                 'nodestroy': True,
                 'target': 'new',
                 'domain': '[]',
             } 
        return True

                
    @api.multi
    def action_upload_shopclues_payment(self):
        print"action_upload_shopclues_payment>>>>>>>>>>>called"
        seller_place_config_obj = self.env['seller.place.config']
        auth_res = seller_place_config_obj.get_authentication(self.market_place_id.id, self.vendor_place_id.id, self.password)
        if auth_res:
            res = self.do_upload_shopclues_payment()
        else:
            raise UserError(_('Credential invalid.!Please contact to Administrator.'))
        return res    