#!/usr/bin/env python3
"""
Apple Wallet Pass Generator - SCALEWAVE BUSINESS CARDS
Clean, professional design following TranzerCode structure exactly
"""

import json
import hashlib
import os
import shutil
import csv
import uuid
from zipfile import ZipFile
from pathlib import Path

# Configuration - EXACT TranzerCode structure preserved
PASS_TYPE_IDENTIFIER = "pass.com.scalewave.contacts.team"
TEAM_IDENTIFIER = "VVA864P233"
ORGANIZATION_NAME = "Scalewave"
OPENSSL_APP = "openssl"
GITHUB_PAGES_URL = "https://kaib03.github.io/digital-contact-cards/"

# Brand Colors (Scalewave Color Palette)
COLORS = {
    "background": "rgb(255, 255, 255)",      # Pure white background (was greenish)
    "primary_text": "rgb(31, 75, 140)",     # #1f4b8c FORMALIDAD - dark blue
    "accent": "rgb(11, 33, 255)",           # #0b21ff INNOVACIÓN - bright blue
    "labels": "rgb(31, 75, 140)",           # #1f4b8c FORMALIDAD - same as primary for labels
}

def clean_filename(name):
    """Generate a clean filename from name."""
    return name.lower().replace(' ', '-').replace('.', '').replace(',', '')

def create_pass_dict(member_data):
    """Create pass dictionary following TranzerCode structure exactly with Scalewave branding."""
    full_name = f"{member_data['first_name']} {member_data['last_name']}"
    
    # Corrected filename logic for the URL to handle multi-word first names.
    first_name_cleaned = member_data['first_name'].replace(' ', '').lower()
    last_name_cleaned = member_data['last_name'].lower()
    filename = f"{first_name_cleaned}-{last_name_cleaned}"

    qr_url = f"{GITHUB_PAGES_URL.rstrip('/')}/html/{filename}.html"
    
    # EXACT TranzerCode structure - DO NOT CHANGE
    return {
        "formatVersion": 1,
        "serialNumber": str(uuid.uuid4()),
        "passTypeIdentifier": PASS_TYPE_IDENTIFIER,
        "teamIdentifier": TEAM_IDENTIFIER,
        "organizationName": ORGANIZATION_NAME,
        "description": f"{ORGANIZATION_NAME} Contact Card",
        "logoText": "",  # Empty top right as requested
        
        # Scalewave Brand Colors (Updated)
        "foregroundColor": COLORS["primary_text"],      # Dark blue text
        "backgroundColor": COLORS["background"],        # Pure white background
        "labelColor": COLORS["labels"],                 # Dark blue labels
        
        # QR Code with altText for a title
        "barcode": {
            "message": qr_url,
            "format": "PKBarcodeFormatQR",
            "messageEncoding": "iso-8859-1",
            "altText": "Scan for Contact" # This text is rendered near the barcode
        },
        
        # Final Layout: "CONTACT CARD" as a title, side-by-side secondary fields
        "generic": {
            "primaryFields": [
                {
                    "key": "member", 
                    "label": "CONTACT CARD", # Added label to the name field
                    "value": full_name,
                    "textAlignment": "PKTextAlignmentLeft"
                }
            ],
            "secondaryFields": [
                {
                    "key": "title", 
                    "label": "TITLE", 
                    "value": member_data.get('title', 'Team Member'),
                    "textAlignment": "PKTextAlignmentLeft"
                },
                {
                    "key": "contact_info",
                    "label": "CONTACT INFORMATION",
                    "value": "Scan QR Code",
                    "textAlignment": "PKTextAlignmentRight"
                }
            ],
            # NO auxiliaryFields or headerFields to ensure no right-side icon.
            # Back fields with essential contact info
            "backFields": [
                {"label": "Full Contact Info", "key": "website", "value": qr_url},
                {"label": "Email", "key": "email", "value": member_data.get('email', 'N/A')},
                {"label": "Phone", "key": "phone", "value": member_data.get('phone', 'N/A')},
                {"label": "Company", "key": "company", "value": ORGANIZATION_NAME}
            ]
        }
    }

def copy_scalewave_assets():
    """Copy Scalewave assets from assets/images directory."""
    assets_dir = "assets/images"
    # REMOVED thumbnail.png and thumbnail@2x.png to prevent right-side icon
    required_assets = ["icon.png", "icon@2x.png", "logo.png", "logo@2x.png"]
    
    copied_count = 0
    for asset in required_assets:
        src = f"{assets_dir}/{asset}"
        if os.path.exists(src):
            shutil.copy2(src, asset)
            copied_count += 1
        else:
            print(f"   ⚠️  Warning: {asset} not found in {assets_dir}")
    
    return copied_count

def create_manifest_json():
    """Create manifest.json following TranzerCode method exactly."""
    with open("pass.json", "r") as f:
        pass_json = f.read()
    
    hashed_pass_json = hashlib.sha1(pass_json.encode('utf-8')).hexdigest()
    manifest_dict = {"pass.json": hashed_pass_json}
    
    # Hash all asset files that exist (EXACT TranzerCode method)
    # REMOVED thumbnail.png and thumbnail@2x.png from this list
    assets = ["icon.png", "icon@2x.png", "logo.png", "logo@2x.png"]
    for filename in assets:
        if os.path.exists(filename):
            manifest_dict[filename] = hashlib.sha1(
                open(filename, "rb").read()
            ).hexdigest()
    
    with open("manifest.json", "w") as f:
        f.write(json.dumps(manifest_dict, indent=4))

