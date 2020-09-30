# -*- encoding: utf-8 -*-

from odoo import models, fields, api

from num2words import num2words


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def get_number_in_words(self, amount, lang):
        self.ensure_one()
        return num2words(amount, lang=lang)


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    lot_id = fields.Many2one('stock.production.lot', 'Lot/Serial Number')
    life_date = fields.Datetime('EXP.Date', related='lot_id.life_date', store=True)

    @api.onchange('lot_id','life_date')
    @api.depends('lot_id','life_date')
    def change_lot(self):
        for rec in self:
            if rec.life_date and rec.lot_id:
                rec.lot_id.life_date = rec.life_date

    def _prepare_invoice_line(self):
        res = super(SaleOrderLine, self)._prepare_invoice_line()
        res['lot_id'] = self.lot_id.id or False
        return res

    def _prepare_procurement_values(self, group_id=False):
        values = super(SaleOrderLine, self)._prepare_procurement_values(group_id)
        values.update({
            'lot_id': self.lot_id.id or False
        })
        return values
