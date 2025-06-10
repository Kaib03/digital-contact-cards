#!/usr/bin/env python3
"""
Simple Test: Create ONE Apple Wallet Pass (TranzerCode Method)
This creates a single pass to test if our approach works
"""

import json
import hashlib
import os
import shutil
import uuid
from zipfile import ZipFile

# Configuration - EXACT same as TranzerCode 
PASS_TYPE_IDENTIFIER = "pass.com.scalewave.contacts.team"
TEAM_IDENTIFIER = "VVA864P233"
ORGANIZATION_NAME = "Scalewave"
OPENSSL_APP = "openssl"

def create_test_pass_dict():
    """Create a test pass using TranzerCode structure exactly."""
    return {
        "formatVersion": 1,
        "serialNumber": "test-pass-12345",
        "passTypeIdentifier": PASS_TYPE_IDENTIFIER,
        "teamIdentifier": TEAM_IDENTIFIER,
        "organizationName": ORGANIZATION_NAME,
        "description": f"{ORGANIZATION_NAME} Contact Card",
        "logoText": ORGANIZATION_NAME,
        "foregroundColor": "rgb(255, 255, 255)",
        "backgroundColor": "rgb(25, 25, 25)",
        "barcode": {
            "message": "https://kaib03.github.io/digital-contact-cards/html/test.html",
            "format": "PKBarcodeFormatPDF417",
            "messageEncoding": "iso-8859-1",
        },
        "generic": {
            "primaryFields": [
                {"key": "member", "value": "Test User"}
            ],
            "secondaryFields": [
                {"key": "title", "label": "TITLE", "value": "Test Manager"}
            ],
            "auxiliaryFields": [
                {"key": "company", "label": "COMPANY", "value": ORGANIZATION_NAME},
                {"key": "contact", "label": "CONTACT", "value": "Scan for Details"}
            ],
            "backFields": [
                {"label": "Email", "key": "email", "value": "test@scalewave.es"},
                {"label": "Phone", "key": "phone", "value": "+34 123456789"},
                {"label": "Contact Page", "key": "website", "value": "https://kaib03.github.io/digital-contact-cards/html/test.html"}
            ]
        }
    }

def copy_assets_from_tranzer():
    """Copy assets from TranzerCode to use as our assets."""
    tranzer_path = "TranzerCode/PKPassCreator/Generic.pass"
    assets = ["icon.png", "icon@2x.png", "logo.png", "logo@2x.png", "thumbnail.png", "thumbnail@2x.png"]
    
    for asset in assets:
        src = f"{tranzer_path}/{asset}"
        if os.path.exists(src):
            shutil.copy2(src, asset)
            print(f"✓ Copied {asset}")

def create_manifest_json():
    """Create manifest.json following TranzerCode method exactly."""
    with open("pass.json", "r") as f:
        pass_json = f.read()
    
    hashed_pass_json = hashlib.sha1(pass_json.encode('utf-8')).hexdigest()
    manifest_dict = {"pass.json": hashed_pass_json}
    
    # Hash all asset files that exist
    assets = ["icon.png", "icon@2x.png", "logo.png", "logo@2x.png", "thumbnail.png", "thumbnail@2x.png"]
    for filename in assets:
        if os.path.exists(filename):
            manifest_dict[filename] = hashlib.sha1(
                open(filename, "rb").read()
            ).hexdigest()
    
    with open("manifest.json", "w") as f:
        f.write(json.dumps(manifest_dict, indent=4))

def create_test_pass():
    """Create a test pass following TranzerCode method exactly."""
    certificate_path = "certs/YourPassTypeID.p12"
    certificate_password = "samerroz1"  # The password you entered earlier
    wwdr_path = "certs/WWDR.pem"
    
    print("🔧 Creating test pass...")
    
    # Step 1: Create pass.json
    pass_dict = create_test_pass_dict()
    with open("pass.json", "w") as f:
        json.dump(pass_dict, f, indent=2)
    print("✓ Created pass.json")
    
    # Step 2: Copy assets from TranzerCode
    copy_assets_from_tranzer()
    
    # Step 3: Create manifest.json
    create_manifest_json()
    print("✓ Created manifest.json")
    
    # Step 4: Create certificates (following TranzerCode exactly)
    key_password = "password"
    
    print("🔐 Creating certificates...")
    os_code = os.system(f"{OPENSSL_APP} pkcs12 -in {certificate_path} -clcerts -nokeys -out passcertificate.pem -passin pass:{certificate_password}")
    if os_code != 0:
        raise Exception("could not create pass certificate")
    
    os_code = os.system(f"{OPENSSL_APP} pkcs12 -in {certificate_path} -nocerts -out passkey.pem -passin pass:{certificate_password} -passout pass:{key_password}")
    if os_code != 0:
        raise Exception("could not create pass key")
    
    # Step 5: Create signature (following TranzerCode exactly)
    print("✍️  Creating signature...")
    os_code = os.system(f"{OPENSSL_APP} smime -binary -sign -certfile {wwdr_path} -signer passcertificate.pem -inkey passkey.pem -in manifest.json -out signature -outform DER -passin pass:{key_password}")
    if os_code != 0:
        raise Exception("could not create signature")
    
    # Step 6: Create pkpass file (following TranzerCode exactly)
    print("📦 Creating .pkpass file...")
    os.makedirs("signed_passes", exist_ok=True)
    
    asset_files = ["signature", "pass.json", "manifest.json"]
    assets = ["icon.png", "icon@2x.png", "logo.png", "logo@2x.png", "thumbnail.png", "thumbnail@2x.png"]
    for filename in assets:
        if os.path.exists(filename):
            asset_files.append(filename)
    
    with ZipFile("signed_passes/test.pkpass", "w") as zip_file:
        for asset_file in asset_files:
            zip_file.write(asset_file)
    
    # Step 7: Clean up temporary files
    print("🧹 Cleaning up...")
    temp_files = ["pass.json", "manifest.json", "passcertificate.pem", "passkey.pem", "signature"] + assets
    for temp_file in temp_files:
        if os.path.exists(temp_file):
            os.remove(temp_file)
    
    print("✅ Test pass created: signed_passes/test.pkpass")
    print("🍎 Try opening this file on your iPhone/Mac to test!")

if __name__ == "__main__":
    try:
        create_test_pass()
    except Exception as e:
        print(f"❌ Error: {e}") 