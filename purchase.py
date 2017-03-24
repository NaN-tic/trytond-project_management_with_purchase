# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.pool import PoolMeta
from decimal import Decimal
from trytond.transaction import Transaction
from trytond.pool import Pool

__all__ = ['PurchaseLine', 'ProjectSummary', 'Work']


class Work:
    __name__ = 'project.work'
    __metaclass__ = PoolMeta

    @classmethod
    def _get_summary_models(cls):
        res = super(Work, cls)._get_summary_models()
        return res + [('purchase.line', 'work', 'get_total')]


class ProjectSummary:

    __name__ = 'project.work.summary'
    __metaclass__ = PoolMeta

    @classmethod
    def union_models(cls):
        res = super(ProjectSummary, cls).union_models()
        return ['purchase.line'] + res


class PurchaseLine:
    __metaclass__ = PoolMeta
    __name__ = 'purchase.line'

    @classmethod
    def _get_cost(cls, purchase_lines):
        limit_date = Transaction().context.get('limit_date')
        return dict((w.id, w.amount) for w in purchase_lines
            if (limit_date == None or w.purchase.purchase_date <= limit_date))

    @classmethod
    def _get_revenue(cls, purchase_lines):
        return dict.fromkeys([w.id for w in purchase_lines], Decimal(0))

    @staticmethod
    def _get_summary_related_field():
        return 'work'

    @classmethod
    def get_total(cls, lines, names):
        res = {}
        pool = Pool()
        Work = pool.get('project.work')
        for name in Work._get_summary_fields():
            res[name] = {}

        limit_date = Transaction().context.get('limit_date')
        for line in lines:
            if line.type != 'line':
                continue

            res['progress_cost'][line.id] = Decimal(0)
            if limit_date != None and line.purchase.purchase_date > limit_date:
                res['progress_cost'][line.id] = Decimal(0)
            elif (line.purchase.state in ('processing') and
                    line.purchase.shipment_state != 'received'):
                res['progress_cost'][line.id] = line.amount
            elif line.purchase.state in ('done'):
                res['progress_cost'][line.id] = \
                    line._get_shipped_quantity() * line.unit_price

            res['revenue'][line.id] = Decimal(0)
            res['progress_revenue'][line.id] = Decimal(0)
            res['cost'][line.id] = Decimal(0)

        for key in res.keys():
            if key not in names:
                del res[key]
        return res
