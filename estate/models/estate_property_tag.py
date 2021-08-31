from odoo import models,fields
class EstatePropertyTag(models.Model):
    _description = 'Tag to properties'
    _name = "estate.tag"
    _order = "name"

    ## Constraints from SQL

    _sql_constraints = [
        ('check_name_unique', 'UNIQUE(name)',
         'The tag must be unique'),
    ]

    ## Fields base

    name = fields.Char(required=True)
    color = fields.Integer()
  
    