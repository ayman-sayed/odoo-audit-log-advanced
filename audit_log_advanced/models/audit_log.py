# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AuditLog(models.Model):
    _name = 'audit.log'
    _description = 'Audit Log'
    _order = 'action_date desc'
    _rec_name = 'action_description'

    # Basic Information
    model_name = fields.Char(string='Model Name', required=True, index=True)
    model_description = fields.Char(string='Model Description')
    record_id = fields.Integer(string='Record ID', required=True, index=True)
    record_name = fields.Char(string='Record Name')

    # Action Details
    action_type = fields.Selection([
        ('create', 'Create'),
        ('write', 'Update'),
        ('unlink', 'Delete'),
        ('message', 'Chatter Message'),
        ('attachment', 'Attachment'),
    ], string='Action Type', required=True, index=True)

    action_description = fields.Text(string='Action Description')

    # User Information
    user_id = fields.Many2one('res.users', string='User', required=True, default=lambda self: self.env.user, index=True)
    user_name = fields.Char(string='User Name', related='user_id.name', store=True)

    # Field Changes
    field_name = fields.Char(string='Field Name')
    field_description = fields.Char(string='Field Description')
    old_value = fields.Text(string='Old Value')
    new_value = fields.Text(string='New Value')

    # Message/Attachment Details
    message_body = fields.Html(string='Message Body')
    message_type = fields.Selection([
        ('email', 'Email'),
        ('comment', 'Comment'),
        ('notification', 'Notification'),
    ], string='Message Type')

    attachment_name = fields.Char(string='Attachment Name')
    attachment_mimetype = fields.Char(string='Attachment Type')
    attachment_id = fields.Many2one('ir.attachment', string='Attachment', ondelete='set null')
    attachment_url = fields.Char(string='Download Link', compute='_compute_attachment_url')

    # Timestamp
    action_date = fields.Datetime(string='Action Date', default=fields.Datetime.now, required=True, index=True)

    # Additional Context
    company_id = fields.Many2one('res.company', string='Company', index=True)
    operating_unit_id = fields.Many2one('operating.unit', string='Operating Unit', index=True)

    @api.depends('attachment_id')
    def _compute_attachment_url(self):
        """Compute download URL for attachment"""
        for record in self:
            if record.attachment_id:
                record.attachment_url = f'/web/content/{record.attachment_id.id}?download=true'
            else:
                record.attachment_url = False

    def name_get(self):
        """Custom display name for audit log records"""
        result = []
        for record in self:
            name = f"{record.model_description or record.model_name} - {record.action_type.title()} by {record.user_name}"
            result.append((record.id, name))
        return result
