# -*- coding: utf-8 -*-

from odoo import models, api
import logging

_logger = logging.getLogger(__name__)


class IrAttachmentAudit(models.Model):
    """
    Override ir.attachment to track attachment uploads.
    """
    _inherit = 'ir.attachment'

    @api.model_create_multi
    def create(self, vals_list):
        """Override create to log attachment creation"""
        attachments = super(IrAttachmentAudit, self).create(vals_list)

        for attachment, vals in zip(attachments, vals_list):
            try:
                # Check if this attachment is linked to a tracked model
                res_model = vals.get('res_model') or attachment.res_model
                res_id = vals.get('res_id') or attachment.res_id
                res_field = vals.get('res_field') or attachment.res_field

                # Skip if this is a binary field attachment (will be logged by write method)
                if res_field:
                    continue

                if res_model and res_id:
                    # Check if the model is tracked
                    is_tracked = self.env['audit.log.config'].is_model_tracked(res_model)

                    if is_tracked:
                        # Get the record to log the attachment
                        record = self.env[res_model].browse(res_id)
                        if record.exists():
                            audit_log = self.env['audit.log'].sudo()

                            audit_vals = {
                                'model_name': res_model,
                                'model_description': record._description or res_model,
                                'record_id': res_id,
                                'record_name': record.display_name if hasattr(record, 'display_name') else f"{res_model} #{res_id}",
                                'action_type': 'attachment',
                                'attachment_name': attachment.name,
                                'attachment_mimetype': attachment.mimetype,
                                'attachment_id': attachment.id,
                                'action_description': f"Added attachment: {attachment.name}",
                                'company_id': record._get_company_id() if hasattr(record, '_get_company_id') else False,
                                'operating_unit_id': record._get_operating_unit_id() if hasattr(record, '_get_operating_unit_id') else False,
                            }

                            audit_log.create(audit_vals)
            except Exception as e:
                _logger.warning(f"Error logging attachment creation: {e}")

        return attachments

    def unlink(self):
        """Override unlink to log attachment deletion"""
        for attachment in self:
            try:
                res_model = attachment.res_model
                res_id = attachment.res_id

                if res_model and res_id:
                    # Check if the model is tracked
                    is_tracked = self.env['audit.log.config'].is_model_tracked(res_model)

                    if is_tracked:
                        # Get the record to log the attachment deletion
                        record = self.env[res_model].browse(res_id)
                        if record.exists():
                            audit_log = self.env['audit.log'].sudo()

                            audit_vals = {
                                'model_name': res_model,
                                'model_description': record._description or res_model,
                                'record_id': res_id,
                                'record_name': record.display_name if hasattr(record, 'display_name') else f"{res_model} #{res_id}",
                                'action_type': 'attachment',
                                'attachment_name': attachment.name,
                                'attachment_mimetype': attachment.mimetype,
                                'attachment_id': attachment.id,
                                'action_description': f"Deleted attachment: {attachment.name}",
                                'company_id': record._get_company_id() if hasattr(record, '_get_company_id') else False,
                                'operating_unit_id': record._get_operating_unit_id() if hasattr(record, '_get_operating_unit_id') else False,
                            }

                            audit_log.create(audit_vals)
            except Exception as e:
                _logger.warning(f"Error logging attachment deletion: {e}")

        return super(IrAttachmentAudit, self).unlink()
