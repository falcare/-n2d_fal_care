# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class PurchaseOrderInlineInherit(models.Model):
    _inherit = 'purchase.order.line'

    def _get_product_purchase_description(self, product_lang):
        self.ensure_one()
        name = product_lang.name
        if product_lang.description_purchase:
            name += '\n' + product_lang.description_purchase

        return name
