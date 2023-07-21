{
    "name": "Default Product UOM for Sales",
    "version": "6.1.0",
    "category": "Sales",
    "author": 'Zero Systems',
    "company": 'Zero for Information Systems',
    "website": "https://www.erpzero.com",
    "email": "sales@erpzero.com",
    "sequence": 0,
    "summary": """ default Unit value of a product in sales and Purchase UoM for Bill """,
    'description': """
        Set default Unit value of a product in sales and Purchase UoM for Bill
      """,
    "depends": ["sale_management","account"],
    "data": [
        "views/view.xml",
    ],
    'license': 'OPL-1',
    # 'live_test_url': 'https://youtu.be/T82sTeIwrm8',
    'images': ['static/description/pricelist_round_with_fixed.png'],
    'installable': True,
    'auto_install': False,
    'application': False,
    'price': 15.0,
    'currency': 'EUR',
}
