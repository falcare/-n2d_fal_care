# -*- encoding: utf-8 -*-

from odoo import models, api


class StockRule(models.Model):
    _inherit = 'stock.rule'

    def _get_stock_move_values(self, product_id, product_qty, product_uom, location_id, name, origin, company_id,
                               values):

        result = super(StockRule, self)._get_stock_move_values(product_id, product_qty, product_uom, location_id, name, origin, company_id,
                               values)
        if values.get('lot_id', False):
            result['lot_id'] = values['lot_id']

        return result
