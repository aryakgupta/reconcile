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
    _name = "bulk.order.import"
    _description = "Bulk Order Import"

    file_path = fields.Char('File Path')
    csv_file = fields.Binary('CSV File')
    market_place_id = fields.Many2one('market.place', 'Market Place', required=True)
    vendor_place_id = fields.Many2one('vendor.place', 'Vendor Place', required=True)
    password = fields.Char(string='Password', required=True, copy=False)    
    market_place_type = fields.Selection([
                                ('flipkart', 'Flipkart'),
                                ('amazon', 'Amazon'),
                                ], string='Market Place Type ', required=True, copy=False)    
    
    @api.multi
    def _read_csv_data(self):
        """
            Reads CSV from given path and Return list of dict with Mapping
        """
        print"_read_csv_data>>>>>>>>>>>called"
        data = csv.reader(base64.decodestring(self.csv_file).splitlines())
        fields = data.next()
        print"fields>>>>>>>>",fields
        data_lines = []
        for row in data:
            items = dict(zip(fields, row))
            for key, val in items.iteritems():
                if val in ['Null','null']:
                    items[key] = 0
            data_lines.append(items)
        return fields,data_lines

    @api.multi
    def do_remove_exisit_order(self, data_lines):
        """
            This method will delete exisitin
        """
        seller_place_order_obj = self.env['seller.place.order']
        for data in data_lines:
            order_item_id = data['ORDER ITEM ID']
            order_id = data['Order Id']
            order_date = data['Ordered On']    
            market_place_id =  self.market_place_id.id
            vendor_place_id =  self.vendor_place_id.id  
            seller_place_order_res = seller_place_order_obj.search([('order_id','=',order_id),
                                                                    ('order_item_id','=',order_item_id),
                                                                    ('order_date','=',order_date),
                                                                    ('market_place_id','=',market_place_id),
                                                                    ('vendor_place_id','=',vendor_place_id)])
            if seller_place_order_res:
                seller_place_order_res.unlink()
