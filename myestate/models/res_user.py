from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError

class Resuser(models.Model):
   _inherit  = 'res.users'



   property_id = fields.One2many('estate.property', 'salesman_id')
   is_buyer = fields.Boolean()