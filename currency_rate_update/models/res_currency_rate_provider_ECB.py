# Copyright 2009 Camptocamp
# Copyright 2009 Grzegorz Grzelak
# Copyright 2019 Brainbean Apps (https://brainbeanapps.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import xml.sax
import urllib
import json
from collections import defaultdict
from datetime import date, timedelta
from urllib.request import urlopen

from odoo import fields, models


class ResCurrencyRateProviderECB(models.Model):
    _inherit = "res.currency.rate.provider"

    service = fields.Selection(selection_add=[("UAE", "Central Bank Of the UAE")])

    def _get_supported_currencies(self):
        self.ensure_one()
        if self.service != "UAE":
            return super()._get_supported_currencies()
        return [
            "USD",
            "GBP",
            "EUR",
            "SAR"
        ]

    def _obtain_rates(self, base_currency, currencies, date_from):
        self.ensure_one()
        if self.service != "UAE":
            return super()._obtain_rates(
                base_currency, currencies, date_from
            )
        invert_calculation = False
        if base_currency != "ِAED":
            invert_calculation = True
            if base_currency not in currencies:
                currencies.append(base_currency)

        url = "https://www.centralbank.ae/en/fx-rates"

        list_curr = []
        for line in urllib.request.urlopen(url):
            line_decode = line.decode('utf-8')
            line_string = line_decode.strip()
            if "US Dollar" in line_string:
                usd_rate = line_string.replace('<tbody>', '').replace('<tr>', '').replace('US Dollar', '').replace('<td>', '').replace('</td>', '')
                usd = {"cur": "USD",
                       "rate": float(usd_rate.strip())}
                list_curr.append(usd)
            if "Euro" in line_string:
                eur_rate = line_string.replace('</tr>', '').replace('<tr>', '').replace('<td>Euro</td>', '').replace('<td>', '').replace('</td>', '')
                eur = {"cur": "EUR",
                       "rate": float(eur_rate.strip())}
                list_curr.append(eur)
            if "GB Pound" in line_string:
                gbp_rate = line_string.replace('</tr>', '').replace('<tr>', '').replace('<td>GB Pound</td>', '').replace('<td>', '').replace('</td>', '')
                gbp = {"cur": "GBP",
                       "rate": float(gbp_rate.strip())}
                list_curr.append(gbp)
            if "Saudi Riyal" in line_string:
                sar_rate = line_string.replace('</tr>', '').replace('<tr>', '').replace('<td>Saudi Riyal</td>', '').replace('<td>', '').replace('</td>', '')
                sar = {"cur": "SAR",
                       "rate": float(sar_rate.strip())}
                list_curr.append(sar)
        return list_curr
