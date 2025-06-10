#!/bin/bash

echo "🚀 Deploying Digital Contact Cards to GitHub Pages..."

# Regenerate contact cards
echo "📊 Regenerating contact cards..."
python scripts/generate_contact_cards.py

# Copy files to deployment directories
echo "📁 Copying files to deployment directories..."
cp output/html/* html/
cp output/vcf/* vcf/

echo "✅ Deployment preparation complete!"
echo ""
echo "Next steps:"
echo "1. git add ."
echo "2. git commit -m \"Update contact cards\""
echo "3. git push origin main"
echo ""
echo "Your GitHub Pages site will update automatically in a few minutes." 