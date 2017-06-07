# -*- encoding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2016 Compassion CH (http://www.compassion.ch)
#    Releasing children from poverty in Jesus' name
#    @author: Emanuel Cino <ecino@compassion.ch>
#
#    The licence is in the file __openerp__.py
#
##############################################################################
import base64

from openerp import api, models, fields
import logging


logger = logging.getLogger(__name__)


class CommunicationAttachment(models.Model):
    _name = 'partner.communication.attachment'
    _description = 'Communication Attachment'

    ##########################################################################
    #                                 FIELDS                                 #
    ##########################################################################
    name = fields.Char(required=True)
    communication_id = fields.Many2one(
        'partner.communication.job', 'Communication', required=True,
        ondelete='cascade')
    report_name = fields.Char(
        required=True, help='Identifier of the report used to print')
    attachment_id = fields.Many2one(
        'ir.attachment', string="Attachments", required=True)
    data = fields.Binary(compute='_compute_data')

    def _compute_data(self):
        for attachment in self:
            attachment.data = base64.b64decode(attachment.attachment_id.datas)

    @api.model
    def create(self, vals):
        """
        Allows to send binary data for attachment instead of record.
        :param vals: vals for creation
        :return: record created
        """
        if 'data' in vals and 'attachment_id' not in vals:
            name = vals['name']
            attachment = self.env['ir.attachment'].create({
                'datas_fname': name,
                'res_model': self._name,
                'datas': vals['data'],
                'name': name
            })
            vals['attachment_id'] = attachment.id

        res = super(CommunicationAttachment, self).create(vals)
        res.attachment_id.res_id = res.id
        return res

    @api.multi
    def print_attachments(self):
        report_obj = self.env['report']
        for attachment in self:
            report = report_obj._get_report_from_name(attachment.report_name)
            behaviour = report.behaviour()[report.id]
            printer = behaviour['printer']
            if printer:
                printer.with_context(
                    print_name=self.env.user.firstname[:3] + ' ' +
                    attachment.name
                ).print_document(
                    report, attachment.data, report.report_type)
        return True
