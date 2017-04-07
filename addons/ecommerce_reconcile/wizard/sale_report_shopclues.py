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

class SellerSaleReportShopclues(models.TransientModel):
    _inherit = "seller.sale.report"

    @api.multi
    def do_shopclues_seller_sale_report(self):
        """
            This method is used to extract the Shopclues sale report in xls format.
        """
        shopclues_seller_place_order_obj = self.env['shopclues.seller.place.order']
        shopclues_seller_place_payment_obj = self.env['shopclues.seller.place.payment']
        str1="Date"
        str2="Shipment Date"
        str3="Order Id"
        str4="SKU"
        str5="Order Status"
        str6="Product Details"
        str7="Buyer Name"
        str8="Shipping City"
        str9="Shipping State"
        str10="Shipping Pincode"
        str11="Item Count/Quantity"
        str12="Payment Type"
        str13="Payment Details"
        str14="Order SubTotal"
        str15="Collectable Amount"
        str16="Merchant SKU"
        str17="Shipment ID"
        str18="Tracking No"
        str19="Carrier Name"
        str20="Merchant Name"
        str21="Merchant Type"
        str22="Merchant City"
        str23="Regular Selling Price"
        str24="Total Merchnat discount and permotions"
        str25="Invoice Value"
        str26="Shipping Cost"
        str27="Weight(Grams)"
        str28="SKU ID"
        #Payment data
        str29="Product ID"
        str30="Merchant Reference No"
        str31="Product"
        str32="Status"
        str33="Billing Type"
        str34="Net Payout"
        str35="Shipping Cost (A)"
        str36="Total Shipping Cost (A)"
        str37="Selling Price (B)"
        str38="Total Selling Price (B)"
        str39="Merchant Order Total (C=A+B)"
        str40="Total Merchant Order Total"
        str41="Remote Address Shipping"
        str42="Order Total"
        str43="Sigma Order Total"
        str44="Deal Price"
        str45="Total Deal Price"
        str46="Unit Target Payout(If any)"
        str47="Selling Service Fee ( Before tax )"
        str48="Total Selling Service Fee ( Before tax )"
        str49="Selling Service Fee ( After tax )"
        str50="Total Selling Service Fee ( After tax )"
        str51="Fullfillment Service Fee ( Before tax )"
        str52="Total Fullfillment Service Fee ( Before tax )"
        str53="Fullfillment Service Fee (After Tax)"
        str54="Total Fullfillment Service Fee (After Tax)"
        str55="Total Service Fee"
        str56="Sigma Total Service Fee"
        str57="Service Tax Rate"
        str58="TP Selling Fee"
        str59="Weight (in Grams)"
        str60="Customer Name"  
        str61="State" 
        str62="Invoice" 
        
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
        for i in range(0,63):
            worksheet.col(i).width = 500*8
        #This block is use to  Write some data headers.
        for i in range(1,63):
            print"i>>>>>>>>>>>>",str(i)
            str_val= 'str'+ str(i)
            str_val = vars()[str_val]
            print"str_val>>>>>>>>",str_val
            if i <= 28:
                worksheet.write(0,i-1, str_val,style=bold_style)       
            else:
                worksheet.write(0,i-1, str_val,style=yellow_style_bold)
                             
        
        # Some data we want to write to the worksheet.
        shopclues_seller_place_order_res = shopclues_seller_place_order_obj.search([('order_date','>=',self.start_date),
                                                                                    ('order_date','<=',self.end_date)])
        print"shopclues_seller_place_order_res>>>>>>>",shopclues_seller_place_order_res
            
        list =[]        
        for shopclues_seller_place_order in shopclues_seller_place_order_res:
            line_data =[]
            line_data.append(shopclues_seller_place_order.order_date)
            line_data.append(shopclues_seller_place_order.shipment_date)
            line_data.append(shopclues_seller_place_order.order_id)
            line_data.append(shopclues_seller_place_order.sku)
            line_data.append(shopclues_seller_place_order.order_status)
            line_data.append(shopclues_seller_place_order.product_details)
            line_data.append(shopclues_seller_place_order.buyer_name)
            line_data.append(shopclues_seller_place_order.shipping_city)
            line_data.append(shopclues_seller_place_order.shipping_state)
            line_data.append(shopclues_seller_place_order.shipping_pincode)
            line_data.append(shopclues_seller_place_order.quantity)
            line_data.append(shopclues_seller_place_order.payment_type)
            line_data.append(shopclues_seller_place_order.payment_details)
            line_data.append(shopclues_seller_place_order.order_subtotal)
            line_data.append(shopclues_seller_place_order.collectable_amount)
            line_data.append(shopclues_seller_place_order.merchant_sku)
            line_data.append(shopclues_seller_place_order.shipment_id)
            line_data.append(shopclues_seller_place_order.tracking_no)
            line_data.append(shopclues_seller_place_order.carrier_name)
            line_data.append(shopclues_seller_place_order.merchant_name)
            line_data.append(shopclues_seller_place_order.merchant_type)
            line_data.append(shopclues_seller_place_order.merchant_city)
            line_data.append(shopclues_seller_place_order.regular_selling_price)
            line_data.append(shopclues_seller_place_order.total_merchnat_discount_permotions)
            line_data.append(shopclues_seller_place_order.invoice_value)
            line_data.append(shopclues_seller_place_order.shipping_cost)
            line_data.append(shopclues_seller_place_order.weight)
            line_data.append(shopclues_seller_place_order.sku_id)

            shopclues_seller_place_payment_res = shopclues_seller_place_payment_obj.search([('order_id','=',shopclues_seller_place_order.order_id)])
            
            Product_ID = []
            Merchant_Reference_No = []
            Product = []
            Status = []
            Billing_Type = []
            Net_Payout = []
            Shipping_Cost = []
            Total_Shipping_Cost = 0.0
            Selling_Price = []
            Total_Selling_Price = 0.0
            Merchant_Order_Total = []
            Total_Merchant_Order_Total = 0.0
            Remote_Address_Shipping = False
            Order_Total = []
            Sigma_Order_Total = 0.0
            Deal_Price = []
            Total_Deal_Price = 0.0
            Unit_Target_Payout = False
            Selling_Service_Fee_bt = []
            Total_Selling_Service_Fee_bt = 0.0
            Selling_Service_Fee_at = []
            Total_Selling_Service_Fee_at = 0.0
            Fullfillment_Service_Fee_bt = []
            Total_Fullfillment_Service_Fee_bt =0.0 
            Fullfillment_Service_Fee_at = []
            Total_Fullfillment_Service_Fee_at =0.0             
            Total_Service_Fee = []
            Sigma_Total_Service_Fee = 0.0
            Service_Tax_Rate = []
            TP_Selling_Fee = []
            Weight = []
            Customer_Name = False
            State = []
            Invoice = []
            for shopclues_seller_place_payment in shopclues_seller_place_payment_res:
                Product_ID.append(str(shopclues_seller_place_payment.product_id))
                Merchant_Reference_No.append(str(shopclues_seller_place_payment.merchant_reference_no))
                Product.append(str(shopclues_seller_place_payment.product))
                Status.append(str(shopclues_seller_place_payment.status))
                Billing_Type.append(str(shopclues_seller_place_payment.billing_type))
                Net_Payout.append(str(shopclues_seller_place_payment.net_payout))
                Shipping_Cost.append(str(shopclues_seller_place_payment.shipping_cost))
                Total_Shipping_Cost = Total_Shipping_Cost + shopclues_seller_place_payment.shipping_cost
                Selling_Price.append(str(shopclues_seller_place_payment.selling_price))
                Total_Selling_Price = Total_Selling_Price + shopclues_seller_place_payment.selling_price
                Merchant_Order_Total.append(str(shopclues_seller_place_payment.merchant_Order_total))
                Total_Merchant_Order_Total = Total_Merchant_Order_Total + shopclues_seller_place_payment.merchant_Order_total
                Remote_Address_Shipping = shopclues_seller_place_payment.remote_address_shipping
                Order_Total.append(str(shopclues_seller_place_payment.order_total))
                Sigma_Order_Total = Sigma_Order_Total + shopclues_seller_place_payment.order_total
                Deal_Price.append(str(shopclues_seller_place_payment.deal_price))
                Total_Deal_Price = Total_Deal_Price + shopclues_seller_place_payment.deal_price
                Unit_Target_Payout = shopclues_seller_place_payment.unit_target_payout
                Selling_Service_Fee_bt.append(str(shopclues_seller_place_payment.selling_service_fee_before_tax))
                Total_Selling_Service_Fee_bt = Total_Selling_Service_Fee_bt + shopclues_seller_place_payment.selling_service_fee_before_tax
                Selling_Service_Fee_at.append(str(shopclues_seller_place_payment.selling_service_fee_after_tax))
                Total_Selling_Service_Fee_at = + shopclues_seller_place_payment.selling_service_fee_after_tax
                Fullfillment_Service_Fee_bt.append(str(shopclues_seller_place_payment.fullfillment_service_fee_before_tax))
                Total_Fullfillment_Service_Fee_bt = Total_Fullfillment_Service_Fee_bt + shopclues_seller_place_payment.fullfillment_service_fee_before_tax
                Fullfillment_Service_Fee_at.append(str(shopclues_seller_place_payment.fullfillment_service_fee_after_tax))
                Total_Fullfillment_Service_Fee_at = Total_Fullfillment_Service_Fee_at + shopclues_seller_place_payment.fullfillment_service_fee_after_tax
                Total_Service_Fee.append(str(shopclues_seller_place_payment.total_service_fee))
                Sigma_Total_Service_Fee = Sigma_Total_Service_Fee + shopclues_seller_place_payment.total_service_fee
                Service_Tax_Rate.append(str(shopclues_seller_place_payment.service_tax_rate))
                TP_Selling_Fee.append(str(shopclues_seller_place_payment.tp_selling_fee))
                Weight.append(str(shopclues_seller_place_payment.weight))
                Customer_Name = shopclues_seller_place_payment.customer_name
                State.append(str(shopclues_seller_place_payment.state))
                Invoice.append(str(shopclues_seller_place_payment.invoice))

            Product_ID = ('\r\n'.join(Product_ID))
            Merchant_Reference_No = ('\r\n'.join(Merchant_Reference_No))
            Product = ('\r\n'.join(Product))
            Status = ('\r\n'.join(Status))
            Billing_Type = ('\r\n'.join(Billing_Type))
            Net_Payout = ('\r\n'.join(Net_Payout))
            Shipping_Cost = ('\r\n'.join(Shipping_Cost))
            Selling_Price = ('\r\n'.join(Selling_Price))
            Merchant_Order_Total = ('\r\n'.join(Merchant_Order_Total))
            Order_Total = ('\r\n'.join(Order_Total))
            Deal_Price = ('\r\n'.join(Deal_Price))
            Selling_Service_Fee_bt = ('\r\n'.join(Selling_Service_Fee_bt))
            Selling_Service_Fee_at = ('\r\n'.join(Selling_Service_Fee_at))
            Fullfillment_Service_Fee_bt = ('\r\n'.join(Fullfillment_Service_Fee_bt))
            Fullfillment_Service_Fee_at = ('\r\n'.join(Fullfillment_Service_Fee_at))
            Total_Service_Fee = ('\r\n'.join(Total_Service_Fee))
            Service_Tax_Rate = ('\r\n'.join(Service_Tax_Rate))
            TP_Selling_Fee = ('\r\n'.join(TP_Selling_Fee))
            Weight = ('\r\n'.join(Weight))
            State = ('\r\n'.join(State))
            Invoice = ('\r\n'.join(Invoice))
 
            line_data.append(Product_ID)
            line_data.append(Merchant_Reference_No)
            line_data.append(Product)
            line_data.append(Status)
            line_data.append(Billing_Type)
            line_data.append(Net_Payout)
            line_data.append(Shipping_Cost)
            line_data.append(Total_Shipping_Cost)
            line_data.append(Selling_Price)
            line_data.append(Total_Selling_Price)
            line_data.append(Merchant_Order_Total)
            line_data.append(Total_Merchant_Order_Total)
            line_data.append(Remote_Address_Shipping)
            line_data.append(Order_Total)
            line_data.append(Sigma_Order_Total)
            line_data.append(Deal_Price)
            line_data.append(Total_Deal_Price)
            line_data.append(Unit_Target_Payout)
            line_data.append(Selling_Service_Fee_bt)
            line_data.append(Total_Selling_Service_Fee_bt)
            line_data.append(Selling_Service_Fee_at)
            line_data.append(Total_Selling_Service_Fee_at)
            line_data.append(Fullfillment_Service_Fee_bt)
            line_data.append(Total_Fullfillment_Service_Fee_bt)
            line_data.append(Fullfillment_Service_Fee_at)
            line_data.append(Total_Fullfillment_Service_Fee_at)
            line_data.append(Total_Service_Fee)
            line_data.append(Sigma_Total_Service_Fee)
            line_data.append(Service_Tax_Rate)
            line_data.append(TP_Selling_Fee)
            line_data.append(Weight)
            line_data.append(Customer_Name)
            line_data.append(State)
            line_data.append(Invoice)
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
        
        file_name='ShopcluesSaleReport-'+str(self.start_date) +'_'+str(self.end_date)+'-' +str(self.market_place_id.name.name)+'_'+ str(self.vendor_place_id.name.name) + '.xls'
        self.write({'filedata':out, 'filename':file_name})        
        
        return {
                    'name':'Shopclues Seller Sale Report',
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
    def action_shopclues_seller_sale_report(self):
        print"action_shopclues_seller_sale_report>>>>>>>>>>>called"
        seller_place_config_obj = self.env['seller.place.config']
        auth_res = seller_place_config_obj.get_authentication(self.market_place_id.id, self.vendor_place_id.id, self.password)
        if auth_res:
            res = self.do_shopclues_seller_sale_report()
        else:
            raise UserError(_('Credential invalid.!Please contact to Administrator.'))
        return res 