# -*- coding: utf-8 -*-

from odoo import models, api
import logging

_logger = logging.getLogger(__name__)


class MailThreadAudit(models.AbstractModel):
    """
    Override mail.thread to catch message_post calls for chatter tracking.
    """
    _inherit = 'mail.thread'

    def message_post(self, **kwargs):
        """Override message_post to log chatter messages"""
        result = super(MailThreadAudit, self).message_post(**kwargs)

        # Check if this model should be tracked
        should_track = False
        try:
            should_track = self.env['audit.log.config'].is_model_tracked(self._name)
        except Exception as e:
            _logger.debug(f"Error checking should_track: {e}")

        if should_track:
            try:
                # Check if there's a message body or subject
                if kwargs.get('body') or kwargs.get('subject'):
                    self._log_message(kwargs)

                # Check for attachments in the result
                if result and hasattr(result, 'attachment_ids') and result.attachment_ids:
                    self._log_attachments_from_message(result.attachment_ids)
            except Exception as e:
                _logger.warning(f"Error logging message/attachments for {self._name}: {e}")

        return result
