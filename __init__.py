# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import Pool
import purchase

def register():
    Pool.register(
        purchase.PurchaseLine,
        purchase.Work,
        purchase.ProjectSummary,
        module='project_management_with_purchase', type_='model')