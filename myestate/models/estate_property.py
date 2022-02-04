
from dataclasses import field
from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection([('accepted','Accepted'),('refuse','Refused')])
    partner_id = fields.Many2one('res.partner', domain="[('is_buyer','=',True)]")
    property_id = fields.Many2one('estate.property')
    property_type_id = fields.Many2one(related='property_id.property_type_id', store=True)


    def action_accepted(self):
        for record in self:
            record.status = "accepted"
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id

    
    def action_refused(self):
        for record in self:
            record.status = "refuse" 

class EstatePropertyTag(models.Model):
    _name = 'estate.property.tag'
    _description = 'Estate Property Tag'
    _sql_constraints = [('unique_property_tag_name', 'unique(name)', 'Tag cannot be duplicated')]


    name = fields.Char()
    color = fields.Integer()

class EstatePropertyType(models.Model):
    _name = 'estate.property.type'
    _description = 'Estate Property Type'
    _sql_constraints = [('unique_property_type_name', 'unique(name)', 'Type cannot be duplicated')]

    name = fields.Char()
    property_ids = fields.One2many('estate.property','property_type_id')
    offer_ids = fields.One2many('estate.property.offer', 'property_type_id')
    offer_count = fields.Integer(compute= '_compute_offer_count')

    @api.depends('offer_ids')
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = 'Estate Property'
    #_sql_constraints = [('positive_price', 'check(expected_price >0)', 'Enter positive value')]
    _order = "id desc"

    #def test(self):
    #   return fields.Datetime.now()
    def get_description(self):
        print(self.env.user.name)
        # if self.env.context.get('my_property_search'):
        return self.env.user.name + '\'s property'


    name = fields.Char(string="Title", default="Unknown", required=True)
    description = fields.Text(default=get_description)
    postcode = fields.Char()
    date_availability = fields.Date(default = lambda self: fields.Datetime.now(), copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(copy=False, readonly=True)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection([
        ('north','North'),
        ('south','South'),
        ('east','East'),
        ('west','West')
    ])
    active = fields.Boolean(default=True)
    image = fields.Image()
    property_type_id = fields.Many2one('estate.property.type')
    salesman_id = fields.Many2one('res.users')
    buyer_id = fields.Many2one('res.partner')
    property_tag_ids = fields.Many2many('estate.property.tag')
    property_offer_ids = fields.One2many('estate.property.offer','property_id')
    total_area = fields.Integer(compute="_compute_area", inverse="_inverse_area")
    best_price = fields.Float(compute="_compute_best_price", store=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline")
    state = fields.Selection([('new','New'),('sold','Sold'),('cancel','Cancelled')], default = 'new')
    currency_id = fields.Many2one('res.currency', default=lambda self: self.env.company.currency_id)


    def open_offers(self):
        view_id = self.env.ref('myestate.estate_property_offer_tree').id
        return {
            "name":"Offers",
            "type":"ir.actions.act_window",
            "res_model":"estate.property.offer",
            "views":[[view_id, 'tree']],
            # "res_id": 2,
            "target":"new",
            "domain": [('property_id', '=', self.id)]
        }

    @api.onchange('garden')
    def _onchange_garden(self):
        for record in self:
            if record.garden:
                record.garden_area = 10
                record.garden_orientation = 'north'
            else:
                record.garden_area = 0
                record.garden_orientation = None


    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(record.date_availability, days=record.validity)

   
    @api.depends('property_offer_ids.price')
    def _compute_best_price(self): # Recordset [ Collection  of records]
        for record in self:
            max_price = 0
            for offer in record.property_offer_ids:
                if offer.price > max_price:
                    max_price = offer.price
            record.best_price = max_price


    @api.depends('living_area', 'garden_area')
    def _compute_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area


    def _inverse_area(self):
        for record in self:
            record.living_area = record.garden_area = record.total_area / 2

    
    def action_sold(self):
        #print("\n\n In action sold")
        for record in self:
            if record.state=="cancel":
                raise UserError("Cancel Property can't be Sold!!")
            record.state = 'sold'


    def action_cancel(self):
        for record in self:
            if record.state=="sold":
                raise UserError("Sold Property can't be Cancelled!")
            record.state = 'cancel'


    @api.constrains('living_area', 'garden_area')
    def _check_garden_area(self):
        for record in self:
            if record.living_area < record.garden_area:
                raise ValidationError("Garden cannot be bigger than living area")


    @api.constrains('living_area', 'garden_area')
    def _check_garden_area(self):
        for record in self:
            if record.living_area < record.garden_area:
                raise ValidationError("Garden cannot be bigger than living area")

class MyProperty(models.Model):
    _name="estate.my.property"
    _description="Estate My Property"
    _inherit='estate.property'