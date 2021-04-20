# -*- encoding: utf-8 -*-

{
    "name": "Fal Care",
    "version": "1.0",
    "author": "Hossam Hassan",
    "license": "AGPL-3",
    "category": "Sale",
    "depends": [
        'base',
        'sale_management',
        'stock',
        'product_expiry',
        'account',
        'stock_dropshipping',
        'delivery'
    ],
    "data": [
        'views/stock_production_lot_inherit.xml',
        'views/account_move_inherit.xml',
        'views/sale_order_inherit.xml',
        'views/stock_move_inherit.xml',
        'report/invoice_document_view.xml',
        'report/sale_order_document_view.xml',
        'report/sale_stock_report_invoice_document.xml',
    ],
    'external_dependencies': {
        'python': [
            'num2words',
        ],
    },
}
