#!/bin/bash
# Script to upload audit_log_advanced module to GitHub
# استبدل YOUR_USERNAME باسم المستخدم بتاعك على GitHub

set -e  # Stop on error

echo "🚀 Starting upload process for audit_log_advanced module..."

# التأكد إننا في المجلد الصحيح
cd /home/ayman/odoo/odoo18/Vision-express/audit_log_advanced

# 1. Initialize Git
echo "📦 Initializing Git repository..."
git init

# 2. Create branch 18.0 (IMPORTANT!)
echo "🌿 Creating branch 18.0..."
git checkout -b 18.0

# 3. Create .gitignore
echo "📝 Creating .gitignore..."
cat > .gitignore << 'EOF'
# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class
*.so
.Python

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
*.manifest
*.spec

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Translations
*.mo
*.pot

# Odoo
.odoo_test/

# Scrapy stuff:
.scrapy

# Sphinx documentation
docs/_build/

# PyBuilder
target/

# Jupyter Notebook
.ipynb_checkpoints

# pyenv
.python-version

# celery beat schedule file
celerybeat-schedule

# SageMath parsed files
*.sage.py

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# Spyder project settings
.spyderproject
.spyproject

# Rope project settings
.ropeproject

# mkdocs documentation
/site

# mypy
.mypy_cache/
.dmypy.json
dmypy.json

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
Thumbs.db

# SVG source files (keep only PNG)
*.svg
EOF

# 4. Add all files
echo "➕ Adding all files..."
git add .

# 5. Commit
echo "💾 Creating initial commit..."
git commit -m "Initial release: Advanced Audit Log v18.0.1.0.0

🎯 Features:
- Configurable audit logging for any Odoo model
- Track Create/Write/Delete operations with full detail
- Field-level tracking with old → new value comparison
- Track chatter messages and communications
- Track file attachments with complete metadata
- User activity monitoring with precise timestamps
- Advanced filtering by date, user, action type, model
- Compliance ready (ISO, SOX, GDPR)
- Easy to use - no technical knowledge required

💰 Price: \$30.00 USD
📜 License: LGPL-3
🏢 Author: The Light
📧 Support: info@thelight-eg.com
🌐 Website: https://www.thelight.odoo.com

Perfect for:
- Financial institutions requiring audit trails
- Companies needing compliance documentation
- Organizations tracking critical operations
- Businesses requiring accountability

Technical highlights:
- Lightweight and optimized for performance
- Automatic tracking through Python inheritance
- Configurable per model without code changes
- Clean and intuitive interface
- No database structure modifications required
"

echo ""
echo "✅ Git repository initialized successfully!"
echo ""
echo "📌 Next steps:"
echo "1. استبدل YOUR_USERNAME باسم المستخدم بتاعك في السطر التالي:"
echo "2. انسخ والصق الأوامر دي في الـ Terminal:"
echo ""
echo "   cd /home/ayman/odoo/odoo18/Vision-express/audit_log_advanced"
echo "   git remote add origin https://github.com/YOUR_USERNAME/odoo-audit-log-advanced.git"
echo "   git push -u origin 18.0"
echo ""
echo "3. بعد الرفع، روح على Odoo Apps وسجل الـ Repository:"
echo "   ssh://git@github.com/YOUR_USERNAME/odoo-audit-log-advanced.git#18.0"
echo ""
echo "🎉 Good luck!"