#             for seller_place_order in seller_place_order_res:
#                 seller_place_order.unlink()        
        return True
            
    @api.multi
    def do_upload_order(self):
        seller_place_order_obj = self.env['seller.place.order']
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
                if data['Ordered On'] and data['Shipment ID'] and data['ORDER ITEM ID'] and data['Order Id'] and \
                    data['Order State'] and data['Order Type'] and data['FSN'] and data['SKU'] and \
                    data['Product'] and data['Invoice No.'] and data['VAT/CST Rate(%)'] and data['Invoice Date (mm/dd/yy)'] and \
                    data['Invoice Amount'] and data['Selling Price Per Item'] and data['Shipping Charge per item'] and data['Quantity'] and \
                    data['Price inc. FKMP Contribution & Subsidy'] and data['Buyer name'] and data['Ship to name'] and data['Address Line 1'] and \
                    data['Address Line 2'] and data['City'] and data['State'] and data['PIN Code'] and \
                    data['Proc SLA'] and data['Dispatch After date'] and data['Dispatch by date'] and data['Form requirement'] and \
                    data['Tracking ID'] and data['Package Length (cm)'] and data['Package Breadth (cm)'] and data['Package Height (cm)'] and \
                    data['Package Weight (kg)']:
                    print"KKKKKKKKKKK"
            except:
                raise UserError(_('Selected file format is incorrect. !Please select correct file and try again.'))
        record_count = 0
        self.do_remove_exisit_order(data_lines)
        for data in data_lines:
            seller_place_order_dic ={}
            seller_place_order_dic['market_place_id'] =  self.market_place_id.id
            seller_place_order_dic['vendor_place_id'] =  self.vendor_place_id.id
            seller_place_order_dic['shipment_id'] = data['Shipment ID']
            seller_place_order_dic['order_item_id'] = data['ORDER ITEM ID']
            seller_place_order_dic['order_id'] = data['Order Id']
            seller_place_order_dic['order_type'] = data['Order Type']
            seller_place_order_dic['sku'] = data['SKU']
            seller_place_order_dic['product'] = data['Product']
            seller_place_order_dic['invoice_no'] = data['Invoice No.']
            seller_place_order_dic['invoice_amount'] = data['Invoice Amount']
            seller_place_order_dic['seller_price_per_item'] = data['Selling Price Per Item']
            seller_place_order_dic['quantity'] = data['Quantity']
            seller_place_order_dic['buyer_name'] = data['Buyer name']
            seller_place_order_dic['ship_to_name'] = data['Ship to name']
            seller_place_order_dic['address_line1'] = data['Address Line 1']
            seller_place_order_dic['address_line2'] = data['Address Line 2']
            seller_place_order_dic['state'] = data['State']
            seller_place_order_dic['pin_code'] = data['PIN Code']
            seller_place_order_dic['tracking_id'] = data['Tracking ID']
            if data['Invoice Date (mm/dd/yy)']:
                seller_place_order_dic['invoice_date'] = data['Invoice Date (mm/dd/yy)']
            if data['Ordered On']:
                seller_place_order_dic['order_date'] = data['Ordered On']
            seller_place_order_obj.create(seller_place_order_dic)
            record_count = record_count + 1
        if record_count:
            text = '%s Orders created successfully.'%record_count
        else:
            text = 'No Record created.'
        partial = message_wiz_obj.create({'text':text}) 
        return{'name':_("Bulk Seller Order Window"),
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
    def action_upload_order(self):
        print"action_upload_order>>>>>>>>>>>callled"
        seller_place_config_obj = self.env['seller.place.config']
        auth_res = seller_place_config_obj.get_authentication(self.market_place_id.id, self.vendor_place_id.id, self.password)
        if auth_res:
            res = self.do_upload_order()
        else:
            raise UserError(_('Credential invalid.!Please contact to Administrator.'))
        return res    

    @api.multi
    def do_remove_exisit_return_delivery(self, data_lines):
        """
            This method will delete exisiting return delivery.
        """
        seller_place_return_delivery_obj = self.env['seller.place.return.delivery']
        for data in data_lines:
            order_item_id = data['ORDER ITEM ID']
            order_id = data['Order Id']
            completed_date = data['Completed Date']  
            seller_place_return_delivery_res = False  
            market_place_id =  self.market_place_id.id
            vendor_place_id =  self.vendor_place_id.id              
            if completed_date:
                seller_place_return_delivery_res = seller_place_return_delivery_obj.search([('order_id','=',order_id),
                                                                                            ('order_item_id','=',order_item_id),
                                                                                            ('completed_date','=',completed_date),
                                                                                            ('market_place_id','=',market_place_id),
                                                                                            ('vendor_place_id','=',vendor_place_id)])
            else:
                seller_place_return_delivery_res = seller_place_return_delivery_obj.search([('order_id','=',order_id),
                                                                                            ('order_item_id','=',order_item_id),
                                                                                            ('market_place_id','=',market_place_id),
                                                                                            ('vendor_place_id','=',vendor_place_id)])
            if seller_place_return_delivery_res:
                seller_place_return_delivery_res.unlink()                
#                 for seller_place_return_delivery in seller_place_return_delivery_res:
#                     seller_place_return_delivery.unlink()        
        return True
    
    @api.multi
    def do_return_delivery(self):
        seller_place_return_delivery_obj = self.env['seller.place.return.delivery']
        message_wiz_obj = self.env['message.wiz']
        print">>>>do_return_delivery called"
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
                if data['Return Approval Date'] and data['Return Requested Date'] and data['Return ID'] and data['Tracking Id'] and \
                    data['Order Id'] and data['ORDER ITEM ID'] and data['Return Type'] and data['Return Sub Type'] and \
                    data['Replacement Order Item ID'] and data['Return Status'] and data['SKU'] and data['FSN'] and \
                    data['Product'] and data['FF Type'] and data['Return Delivery Promise Date'] and data['Picked Up Date'] and \
                    data['Out For Delivery Date'] and data['Completed Date'] and data['Return Reason'] and data['Return Sub-reason'] and \
                    data['Comments'] and data['Buyer Name'] and data['Buyer Address'] and data['Reverse Logistic Form No'] and \
                    data['Forward Logistic Form No'] and data['Total Price'] and data['Quantity'] and data['Good Quantity'] and \
                    data['Bad Quantity'] and data['Vendor Name']:
                    print"KKKKKKKKKKK"
            except:
                raise UserError(_('Selected file format is incorrect. !Please select correct file for returns delivery and try again.'))
        self.do_remove_exisit_return_delivery(data_lines)
        record_count = 0
        for data in data_lines:        
            seller_place_return_delivery_dic ={} 
            if data['Return Approval Date']:
                seller_place_return_delivery_dic['return_approval_date'] = data['Return Approval Date']
            if data['Return Requested Date']:
                seller_place_return_delivery_dic['return_requested_date'] = data['Return Requested Date']
            if data['Return Delivery Promise Date']:
                seller_place_return_delivery_dic['return_delivery_promise_date'] = data['Return Delivery Promise Date']
            if data['Picked Up Date']:
                seller_place_return_delivery_dic['picked_up_date'] = data['Picked Up Date']
            if data['Completed Date']:
                seller_place_return_delivery_dic['completed_date'] = data['Completed Date']
            seller_place_return_delivery_dic['market_place_id'] =  self.market_place_id.id
            seller_place_return_delivery_dic['vendor_place_id'] =  self.vendor_place_id.id                
            seller_place_return_delivery_dic['return_id'] = data['Return ID']
            seller_place_return_delivery_dic['tracking_id'] = data['Tracking Id']
            seller_place_return_delivery_dic['order_item_id'] = data['ORDER ITEM ID']
            seller_place_return_delivery_dic['order_id'] = data['Order Id']
            seller_place_return_delivery_dic['return_type'] = data['Return Type']
            seller_place_return_delivery_dic['return_sub_type'] = data['Return Sub Type']
            seller_place_return_delivery_dic['replacement_order_item_id'] = data['Replacement Order Item ID']
            seller_place_return_delivery_dic['return_status'] = data['Return Status']
            seller_place_return_delivery_dic['return_reason'] = data['Return Reason']
            seller_place_return_delivery_dic['return_subreason'] = data['Return Sub-reason']
            seller_place_return_delivery_dic['comments'] = data['Comments']
            seller_place_return_delivery_dic['sku'] = data['SKU']
            seller_place_return_delivery_dic['product'] = data['Product']
            seller_place_return_delivery_dic['total_price'] = data['Total Price']
            seller_place_return_delivery_dic['quantity'] = data['Quantity']
            seller_place_return_delivery_dic['vendor_name'] = data['Vendor Name']
            seller_place_return_delivery_obj.create(seller_place_return_delivery_dic)
            record_count = record_count + 1
        if record_count:
            text = '%s Returns Delivery created successfully.'%record_count
        else:
            text = 'No Returns Delivery created.'
        partial = message_wiz_obj.create({'text':text}) 
        return{'name':_("Bulk Seller Return Delivery Window"),
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
    def action_return_delivery(self):
        """
            This method is used to create the return delivery.
        """
        print"action_return_delivery>>>>>>>>>>>callled"
        seller_place_config_obj = self.env['seller.place.config']
        auth_res = seller_place_config_obj.get_authentication(self.market_place_id.id, self.vendor_place_id.id, self.password)
        if auth_res:        
            res = self.do_return_delivery()
        else:
            raise UserError(_('Credential invalid.!Please contact to Administrator.'))            
        return res    
    
    @api.multi
    def do_remove_exisit_transaction(self, data_lines):
        """
            This method will delete exisiting return delivery.
        """
        seller_place_transaction_obj = self.env['seller.place.transaction']
        for data in data_lines:
            order_item_id = data['Order item ID']
            order_id = data['Order ID/FSN']
            invoice_date = data['Invoice Date (Invoice to Buyer)']    
            invoice_date = False
            seller_place_transaction_res = False
            market_place_id =  self.market_place_id.id
            vendor_place_id =  self.vendor_place_id.id                 
            if invoice_date:
                seller_place_transaction_res = seller_place_transaction_obj.search([('order_id','=',order_id),
                                                                                    ('order_item_id','=',order_item_id),
                                                                                    ('invoice_date','=',invoice_date),
                                                                                    ('market_place_id','=',market_place_id),
                                                                                    ('vendor_place_id','=',vendor_place_id)])
            else:
                seller_place_transaction_res = seller_place_transaction_obj.search([('order_id','=',order_id),
                                                                                    ('order_item_id','=',order_item_id),
                                                                                    ('market_place_id','=',market_place_id),
                                                                                    ('vendor_place_id','=',vendor_place_id)])                                                                                    
            if seller_place_transaction_res:   
                seller_place_transaction_res.unlink()             
#                 for seller_place_transaction in seller_place_transaction_res:
#                     seller_place_transaction.unlink()        
        return True    

    @api.multi
    def do_upload_transaction(self):
        seller_place_transaction_obj = self.env['seller.place.transaction']
        message_wiz_obj = self.env['message.wiz']
        print">>>>do_return_delivery called"
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
                if data['Settlement Ref No.'] and data['Order Type'] and data['Fulfilment Type'] and data['Seller SKU'] and \
                    data['wsn'] and data['Order ID/FSN'] and data['Settlement Value (Rs.)'] and data['Order item ID'] and \
                    data['Order Date'] and data['Dispatch Date'] and data['Delivery Date'] and data['Cancellation Date'] and \
                    data['Settlement Date'] and data['Order Status'] and data['Quantity'] and data['Order Item Value (Rs.)'] and \
                    data['Sale Transaction Amount (Rs.)'] and data['Discount Transaction Amount'] and data['Refund (Rs.)'] and data['Protection Fund (Rs.)'] and \
                    data['Total Marketplace Fee (Rs.)'] and data['Service Tax (Rs.)'] and data['Sb Cess Tax(Rs.)'] and data['KK Cess Tax(Rs.)'] and \
                    data['Settlement Value (Rs.)'] and data['Commission Rate'] and data['Commission (Rs.)'] and data['Payment Rate'] and \
                    data['Payment Fee'] and data['Fee Discount (Rs.)'] and data['Cancellation Fee (Rs.)'] and data['Fixed Fee  (Rs.)'] and \
                    data['Admonetaisation Fee (Rs.)'] and data['Dead Weight (In Kgs)'] and data['Chargeable Wt. Slab (In Kgs)'] and data['Chargeable Weight Type'] and \
                    data['Volumetric Weight(In Kgs)'] and data['Shipping Fee (Rs.)'] and data['Reverse Shipping  Fee (Rs.)'] and data['Shipping Fee Reversal (Rs.)'] and \
                    data['Shipping Zone'] and data['Token Of Apology'] and data['Pick And Pack Fee'] and data['Storage Fee'] and \
                    data['Removal Fee'] and data['Invoice ID (Invoice to Buyer)'] and data['Invoice Date (Invoice to Buyer)'] and data['Invoice Date (Invoice to Buyer)'] and \
                    data['Invoice Amount (Invoice to Buyer)'] and data['Sub Category'] and data['Total Offer Amount'] and data['My Offer Share'] and \
                    data['Flipkart Offer Share'] and data['Service Cancellation Fee(Rs.)'] and data['NDD Amount'] and data['Ndd Fee'] and \
                    data['SDD Amount'] and data['Sdd Fee'] and data['Sellable Regular Storage Fee'] and data['Unsellable Regular Storage Fee'] and \
                    data['Sellable Longterm 1 Storage Fee'] and data['Unsellable Longterm 1 Storage Fee'] and data['Sellable Longterm 2 Storage Fee'] and data['Unsellable Longterm 2 Storage Fee'] and \
                    data['Is Replacement'] and data['Multi Product'] and data['Profiler Dead Weight'] and data['Seller Dead Weight'] and \
                    data['Customer Shipping Amount'] and data['Customer Shipping Fee'] and data['Payment Mode Changed']:
                    print"KKKKKKKKKKK"
            except:
                raise UserError(_('Selected file format is incorrect. !Please select correct file for Transaction and try again.'))
        self.do_remove_exisit_transaction(data_lines)
        record_count = 0
        for data in data_lines:        
            seller_place_transaction_dic ={} 
            seller_place_transaction_dic['market_place_id'] =  self.market_place_id.id
            seller_place_transaction_dic['vendor_place_id'] =  self.vendor_place_id.id             
            seller_place_transaction_dic['settlement_ref_no'] = data['Settlement Ref No.']
            seller_place_transaction_dic['order_type'] = data['Order Type']
            seller_place_transaction_dic['sku'] = data['Seller SKU']
            seller_place_transaction_dic['order_id'] = data['Order ID/FSN']
            seller_place_transaction_dic['order_item_id'] = data['Order item ID']
            seller_place_transaction_dic['settlement_value'] = data['Settlement Value (Rs.)']
            if data['Order Date']:
                seller_place_transaction_dic['order_date'] = data['Order Date']
            if data['Dispatch Date']:
                seller_place_transaction_dic['dispatch_date'] = data['Dispatch Date']
            if data['Delivery Date']:
                seller_place_transaction_dic['delivery_date'] = data['Delivery Date']
            if data['Settlement Date']:
                seller_place_transaction_dic['settlement_date'] = data['Settlement Date']
            if data['Invoice Date (Invoice to Buyer)']:
                seller_place_transaction_dic['invoice_date'] = data['Invoice Date (Invoice to Buyer)']
            seller_place_transaction_dic['order_status'] = data['Order Status']
            seller_place_transaction_dic['quantity'] = data['Quantity'] or 0.0
            seller_place_transaction_dic['order_item_value'] = data['Order Item Value (Rs.)'] or 0.0
            seller_place_transaction_dic['sale_transaction_amount'] = data['Sale Transaction Amount (Rs.)'] or 0.0
            seller_place_transaction_dic['discount_transaction_amount'] = data['Discount Transaction Amount'] or 0.0
            seller_place_transaction_dic['refund'] = data['Refund (Rs.)'] or 0.0
            seller_place_transaction_dic['protection_fund'] = data['Protection Fund (Rs.)'] or 0.0
            seller_place_transaction_dic['total_marketplace_fee'] = data['Total Marketplace Fee (Rs.)'] or 0.0
            seller_place_transaction_dic['service_tax'] = data['Service Tax (Rs.)'] or 0.0
            seller_place_transaction_dic['sb_cess_tax'] = data['Sb Cess Tax(Rs.)'] or 0.0
            seller_place_transaction_dic['kk_cess_tax'] = data['KK Cess Tax(Rs.)'] or 0.0
            seller_place_transaction_dic['settlement_value'] = data['Settlement Value (Rs.)'] or 0.0
            seller_place_transaction_dic['commission_rate'] = data['Commission Rate'] or 0.0
            seller_place_transaction_dic['commission'] = data['Commission (Rs.)'] or 0.0
            if data['Payment Rate']:
                seller_place_transaction_dic['payment_rate'] = data['Payment Rate'] or 0.0
            seller_place_transaction_dic['payment_fee'] = data['Payment Fee'] or 0.0
            seller_place_transaction_dic['fee_discount'] = data['Fee Discount (Rs.)'] or 0.0
            if data['Cancellation Fee (Rs.)']:
                seller_place_transaction_dic['cancellation_fee'] = data['Cancellation Fee (Rs.)'] or 0.0
            seller_place_transaction_dic['fixed_fee'] = data['Fixed Fee  (Rs.)'] or 0.0
            seller_place_transaction_dic['admonetaisation_fee'] = data['Admonetaisation Fee (Rs.)'] or 0.0
            seller_place_transaction_dic['shipping_fee'] = data['Shipping Fee (Rs.)'] or 0.0
            seller_place_transaction_dic['reverse_shipping_fee'] = data['Reverse Shipping  Fee (Rs.)'] or 0.0
            seller_place_transaction_dic['shipping_fee_reversal'] = data['Shipping Fee Reversal (Rs.)'] or 0.0
            seller_place_transaction_dic['invoice_amount'] = data['Invoice Amount (Invoice to Buyer)'] or 0.0
            seller_place_transaction_dic['invoice_id'] = data['Invoice ID (Invoice to Buyer)']
            seller_place_transaction_dic['dead_weight'] = data['Dead Weight (In Kgs)']
            seller_place_transaction_dic['volumetric_weight'] = data['Volumetric Weight(In Kgs)']
            
            print">>>>>>>>>>>dic",seller_place_transaction_dic                        
            seller_place_transaction_obj.create(seller_place_transaction_dic)
            record_count = record_count + 1
        if record_count:
            text = '%s Transaction created successfully.'%record_count
        else:
            text = 'No Transaction created.'
        partial = message_wiz_obj.create({'text':text}) 
        return{'name':_("Bulk Seller Transaction Window"),
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
    def action_upload_transaction(self):
        """
            This method is used to upload the transaction.
        """
        print"action_return_delivery>>>>>>>>>>>called"
        seller_place_config_obj = self.env['seller.place.config']
        auth_res = seller_place_config_obj.get_authentication(self.market_place_id.id, self.vendor_place_id.id, self.password)
        if auth_res:
            res = self.do_upload_transaction()
        else:
            raise UserError(_('Credential invalid.!Please contact to Administrator.'))            
        return res