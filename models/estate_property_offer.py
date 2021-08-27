from datetime import date, timedelta
from odoo import api, models,fields

class EstatePropertyOffer(models.Model):

    _description = 'Offers to properties'
    _name = "estate.offer"
    _order = "price desc"

    ## Fields base

    price = fields.Float()
    status = fields.Selection(copy=False, selection=[('accepted',"Accepted"),('refused',"Refused")])
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer(default=7)
    create_date = fields.Date(default=date.today())
    property_type = fields.Many2one('estate.type', related='property_id.property_type_id', store=True)
   

    ## Fields computados / com inversão

    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")
   
    ##  Cáculo da nova deadline
    
    @api.depends("validity")
    def _compute_date_deadline(self):
        for rec in self:
            rec.date_deadline = rec.create_date + timedelta(days=rec.validity)

    def _inverse_date_deadline(self):
        for rec in self:
            rec.create_date = rec.date_deadline

    ## Ação de aceitamento da offer

    def action_accept_offer(self):
        for rec in self:
            rec.status = 'accepted'
            rec.property_id.selling_price=rec.price
        return True

    ## Ação de negação da offer

    def action_refuse_offer(self):
        for rec in self:
            rec.status = 'refused'
        
        return True
        
    