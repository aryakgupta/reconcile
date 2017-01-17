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
    _name = "message.wiz"
    _description = "Message wizard"

    text = fields.Char('Text')
