# -*- coding: utf-8 -*-

from odoo import models, api, SUPERUSER_ID
import logging

_logger = logging.getLogger(__name__)


class Base(models.AbstractModel):
    """
    Override base model to add dynamic audit logging.
    This will apply to ALL models automatically.
    """
    _inherit = 'base'

    def _should_track(self):
        """Check if this model should be tracked"""
        try:
            return self.env['audit.log.config'].is_model_tracked(self._name)
        except:
            return False

    @api.model_create_multi
    def create(self, vals_list):
        """Override create to log record creation"""
        records = super(Base, self).create(vals_list)

        if self._should_track():
            for record, vals in zip(records, vals_list):
                try:
                    record._log_audit('create', vals=vals)
                except Exception as e:
                    _logger.debug(f"Error creating audit log: {e}")

        return records

    def write(self, vals):
        """Override write to log field changes"""
        should_track = self._should_track()


        # Store old values if tracking
        old_values = {}
        if should_track:
            for record in self:
                old_values[record.id] = {
                    field: getattr(record, field, None)
                    for field in vals.keys()
                }

        result = super(Base, self).write(vals)

        # Log changes
        if should_track:
            for record in self:
                try:
                    record._log_audit('write', vals=vals, old_vals=old_values.get(record.id, {}))
                except Exception as e:
                    _logger.debug(f"Error creating audit log: {e}")

        return result

    def unlink(self):
        """Override unlink to log record deletion"""
        if self._should_track():
            for record in self:
                try:
                    record._log_audit('unlink')
                except Exception as e:
                    _logger.debug(f"Error creating audit log: {e}")

        return super(Base, self).unlink()

    def _log_audit(self, action_type, vals=None, old_vals=None):
        """Create audit log entry"""
        audit_log = self.env['audit.log'].sudo()

        for record in self:
            base_vals = {
                'model_name': self._name,
                'model_description': self._description or self._name,
                'record_id': record.id,
                'record_name': record._get_record_name(),
                'action_type': action_type,
                'company_id': record._get_company_id(),
                'operating_unit_id': record._get_operating_unit_id(),
            }

            if action_type == 'create':
                base_vals['action_description'] = f"Created: {base_vals['record_name']}"
                audit_log.create(base_vals)

            elif action_type == 'write' and vals:
                for field_name in vals.keys():
                    field = self._fields.get(field_name)
                    if not field or not field.store:
                        continue

                    old_value = old_vals.get(field_name) if old_vals else getattr(record, field_name, None)
                    new_value = vals.get(field_name)

                    # Special handling for attachment fields
                    if field.type in ['many2many', 'one2many'] and field.comodel_name == 'ir.attachment':
                        record._log_attachment_changes(audit_log, base_vals, field, field_name, old_value, new_value)
                        continue

                    # Special handling for binary fields (don't log the content, just that it changed)
                    if field.type == 'binary':
                        # Check if the field has a related attachment name field
                        attachment_name = None
                        if hasattr(record, f'{field_name}_filename'):
                            attachment_name = getattr(record, f'{field_name}_filename', None)

                        has_old = old_value is not False and old_value is not None
                        has_new = new_value is not False and new_value is not None

                        if has_old != has_new or (has_new and old_value != new_value):
                            audit_vals = base_vals.copy()
                            audit_vals.update({
                                'field_name': field_name,
                                'field_description': field.string,
                                'attachment_name': attachment_name or f'{field.string} file',
                                'action_type': 'attachment',
                                'old_value': 'File Present' if has_old else 'No File',
                                'new_value': 'File Present' if has_new else 'No File',
                                'action_description': f"{'Updated' if has_old and has_new else 'Added' if has_new else 'Removed'} file in {field.string}",
                            })
                            audit_log.create(audit_vals)
                        continue

                    old_str = record._format_field_value(field, old_value)
                    new_str = record._format_field_value(field, new_value)

                    if old_str != new_str:
                        audit_vals = base_vals.copy()
                        audit_vals.update({
                            'field_name': field_name,
                            'field_description': field.string,
                            'old_value': old_str,
                            'new_value': new_str,
                            'action_description': f"Changed {field.string} from '{old_str}' to '{new_str}'",
                        })
                        audit_log.create(audit_vals)

            elif action_type == 'unlink':
                base_vals['action_description'] = f"Deleted: {base_vals['record_name']}"
                audit_log.create(base_vals)

    def _log_attachment_changes(self, audit_log, base_vals, field, field_name, old_value, new_value):
        """Log changes in attachment fields"""
        try:
            # Get old and new attachment lists
            old_attachments = old_value if old_value else self.env['ir.attachment']

            # Parse new_value from vals (can be commands like [(4, id), (3, id)])
            if isinstance(new_value, list):
                new_attachment_ids = []
                removed_attachment_ids = []

                for command in new_value:
                    if isinstance(command, (list, tuple)) and len(command) > 0:
                        cmd = command[0]
                        if cmd == 4:  # Link existing (add)
                            new_attachment_ids.append(command[1])
                        elif cmd == 3:  # Unlink (remove)
                            removed_attachment_ids.append(command[1])
                        elif cmd == 6:  # Replace all
                            new_attachment_ids = command[2] if len(command) > 2 else []
                            if old_attachments:
                                removed_attachment_ids = old_attachments.ids

                # Log added attachments
                if new_attachment_ids:
                    attachments = self.env['ir.attachment'].browse(new_attachment_ids)
                    for attachment in attachments:
                        audit_vals = base_vals.copy()
                        audit_vals.update({
                            'action_type': 'attachment',
                            'attachment_name': attachment.name,
                            'attachment_mimetype': attachment.mimetype,
                            'action_description': f"Added attachment to {field.string}: {attachment.name}",
                        })
                        audit_log.create(audit_vals)

                # Log removed attachments
                if removed_attachment_ids:
                    attachments = self.env['ir.attachment'].browse(removed_attachment_ids)
                    for attachment in attachments:
                        if attachment.exists():
                            audit_vals = base_vals.copy()
                            audit_vals.update({
                                'action_type': 'attachment',
                                'attachment_name': attachment.name,
                                'action_description': f"Removed attachment from {field.string}: {attachment.name}",
                            })
                            audit_log.create(audit_vals)
        except Exception as e:
            _logger.debug(f"Error logging attachment changes: {e}")

    def _log_message(self, message_kwargs):
        """Log chatter message"""
        audit_log = self.env['audit.log'].sudo()

        for record in self:
            audit_vals = {
                'model_name': self._name,
                'model_description': self._description or self._name,
                'record_id': record.id,
                'record_name': record._get_record_name(),
                'action_type': 'message',
                'message_body': message_kwargs.get('body', ''),
                'message_type': message_kwargs.get('message_type', 'comment'),
                'action_description': f"Posted message: {message_kwargs.get('subject', 'No subject')}",
                'company_id': record._get_company_id(),
                'operating_unit_id': record._get_operating_unit_id(),
            }
            audit_log.create(audit_vals)

    def _log_attachments_from_message(self, attachment_ids):
        """Log attachments from message result"""
        audit_log = self.env['audit.log'].sudo()

        for record in self:
            for attachment in attachment_ids:
                try:
                    audit_vals = {
                        'model_name': self._name,
                        'model_description': self._description or self._name,
                        'record_id': record.id,
                        'record_name': record._get_record_name(),
                        'action_type': 'attachment',
                        'attachment_name': attachment.name,
                        'attachment_mimetype': attachment.mimetype,
                        'attachment_id': attachment.id,
                        'action_description': f"Added attachment via chatter: {attachment.name}",
                        'company_id': record._get_company_id(),
                        'operating_unit_id': record._get_operating_unit_id(),
                    }
                    audit_log.create(audit_vals)
                except Exception as e:
                    _logger.warning(f"Error logging attachment {attachment.name}: {e}")

    def _log_attachments(self, message_kwargs):
        """Log attachment additions"""
        audit_log = self.env['audit.log'].sudo()

        for record in self:
            # Handle attachment_ids
            if message_kwargs.get('attachment_ids'):
                attachments = self.env['ir.attachment'].browse(message_kwargs['attachment_ids'])
                for attachment in attachments:
                    audit_vals = {
                        'model_name': self._name,
                        'model_description': self._description or self._name,
                        'record_id': record.id,
                        'record_name': record._get_record_name(),
                        'action_type': 'attachment',
                        'attachment_name': attachment.name,
                        'attachment_mimetype': attachment.mimetype,
                        'action_description': f"Added attachment: {attachment.name}",
                        'company_id': record._get_company_id(),
                        'operating_unit_id': record._get_operating_unit_id(),
                    }
                    audit_log.create(audit_vals)

            # Handle attachments tuples
            if message_kwargs.get('attachments'):
                for attachment_tuple in message_kwargs['attachments']:
                    if len(attachment_tuple) >= 2:
                        filename = attachment_tuple[0]
                        audit_vals = {
                            'model_name': self._name,
                            'model_description': self._description or self._name,
                            'record_id': record.id,
                            'record_name': record._get_record_name(),
                            'action_type': 'attachment',
                            'attachment_name': filename,
                            'action_description': f"Added attachment: {filename}",
                            'company_id': record._get_company_id(),
                            'operating_unit_id': record._get_operating_unit_id(),
                        }
                        audit_log.create(audit_vals)

    def _format_field_value(self, field, value):
        """Format field value for display"""
        if value is False or value is None:
            return 'Empty'

        try:
            if field.type == 'many2one':
                if isinstance(value, int):
                    related_record = self.env[field.comodel_name].browse(value)
                    return related_record.display_name if related_record.exists() else str(value)
                elif hasattr(value, 'display_name'):
                    return value.display_name
            elif field.type == 'selection':
                if callable(field.selection):
                    selection = field.selection(self)
                else:
                    selection = field.selection
                selection_dict = dict(selection)
                return selection_dict.get(value, str(value))
            elif field.type in ['many2many', 'one2many']:
                if hasattr(value, 'mapped'):
                    names = value.mapped('display_name')
                    return ', '.join([str(n) for n in names]) if names else 'Empty'
            elif field.type == 'boolean':
                return 'Yes' if value else 'No'
            elif field.type in ['float', 'monetary']:
                return f"{value:.2f}"
        except Exception as e:
            _logger.debug(f"Error formatting value: {e}")

        return str(value)

    def _get_record_name(self):
        """Get record name safely"""
        try:
            if hasattr(self, 'name') and self.name:
                return self.name
            elif hasattr(self, 'display_name'):
                return self.display_name
        except:
            pass
        return f"{self._name} #{self.id}"

    def _get_company_id(self):
        """Get company ID safely"""
        try:
            if hasattr(self, 'company_id') and self.company_id:
                return self.company_id.id
        except:
            pass
        return False

    def _get_operating_unit_id(self):
        """Get operating unit ID safely"""
        try:
            if hasattr(self, 'operating_unit_id') and self.operating_unit_id:
                return self.operating_unit_id.id
        except:
            pass
        return False
