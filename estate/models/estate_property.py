from odoo.exceptions import RedirectWarning, UserError, ValidationError
from odoo import api, models,fields

class EstateProperty(models.Model):

    _description = 'IAP Lead Enrichment API'
    _name = "estate.property"
    _order = "id desc"

    ## Fields base

    name = fields.Char(required=True, string="Name")
    description = fields.Text()
    postcode = fields.Char()
    date_avaliability = fields.Date(copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float( copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection( string='Orientation', selection=[('south', 'South'), ('north', 'North'),('east', 'East'),('west', 'West')])
    state = fields.Selection(string="State",selection=[('new',"New"),('offer_received',"Offer Received"),
    ('offer_accepted',"Offer Accepted"),('sold',"Sold"),('canceled',"Canceled")], required=True, copy=False, default='new')

    ## Constraints from SQL

    _sql_constraints = [
        ('check_selling_price', 'CHECK(selling_price >= 0)',
         'The expected price must be strictly positive'),
        ('check_selling_price', 'CHECK(selling_price > 0)',
        'The price of the offer must be strictly positive'),
    ]

    ## Fields entre models

    property_type_id=fields.Many2one("estate.type",string="Type")
    salesperson = fields.Many2one('res.users', string='Salesperson', default=lambda self: self.env.user)
    buyer = fields.Many2one('res.partner', string="Buyer", copy=False)
  

    tag_ids=fields.Many2many("estate.tag", string="Tags")
    offer_ids = fields.One2many("estate.offer", "property_id", string="Offers")

    ## Fields computados 

    total_area = fields.Float(compute="_compute_total_area")
    best_price = fields.Float(compute="_compute_best_price")
   

    ## Cálculo do field área total

    @api.depends("living_area","garden_area")
    def _compute_total_area(self):
        for rec in self:
            rec.total_area = rec.living_area + rec.garden_area


    ## Cálculo da maior oferta

    @api.depends("offer_ids")
    def _compute_best_price(self):
        for rec in self:
            best = 0
            for x in rec.offer_ids:
                if x.price > best:
                    best = x.price
            rec.best_price = best
            
 
    ## Automatização dos fields relacionados à garden
           
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden==True:
            self.garden_area = 10
            self.garden_orientation = 'north'
        if self.garden == False:
            self.garden_area = None
            self.garden_orientation = None

    ## Ação de cancelamento da property

    def action_cancel_property(self):
        for rec in self:
            if rec.state == 'sold':
                raise UserError("A sold property can not be cancelled")
            else:
                rec.state = 'canceled'
        
        return True

    ## Ação de venda da property

    def action_sell_property(self):
        for rec in self:
            if rec.state == 'canceled':
                raise UserError("A canceled property can not be sold")
            else:
                if not rec.buyer.id:
                    raise UserError("A property without a buyer can not be sold")
                else: rec.state = 'sold'
        
        return True

    ## Adicionando constrains

    @api.constrains('selling_price','expected_price')
    def _check_price_relation(self):
        for rec in self:
            if rec.selling_price != 0:
                if rec.selling_price<(0.9*rec.expected_price):
                    raise ValidationError("The selling price cannot be lower than 90 percent of the expected price")
   
   ## Overwriting da ação de unlink

    def unlink(self):
        for rec in self:
            if rec.state!='new' or rec.state!='canceled':
                raise UserError('You cannot delete a property if its state is not ‘New’ or ‘Canceled’')
        return super().unlink()

   



