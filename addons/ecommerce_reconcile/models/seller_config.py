# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from itertools import groupby
from datetime import datetime, timedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
from odoo.tools.misc import formatLang

import odoo.addons.decimal_precision as dp


class SellerPlaceConfig(models.Model):
    _name = "seller.place.config"
    _description = "Seller Place Config"
    _order = 'id desc'


    market_place_id = fields.Many2one('market.place', 'Market Place')
    vendor_place_id = fields.Many2one('vendor.place', 'Vendor Place')
    password = fields.Char(string='Password', required=True, copy=False)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('de-active', 'De-Active'),
        ], string='Status', readonly=True, copy=False, default='draft')

    market_place_type = fields.Selection([
                                ('flipkart', 'Flipkart'),
                                ('amazon', 'Amazon'),
                                ], string='Market Place Type ', copy=False) 
    
    @api.multi
    def get_authentication(self, market_place_id, vendor_place_id, password):
        """
            This method is used to check weather
            enter credential valid or not.
        """
        seller_place_config_res = self.search([('market_place_id','=',market_place_id),
                                               ('vendor_place_id','=',vendor_place_id),
                                               ('password','=',password),
                                               ('state','=','active')])
        print"seller_place_config_res>>>>>>>>.",seller_place_config_res
        if seller_place_config_res:
            return True
        return False
    
    @api.multi
    def action_activate(self):
        self.write({'state': 'active'})
        
    @api.multi
    def action_deactivate(self):
        self.write({'state': 'de-active'})
                
class MarketPlace(models.Model):
    _name = "market.place"
    _description = "Market Place Config"
    _order = 'id desc'

    name = fields.Many2one('res.partner', 'Partner')
    market_place_type = fields.Selection([
                                ('flipkart', 'Flipkart'),
                                ('amazon', 'Amazon'),
                                ], string='Market Place Type ', required=True,copy=False)     
    
class VendorPlace(models.Model):
    _name = "vendor.place"
    _description = "Vendor Place Config"
    _order = 'id desc'

    name = fields.Many2one('res.partner', 'Partner')
    market_place_type = fields.Selection([
                                ('flipkart', 'Flipkart'),
                                ('amazon', 'Amazon'),
                                ], string='Market Place Type ', required=True, copy=False) 
        
