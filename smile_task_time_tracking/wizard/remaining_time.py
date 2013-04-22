# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2013 Smile (<http://www.smile.fr>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp.osv import fields
from openerp.osv.osv import except_osv
from openerp.osv.orm import TransientModel
import openerp.addons.decimal_precision as dp


class RemainingTimeWizard(TransientModel):
    _name = 'project.task.remaining_time.wizard'
    _description = "Task's Remaining Time Wizard"

    def _get_task_id(self, context=None):
        if context is None:
            context = {}
        task_ids = context.get('active_ids', [])
        if len(task_ids) != 1 or context.get('active_model', None) != 'project.task':
            raise except_osv('Error', 'Wrong context.')
        return task_ids[0]

    def view_init(self, cr, uid, fields_list, context=None):
        return self._get_task_id(context)

    _columns = {
    }

    def button_update_remaining_time(self, cr, uid, ids, context=None):
        ids = isinstance(ids, (tuple, list)) and ids or [ids]
        if not ids or len(ids) > 1:
            return False
        wizard = self.browse(cr, uid, ids[0], context)
        lpool = self.pool.get('project.task.remaining_time.line')
        task_id = self._get_task_id(context)


        # Archive all active remaining time lines
        active_line_ids = lpool.search(cr, uid, [('task_id', '=', task_id), ('archived', '=', False)], context=context)
        lpool.write(cr, uid, active_line_ids, {'archived': True}, context=context)
        # Create our new remaining time line
        lpool.create(cr, uid, {'task_id': task_id
          }, context)


        # Go back to the task we've just updated
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': self.pool.get('ir.model.data').get_object_reference(cr, uid, 'project', 'view_task_form2')[1],
            'res_model': 'project.task',
            'res_id': task_id,
            'target': 'current',
            'context': context,
        }

    def button_close(self, cr, uid, ids, context=None):
        return {'type': 'ir.actions.act_window_close'}