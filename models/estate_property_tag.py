from odoo import models,fields
class EstatePropertyTag(models.Model):
    _description = 'Tag to properties'
    _name = "estate.tag"
    _order = "name"

    ## Fields base

    name = fields.Char(required=True)
    color = fields.Integer()
  