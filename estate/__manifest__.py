{
    'name': "Estate",
    'application': True,
    'depends': [
        'base'
        
    ],
    'data': [
        'security/ir.model.access.csv',             
        'views/estate_property_type_views.xml',
        'report/estate_report.xml',
        'report/estate_report_views.xml',
        'views/res_users_views.xml',  
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_menus.xml',
       
    ]
}