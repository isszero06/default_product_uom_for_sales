
from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError

class ProductTemplate(models.Model):
    _inherit = "product.template"

    sale_uom_id = fields.Many2one("uom.uom", "Default Sale UoM",default=lambda self: self.uom_id.id)

    @api.constrains('uom_id', 'sale_uom_id')
    def _check_uom(self):
        if any(template.uom_id and template.sale_uom_id and template.uom_id.category_id != template.sale_uom_id.category_id for template in self):
            raise ValidationError(_('The default Unit of Measure and the sales Unit of Measure must be in the same category.'))


    @api.onchange('uom_id')
    def _onchange_uom_id(self):
        if self.uom_id:
            self.sale_uom_id = self.uom_id.id

    @api.onchange('sale_uom_id')
    def _onchange_uom_id(self):
        if self.uom_id and self.sale_uom_id and self.uom_id.category_id != self.sale_uom_id.category_id:
            self.sale_uom_id = self.uom_id

            
class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    @api.depends('display_type', 'product_id', 'product_packaging_qty')
    def _compute_product_uom_qty(self):
        res = super(SaleOrderLine, self)._compute_product_uom_qty()
        for line in self:
            if line.product_id and line.product_id.product_tmpl_id.sale_uom_id:
                line.product_uom = line.product_id.product_tmpl_id.sale_uom_id

        return res

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    @api.depends('product_id')
    def _compute_product_uom_id(self):
        res = super(AccountMoveLine, self)._compute_product_uom_id()
        for line in self:
            if line.move_id.is_sale_document(include_receipts=True):
                if line.product_id:
                    if line.product_id.product_tmpl_id.sale_uom_id:
                        line.product_uom_id = line.product_id.product_tmpl_id.sale_uom_id
                    else:
                        line.product_uom_id = line.product_id.product_tmpl_id.uom_id
            if line.move_id.is_purchase_document(include_receipts=True):
                if line.product_id:
                    if line.product_id.product_tmpl_id.uom_po_id:
                        line.product_uom_id = line.product_id.product_tmpl_id.uom_po_id
                    else:
                        line.product_uom_id = line.product_id.product_tmpl_id.uom_id
