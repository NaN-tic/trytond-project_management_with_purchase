# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.model import fields
from trytond.pyson import Eval
from decimal import Decimal

__all__ = ['PurchaseLine', 'ProjectSummary', 'Work']


class Work:
    __name__ = 'project.work'
    __metaclass__ = PoolMeta

    @classmethod
    def _get_related_cost_and_revenue(cls):
        res = super(Work, cls)._get_related_cost_and_revenue()
        return res + [('purchase.line', 'parent', '_get_revenue',
            '_get_cost')]


class ProjectSummary:

    __name__ = 'project.work.summary'
    __metaclass__ = PoolMeta

    # @classmethod
    # def union_models(cls):
    #     res = super(ProjectSummary, cls).union_models()
    #     return ['purchase.line'] + res



#TODO: project revenue uses work field, but until unionmixing works correctly
#      i create a new field.

class PurchaseLine:
    __metaclass__ = PoolMeta
    __name__ = 'purchase.line'

    parent = fields.Many2One('project.work', 'Work Effort', select=True,
        domain=[
            ('company', '=', Eval('_parent_purchase', {}).get('company', -1)),
            ])


    @classmethod
    def _get_cost(cls, purchase_lines):
        return dict( (w.id, w.amount) for w in purchase_lines)

    @classmethod
    def _get_revenue(cls, purchase_lines):
        return dict.fromkeys([w.id for w in purchase_lines], Decimal(0))
