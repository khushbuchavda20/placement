from odoo import models, fields,api


class Property(models.Model):
    _name="property"

    name = fields.Char(string="Title")
    category = fields.Selection([('house','House'), ('villa', 'Villa')])
    price = fields.Float()
    image = fields.Image()