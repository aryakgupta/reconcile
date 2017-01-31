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
    def do_remove_amazon_exisit_order(self, data_lines):
        """
            This method will delete exisitin
        """
        amazon_seller_place_order_obj = self.env['amazon.seller.place.order']
        for data in data_lines:
            order_id = data['Order ID']
            order_date = data['Date']    
            market_place_id =  self.market_place_id.id
            vendor_place_id =  self.vendor_place_id.id  
            amazon_seller_place_order_res = amazon_seller_place_order_obj.search([('order_id','=',order_id),
                                                                                  ('order_date','=',order_date),
                                                                                  ('market_place_id','=',market_place_id),
                                                                                  ('vendor_place_id','=',vendor_place_id)])
            if amazon_seller_place_order_res:
                amazon_seller_place_order_res.unlink()
#             for seller_place_order in seller_place_order_res:
#                 seller_place_order.unlink()        
        return True
            
    @api.multi
    def do_upload_amazon_order(self):
        amazon_seller_place_order_obj = self.env['amazon.seller.place.order']
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
                if data['Date'] and data['Order ID'] and data['SKU'] and data['Transaction type'] and \
                    data['Payment Type'] and data['Payment Detail'] and data['Amount'] and data['Quantity'] and \
                    data['Product Title']:
                    print"KKKKKKKKKKK"
            except:
                raise UserError(_('Selected file format is incorrect. !Please select correct file and try again.'))
        record_count = 0
        self.do_remove_amazon_exisit_order(data_lines)
        for data in data_lines:
            seller_place_order_dic ={}
            seller_place_order_dic['market_place_id'] =  self.market_place_id.id
            seller_place_order_dic['vendor_place_id'] =  self.vendor_place_id.id
            seller_place_order_dic['order_id'] = data['Order ID']
            seller_place_order_dic['sku'] = data['SKU']
            seller_place_order_dic['transaction_type'] = data['Transaction type']
            seller_place_order_dic['payment_type'] = data['Payment Type']
            seller_place_order_dic['payment_detail'] = data['Payment Detail']
            amount = data['Amount'].replace(',','').replace('Rs. ','')
            seller_place_order_dic['amount'] = amount
            seller_place_order_dic['quantity'] = data['Quantity']
            seller_place_order_dic['product_title'] = data['Product Title']
            if data['Date']:
                seller_place_order_dic['order_date'] = data['Date']
            amazon_seller_place_order_obj.create(seller_place_order_dic)
            record_count = record_count + 1
        if record_count:
            text = '%s Orders created successfully.'%record_count
        else:
            text = 'No Record created.'
        partial = message_wiz_obj.create({'text':text}) 
        return{'name':_("Bulk Amazon Seller Order Window"),
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
    def action_upload_amazon_order(self):
        print"action_upload_order>>>>>>>>>>>callled"
        seller_place_config_obj = self.env['seller.place.config']
        auth_res = seller_place_config_obj.get_authentication(self.market_place_id.id, self.vendor_place_id.id, self.password)
        if auth_res:
            res = self.do_upload_amazon_order()
        else:
            raise UserError(_('Credential invalid.!Please contact to Administrator.'))
        return res    
