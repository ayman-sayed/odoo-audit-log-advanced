===============================================
Advanced Audit Log - Track All Changes
===============================================

.. image:: https://img.shields.io/badge/license-LGPL--3-blue.svg
   :target: https://www.gnu.org/licenses/lgpl-3.0-standalone.html
   :alt: License: LGPL-3

.. image:: https://img.shields.io/badge/Odoo-18.0-blue.svg
   :target: https://odoo.com/page/download
   :alt: Odoo 18.0

Track Every Action in Your Odoo System
=======================================

A powerful, flexible, and easy-to-use **audit logging system** that helps you maintain
complete transparency and compliance by tracking all changes, messages, and attachments
across your Odoo database.

**Table of contents**

.. contents::
   :local:

Key Features
============

* **Configurable Tracking**: Enable tracking for any model through simple UI configuration
* **Complete Action Tracking**: Track Create, Update, Delete operations
* **Field-Level Tracking**: Monitor specific fields or all fields per model
* **Message Tracking**: Log all chatter messages and communications
* **Attachment Tracking**: Track file uploads and downloads
* **User Activity Monitoring**: See who did what and when
* **Advanced Filtering**: Filter by date, user, action type, model, and more
* **Compliance Ready**: Perfect for audit requirements and regulatory compliance
* **Easy to Use**: No technical knowledge required - configure through UI

What You Can Track
==================

* Record creation with all initial values
* Field changes with old → new value comparison
* Record deletion with final values before deletion
* Chatter messages (comments, notes, emails)
* File attachments with metadata
* User information and timestamp for every action
* Company and Operating Unit context

Perfect For
===========

* 📊 **Finance**: Track all changes to invoices, payments, journal entries
* 👥 **HR**: Monitor employee record changes, salary modifications
* 📦 **Inventory**: Log stock movements, transfer approvals, quantity adjustments
* 💼 **Sales**: Track quotation changes, order modifications, delivery confirmations
* 🔐 **Security**: Maintain complete audit trail for security compliance

Configuration
=============

Installation
------------

1. Purchase and download the module from Odoo Apps
2. Upload to your Odoo instance
3. Update the app list in Odoo
4. Install the module from Apps menu

Adding Models to Track
-----------------------

1. Go to **Audit Logs → Configuration**
2. Click **Create**
3. Select the model you want to track
4. Configure tracking options:

   * **Active**: Enable/disable tracking
   * **Track Create**: Log record creation
   * **Track Write**: Log field changes
   * **Track Delete**: Log record deletion
   * **Track Messages**: Log chatter messages
   * **Track Attachments**: Log file attachments

5. Optionally select specific fields to track
6. Save

Usage
=====

Viewing Audit Logs
------------------

After installation, you'll find a new menu: **Audit Logs**

Main Menus
~~~~~~~~~~

* **Audit Logs**: View all logs
* **Configuration**: Configure tracking settings

Filters
~~~~~~~

**By Date:**

* Today
* This Week
* This Month

**By Action Type:**

* Create Actions
* Update Actions
* Delete Actions
* Messages
* Attachments

**Group By:**

* Model
* Action Type
* User
* Date
* Operating Unit
* Company

Examples
========

Example 1: Field Change
-----------------------

::

   Date: 2025-11-05 14:30:00
   User: Ahmed Mohamed
   Model: Transfer Request
   Record: WH000123
   Action: Write
   Field: State
   Old Value: Draft
   New Value: Checker

Example 2: Chatter Message
---------------------------

::

   Date: 2025-11-05 15:45:00
   User: Mohamed Ali
   Model: Transaction Deposit
   Record: TD000456
   Action: Message
   Type: Comment
   Body: "Confirmed by bank"

Example 3: Attachment
---------------------

::

   Date: 2025-11-05 16:20:00
   User: Sara Ahmed
   Model: Transaction Withdrawal
   Record: TW000789
   Action: Attachment
   File: bank_receipt.pdf
   Type: application/pdf

Technical Details
=================

Models
------

**audit.log**
  Main model for storing audit logs

**audit.log.config**
  Configuration model for tracking settings

**base.model.audit**
  Abstract mixin model that adds audit functionality

Extending the Module
--------------------

To add tracking to a new model:

**Through UI** (Recommended):
  Go to Configuration and add the model

**Through Code**:

.. code-block:: python

   class YourModel(models.Model):
       _name = 'your.model'
       _inherit = ['your.model', 'base.model.audit']

Dependencies
============

* base
* mail

Known issues / Roadmap
======================

* Add export functionality for audit logs
* Add email notifications for critical changes
* Add dashboard with audit statistics
* Add API for external audit systems

Bug Tracker
===========

Bugs are tracked on `GitHub Issues <https://github.com/yourusername/audit_log_advanced/issues>`_.

In case of trouble, please check there if your issue has already been reported.
If you spotted it first, help us smash it by providing detailed and welcomed feedback.

Credits
=======

Authors
~~~~~~~

* The Light

Contributors
~~~~~~~~~~~~

* The Light <support@thelight.tech>

Maintainers
~~~~~~~~~~~

This module is maintained by **The Light**.

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

To contribute to this module, please visit https://www.thelight.odoo.com.

License
=======

This module is licensed under the LGPL-3 license.

For more information, please see the LICENSE file in the module directory.