def create_single_pass(member_data, certificate_path, certificate_password, wwdr_path):
    """Create a single pass following TranzerCode method exactly."""
    full_name = f"{member_data['first_name']} {member_data['last_name']}"
    filename = clean_filename(full_name)
    
    print(f"🔧 Creating Scalewave business card for: {full_name}")
    
    try:
        # Step 1: Create pass.json (TranzerCode structure)
        pass_dict = create_pass_dict(member_data)
        with open("pass.json", "w") as f:
            json.dump(pass_dict, f, indent=2)
        
        # Step 2: Copy Scalewave assets
        assets_copied = copy_scalewave_assets()
        if assets_copied < 4:  # Need at least icon and logo files
            print(f"   ⚠️  Warning: Only {assets_copied} assets copied for {full_name}")
        
        # Step 3: Create manifest.json (EXACT TranzerCode method)
        create_manifest_json()
        
        # Step 4: Create certificates (EXACT TranzerCode commands)
        key_password = "password"
        
        os_code = os.system(f"{OPENSSL_APP} pkcs12 -in {certificate_path} -clcerts -nokeys -out passcertificate.pem -passin pass:{certificate_password} 2>/dev/null")
        if os_code != 0:
            raise Exception("could not create pass certificate")
        
        os_code = os.system(f"{OPENSSL_APP} pkcs12 -in {certificate_path} -nocerts -out passkey.pem -passin pass:{certificate_password} -passout pass:{key_password} 2>/dev/null")
        if os_code != 0:
            raise Exception("could not create pass key")
        
        # Step 5: Create signature (EXACT TranzerCode method)
        os_code = os.system(f"{OPENSSL_APP} smime -binary -sign -certfile {wwdr_path} -signer passcertificate.pem -inkey passkey.pem -in manifest.json -out signature -outform DER -passin pass:{key_password} 2>/dev/null")
        if os_code != 0:
            raise Exception("could not create signature")
        
        # Step 6: Create pkpass file (EXACT TranzerCode method)
        asset_files = ["signature", "pass.json", "manifest.json"]
        # REMOVED thumbnail.png and thumbnail@2x.png from this list
        assets = ["icon.png", "icon@2x.png", "logo.png", "logo@2x.png"]
        for asset_filename in assets:
            if os.path.exists(asset_filename):
                asset_files.append(asset_filename)
        
        with ZipFile(f"signed_passes/{filename}.pkpass", "w") as zip_file:
            for asset_file in asset_files:
                zip_file.write(asset_file)
        
        # Step 7: Clean up temporary files (EXACT TranzerCode method)
        temp_files = ["pass.json", "manifest.json", "passcertificate.pem", "passkey.pem", "signature"] + assets
        for temp_file in temp_files:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        
        print(f"   ✅ Created: signed_passes/{filename}.pkpass")
        return True
        
    except Exception as e:
        print(f"   ❌ Error: {e}")
        # Clean up on error
        temp_files = ["pass.json", "manifest.json", "passcertificate.pem", "passkey.pem", "signature"]
        # REMOVED thumbnail.png and thumbnail@2x.png from this list
        assets = ["icon.png", "icon@2x.png", "logo.png", "logo@2x.png"]
        for temp_file in temp_files + assets:
            if os.path.exists(temp_file):
                os.remove(temp_file)
        return False

def main():
    """Main function following TranzerCode approach with Scalewave branding."""
    print("🚀 Scalewave Business Card Generator (Apple Wallet)")
    print("=" * 60)
    print("🎨 Using Scalewave brand colors:")
    print(f"   Background: {COLORS['background']}")
    print(f"   Text: {COLORS['primary_text']}")
    print(f"   Accent: {COLORS['accent']}")
    print()
    
    # Check prerequisites
    if not os.path.exists("team_data.csv"):
        print("❌ Error: team_data.csv not found!")
        return
    
    if not os.path.exists("assets/images"):
        print("❌ Error: assets/images directory not found!")
        return
    
    # Create output directory
    os.makedirs("signed_passes", exist_ok=True)
    
    # Configuration
    certificate_path = "certs/YourPassTypeID.p12"
    certificate_password = "samerroz1"  # Your certificate password
    wwdr_path = "certs/WWDR.pem"
    
    # Verify certificates exist
    if not os.path.exists(certificate_path):
        print(f"❌ Error: Certificate not found at {certificate_path}")
        return
    
    if not os.path.exists(wwdr_path):
        print(f"❌ Error: WWDR certificate not found at {wwdr_path}")
        return
    
    # Read team data
    with open("team_data.csv", "r") as f:
        team_data = list(csv.DictReader(f))
    
    print(f"📊 Found {len(team_data)} team members")
    print(f"🔑 Using certificate: {certificate_path}")
    print(f"🔐 Using WWDR: {wwdr_path}")
    print()
    
    # Create passes
    successful = 0
    failed = 0
    
    for member in team_data:
        if create_single_pass(member, certificate_path, certificate_password, wwdr_path):
            successful += 1
        else:
            failed += 1
    
    print()
    print("🎉 Scalewave business card generation complete!")
    print(f"✅ Successful: {successful}")
    print(f"❌ Failed: {failed}")
    print(f"📁 Find your business cards in: signed_passes/")
    
    if successful > 0:
        print()
        print("🍎 Testing Instructions:")
        print("1. AirDrop a .pkpass file to your iPhone")
        print("2. Tap the file to open it")
        print("3. It should open in Apple Wallet with Scalewave branding")
        print("4. Scan the QR code to test the contact page")

if __name__ == "__main__":
    main() 