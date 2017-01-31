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
from xlrd import open_workbook
import cStringIO
import xlwt
from xlwt import *

_logger = logging.getLogger("Seller Sale Report")


class SellerSaleReport(models.TransientModel):
    _name = "seller.sale.report"
    _description = "seller.sale.report"

    filename = fields.Char('File Name')
    filedata = fields.Binary('CSV File')
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    market_place_id = fields.Many2one('market.place', 'Market Place', required=True)
    vendor_place_id = fields.Many2one('vendor.place', 'Vendor Place', required=True)
    password = fields.Char(string='Password', required=True, copy=False) 
    market_place_type = fields.Selection([
                                ('flipkart', 'Flipkart'),
                                ('amazon', 'Amazon'),
                                ], string='Market Place Type ', required=True,copy=False)         
    

    @api.multi
    def do_seller_sale_report(self):
        """
            This method is used to extract the sale report in CSV format.
        """
        seller_place_order_obj = self.env['seller.place.order']
        seller_place_return_delivery_obj = self.env['seller.place.return.delivery']
        seller_place_transaction_obj = self.env['seller.place.transaction']
        str1="Ordered On"
        str2="Shipment ID"
        str3="Order Id"
        str4="ORDER ITEM ID"
        str5="Order State"
        str6="SKU"
        str7="Product"
        str8="Invoice No."
        str9="Invoice Date"
        str10="Invoice Amount"
        str11="Selling Price Per Item"
        str12="Shipping Charge per item"
        str13="Quantity"
        str14="Buyer name"
        str15="Ship to name"
        str16="State"
        str17="Tracking ID"
        str18="Order Return Delivery"
        str19="TR. Settlement Value (Rs.)"
        str20="TR. Total Settlement Value (Rs.)"
        str21="TR. Order Date"
        str22="TR. Settlement Date"
        str23="TR. Order Status"
        str24="TR. Dead Weight (In Kgs)"
        str25="TR. Volumetric Weight(In Kgs)"
        str26="TR. Shipping Fee (Rs.)"
        str27="TR. Total Shipping Fee (Rs.)"
        str28="TR. Reverse Shipping  Fee (Rs.)"
        str29="TR. Total Reverse Shipping  Fee (Rs.)"
        str30="TR. Invoice"
        str31="TR. Transaction No."
        list=[]
        seller_place_order_res = seller_place_order_obj.search([('order_date','>=',self.start_date),
                                                                ('order_date','<=',self.end_date)])
        print"seller_place_order_res>>>>>>>",seller_place_order_res
        
        
        fl = cStringIO.StringIO()
        workbook = xlwt.Workbook()#xlsxwriter.Workbook()
        worksheet = workbook.add_sheet('New Sheet',cell_overwrite_ok=True)
        
        font = xlwt.Font()
        font.bold = True
        bold_style = xlwt.XFStyle()
        bold_style.font = font
        style = xlwt.easyxf('font: bold 1, color red;')
        back_color = xlwt.easyxf('pattern: back_colour yellow')
        
        """pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_back_colour = xlwt.Style.colour_map['yellow']
        style.pattern = pattern"""
        
        
        """# Add a number format for cells with money.
        money_format = workbook.add_format({'num_format': '$#,##0'})
        
        # Add an Excel date format.
        date_format = workbook.add_format({'num_format': 'mmmm d yyyy'})"""
        style1 = xlwt.easyxf('font: bold 1;pattern: pattern solid, fore_colour green;')#For bold and bg_color
        style2 = xlwt.easyxf('pattern: pattern solid, fore_colour green;')#For bold and bg_color
        yellow_style_bold = xlwt.easyxf('font: bold 1;pattern: pattern solid, fore_colour yellow;')#For bold and bg_color
        yellow_style = xlwt.easyxf('pattern: pattern solid, fore_colour yellow;')#For bold and bg_color
        orange_style_bold = xlwt.easyxf('font: bold 1;pattern: pattern solid, fore_colour orange;')#For bold and bg_color
        orange_style = xlwt.easyxf('pattern: pattern solid, fore_colour orange;')#For bold and bg_color
        pink_style_bold = xlwt.easyxf('font: bold 1;pattern: pattern solid, fore_colour pink;')#For bold and bg_color
        pink_style = xlwt.easyxf('pattern: pattern solid, fore_colour pink;')#For bold and bg_color                        
        worksheet.col(0).width = 500*8
        worksheet.col(1).width = 500*8
        worksheet.col(2).width = 500*20
        worksheet.col(3).width = 500*8
        worksheet.col(4).width = 500*8
        worksheet.col(5).width = 500*8
        worksheet.col(6).width = 500*15
        worksheet.col(7).width = 500*15
        worksheet.col(8).width = 500*15
        worksheet.col(9).width = 500*8
        worksheet.col(10).width = 500*12
        worksheet.col(11).width = 500*8
        worksheet.col(12).width = 500*12
        worksheet.col(13).width = 500*8
        worksheet.col(14).width = 500*8
        worksheet.col(15).width = 500*15
        worksheet.col(16).width = 500*15
        worksheet.col(17).width = 500*8
        worksheet.col(18).width = 500*15
        worksheet.col(19).width = 500*8
        worksheet.col(20).width = 500*12
        worksheet.col(21).width = 500*12
        worksheet.col(22).width = 500*12
        worksheet.col(23).width = 500*12
        worksheet.col(24).width = 500*12
        worksheet.col(25).width = 500*12
        worksheet.col(26).width = 500*8
        worksheet.col(27).width = 500*12
        worksheet.col(28).width = 500*12
        worksheet.col(29).width = 500*12
        worksheet.col(30).width = 500*12
        worksheet.col(31).width = 500*12
        # Write some data headers.
        worksheet.write(0,0, str1,style=bold_style)
        worksheet.write(0,1, str2,style=bold_style)
        worksheet.write(0,2, str3,style=bold_style)
        worksheet.write(0,3, str4,style=bold_style)
        worksheet.write(0,4, str5,style=bold_style)
        worksheet.write(0,5, str6,style=bold_style)
        worksheet.write(0,6, str7,style=bold_style)
        worksheet.write(0,7, str8,style=bold_style)
        worksheet.write(0,8, str9,style=bold_style)
        worksheet.write(0,9, str10,style=bold_style)
        worksheet.write(0,10, str11,style=bold_style)
        worksheet.write(0,11, str12,style=bold_style)
        worksheet.write(0,12, str13,style=yellow_style_bold)
        worksheet.write(0,13, str14,style=bold_style)
        worksheet.write(0,14, str15,style=bold_style)
        worksheet.write(0,15, str16,style=bold_style)
        worksheet.write(0,16, str17,style=bold_style)
        worksheet.write(0,17, str18,style=bold_style)
        worksheet.write(0,18, str19,style=bold_style)
        worksheet.write(0,19, str20,style=orange_style_bold)
        worksheet.write(0,20, str21,style=bold_style)
        worksheet.write(0,21, str22,style=bold_style)
        worksheet.write(0,22, str23,style=bold_style)
        worksheet.write(0,23, str24,style=bold_style)
        worksheet.write(0,24, str25,style=bold_style)
        worksheet.write(0,25, str26,style=pink_style_bold)
        worksheet.write(0,26, str27,style=bold_style)
        worksheet.write(0,27, str28,style=bold_style)
        worksheet.write(0,28, str29,style=bold_style)
        worksheet.write(0,29, str30,style=bold_style)
        worksheet.write(0,30, str31,style=bold_style)
        
        # Some data we want to write to the worksheet.
        """expenses = (
            ['Rent', '2013-01-13', 1000],
            ['Gas',  '2013-01-14',  100],
            ['Food', '2013-01-16',  300],
            ['Gym',  '2013-01-20',   50],
            )"""
        
        for seller_place_order in seller_place_order_res:
            line_data =[]
            order_id = seller_place_order.order_id
            order_item_id = seller_place_order.order_item_id
            line_data.append(seller_place_order.order_date)
            line_data.append(seller_place_order.shipment_id)
            line_data.append(order_id)
            line_data.append(order_item_id)
            line_data.append(seller_place_order.order_state)
            line_data.append(seller_place_order.sku)
            line_data.append(seller_place_order.product)
            line_data.append(seller_place_order.invoice_no)
            line_data.append(seller_place_order.invoice_date)
            line_data.append(seller_place_order.invoice_amount)
            line_data.append(seller_place_order.seller_price_per_item)
            line_data.append(seller_place_order.shipping_charge_per_item)
            line_data.append(seller_place_order.quantity)
            line_data.append(seller_place_order.buyer_name)
            line_data.append(seller_place_order.ship_to_name)
            line_data.append(seller_place_order.state)
            line_data.append(seller_place_order.tracking_id)
            
            seller_place_return_delivery_res = seller_place_return_delivery_obj.search([('order_id','=',order_id),
                                                                                        ('order_item_id','=',order_item_id)])
            if seller_place_return_delivery_res:
                line_data.append(True)
            else:
                line_data.append(False)
            order_item_list = order_item_id.split("'")
            print"order_item_list>>>>>>>>>",order_item_list
            settlement_val = []
            total_settlement_val = 0.0
            order_date = []
            settlement_date = []
            order_status = []
            dead_weight = []
            volumetric_weight = []
            shipping_fee = []
            total_shipping_fee = 0.0
            reverse_shipping_fee = []
            total_everse_shipping_fee = 0.0
            transaction_no = 0
            invoice_id = []             
            if len(order_item_list)==2:
                order_item_str = 'OI:' + str(order_item_list[1])
                seller_place_transaction_res = seller_place_transaction_obj.search([('order_id','=',order_id),
                                                                                    ('order_item_id','=',order_item_str)])

                #product_name = (''.join(prod_name)).strip().rstrip()
                
                for seller_place_transaction in seller_place_transaction_res:
                    settlement_value = seller_place_transaction.settlement_value
                    settlement_val.append(str(settlement_value))
                    total_settlement_val = total_settlement_val + float(settlement_value)
                    order_date.append(str(seller_place_transaction.order_date))
                    settlement_date.append(str(seller_place_transaction.settlement_date))
                    order_status.append(str(seller_place_transaction.order_status))
                    dead_weight.append(str(seller_place_transaction.dead_weight))
                    volumetric_weight.append(str(seller_place_transaction.volumetric_weight))
                    shipping_fee.append(str(seller_place_transaction.shipping_fee))
                    total_shipping_fee = total_shipping_fee + float(seller_place_transaction.shipping_fee)
                    reverse_shipping_fee.append(str(seller_place_transaction.reverse_shipping_fee))
                    total_everse_shipping_fee = total_everse_shipping_fee + float(seller_place_transaction.shipping_fee_reversal)
                    invoice_id.append(seller_place_transaction.invoice_id)
                    transaction_no = transaction_no + 1
            print"settlement_val>>>>",settlement_val
            settlement_val = ('\r\n'.join(settlement_val))
            order_date =  ('\r\n'.join(order_date)).strip().rstrip()
            settlement_date = ('\r\n'.join(settlement_date)).strip().rstrip()
            order_status = ('\r\n'.join(order_status)).strip().rstrip()
            dead_weight = ('\r\n'.join(dead_weight)).strip().rstrip()
            volumetric_weight = ('\r\n'.join(volumetric_weight)).strip().rstrip()
            shipping_fee = ('\r\n'.join(shipping_fee)).strip().rstrip()
            reverse_shipping_fee = ("\r\n".join(reverse_shipping_fee)).strip().rstrip() 
            invoice_id = ("\r\n".join(invoice_id)).strip().rstrip()   
            print"settlement_val>>>>>>",settlement_val
            print"reverse_shipping_fee>>>>>>>>",reverse_shipping_fee                
            line_data.append(settlement_val)
            line_data.append(total_settlement_val)
            line_data.append(order_date)
            line_data.append(settlement_date)
            line_data.append(order_status)
            line_data.append(dead_weight)
            line_data.append(volumetric_weight)
            line_data.append(shipping_fee)
            line_data.append(total_shipping_fee)
            line_data.append(reverse_shipping_fee)
            line_data.append(total_everse_shipping_fee)    
            line_data.append(invoice_id)
            line_data.append(transaction_no)
            list.append(line_data)
        
        
        print"list>>>>>>>>>>>",list
        # Start from the first cell below the headers.
        row = 1
        col = 0        
        for line_data in list:
            print"line_data>>>>>",line_data
            worksheet.write(row, col, line_data[0])  
            worksheet.write(row, col + 1, line_data[1])             
            worksheet.write(row, col + 2, line_data[2])
            worksheet.write(row, col + 3, line_data[3])
            worksheet.write(row, col + 4, line_data[4])
            worksheet.write(row, col + 5, line_data[5])
            worksheet.write(row, col + 6, line_data[6])
            worksheet.write(row, col + 7, line_data[7])
            worksheet.write(row, col + 8, line_data[8])
            worksheet.write(row, col + 9, line_data[9])
            worksheet.write(row, col + 10, line_data[10])
            worksheet.write(row, col + 11, line_data[11])
            worksheet.write(row, col + 12, line_data[12])
            worksheet.write(row, col + 13, line_data[13])
            worksheet.write(row, col + 14, line_data[14])
            worksheet.write(row, col + 15, line_data[15])
            worksheet.write(row, col + 16, line_data[16])
            worksheet.write(row, col + 17, line_data[17])
            worksheet.write(row, col + 18, line_data[18])
            worksheet.write(row, col + 19, line_data[19])
            worksheet.write(row, col + 20, line_data[20])
            worksheet.write(row, col + 21, line_data[21])
            worksheet.write(row, col + 22, line_data[22])
            worksheet.write(row, col + 23, line_data[23])
            worksheet.write(row, col + 24, line_data[24])
            worksheet.write(row, col + 25, line_data[25])
            worksheet.write(row, col + 26, line_data[26])
            worksheet.write(row, col + 27, line_data[27])
            worksheet.write(row, col + 28, line_data[28])
            worksheet.write(row, col + 29, line_data[29])
            worksheet.write(row, col + 30, line_data[30])
            row = row + 1                     
        print "row:::::::",row



        workbook.save(fl)
        fl.seek(0)
        data = fl.read()
        out=base64.encodestring(data)
        
        file_name='SaleReport-'+str(self.start_date) +'_'+str(self.end_date)+'-' +str(self.market_place_id.name.name)+'_'+ str(self.vendor_place_id.name.name) + '.xls'
        self.write({'filedata':out, 'filename':file_name})        
        
        return {
                    'name':'Seller Sale Report',
                    'res_model':'seller.sale.report',
                    'type':'ir.actions.act_window',
                    'view_type':'form',
                    'view_mode':'form',
                    'target':'new',
                    'nodestroy': True,
                    #'context': context,
                    'res_id': self.id,
                    }   
        
              
        return True 
    
    @api.multi
    def action_seller_sale_report(self):
        print"action_upload_order>>>>>>>>>>>callled"
        seller_place_config_obj = self.env['seller.place.config']
        auth_res = seller_place_config_obj.get_authentication(self.market_place_id.id, self.vendor_place_id.id, self.password)
        if auth_res:
            res = self.do_seller_sale_report()
        else:
            raise UserError(_('Credential invalid.!Please contact to Administrator.'))
        return res  
    
    @api.multi
    def do_amazon_seller_sale_report(self):
        """
            This method is used to extract the Amazon sale report in xls format.
        """
        amazon_seller_place_order_obj = self.env['amazon.seller.place.order']
        str1="Date"
        str2="Order ID"
        str3="SKU"
        str4="Transaction type"
        str5="Payment Type"
        str6="Payment Detail"
        str7="Amount"
        str8="Total Amount"
        str9="Quantity"
        str10="Total Quantity"
        str11="Product Title"
        fl = cStringIO.StringIO()
        workbook = xlwt.Workbook()#xlsxwriter.Workbook()
        worksheet = workbook.add_sheet('New Sheet',cell_overwrite_ok=True)
        
        font = xlwt.Font()
        font.bold = True
        bold_style = xlwt.XFStyle()
        bold_style.font = font
        style = xlwt.easyxf('font: bold 1, color red;')
        back_color = xlwt.easyxf('pattern: back_colour yellow')
        
        """pattern = xlwt.Pattern()
        pattern.pattern = xlwt.Pattern.SOLID_PATTERN
        pattern.pattern_back_colour = xlwt.Style.colour_map['yellow']
        style.pattern = pattern"""
        
        
        """# Add a number format for cells with money.
        money_format = workbook.add_format({'num_format': '$#,##0'})
        
        # Add an Excel date format.
        date_format = workbook.add_format({'num_format': 'mmmm d yyyy'})"""
        style1 = xlwt.easyxf('font: bold 1;pattern: pattern solid, fore_colour green;')#For bold and bg_color
        style2 = xlwt.easyxf('pattern: pattern solid, fore_colour green;')#For bold and bg_color
        yellow_style_bold = xlwt.easyxf('font: bold 1;pattern: pattern solid, fore_colour yellow;')#For bold and bg_color
        yellow_style = xlwt.easyxf('pattern: pattern solid, fore_colour yellow;')#For bold and bg_color
        orange_style_bold = xlwt.easyxf('font: bold 1;pattern: pattern solid, fore_colour orange;')#For bold and bg_color
        orange_style = xlwt.easyxf('pattern: pattern solid, fore_colour orange;')#For bold and bg_color
        pink_style_bold = xlwt.easyxf('font: bold 1;pattern: pattern solid, fore_colour pink;')#For bold and bg_color
        pink_style = xlwt.easyxf('pattern: pattern solid, fore_colour pink;')#For bold and bg_color                        
        worksheet.col(0).width = 500*8
        worksheet.col(1).width = 500*8
        worksheet.col(2).width = 500*20
        worksheet.col(3).width = 500*8
        worksheet.col(4).width = 500*8
        worksheet.col(5).width = 500*8
        worksheet.col(6).width = 500*15
        worksheet.col(7).width = 500*15
        worksheet.col(8).width = 500*15
        worksheet.col(9).width = 500*8
        worksheet.col(10).width = 500*12
        # Write some data headers.
        worksheet.write(0,0, str1,style=bold_style)
        worksheet.write(0,1, str2,style=bold_style)
        worksheet.write(0,2, str3,style=bold_style)
        worksheet.write(0,3, str4,style=bold_style)
        worksheet.write(0,4, str5,style=bold_style)
        worksheet.write(0,5, str6,style=bold_style)
        worksheet.write(0,6, str7,style=bold_style)
        worksheet.write(0,7, str8,style=yellow_style_bold)
        worksheet.write(0,8, str9,style=bold_style)
        worksheet.write(0,9, str10,style=orange_style_bold)
        worksheet.write(0,10, str11,style=bold_style)
        
        # Some data we want to write to the worksheet.
        """expenses = (
            ['Rent', '2013-01-13', 1000],
            ['Gas',  '2013-01-14',  100],
            ['Food', '2013-01-16',  300],
            ['Gym',  '2013-01-20',   50],
            )"""
            
        amazon_seller_place_order_res = amazon_seller_place_order_obj.search([('order_date','>=',self.start_date),
                                                                ('order_date','<=',self.end_date)])
        print"amazon_seller_place_order_res>>>>>>>",amazon_seller_place_order_res
                    
        amazon_sale_order_dic ={}
        for amazon_seller_place_order in amazon_seller_place_order_res:
            if amazon_seller_place_order.order_id:
                order_id = amazon_seller_place_order.order_id
                if amazon_sale_order_dic.has_key(order_id):
                    amazon_sale_order_dic[order_id].append(amazon_seller_place_order.id) 
                else:
                    amazon_sale_order_dic[order_id] = [amazon_seller_place_order.id]
        #Prepare final list i.e write in .xls file            
        list=[]
        for amazon_order_key,amazon_order_ids in amazon_sale_order_dic.iteritems():
            line_data =[]
            Date = []
            SKU = []
            Transaction_type = []
            Payment_Type = []
            Payment_Detail = []
            Amount = []
            Total_Amount =0.0
            Quantity =[]
            Total_Quantity = 0.0
            Product_Title = []
            for amazon_order_id in amazon_order_ids:
                amazon_seller_place_order = amazon_seller_place_order_obj.search([('id','=',amazon_order_id)])
                Date.append(amazon_seller_place_order.order_date)
                SKU.append(amazon_seller_place_order.sku)
                Transaction_type.append(amazon_seller_place_order.transaction_type)
                Payment_Type.append(amazon_seller_place_order.payment_type)
                Payment_Detail.append(str(amazon_seller_place_order.payment_detail))
                Amount.append(str(amazon_seller_place_order.amount))
                Total_Amount = Total_Amount + amazon_seller_place_order.amount
                Quantity.append(str(amazon_seller_place_order.quantity))
                Total_Quantity = Total_Quantity + amazon_seller_place_order.quantity
                Product_Title.append(str(amazon_seller_place_order.product_title))
            Date = ('\r\n'.join(Date))
            SKU = ('\r\n'.join(SKU))
            Transaction_type = ('\r\n'.join(Transaction_type))
            Payment_Type = ('\r\n'.join(Payment_Type))
            Payment_Detail = ('\r\n'.join(Payment_Detail))
            print"Amount>>>>..",Amount
            Amount = ('\r\n'.join(Amount))
            Quantity = ('\r\n'.join(Quantity))
            Product_Title = ('\r\n'.join(Product_Title))

            line_data.append(Date)
            line_data.append(amazon_order_key)
            line_data.append(SKU)
            line_data.append(Transaction_type)
            line_data.append(Payment_Type)
            line_data.append(Payment_Detail)
            line_data.append(Amount)
            line_data.append(Total_Amount)
            line_data.append(Quantity)
            line_data.append(Total_Quantity)
            line_data.append(Product_Title)
            
            list.append(line_data)
            
        
        print"list>>>>>>>>>>>",list
        # Start from the first cell below the headers.
        row = 1
        col = 0        
        for line_data in list:
            print"line_data>>>>>",line_data
            print"len of line_data",len(line_data)
            worksheet.write(row, col, line_data[0])  
            worksheet.write(row, col + 1, line_data[1])             
            worksheet.write(row, col + 2, line_data[2])
            worksheet.write(row, col + 3, line_data[3])
            worksheet.write(row, col + 4, line_data[4])
            worksheet.write(row, col + 5, line_data[5])
            worksheet.write(row, col + 6, line_data[6])
            worksheet.write(row, col + 7, line_data[7])
            worksheet.write(row, col + 8, line_data[8])
            worksheet.write(row, col + 9, line_data[9])
            worksheet.write(row, col + 10, line_data[10])
            row = row + 1                     
        print "row:::::::",row

        workbook.save(fl)
        fl.seek(0)
        data = fl.read()
        out=base64.encodestring(data)
        
        file_name='AmazonSaleReport-'+str(self.start_date) +'_'+str(self.end_date)+'-' +str(self.market_place_id.name.name)+'_'+ str(self.vendor_place_id.name.name) + '.xls'
        self.write({'filedata':out, 'filename':file_name})        
        
        return {
                    'name':'Amazon Seller Sale Report',
                    'res_model':'seller.sale.report',
                    'type':'ir.actions.act_window',
                    'view_type':'form',
                    'view_mode':'form',
                    'target':'new',
                    'nodestroy': True,
                    #'context': context,
                    'res_id': self.id,
                    }   
        return True     
    
    @api.multi
    def action_amazon_seller_sale_report(self):
        print"action_seller_amazon_sale_report>>>>>>>>>>>callled"
        seller_place_config_obj = self.env['seller.place.config']
        auth_res = seller_place_config_obj.get_authentication(self.market_place_id.id, self.vendor_place_id.id, self.password)
        if auth_res:
            res = self.do_amazon_seller_sale_report()
        else:
            raise UserError(_('Credential invalid.!Please contact to Administrator.'))
        return res      