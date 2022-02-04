from email.policy import default
from odoo import models, fields

class Placement(models.Model):
    _name = 'placement.placement'
    _description = 'Placement Management System'

    name = fields.Char(string="Name",required=True)
    address = fields.Char(string="Address")
    description = fields.Text(string="Description")
    email_id = fields.Char(string="Email-ID",required=True)
    contact = fields.Char(string="Contact")
    interested_subject = fields.Text(string="Interested_Subject")
    branch = fields.Char(string="Branch",default = "MCA",readonly=True)
    university = fields.Char(string="University Name")
    dob = fields.Date(string="Date Of Birth",default = lambda self: fields.Datetime.now())
    year = fields.Selection([
        ('1st','1st'),
        ('2nd','2nd')
    ])
   

    