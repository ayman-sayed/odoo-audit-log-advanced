# -*- coding: utf-8 -*-
{
    'name': 'Advanced Audit Log - Track All Changes',
    'version': '18.0.1.0.0',
    'category': 'Tools',
    'summary': 'Comprehensive audit logging system to track all changes, messages, and attachments on any Odoo model',
    'description': """
Advanced Audit Log - Professional Audit Trail System
=====================================================

Track Every Action in Your Odoo System
---------------------------------------
A powerful, flexible, and easy-to-use audit logging system that helps you maintain complete transparency
and compliance by tracking all changes, messages, and attachments across your Odoo database.

Key Features
------------
✓ **Configurable Tracking**: Enable tracking for any model through simple UI configuration
✓ **Complete Action Tracking**: Track Create, Update, Delete operations
✓ **Field-Level Tracking**: Monitor specific fields or all fields per model
✓ **Message Tracking**: Log all chatter messages and communications
✓ **Attachment Tracking**: Track file uploads and downloads
✓ **User Activity Monitoring**: See who did what and when
✓ **Advanced Filtering**: Filter by date, user, action type, model, and more
✓ **Compliance Ready**: Perfect for audit requirements and regulatory compliance
✓ **Easy to Use**: No technical knowledge required - configure through UI

What You Can Track
------------------
• Record creation with all initial values
• Field changes with old → new value comparison
• Record deletion with final values before deletion
• Chatter messages (comments, notes, emails)
• File attachments with metadata
• User information and timestamp for every action
• Company and Operating Unit context

Perfect For
-----------
• Financial institutions requiring audit trails
• Companies needing compliance documentation (ISO, SOX, GDPR)
• Organizations tracking critical business operations
• Businesses requiring accountability and transparency
• Teams needing detailed change history

How It Works
------------
1. Install the module
2. Go to Audit Logs → Configuration
3. Select models you want to track
4. Choose which actions to track (Create/Write/Delete/Messages/Attachments)
5. Optionally select specific fields to monitor
6. Done! All changes are automatically logged

Use Cases
---------
📊 **Finance**: Track all changes to invoices, payments, journal entries
👥 **HR**: Monitor employee record changes, salary modifications
📦 **Inventory**: Log stock movements, transfer approvals, quantity adjustments
💼 **Sales**: Track quotation changes, order modifications, delivery confirmations
🔐 **Security**: Maintain complete audit trail for security compliance

Technical Highlights
--------------------
• Lightweight and optimized for performance
• Automatic tracking through Python inheritance
• Configurable per model without code changes
• Clean and intuitive interface
• Easy integration with existing Odoo installations
• No database structure modifications required

Support & Documentation
-----------------------
• Comprehensive user guide included
• Video tutorials available
• Professional support available
• Regular updates and improvements
    """,
    'author': 'The Light',
    'maintainer': 'The Light',
    'website': 'https://www.thelight.odoo.com',
    'support': 'info@thelight-egy.com',

    # Pricing
    'price': 30.00,
    'currency': 'USD',

    # Images
    'images': [
        'static/description/banner.png',
        'static/description/icon.png',
    ],

    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/audit_log_views.xml',
        'views/audit_config_views.xml',
        'data/default_config.xml',
    ],

    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',

    # Additional metadata for Odoo Apps
    'live_test_url': 'https://demo.thelight.tech/audit_log',
    'external_dependencies': {
        'python': [],
    },
}
