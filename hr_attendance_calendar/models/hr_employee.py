# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2016 Open Net Sarl (https://www.open-net.ch)
#    Copyright (C) 2018 Compassion CH (http://www.compassion.ch)
#    @author: Eicher Stephane <seicher@compassion.ch>
#    @author: Coninckx David <david@coninckx.com>
#
#    The licence is in the file __manifest__.py
#
##############################################################################

import datetime

from odoo import models, fields, api


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    ##########################################################################
    #                                 FIELDS                                 #
    ##########################################################################
    extra_hours = fields.Float(compute='_compute_extra_hours',
                               store=True)
    extra_hours_lost = fields.Float(compute='_compute_extra_hours_lost',
                                    store=True)
    attendance_days_ids = fields.One2many('hr.attendance.day', 'employee_id',
                                          "Attendance day")
    annual_balance = fields.Float()

    extra_hours_formatted = fields.Char(string="Balance",
                                        compute='_compute_formatted_hours')

    time_warning_balance = fields.Char(compute='_compute_time_warning_balance')

    time_warning_today = fields.Char(compute='_compute_time_warning_today')

    extra_hours_today = fields.Char(compute='_compute_extra_hours_today')

    today_hour = fields.Char(compute='_compute_today_hour')

    today_hour_formatted = fields.Char(compute='_compute_today_hour_formatted')

    ##########################################################################
    #                             FIELDS METHODS                             #
    ##########################################################################

    @api.multi
    @api.depends('attendance_days_ids.extra_hours', 'annual_balance')
    def _compute_extra_hours(self):
        for employee in self:

            start_year = datetime.date.today().replace(month=1, day=1)
            start_year = fields.Date.to_string(start_year)
            yesterday = datetime.date.today() - datetime.timedelta(days=1)
            yesterday = fields.Date.to_string(yesterday)

            attendance_day_ids = employee.attendance_days_ids.filtered(
                lambda r: start_year <= r.date <= yesterday)

            extra_hours_sum = sum(attendance_day_ids.mapped('extra_hours'))
            extra_hours_lost_sum = sum(attendance_day_ids.
                                       mapped('extra_hours_lost'))

            employee.extra_hours = extra_hours_sum + \
                employee.annual_balance - extra_hours_lost_sum

    @api.multi
    @api.depends('attendance_days_ids.extra_hours_lost')
    def _compute_extra_hours_lost(self):
        for employee in self:
            employee.extra_hours_lost = sum(
                employee.attendance_days_ids.mapped('extra_hours_lost') or [0])

    @api.model
    def _cron_create_attendance(self):
        att_day = self.env['hr.attendance.day']
        employees = self.search([])
        today = fields.Date.today()
        for employee in employees:
            att_days = att_day.search(
                [('name', '=', today), ('employee_id', '=', employee.id)])
            if not att_days:
                att_day.create({
                    'date': today,
                    'employee_id': employee.id
                })

    @api.multi
    @api.depends('today_hour')
    def _compute_extra_hours_today(self):
        for employee in self:
            employee.extra_hours_today = \
                '-' if float(employee.today_hour) < 0 else ''
            employee.extra_hours_today += employee. \
                convert_hour_to_time(employee.today_hour)

    @api.multi
    def _compute_time_warning_balance(self):
        for employee in self:
            if employee.extra_hours < 0:
                employee.time_warning_balance = 'red'
            elif employee.extra_hours >= 19:
                employee.time_warning_balance = 'orange'
            else:
                employee.time_warning_balance = 'green'

    @api.multi
    @api.depends('today_hour')
    def _compute_time_warning_today(self):
        for employee in self:
            employee.time_warning_today = \
                'red' if float(employee.today_hour) < 0 else 'green'

    @api.multi
    def _compute_today_hour(self):
        for employee in self:
            current_att_day = self.env['hr.attendance.day'].search([
                ('employee_id', '=', employee.id),
                ('date', '=', fields.Date.today())])
            employee.today_hour = \
                employee.compute_today_hour() - current_att_day.due_hours

    @api.multi
    def _compute_formatted_hours(self):
        for employee in self:
            employee.extra_hours_formatted = \
                '-' if employee.extra_hours < 0 else ''
            employee.extra_hours_formatted += \
                employee.convert_hour_to_time(abs(employee.extra_hours))

    @api.multi
    @api.depends('today_hour')
    def _compute_today_hour_formatted(self):
        for employee in self:
            today_hour = employee.compute_today_hour()
            thf = '-' if today_hour < 0 else ''
            thf += employee.convert_hour_to_time(float(today_hour))
            employee.today_hour_formatted = thf

    @api.multi
    def convert_hour_to_time(self, hour):
        hour = float(hour)
        return '{:02d}:{:02d}'.format(*divmod(int(abs(hour * 60)), 60))

    @api.multi
    def compute_today_hour(self):
        self.ensure_one()

        today = fields.Date.today()
        attendances_today = self.env['hr.attendance'].search([
            ('employee_id', '=', self.id), ('check_in', '>=', today)])
        worked_hours = 0

        for attendance in attendances_today:
            if attendance.check_out:
                worked_hours += attendance.worked_hours
            else:
                delta = datetime.datetime.now() \
                    - fields.Datetime.from_string(attendance.check_in)
                worked_hours += delta.total_seconds() / 3600.0

        return worked_hours
