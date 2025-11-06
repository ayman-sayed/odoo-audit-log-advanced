#!/bin/bash
# Script to clean and re-commit the module properly

set -e

echo "🧹 Cleaning repository for fresh submission..."

cd /home/ayman/odoo/odoo18/odoo-audit-log-advanced/audit_log_advanced

# Remove git history
echo "📦 Removing old git history..."
rm -rf .git

# Re-initialize
echo "🔄 Re-initializing git repository..."
git init
git checkout -b 18.0

# Create proper .gitignore
echo "📝 Creating .gitignore..."
cat > .gitignore << 'EOF'
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class
*.so

# Odoo
*.pyc
*.pyo
.odoo_test/

# IDEs
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Keep only PNG, not SVG source files
*.svg

# Temp files
*~
*.bak
*.orig

# Logs
*.log

# Documentation build
docs/_build/
EOF

# Add all files
echo "➕ Adding files..."
git add .

# Create clean commit
echo "💾 Creating clean commit..."
git commit -m "Release: Advanced Audit Log v18.0.1.0.0

Professional audit trail system for Odoo 18.0

🎯 Features:
✓ Configurable tracking for any Odoo model
✓ Track Create/Write/Delete operations
✓ Field-level tracking with old → new value comparison
✓ Track chatter messages and communications
✓ Track file attachments with complete metadata
✓ User activity monitoring with timestamps
✓ Advanced filtering and search capabilities
✓ Compliance ready (ISO, SOX, GDPR)
✓ Easy to use - no technical knowledge required

💰 Price: \$30 USD
📜 License: LGPL-3
🏢 Author: The Light
📧 Support: info@thelight-eg.com
🌐 Website: https://www.thelight.odoo.com

Perfect for financial institutions, healthcare providers,
government organizations, and any business requiring
complete audit trails for compliance and security.

Technical highlights:
• Lightweight and optimized for performance
• Automatic tracking through Python inheritance
• Configurable per model without code changes
• Clean and intuitive user interface
• Easy integration with existing Odoo installations
• No database structure modifications required
• Compatible with Odoo 18.0 Community and Enterprise
"

echo ""
echo "✅ Repository cleaned and ready!"
echo ""
echo "📌 Next step: Force push to GitHub"
echo ""
echo "Run these commands:"
echo "  git remote add origin git@github.com:ayman-sayed/odoo-audit-log-advanced.git"
echo "  git push -f origin 18.0"
echo ""
echo "⚠️  Warning: This will overwrite the remote branch!"
echo ""
