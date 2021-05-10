# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'

    # args[['company_id', 'in', [1, False]]]
    def name_get(self):
        self.browse(self.ids).read(['name', 'default_code'])
        return [(template.id, template.default_code or ' ')
                for template in self]
