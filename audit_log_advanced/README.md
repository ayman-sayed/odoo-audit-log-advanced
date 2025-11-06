# Advanced Audit Log Module

## Description

A flexible and configurable audit logging system for Odoo that allows you to track all actions on any model through a simple configuration interface.

---

## Features

### 1. **Configurable Tracking**
- Configure audit logging for any Odoo model through UI
- No code changes required to add new models
- Enable/disable tracking per model with a simple toggle

### 2. **Comprehensive Action Tracking**
- **Create**: Log when new records are created
- **Write**: Log field changes with old and new values
- **Delete**: Log when records are deleted
- **Messages**: Track chatter messages
- **Attachments**: Track file uploads

### 3. **Granular Field Selection**
- Select specific fields to track per model
- Or track all fields if no specific fields are selected
- Easy field management through UI

### 4. **Detailed Information**
- User who performed the action
- Date and time of action
- Field name and description
- Old value and new value
- Company and Operating Unit context

### 5. **User-Friendly Interface**
- Clean and intuitive views
- Advanced filtering and search
- Group by various criteria
- Separate views for each tracked model

---

## Installation

1. Place the module in your Odoo addons directory
2. Update the app list in Odoo
3. Install the module from Apps menu

```bash
# Update module list
odoo-bin -u audit_log_advanced -d your_database_name
```

---

## Configuration

### Adding Models to Track

1. Go to **Audit Logs → Configuration**
2. Click **Create**
3. Select the model you want to track
4. Configure tracking options:
   - **Active**: Enable/disable tracking
   - **Track Create**: Log record creation
   - **Track Write**: Log field changes
   - **Track Delete**: Log record deletion
   - **Track Messages**: Log chatter messages
   - **Track Attachments**: Log file attachments
5. Optionally select specific fields to track
6. Save

---

## Usage

### Viewing Audit Logs

After installation, you'll find a new menu: **Audit Logs**

#### Main Menus:
- **Audit Logs**: View all logs
- **Configuration**: Configure tracking settings

### Filters

**By Date:**
- Today
- This Week
- This Month

**By Action Type:**
- Create Actions
- Update Actions
- Delete Actions
- Messages
- Attachments

**Group By:**
- Model
- Action Type
- User
- Date
- Operating Unit
- Company

---

## Examples

### Example 1: Field Change
```
Date: 2025-11-05 14:30:00
User: Ahmed Mohamed
Model: Transfer Request
Record: WH000123
Action: Write
Field: State
Old Value: Draft
New Value: Checker
```

### Example 2: Chatter Message
```
Date: 2025-11-05 15:45:00
User: Mohamed Ali
Model: Transaction Deposit
Record: TD000456
Action: Message
Type: Comment
Body: "Confirmed by bank"
```

### Example 3: Attachment
```
Date: 2025-11-05 16:20:00
User: Sara Ahmed
Model: Transaction Withdrawal
Record: TW000789
Action: Attachment
File: bank_receipt.pdf
Type: application/pdf
```

---

## Technical Details

### Models

**audit.log**
- Main model for storing audit logs

**audit.log.config**
- Configuration model for tracking settings

**base.model.audit**
- Abstract mixin model that adds audit functionality

---

## Extending the Module

To add tracking to a new model:

1. **Through UI** (Recommended):
   - Go to Configuration and add the model

2. **Through Code**:
   ```python
   class YourModel(models.Model):
       _name = 'your.model'
       _inherit = ['your.model', 'base.model.audit']
   ```

---

## Permissions

- **Normal Users**: Read-only access to audit logs
- **System Administrators**: Full access to logs and configuration

---

## Dependencies

- base
- mail

---

## Version

- **Version**: 18.0.1.0.0
- **Odoo Version**: 18.0
- **License**: LGPL-3
- **Author**: The Light

---

**Built with ❤️ by The Light**
