# -*- encoding: utf-8 -*-

from odoo import fields, models, api


class StockMove(models.Model):
    _inherit = 'stock.move'

    lot_id = fields.Many2one('stock.production.lot', 'Lot/Serial Number')
    life_date = fields.Datetime('EXP.Date', related='lot_id.life_date', store=False)

    @api.onchange('lot_id', 'life_date')
    @api.depends('lot_id', 'life_date')
    def change_lot(self):
        for rec in self:
            if rec.life_date and rec.lot_id:
                rec.lot_id.life_date = rec.life_date

    def _prepare_move_line_vals(self, quantity=None, reserved_quant=None):
        vals = super(StockMove, self)._prepare_move_line_vals(quantity=quantity, reserved_quant=reserved_quant)
        if self.lot_id:
            vals['lot_id'] = self.lot_id.id
        return vals
