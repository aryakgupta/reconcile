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
    def do_remove_paytm_exisit_order(self, data_lines):
        """
            This method will delete exisitin
        """
        paytm_seller_place_order_obj = self.env['paytm.seller.place.order']
        for data in data_lines:
            order_id = data['order_id']
            order_date = data['creation date']    
            market_place_id =  self.market_place_id.id
            vendor_place_id =  self.vendor_place_id.id  
            paytm_seller_place_order_res = paytm_seller_place_order_obj.search([('order_id','=',order_id),
                                                                                  ('order_date','=',order_date),
                                                                                  ('market_place_id','=',market_place_id),
                                                                                  ('vendor_place_id','=',vendor_place_id)])
            if paytm_seller_place_order_res:
                paytm_seller_place_order_res.unlink()
        return True
            
    @api.multi
    def do_upload_paytm_order(self):
        paytm_seller_place_order_obj = self.env['paytm.seller.place.order']
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
                if data['item_id'] and data['item_name'] and data['merchant_id'] and data['item.sku'] and \
                    data['item.product_id'] and data['item status'] and data['updation date'] and data['updation time'] and \
                    data['item_mrp'] and data['item_price'] and data['qty'] and data['shipping_amount'] and \
                    data['estimated shipping date'] and data['order_id'] and data['creation date'] and data['creation time'] and \
                    data['fulfillment service id'] and data['SLAextended'] and data['customer_firstname'] and data['customer_lastname'] and \
                    data['customer_email'] and data['phone'] and data['address'] and \
                    data['city'] and data['state'] and data['pincode'] and data['invoice_id'] and \
                    data['attributes'] and data['replacement_flag'] and data['warehouse_id']:
                    print"KKKKKKKKKKK"
            except:
                raise UserError(_('Selected file format is incorrect. !Please select correct file for Paytm order and try again.'))
        record_count = 0
        self.do_remove_paytm_exisit_order(data_lines)
        for data in data_lines:
            seller_place_order_dic ={}
            seller_place_order_dic['market_place_id'] =  self.market_place_id.id
            seller_place_order_dic['vendor_place_id'] =  self.vendor_place_id.id
            seller_place_order_dic['order_id'] = data['order_id']
            seller_place_order_dic['item_id'] = data['item_id']
            seller_place_order_dic['item_name'] = data['item_name']
            seller_place_order_dic['merchant_id'] = data['merchant_id']
            seller_place_order_dic['item_sku'] = data['item.sku']
            seller_place_order_dic['item_product_id'] = data['item.product_id']
            seller_place_order_dic['item_status'] = data['item status']
            if data['updation date']:
                seller_place_order_dic['updation_date'] = data['updation date']
            seller_place_order_dic['item_mrp'] = data['item_mrp']
            seller_place_order_dic['item_price'] = data['item_price']
            seller_place_order_dic['quantity'] = data['qty']
            seller_place_order_dic['shipping_amount'] = data['shipping_amount']
            seller_place_order_dic['estimated_shipping_date'] = data['estimated shipping date']
            if data['creation date']:
                seller_place_order_dic['order_date'] = data['creation date']
            seller_place_order_dic['fulfillment_service_id'] = data['fulfillment service id']
            seller_place_order_dic['sla_extended'] = data['SLAextended']
            seller_place_order_dic['customer_firstname'] = data['customer_firstname']
            seller_place_order_dic['customer_lastname'] = data['customer_lastname']
            seller_place_order_dic['customer_email'] = data['customer_email']
            seller_place_order_dic['phone'] = data['phone']
            seller_place_order_dic['address'] = data['address']
            seller_place_order_dic['city'] = data['city']
            seller_place_order_dic['state'] = data['state']
            seller_place_order_dic['pincode'] = data['pincode']
            seller_place_order_dic[''] = data['invoice_id']
            seller_place_order_dic['attributes'] = data['attributes']
            seller_place_order_dic['replacement_flag'] = data['replacement_flag']
            seller_place_order_dic['paytm_warehouse_id'] = data['warehouse_id']
            paytm_seller_place_order_obj.create(seller_place_order_dic)
            record_count = record_count + 1
        if record_count:
            text = '%s Orders created successfully.'%record_count
        else:
            text = 'No Record created.'
        partial = message_wiz_obj.create({'text':text}) 
        return{'name':_("Bulk Paytm Seller Order Window"),
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
    def action_upload_paytm_order(self):
        print"action_upload_paytm_order>>>>>>>>>>>callled"
        seller_place_config_obj = self.env['seller.place.config']
        auth_res = seller_place_config_obj.get_authentication(self.market_place_id.id, self.vendor_place_id.id, self.password)
        if auth_res:
            res = self.do_upload_paytm_order()
        else:
            raise UserError(_('Credential invalid.!Please contact to Administrator.'))
        return res    


    @api.multi
    def do_remove_paytm_exisit_payment(self, data_lines):
        """
            This method will delete existing payment data.
        """
        paytm_seller_place_payment_obj = self.env['paytm.seller.place.payment']
        for data in data_lines:
            order_id = data['Order ID']
            order_date = data['Order Creation Date']    
            market_place_id =  self.market_place_id.id
            vendor_place_id =  self.vendor_place_id.id  
            paytm_seller_place_payment_res = paytm_seller_place_payment_obj.search([('order_id','=',order_id),
                                                                                  ('order_date','=',order_date),
                                                                                  ('market_place_id','=',market_place_id),
                                                                                  ('vendor_place_id','=',vendor_place_id)])
            if paytm_seller_place_payment_res:
                paytm_seller_place_payment_res.unlink()
#             for seller_place_order in seller_place_order_res:
#                 seller_place_order.unlink()        
        return True
            
    @api.multi
    def do_upload_paytm_payment(self):
        paytm_seller_place_payment_obj = self.env['paytm.seller.place.payment']
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
                if data['Order ID'] and data['Order Item ID'] and data['Order Creation Date'] and data['Return Date'] and \
                    data['Product ID'] and data['Product Name'] and data['Merchant SKU'] and data['Order Item Status'] and \
                    data['Settlement Date'] and data['Payment Type'] and data['Payment Status'] and data['Adjustment Reason'] and \
                    data['Total Price'] and data['Marketplace Commission'] and data['Logistics Charges'] and data['PG Commission'] and \
                    data['Penalty'] and data['Adjustment Amount'] and data['Adjustment Taxes'] and data['Net Adjustments'] and \
                    data['Service Tax'] and data['Payable Amount'] and data['Payout - Wallet'] and data['Payout - PG'] and \
                    data['Payout - COD'] and data['Wallet UTR'] and data['PG UTR'] and data['COD UTR'] and data['Operator Reference Number']:
                    print"KKKKKKKKKKK"
            except:
                raise UserError(_('Selected file format is incorrect. !Please select correct file format for paytm payment sheet and try again.'))
        record_count = 0
        self.do_remove_paytm_exisit_payment(data_lines)
        for data in data_lines:
            seller_place_payment_dic ={}
            seller_place_payment_dic['market_place_id'] =  self.market_place_id.id
            seller_place_payment_dic['vendor_place_id'] =  self.vendor_place_id.id
            seller_place_payment_dic['order_id'] = data['Order ID']
            seller_place_payment_dic['order_item_id'] = data['Order Item ID']
            if data['Order Creation Date']:
                seller_place_payment_dic['order_date'] = data['Order Creation Date']            
            if data['Return Date']:
                print"data['Return Date']>>>>>>>>>>>>>>>>",data['Return Date']
                seller_place_payment_dic['return_date'] = data['Return Date']
            seller_place_payment_dic['product_id'] = data['Product ID']
            seller_place_payment_dic['product_name'] = data['Product Name']
            seller_place_payment_dic['merchant_sku'] = data['Merchant SKU']
            seller_place_payment_dic['order_item_status'] = data['Order Item Status']
            if data['Settlement Date']:
                seller_place_payment_dic['settlement_date'] = data['Settlement Date']
            seller_place_payment_dic['payment_type'] = data['Payment Type']
            seller_place_payment_dic['payment_status'] = data['Payment Status']
            seller_place_payment_dic['adjustment_reason'] = data['Adjustment Reason']
            seller_place_payment_dic['total_price'] = data['Total Price']
            seller_place_payment_dic['marketplace_commission'] = data['Marketplace Commission']
            seller_place_payment_dic['logistics_charges'] = data['Logistics Charges']
            seller_place_payment_dic['pg_commission'] = data['PG Commission']
            seller_place_payment_dic['penalty'] = data['Penalty']
            seller_place_payment_dic['adjustment_amount'] = data['Adjustment Amount']
            seller_place_payment_dic['adjustment_taxes'] = data['Adjustment Taxes']
            seller_place_payment_dic['net_adjustments'] = data['Net Adjustments']
            seller_place_payment_dic['service_tax'] = data['Service Tax']
            seller_place_payment_dic['payable_amount'] = data['Payable Amount']
            seller_place_payment_dic['payout_wallet'] = data['Payable Amount']
            seller_place_payment_dic['payout_pg'] = data['Payout - PG']
            seller_place_payment_dic['payout_cod'] = data['Payout - COD']
            seller_place_payment_dic['wallet_utr'] = data['Wallet UTR']
            seller_place_payment_dic['pg_utr'] = data['PG UTR']
            seller_place_payment_dic['cod_utr'] = data['COD UTR']
            seller_place_payment_dic['operator_reference_number'] = data['Operator Reference Number']
            paytm_seller_place_payment_obj.create(seller_place_payment_dic)
            record_count = record_count + 1
        if record_count:
            text = '%s Orders created successfully.'%record_count
        else:
            text = 'No Record created.'
        partial = message_wiz_obj.create({'text':text}) 
        return{'name':_("Bulk Paytm Seller Payment Window"),
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
    def action_upload_paytm_payment(self):
        print"action_upload_paytm_payment>>>>>>>>>>>callled"
        seller_place_config_obj = self.env['seller.place.config']
        auth_res = seller_place_config_obj.get_authentication(self.market_place_id.id, self.vendor_place_id.id, self.password)
        if auth_res:
            res = self.do_upload_paytm_payment()
        else:
            raise UserError(_('Credential invalid.!Please contact to Administrator.'))
        return res    