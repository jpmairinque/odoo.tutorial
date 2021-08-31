from odoo.tests.common import SavepointCase
from odoo.exceptions import UserError
from odoo.tests import tagged


@tagged('post_install', '-at_install')
class EstateTestCase(SavepointCase):

    @classmethod
    def setUpClass(cls):
        
        super(EstateTestCase, cls).setUpClass()

        cls.properties = cls.env['estate.property'].create({
            'name':'testprop',
            'state':'sold',
            'living_area':10,
            'garden_area':40
        })


    def test_creation_area(self):
        self.properties.living_area = 20
        self.assertRecordValues(self.properties, [
           {'name': 'testprop', 'total_area': 50},
        ])