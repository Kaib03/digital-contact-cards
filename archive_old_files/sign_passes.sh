#!/bin/bash

#
# Simple Apple Wallet Pass Signer - Following TranzerCode Method
#
# This script follows the exact same approach as the working TranzerCode
# but processes multiple passes from our CSV data.
#

set -e

# Configuration
P12_CERT_PATH="certs/YourPassTypeID.p12"
WWDR_CERT_PATH="certs/AppleWWDRCAG4.cer"
PASSES_DIR="wallet_passes"
OUTPUT_DIR="signed_passes"

echo "--- Simple Apple Wallet Pass Signer ---"

# Check prerequisites
if [ ! -f "$P12_CERT_PATH" ]; then
    echo "❌ Error: Certificate not found at $P12_CERT_PATH"
    exit 1
fi

if [ ! -f "$WWDR_CERT_PATH" ]; then
    echo "❌ Error: WWDR certificate not found at $WWDR_CERT_PATH"
    exit 1
fi

# Get password
read -s -p "Enter the .p12 certificate password: " CERT_PASSWORD
echo

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Process each pass
for pass_dir in "$PASSES_DIR"/*_pass; do
    if [ -d "$pass_dir" ]; then
        pass_name=$(basename "$pass_dir" _pass)
        echo "🔧 Processing: $pass_name"
        
        # Navigate to pass directory
        cd "$pass_dir"
        
        # Step 1: Extract certificates (following TranzerCode exactly)
        openssl pkcs12 -in "../../$P12_CERT_PATH" -clcerts -nokeys -out passcertificate.pem -passin pass:"$CERT_PASSWORD"
        openssl pkcs12 -in "../../$P12_CERT_PATH" -nocerts -out passkey.pem -passin pass:"$CERT_PASSWORD" -passout pass:"password"
        openssl x509 -inform der -in "../../$WWDR_CERT_PATH" -out wwdr.pem
        
        # Step 2: Create manifest.json (following TranzerCode method)
        echo "{" > manifest.json
        for file in *.png pass.json; do
            if [ -f "$file" ]; then
                hash=$(openssl sha1 -binary "$file" | openssl base64)
                echo "  \"$file\": \"$hash\"," >> manifest.json
            fi
        done
        # Remove last comma and close JSON
        sed -i '' '$ s/,$//' manifest.json
        echo "}" >> manifest.json
        
        # Step 3: Create signature (following TranzerCode exactly)
        openssl smime -binary -sign -certfile wwdr.pem -signer passcertificate.pem -inkey passkey.pem -in manifest.json -out signature -outform DER -passin pass:"password"
        
        # Step 4: Create .pkpass file (following TranzerCode method)
        files_to_zip="signature pass.json manifest.json"
        for file in *.png; do
            if [ -f "$file" ]; then
                files_to_zip="$files_to_zip $file"
            fi
        done
        
        zip -q "../../$OUTPUT_DIR/$pass_name.pkpass" $files_to_zip
        
        # Step 5: Clean up temporary files
        rm passcertificate.pem passkey.pem wwdr.pem signature manifest.json
        
        echo "✅ Created: $OUTPUT_DIR/$pass_name.pkpass"
        
        # Return to original directory
        cd - > /dev/null
    fi
done

echo "🎉 All passes signed successfully!"
echo "📁 Find them in: $OUTPUT_DIR/" 