# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AuditConfiguration(models.Model):
    _name = 'audit.log.config'
    _description = 'Audit Configuration'

    name = fields.Char(string='Configuration Name', required=True, default='Audit Configuration')

    model_ids = fields.Many2many(
        'ir.model',
        'audit_config_model_rel',
        'config_id',
        'model_id',
        string='Models to Track',
        domain=[('transient', '=', False)],
        help='Select models to track all their changes'
    )

    active = fields.Boolean(string='Active', default=True)

    @api.model
    def get_tracked_models(self):
        """Get list of tracked model names"""
        config = self.search([('active', '=', True)], limit=1)
        if config and config.model_ids:
            return config.model_ids.mapped('model')
        return []

    @api.model
    def is_model_tracked(self, model_name):
        """Check if a model is tracked"""
        tracked_models = self.get_tracked_models()
        return model_name in tracked_models
