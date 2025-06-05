#!/usr/bin/env python3
"""
Apple Wallet Pass Generator

This script automates the creation of Apple Wallet pass bundles (.pkpass preparation) 
for multiple team members from a CSV data source.

The generated passes will contain:
- QR codes linking to individual contact card pages
- Contact information displayed on the pass
- Company branding and styling

Usage:
    python generate_wallet_passes.py

Requirements:
    - team_data.csv file in the root directory
    - Company logo and icons in assets directory
    - Pass Type ID and Team ID from Apple Developer Account holder
    - Updated config_wallet_passes.py with correct values

Output:
    - Individual pass folders ready for signing
    - Each folder contains pass.json and required image assets
"""

import csv
import json
import os
import re
import shutil
import sys
import uuid
from pathlib import Path
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO

# Import configuration
sys.path.append(str(Path(__file__).parent.parent))
try:
    import config_wallet_passes as config
except ImportError:
    print("❌ Error: config_wallet_passes.py not found!")
    print("Please make sure config_wallet_passes.py exists in the project root.")
    sys.exit(1)


class WalletPassGenerator:
    def __init__(self, base_dir=None):
        """Initialize the generator with directory paths."""
        if base_dir is None:
            base_dir = Path(__file__).parent.parent
        else:
            base_dir = Path(base_dir)
        
        self.base_dir = base_dir
        self.output_dir = base_dir / "wallet_passes"
        self.assets_dir = base_dir / "assets"
        self.csv_file = base_dir / "team_data.csv"
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
    
    def clean_filename(self, first_name, last_name):
        """Generate a clean filename from first and last name."""
        filename = f"{first_name}-{last_name}".lower()
        filename = re.sub(r'[^a-z0-9\-]', '', filename)
        filename = re.sub(r'-+', '-', filename)
        return filename.strip('-')
    
    def read_csv_data(self):
        """Read team data from CSV file."""
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                return list(reader)
        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file not found: {self.csv_file}")
    
    def generate_serial_number(self):
        """Generate a unique serial number for the pass."""
        return str(uuid.uuid4())
    
    def create_pass_json(self, member_data):
        """Create the pass.json content for a team member."""
        filename = self.clean_filename(member_data['first_name'], member_data['last_name'])
        
        # QR code message - link to their contact page
        qr_message = f"{config.GITHUB_PAGES_URL}/html/{filename}.html"
        
        # Create pass structure
        pass_data = {
            "passTypeIdentifier": config.PASS_TYPE_IDENTIFIER,
            "formatVersion": 1,
            "organizationName": config.ORGANIZATION_NAME,
            "teamIdentifier": config.TEAM_IDENTIFIER,
            "serialNumber": self.generate_serial_number(),
            "description": config.PASS_DESCRIPTION,
            
            # Barcode (QR code)
            "barcode": {
                "message": qr_message,
                "format": "PKBarcodeFormatQR",
                "messageEncoding": "iso-8859-1"
            },
            
            # Alternative barcodes for older devices
            "barcodes": [
                {
                    "message": qr_message,
                    "format": "PKBarcodeFormatQR",
                    "messageEncoding": "iso-8859-1"
                }
            ],
            
            # Visual appearance from config
            "backgroundColor": config.PASS_STYLING["backgroundColor"],
            "foregroundColor": config.PASS_STYLING["foregroundColor"],
            "labelColor": config.PASS_STYLING["labelColor"],
            
            # Generic pass structure
            "generic": {
                "primaryFields": [
                    {
                        "key": "name",
                        "label": "NAME",
                        "value": f"{member_data['first_name']} {member_data['last_name']}"
                    },
                    {
                        "key": "title",
                        "label": "TITLE",
                        "value": member_data['title']
                    }
                ],
                "secondaryFields": [],
                "auxiliaryFields": [],
                "backFields": []
            }
        }
        
        # Keep the pass minimal and professional - only name, title, logo, and QR code
        # No additional fields to maintain clean appearance
        
        # Add web service URL if configured
        if config.WEB_SERVICE_URL:
            pass_data["webServiceURL"] = config.WEB_SERVICE_URL
            pass_data["authenticationToken"] = config.AUTHENTICATION_TOKEN
        
        return pass_data
    
    def download_and_resize_image(self, url, output_path, target_size):
        """Download an image from URL and resize it to target dimensions."""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            
            image = Image.open(BytesIO(response.content))
            
            # Convert to RGB if necessary (for PNG with transparency)
            if image.mode in ('RGBA', 'LA'):
                background = Image.new('RGB', image.size, (255, 255, 255))
                background.paste(image, mask=image.split()[-1] if image.mode == 'RGBA' else None)
                image = background
            elif image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Resize maintaining aspect ratio
            image.thumbnail(target_size, Image.Resampling.LANCZOS)
            
            # Create final image with exact target size (padding if needed)
            final_image = Image.new('RGB', target_size, (255, 255, 255))
            paste_x = (target_size[0] - image.width) // 2
            paste_y = (target_size[1] - image.height) // 2
            final_image.paste(image, (paste_x, paste_y))
            
            final_image.save(output_path,
                             optimize=False,          # don't strip chunks
                             compress_level=0)        # PNG, lossless, no extra squeeze
            return True
        except Exception as e:
            print(f"Error downloading/processing image from {url}: {e}")
            return False
    
    def create_default_icon(self, output_path, size, text="S"):
        """Create a default icon with company initial."""
        image = Image.new('RGB', size, (25, 25, 25))  # Dark background
        draw = ImageDraw.Draw(image)
        
        # Try to use a nice font, fall back to default
        try:
            font_size = size[0] // 2
            font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", font_size)
        except:
            font = ImageFont.load_default()
        
        # Calculate text position to center it
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (size[0] - text_width) // 2
        y = (size[1] - text_height) // 2
        
        draw.text((x, y), text, fill=(255, 255, 255), font=font)
        image.save(output_path)
    
    def prepare_pass_images(self, member_data, pass_folder):
        """Prepare all required images for the pass."""
        # Use image specs from config
        image_specs = config.IMAGE_SPECS
        
        # Try to download company logo
        logo_url = member_data.get('company_logo_url')
        logo_created = False
        
        if logo_url:
            # Create logo images
            for logo_name in ["logo.png", "logo@2x.png", "logo@3x.png"]:
                logo_path = pass_folder / logo_name
                target_size = image_specs[logo_name]
                if self.download_and_resize_image(logo_url, logo_path, target_size):
                    logo_created = True
        
        if not logo_created:
            # Create default logo with company initial
            company_initial = member_data['company_name'][0].upper() if member_data['company_name'] else "S"
            for logo_name in ["logo.png", "logo@2x.png", "logo@3x.png"]:
                logo_path = pass_folder / logo_name
                target_size = image_specs[logo_name]
                self.create_default_icon(logo_path, target_size, company_initial)
        
        # Create icon images (can be same as logo or different)
        for icon_name in ["icon.png", "icon@2x.png", "icon@3x.png"]:
            icon_path = pass_folder / icon_name
            target_size = image_specs[icon_name]
            
            # Try to use logo first, then create default
            if logo_created and logo_url:
                if not self.download_and_resize_image(logo_url, icon_path, target_size):
                    self.create_default_icon(icon_path, target_size, member_data['first_name'][0].upper())
            else:
                self.create_default_icon(icon_path, target_size, member_data['first_name'][0].upper())
    
    def generate_pass_bundle(self, member_data):
        """Generate a complete pass bundle for a team member."""
        filename = self.clean_filename(member_data['first_name'], member_data['last_name'])
        pass_folder = self.output_dir / f"{filename}_pass"
        
        # Create pass folder
        pass_folder.mkdir(exist_ok=True)
        
        print(f"Generating pass for {member_data['first_name']} {member_data['last_name']}...")
        
        # Generate pass.json
        pass_data = self.create_pass_json(member_data)
        
        # Write pass.json
        with open(pass_folder / "pass.json", 'w', encoding='utf-8') as f:
            json.dump(pass_data, f, indent=2, ensure_ascii=False)
        
        # Prepare images
        self.prepare_pass_images(member_data, pass_folder)
        
        print(f"✓ Pass bundle created: {pass_folder}")
        return pass_folder
    
    def validate_csv_data(self, data):
        """Validate CSV data and required fields."""
        required_fields = ['first_name', 'last_name', 'email', 'company_name']
        
        for i, row in enumerate(data, 1):
            for field in required_fields:
                if not row.get(field, '').strip():
                    raise ValueError(f"Missing required field '{field}' in row {i}")
        
        return True
    
    def create_signing_instructions(self):
        """Create instructions file for the person who will sign the passes."""
        instructions = f"""# Apple Wallet Pass Signing Instructions

Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Overview
This folder contains unsigned Apple Wallet pass bundles for the {config.ORGANIZATION_NAME} team.
Each subfolder (ending with '_pass') contains a complete pass ready for signing.

## Configuration Used
- Pass Type Identifier: {config.PASS_TYPE_IDENTIFIER}
- Team Identifier: {config.TEAM_IDENTIFIER}
- Organization: {config.ORGANIZATION_NAME}
- GitHub Pages URL: {config.GITHUB_PAGES_URL}

## Signing Process

### Prerequisites:
1. Apple Developer Account with Pass Type ID created
2. Pass Type ID Certificate installed in Keychain
3. Apple WWDR Certificate installed in Keychain  
4. `signpass` utility (download from Apple Developer portal)

### Signing Command:
For each pass folder, run:
```bash
./signpass -p /path/to/FOLDER_NAME_pass
```

This will create a `.pkpass` file for each folder.

### Example:
```bash
./signpass -p jane-doe_pass
./signpass -p john-smith_pass
./signpass -p sarah-johnson_pass
./signpass -p michael-brown_pass
```

## Batch Signing Script:
You can create a simple script to sign all passes:

```bash
#!/bin/bash
for folder in *_pass; do
    if [ -d "$folder" ]; then
        echo "Signing $folder..."
        ./signpass -p "$folder"
    fi
done
```

## After Signing:
You'll have `.pkpass` files ready for distribution. These can be:
- Emailed to team members
- Shared via AirDrop
- Hosted on a website with "Add to Apple Wallet" links
- Distributed via QR codes

## Troubleshooting:
- If signing fails, check that certificates are properly installed in Keychain
- Verify Pass Type ID and Team ID match your Apple Developer account
- Ensure all image files are present and properly formatted

Generated pass folders: {len(list(self.output_dir.glob('*_pass')))}
"""
        
        with open(self.output_dir / "SIGNING_INSTRUCTIONS.md", 'w', encoding='utf-8') as f:
            f.write(instructions)
    
    def generate_all(self):
        """Generate all wallet passes from CSV data."""
        print("🚀 Starting Apple Wallet Pass Generation...")
        print(f"Reading data from: {self.csv_file}")
        
        # Validate configuration first
        if not config.validate_config():
            print("\n❌ Configuration validation failed!")
            print("Please update config_wallet_passes.py with the correct values.")
            return []
        
        # Read and validate CSV data
        csv_data = self.read_csv_data()
        self.validate_csv_data(csv_data)
        
        print(f"Found {len(csv_data)} team members")
        
        # Clean output directory
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        self.output_dir.mkdir(parents=True)
        
        # Generate passes for each team member
        generated_passes = []
        for member_data in csv_data:
            try:
                pass_folder = self.generate_pass_bundle(member_data)
                generated_passes.append(pass_folder)
            except Exception as e:
                print(f"❌ Error generating pass for {member_data.get('first_name', 'Unknown')}: {e}")
                continue
        
        # Create signing instructions
        self.create_signing_instructions()
        
        print(f"\n✅ Generated {len(generated_passes)} wallet pass bundles!")
        print(f"📁 Output location: {self.output_dir}")
        print(f"📋 Check SIGNING_INSTRUCTIONS.md for next steps")
        
        return generated_passes


def main():
    """Main function."""
    try:
        # Check configuration first
        print("🔍 Validating configuration...")
        if not config.validate_config():
            print("\n❌ Please update config_wallet_passes.py before proceeding.")
            print("Run: python config_wallet_passes.py to see instructions.")
            return
        
        # Initialize generator
        generator = WalletPassGenerator()
        
        # Generate all passes
        passes = generator.generate_all()
        
        if passes:
            print(f"\n🎉 Success! Generated {len(passes)} Apple Wallet passes.")
            print("\n📋 Next steps:")
            print("1. Review the generated pass folders")
            print("2. Send the entire wallet_passes folder to your Apple Developer Account holder")
            print("3. They can sign the passes using the provided instructions")
            print("4. Distribute the signed .pkpass files to your team!")
        else:
            print("\n❌ No passes were generated. Check the errors above.")
        
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
        print("Make sure team_data.csv exists in the project root directory.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        raise


if __name__ == "__main__":
    main() 