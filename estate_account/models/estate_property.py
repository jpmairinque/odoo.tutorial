from odoo import models,fields

class InheritedEstateProperty(models.Model):
    
    _inherit = "estate.property"

    def action_sell_property(self):
        action_sell = super().action_sell_property()
        journal = self.env['account.move'].with_context(default_move_type='out_invoice')._get_default_journal()
        print(journal)
        self.env['account.move'].create({
            'partner_id':self.buyer.id,
            'move_type':'out_invoice',
            'journal_id':journal.id,
            'invoice_line_ids': [
                (0, 0, {
                    'name': self.name,
                    'quantity': 1,
                    'price_unit': self.selling_price,
                }),
                 (0, 0, {
                    'name': 'Administrative Fees',
                    'quantity': 1,
                    'price_unit': 100,
                })
                
            ]
            

        })
        return action_sell

  