#!/usr/bin/env python3
"""
Apple Wallet Pass Generator - TranzerCode Method
This follows the EXACT working approach from TranzerCode
"""

import json
import hashlib
import os
import sys
import shutil
import csv
import uuid
from typing import Callable, Optional, TypedDict
from zipfile import ZipFile
from pathlib import Path

# Configuration
PASS_TYPE_IDENTIFIER = "pass.com.scalewave.contacts.team"
TEAM_IDENTIFIER = "VVA864P233" 
ORGANIZATION_NAME = "Scalewave"
OPENSSL_APP = "openssl"
SUPPORTED_ASSET_FILES = [
    "icon.png",
    "icon@2x.png", 
    "logo.png",
    "logo@2x.png",
    "thumbnail.png",
    "thumbnail@2x.png",
]

def create_pass_dict(member_data):
    """Create pass dictionary following TranzerCode structure exactly."""
    full_name = f"{member_data['first_name']} {member_data['last_name']}"
    filename = full_name.lower().replace(' ', '-').replace('.', '')
    qr_url = f"https://kaib03.github.io/digital-contact-cards/html/{filename}.html"
    
    return {
        "formatVersion": 1,
        "serialNumber": str(uuid.uuid4()),
        "passTypeIdentifier": PASS_TYPE_IDENTIFIER,
        "teamIdentifier": TEAM_IDENTIFIER,
        "organizationName": ORGANIZATION_NAME,
        "description": f"{ORGANIZATION_NAME} Contact Card",
        "logoText": ORGANIZATION_NAME,
        "foregroundColor": "rgb(255, 255, 255)",
        "backgroundColor": "rgb(25, 25, 25)",
        "barcode": {
            "message": qr_url,
            "format": "PKBarcodeFormatPDF417", 
            "messageEncoding": "iso-8859-1",
        },
        "generic": {
            "primaryFields": [
                {"key": "member", "value": full_name}
            ],
            "secondaryFields": [
                {"key": "title", "label": "TITLE", "value": member_data.get('title', 'Team Member')}
            ],
            "auxiliaryFields": [
                {"key": "company", "label": "COMPANY", "value": ORGANIZATION_NAME},
                {"key": "contact", "label": "CONTACT", "value": "Scan for Details"}
            ],
            "backFields": [
                {"label": "Email", "key": "email", "value": member_data.get('email', 'N/A')},
                {"label": "Phone", "key": "phone", "value": member_data.get('phone', 'N/A')},
                {"label": "Contact Page", "key": "website", "value": qr_url}
            ]
        }
    }

def create_manifest_json():
    """Create manifest.json following TranzerCode method exactly."""
    with open("pass.json", "r") as f:
        pass_json = f.read()
    
    hashed_pass_json = hashlib.sha1(pass_json.encode('utf-8')).hexdigest()
    manifest_dict = {"pass.json": hashed_pass_json}
    
    # Hash all asset files that exist
    for filename in SUPPORTED_ASSET_FILES:
        if os.path.exists(filename):
            manifest_dict[filename] = hashlib.sha1(
                open(filename, "rb").read()
            ).hexdigest()
    
    with open("manifest.json", "w") as f:
        f.write(json.dumps(manifest_dict, indent=4))

def create_single_pass(member_data, certificate_path, certificate_password, wwdr_path):
    """Create a single pass following TranzerCode method exactly."""
    full_name = f"{member_data['first_name']} {member_data['last_name']}"
    filename = full_name.lower().replace(' ', '-').replace('.', '')
    
    print(f"🔧 Creating pass for: {full_name}")
    
    # Step 1: Create pass.json
    pass_dict_data = create_pass_dict(member_data)
    pass_dict_json = json.dumps(pass_dict_data, indent=2)
    with open("pass.json", "w") as f:
        f.write(pass_dict_json)
    
    # Step 2: Copy required assets (create minimal assets if they don't exist)
    create_minimal_assets()
    
    # Step 3: Create manifest.json
    create_manifest_json()
    
    # Step 4: Create certificates (following TranzerCode exactly)
    key_password = "password"
    
    os_code = os.system(f"{OPENSSL_APP} pkcs12 -in {certificate_path} -clcerts -nokeys -out passcertificate.pem -passin pass:{certificate_password}")
    if os_code != 0:
        raise Exception("could not create pass certificate")
    
    os_code = os.system(f"{OPENSSL_APP} pkcs12 -in {certificate_path} -nocerts -out passkey.pem -passin pass:{certificate_password} -passout pass:{key_password}")
    if os_code != 0:
        raise Exception("could not create pass key")
    
    # Step 5: Create signature (following TranzerCode exactly)
    os_code = os.system(f"{OPENSSL_APP} smime -binary -sign -certfile {wwdr_path} -signer passcertificate.pem -inkey passkey.pem -in manifest.json -out signature -outform DER -passin pass:{key_password}")
    if os_code != 0:
        raise Exception("could not create signature")
    
    # Step 6: Create pkpass file (following TranzerCode exactly)
    asset_files = ["signature", "pass.json", "manifest.json"]
    for filename in SUPPORTED_ASSET_FILES:
        if os.path.exists(filename):
            asset_files.append(filename)
    
    with ZipFile(f"signed_passes/{filename}.pkpass", "w") as zip_file:
        for asset_file in asset_files:
            zip_file.write(asset_file)
    
    # Step 7: Clean up temporary files
    temp_files = ["pass.json", "manifest.json", "passcertificate.pem", "passkey.pem", "signature"] + SUPPORTED_ASSET_FILES
    for temp_file in temp_files:
        if os.path.exists(temp_file):
            os.remove(temp_file)
    
    print(f"✅ Created: signed_passes/{filename}.pkpass")

def create_minimal_assets():
    """Create minimal required assets if they don't exist."""
    # Copy existing logo if available
    logo_source = "assets/images/logo_scalewave_cropped.png"
    if os.path.exists(logo_source):
        shutil.copy2(logo_source, "logo.png")
        shutil.copy2(logo_source, "logo@2x.png")
    
    # Create minimal icons using TranzerCode's approach
    tranzer_assets = "TranzerCode/PKPassCreator/Generic.pass"
    if os.path.exists(tranzer_assets):
        for asset in SUPPORTED_ASSET_FILES:
            if os.path.exists(f"{tranzer_assets}/{asset}"):
                shutil.copy2(f"{tranzer_assets}/{asset}", asset)

def main():
    """Main function following TranzerCode approach."""
    print("🚀 Apple Wallet Pass Generator (TranzerCode Method)")
    
    # Create output directory
    os.makedirs("signed_passes", exist_ok=True)
    
    # Get inputs
    certificate_path = input("Enter path to your .p12 certificate: ").strip()
    if not certificate_path:
        certificate_path = "certs/YourPassTypeID.p12"
    
    certificate_password = input("Enter certificate password: ").strip()
    
    wwdr_path = input("Enter path to WWDR certificate: ").strip()
    if not wwdr_path:
        wwdr_path = "certs/AppleWWDRCAG4.cer"
    
    # Read team data
    with open("team_data.csv", "r") as f:
        team_data = list(csv.DictReader(f))
    
    print(f"Found {len(team_data)} team members")
    
    # Create passes
    for member in team_data:
        try:
            create_single_pass(member, certificate_path, certificate_password, wwdr_path)
        except Exception as e:
            print(f"❌ Error creating pass for {member.get('first_name', 'Unknown')}: {e}")
    
    print("🎉 Pass generation complete!")
    print("📁 Find your passes in: signed_passes/")

if __name__ == "__main__":
    main() 