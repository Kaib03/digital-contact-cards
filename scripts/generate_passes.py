#!/usr/bin/env python3
"""
Fixed Apple Wallet Pass Generator - EXACT TranzerCode Structure

This generator creates passes using the EXACT same structure as the working
TranzerCode example, populated with our CSV team data.
"""

import csv
import json
import os
import sys
import uuid
import shutil
from pathlib import Path

# Import configuration
sys.path.append(str(Path(__file__).parent.parent))
import config_wallet_passes as config

class FixedPassGenerator:
    def __init__(self):
        self.base_dir = Path(__file__).parent.parent
        self.output_dir = self.base_dir / "wallet_passes"
        self.assets_dir = self.base_dir / "assets"
        self.csv_file = self.base_dir / "team_data.csv"
        
    def clean_filename(self, name):
        """Generate a clean filename from name."""
        return name.lower().replace(' ', '-').replace('.', '')
    
    def read_team_data(self):
        """Read team data from CSV."""
        with open(self.csv_file, 'r') as f:
            reader = csv.DictReader(f)
            return list(reader)
    
    def create_pass_structure(self, member):
        """Create pass structure EXACTLY like working TranzerCode."""
        full_name = f"{member['first_name']} {member['last_name']}"
        filename = self.clean_filename(full_name)
        qr_url = f"{config.GITHUB_PAGES_URL.rstrip('/')}/html/{filename}.html"
        
        # Use the EXACT structure that works from TranzerCode
        pass_data = {
            "formatVersion": 1,
            "serialNumber": str(uuid.uuid4()),
            "webServiceURL": config.GITHUB_PAGES_URL,
            "authenticationToken": f"scalewave-{filename}-token",
            "locations": [
                {"longitude": -122.3748889, "latitude": 37.6189722},
                {"longitude": -122.03118, "latitude": 37.33182},
            ],
            "barcode": {
                "message": qr_url,
                "format": "PKBarcodeFormatPDF417",
                "messageEncoding": "iso-8859-1",
            },
            "organizationName": config.ORGANIZATION_NAME,
            "description": f"{config.ORGANIZATION_NAME} Contact Card",
            "logoText": config.ORGANIZATION_NAME,
            "foregroundColor": "rgb(255, 255, 255)",
            "backgroundColor": "rgb(25, 25, 25)",
            "passTypeIdentifier": config.PASS_TYPE_IDENTIFIER,
            "teamIdentifier": config.TEAM_IDENTIFIER,
            "generic": {
                "primaryFields": [
                    {"key": "member", "value": full_name}
                ],
                "secondaryFields": [
                    {"key": "title", "label": "TITLE", "value": member.get('title', 'Team Member')}
                ],
                "auxiliaryFields": [
                    {"key": "company", "label": "COMPANY", "value": config.ORGANIZATION_NAME},
                    {"key": "contact", "label": "CONTACT", "value": "Scan for Details"}
                ],
                "backFields": [
                    {
                        "label": "Email",
                        "key": "email",
                        "value": member.get('email', 'N/A')
                    },
                    {
                        "label": "Phone",
                        "key": "phone", 
                        "value": member.get('phone', 'N/A')
                    },
                    {
                        "label": "LinkedIn",
                        "key": "linkedin",
                        "value": member.get('linkedin_url', 'N/A')
                    },
                    {
                        "label": "Contact Page",
                        "key": "website",
                        "value": qr_url
                    }
                ]
            }
        }
        
        return pass_data
    
    def copy_assets(self, pass_dir):
        """Copy image assets to pass directory."""
        required_images = [
            'icon.png', 'icon@2x.png', 'icon@3x.png',
            'logo.png', 'logo@2x.png', 'logo@3x.png'
        ]
        
        for image in required_images:
            src = self.assets_dir / image
            if src.exists():
                shutil.copy2(src, pass_dir / image)
    
    def generate_pass(self, member):
        """Generate a single pass bundle."""
        full_name = f"{member['first_name']} {member['last_name']}"
        filename = self.clean_filename(full_name)
        pass_dir = self.output_dir / f"{filename}_pass"
        
        # Create pass directory
        pass_dir.mkdir(parents=True, exist_ok=True)
        
        # Create pass.json with EXACT working structure
        pass_data = self.create_pass_structure(member)
        with open(pass_dir / "pass.json", 'w') as f:
            json.dump(pass_data, f, indent=2)
        
        # Copy assets
        self.copy_assets(pass_dir)
        
        print(f"✓ Generated pass: {filename}")
        return pass_dir
    
    def generate_all(self):
        """Generate all passes."""
        print("🚀 Generating fixed wallet passes (TranzerCode structure)...")
        
        # Clean output directory
        if self.output_dir.exists():
            shutil.rmtree(self.output_dir)
        self.output_dir.mkdir(parents=True)
        
        # Read team data
        team_data = self.read_team_data()
        print(f"Found {len(team_data)} team members")
        
        # Generate passes
        for member in team_data:
            self.generate_pass(member)
        
        print(f"\n✅ Generated {len(team_data)} pass bundles")
        print(f"📁 Location: {self.output_dir}")

if __name__ == "__main__":
    generator = FixedPassGenerator()
    generator.generate_all() 