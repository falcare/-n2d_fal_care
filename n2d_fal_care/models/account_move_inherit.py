# -*- encoding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from num2words import num2words


class AccountMove(models.Model):
    _inherit = "account.move"

    def get_number_in_words(self, amount, lang):
        self.ensure_one()
        return num2words(amount, lang=lang)


class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    lot_id = fields.Many2one('stock.production.lot', 'Lot/Serial Number')
    life_date = fields.Datetime('EXP.Date', related='lot_id.life_date', store=True)

class saleAdvancePaymentInv(models.TransientModel):
    _inherit = "sale.advance.payment.inv"

    def _prepare_invoice_values(self, order, name, amount, so_line):
        invoice = super(saleAdvancePaymentInv, self)._prepare_invoice_values(order, name, amount, so_line)
        if invoice:
            invoice['invoice_line_ids'][0][2]['lot_id'] = so_line.lot_id.id
            invoice['invoice_line_ids'][0][2]['life_date'] = so_line.life_date

        return invoice
