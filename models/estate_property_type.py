from odoo import api, models,fields

class EstatePropertyType(models.Model):
    _description = 'Types to properties'
    _name = "estate.type"
    _order = "name"

    name = fields.Char(string="Type",required=True)
    property_ids = fields.One2many("estate.property", "property_type_id")
    offer_ids = fields.One2many("estate.offer", "property_type")
    offer_count = fields.Float(compute="_compute_offer_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for rec in self:
            rec.offer_count = rec.offer_ids.price


  
