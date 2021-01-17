# -*- encoding: utf-8 -*-

from odoo import models, fields, api

from num2words import num2words


class SaleOrder(models.Model):
    _inherit = "sale.order"

    def get_number_in_words(self, amount, lang):
        self.ensure_one()
        return num2words(amount, lang=lang)

    # purchase_line_data = self.env['purchase.order.line'].read_group(
    #     [('sale_order_id', 'in', self.ids)],

    def purchase_order_so(self):
        self.ensure_one()
        purchase_line_data = self.env['purchase.order.line'].search(
            [('sale_order_id', '=', self.ids)])

        purchase_order = purchase_line_data.mapped('order_id')

        action = self.env.ref('purchase.purchase_rfq').read()[0]
        action['domain'] = [('id', 'in', purchase_order.ids)]
        return action


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
