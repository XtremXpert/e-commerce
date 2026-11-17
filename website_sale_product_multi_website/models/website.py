# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
from odoo import models
from odoo.fields import Domain


class Website(models.Model):
    _inherit = "website"

    def website_domain(self):
        # Keep the standard behavior by default, but allow specific flows to
        # switch the website restriction from ``website_id`` to ``website_ids``
        # through the ``multi_website_domain`` context.
        if self.env.context.get("multi_website_domain") and self.ids:
            # ``website_ids`` is a many2many: the leaves below are resolved by
            # the ORM (with its joins) when the domain is used in a search, and
            # evaluated record by record when it is used in memory.
            return Domain("website_ids", "=", False) | Domain(
                "website_ids", "in", self.ids
            )
        return super().website_domain()

    def sale_product_domain(self):
        # Reuse the standard published search while enabling the multi-website
        # variant of website_domain() used in website sale flows.
        return super(
            Website, self.with_context(multi_website_domain=True)
        ).sale_product_domain()
