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

class SellerSaleReportPaytm(models.TransientModel):
    _inherit = "seller.sale.report"

    @api.multi
    def do_paytm_seller_sale_report(self):
        """
            This method is used to extract the Paytm sale report in xls format.
        """
        paytm_seller_place_order_obj = self.env['paytm.seller.place.order']
        paytm_seller_place_payment_obj = self.env['paytm.seller.place.payment']
        str1="Date"
        str2="Order ID"
        str3="Item ID"
        str4="Item Name"
        str5="Merchant ID"
        str6="Item Product ID"
        str7="Item Status"
        str8="Item MRP"
        str9="Item Price"
        str10="Quantity"
        str11="Shipping Amount"
        str12="SLAExtended"
        str13="Customer First Name"
        str14="Customer Last Name"
        str15="Customer Email"
        str16="Phone"
        str17="City"
        str18="State"
        str19="Pincode"
        str20="Invoice ID"
        str21="Replacement Flag"
        str22="Warehouse ID"
        str23="Product Name"
        str24="Merchant SKU"
        str25="Order Item Status"
        str26="Settlement Date"
        str27="Payment Type"
        str28="Payment Status"
        str29="Adjustment Reason"
        str30="Total Price"
        str31="Payment Total Price"
        str32="Marketplace Commission"
        str33="Total Marketplace Commission"
        str34="Logistics Charges"
        str35="Total Logistics Charges"
        str36="PG Commission"
        str37="Total PG Commission"
        str38="Penalty"
        str39="Total Penalty"
        str40="Adjustment Amount"
        str41="Total Adjustment Amount"
        str42="Adjustment Taxes"
        str43="Total Adjustment Taxes"
        str44="Net Adjustments"
        str45="Total Net Adjustments"
        str46="Service Tax"
        str47="Total Service Tax"
        str48="Payable Amount"
        str49="Total Payable Amount"
        str50="Payout - Wallet"  
        str51="Total Payout - Wallet" 
        str52="Payout - PG" 
        str53="Total Payout - PG"  
        str54="Payout - COD"  
        str55="Total Payout - COD"  
        str56="Wallet UTR"  
        str57="PG UTR"  
        str58="COD UTR"  
        
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
        
        #This block is used to define column length
        for i in range(0,58):
            worksheet.col(i).width = 500*8
        #This block is use to  Write some data headers.
        for i in range(1,58):
            str_val= 'str'+ str(i)
            str_val = vars()[str_val]
            print"str_val>>>>>>>>",str_val
            if i <= 22:
                worksheet.write(0,i-1, str_val,style=bold_style)       
            else:
                worksheet.write(0,i-1, str_val,style=yellow_style_bold)
                             
        
        # Some data we want to write to the worksheet.
        paytm_seller_place_order_res = paytm_seller_place_order_obj.search([('order_date','>=',self.start_date),
                                                                            ('order_date','<=',self.end_date)])
        print"paytm_seller_place_order_res>>>>>>>",paytm_seller_place_order_res
            
        list =[]        
        for paytm_seller_place_order in paytm_seller_place_order_res:
            line_data =[]
            line_data.append(paytm_seller_place_order.order_date)
            line_data.append(paytm_seller_place_order.order_id)
            line_data.append(paytm_seller_place_order.item_id)
            line_data.append(paytm_seller_place_order.item_name)
            line_data.append(paytm_seller_place_order.merchant_id)
            line_data.append(paytm_seller_place_order.item_product_id)
            line_data.append(paytm_seller_place_order.item_status)
            line_data.append(paytm_seller_place_order.item_mrp)
            line_data.append(paytm_seller_place_order.item_price)
            line_data.append(paytm_seller_place_order.quantity)
            line_data.append(paytm_seller_place_order.shipping_amount)
            line_data.append(paytm_seller_place_order.sla_extended)
            line_data.append(paytm_seller_place_order.customer_firstname)
            line_data.append(paytm_seller_place_order.customer_lastname)
            line_data.append(paytm_seller_place_order.customer_email)
            line_data.append(paytm_seller_place_order.phone)
            line_data.append(paytm_seller_place_order.city)
            line_data.append(paytm_seller_place_order.state)
            line_data.append(paytm_seller_place_order.pincode)
            line_data.append(paytm_seller_place_order.invoice_id)
            line_data.append(paytm_seller_place_order.replacement_flag)
            line_data.append(paytm_seller_place_order.paytm_warehouse_id)


            paytm_seller_place_payment_res = paytm_seller_place_payment_obj.search([('order_id','=',paytm_seller_place_order.order_id),
                                                                                    ('order_item_id','=',paytm_seller_place_order.item_id)])
            
            
            Product_Name = []
            Merchant_SKU = []
            Order_Item_Status = []
            Settlement_Date = []
            Payment_Type = []
            Payment_Status = []
            Adjustment_Reason = []
            Total_Price = []
            Payment_Total_Price = 0.0
            Marketplace_Commission = []
            Total_Marketplace_Commission = 0.0
            Logistics_Charges = []
            Total_Logistics_Charges = 0.0
            PG_Commission = []
            Total_PG_Commission = 0.0
            Penalty = []
            Total_Penalty = 0.0
            Adjustment_Amount = []
            Total_Adjustment_Amount = 0.0
            Adjustment_Taxes =[]
            Total_Adjustment_Taxes = 0.0 
            Net_Adjustments = []
            Total_Net_Adjustments = 0.0
            Service_Tax = []
            Total_Service_Tax = 0.0
            Payable_Amount = []
            Tota_payable_Amount = 0.0
            Payout_Wallet = []
            Total_Payout_Wallet = 0.0
            Payout_PG = []
            Total_Payout_PG = 0.0
            Payout_COD = []
            Total_Payout_COD = 0.0
            Wallet_UTR = []
            PG_UTR = []
            COD_UTR = []
            
            for paytm_seller_place_payment in paytm_seller_place_payment_res:
                Product_Name.append(str(paytm_seller_place_payment.product_name))
                Merchant_SKU.append(str(paytm_seller_place_payment.merchant_sku))
                Order_Item_Status.append(str(paytm_seller_place_payment.order_item_status))
                Settlement_Date.append(str(paytm_seller_place_payment.settlement_date))
                Payment_Type.append(str(paytm_seller_place_payment.payment_type))
                Payment_Status.append(str(paytm_seller_place_payment.payment_status))
                Adjustment_Reason.append(str(paytm_seller_place_payment.adjustment_reason))
                Total_Price.append(str(paytm_seller_place_payment.total_price))
                Payment_Total_Price = Payment_Total_Price + paytm_seller_place_payment.total_price
                Marketplace_Commission.append(str(paytm_seller_place_payment.marketplace_commission))
                Total_Marketplace_Commission = Total_Marketplace_Commission + paytm_seller_place_payment.marketplace_commission
                Logistics_Charges.append(str(paytm_seller_place_payment.logistics_charges))
                Total_Logistics_Charges = Total_Logistics_Charges + paytm_seller_place_payment.logistics_charges
                PG_Commission.append(str(paytm_seller_place_payment.pg_commission))
                Total_PG_Commission = Total_PG_Commission + paytm_seller_place_payment.pg_commission
                Penalty.append(str(paytm_seller_place_payment.penalty))
                Total_Penalty + paytm_seller_place_payment.penalty
                Adjustment_Amount.append(str(paytm_seller_place_payment.adjustment_amount))
                Total_Adjustment_Amount = Total_Adjustment_Amount + paytm_seller_place_payment.adjustment_amount
                Adjustment_Taxes.append(str(paytm_seller_place_payment.adjustment_taxes))
                Total_Adjustment_Taxes = Total_Adjustment_Taxes + paytm_seller_place_payment.adjustment_taxes
                Net_Adjustments.append(str(paytm_seller_place_payment.net_adjustments))
                Total_Net_Adjustments = Total_Net_Adjustments + paytm_seller_place_payment.net_adjustments
                Service_Tax.append(str(paytm_seller_place_payment.service_tax))
                Total_Service_Tax = Total_Service_Tax + paytm_seller_place_payment.service_tax
                Payable_Amount.append(str(paytm_seller_place_payment.payable_amount))
                Tota_payable_Amount = Tota_payable_Amount + paytm_seller_place_payment.payable_amount
                Payout_Wallet.append(str(paytm_seller_place_payment.payout_wallet))
                Total_Payout_Wallet = Total_Payout_Wallet + paytm_seller_place_payment.payout_wallet
                Payout_PG.append(str(paytm_seller_place_payment.payout_pg))
                Total_Payout_PG = Total_Payout_PG + paytm_seller_place_payment.payout_pg                
                Payout_COD.append(str(paytm_seller_place_payment.payout_cod))
                Total_Payout_COD = Total_Payout_COD + paytm_seller_place_payment.payout_cod
                Wallet_UTR.append(str(paytm_seller_place_payment.wallet_utr))
                PG_UTR.append(str(paytm_seller_place_payment.pg_utr))
                COD_UTR.append(str(paytm_seller_place_payment.cod_utr))

            Product_Name = ('\r\n'.join(Product_Name))
            Merchant_SKU = ('\r\n'.join(Merchant_SKU))
            Order_Item_Status = ('\r\n'.join(Order_Item_Status))
            Settlement_Date = ('\r\n'.join(Settlement_Date))
            Payment_Type = ('\r\n'.join(Payment_Type))
            Payment_Status = ('\r\n'.join(Payment_Status))
            Adjustment_Reason = ('\r\n'.join(Adjustment_Reason))
            Total_Price = ('\r\n'.join(Total_Price))
            Marketplace_Commission = ('\r\n'.join(Marketplace_Commission))
            Logistics_Charges = ('\r\n'.join(Logistics_Charges))
            PG_Commission = ('\r\n'.join(PG_Commission))
            Penalty = ('\r\n'.join(Penalty))
            Adjustment_Amount = ('\r\n'.join(Adjustment_Amount))
            Adjustment_Taxes = ('\r\n'.join(Adjustment_Taxes))
            Net_Adjustments = ('\r\n'.join(Net_Adjustments))
            Service_Tax = ('\r\n'.join(Service_Tax))
            Payable_Amount = ('\r\n'.join(Payable_Amount))
            Payout_Wallet = ('\r\n'.join(Payout_Wallet))
            Payout_PG = ('\r\n'.join(Payout_PG))
            Payout_COD = ('\r\n'.join(Payout_COD))
            Wallet_UTR = ('\r\n'.join(Wallet_UTR))
            PG_UTR = ('\r\n'.join(PG_UTR))
            COD_UTR = ('\r\n'.join(COD_UTR))                
 
            line_data.append(Product_Name)
            line_data.append(Merchant_SKU)
            line_data.append(Order_Item_Status)
            line_data.append(Settlement_Date)
            line_data.append(Payment_Type)
            line_data.append(Payment_Status)
            line_data.append(Adjustment_Reason)
            line_data.append(Total_Price)
            line_data.append(Payment_Total_Price)
            line_data.append(Marketplace_Commission)
            line_data.append(Total_Marketplace_Commission)
            line_data.append(Logistics_Charges)
            line_data.append(Total_Logistics_Charges)
            line_data.append(PG_Commission)
            line_data.append(Total_PG_Commission)
            line_data.append(Penalty)
            line_data.append(Total_Penalty)
            line_data.append(Adjustment_Amount)
            line_data.append(Adjustment_Taxes)
            line_data.append(Total_Adjustment_Taxes)
            line_data.append(Total_Adjustment_Amount)
            line_data.append(Net_Adjustments)
            line_data.append(Total_Net_Adjustments)
            line_data.append(Service_Tax)
            line_data.append(Total_Service_Tax)
            line_data.append(Payable_Amount)
            line_data.append(Tota_payable_Amount)
            line_data.append(Payout_Wallet)
            line_data.append(Total_Payout_Wallet)
            line_data.append(Payout_PG)
            line_data.append(Total_Payout_PG)
            line_data.append(Payout_COD)
            line_data.append(Total_Payout_COD)
            line_data.append(Wallet_UTR)
            line_data.append(PG_UTR)
            line_data.append(COD_UTR)
            list.append(line_data)
            
        print"list>>>>>>>>>>>",list
        # Start from the first cell below the headers.
        row = 1
        col = 0        
        for line_data in list:
            i = 0
            print"line_data>>>>>",line_data
            print"len of line_data",len(line_data)
            for line_data_val in line_data:
                worksheet.write(row, col + i, line_data_val)  
                i = i + 1
            row = row + 1                     
        print "row:::::::",row

        workbook.save(fl)
        fl.seek(0)
        data = fl.read()
        out=base64.encodestring(data)
        
        file_name='PaytmSaleReport-'+str(self.start_date) +'_'+str(self.end_date)+'-' +str(self.market_place_id.name.name)+'_'+ str(self.vendor_place_id.name.name) + '.xls'
        self.write({'filedata':out, 'filename':file_name})        
        
        return {
                    'name':'Paytm Seller Sale Report',
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
    def action_paytm_seller_sale_report(self):
        print"action_paytm_seller_sale_report>>>>>>>>>>>called"
        seller_place_config_obj = self.env['seller.place.config']
        auth_res = seller_place_config_obj.get_authentication(self.market_place_id.id, self.vendor_place_id.id, self.password)
        if auth_res:
            res = self.do_paytm_seller_sale_report()
        else:
            raise UserError(_('Credential invalid.!Please contact to Administrator.'))
        return res 