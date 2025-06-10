# Digital Contact Cards - Apple Wallet Passes

This project generates Apple Wallet passes for team members that can be shared via QR codes and added to Apple Wallet.

## How It Works

The project creates digital business cards that:
- Generate Apple Wallet passes (`.pkpass` files)
- Link to individual contact pages on GitHub Pages
- Can be scanned via QR codes or shared directly

## Quick Start

### 1. Generate Passes
```bash
python3 scripts/generate_passes.py
```

### 2. Sign Passes
```bash
./sign_passes.sh
```
Enter your certificate password when prompted.

### 3. Find Signed Passes
Your signed `.pkpass` files will be in the `signed_passes/` directory.

## Project Structure

- `scripts/generate_passes.py` - Generates pass bundles from CSV data
- `sign_passes.sh` - Signs passes with your Apple Developer certificates
- `team_data.csv` - Team member information
- `config_wallet_passes.py` - Apple Developer configuration
- `assets/` - Pass icons and logos
- `certs/` - Apple Developer certificates
- `wallet_passes/` - Generated pass bundles (unsigned)
- `signed_passes/` - Final signed `.pkpass` files
- `html/` - Individual contact card pages
- `TranzerCode/` - Reference implementation that works

## Requirements

- Apple Developer Account with Pass Type ID
- Valid Pass Type ID certificate in `certs/`
- Apple WWDR certificate in `certs/`
- Python 3.x
- OpenSSL

## Notes

This implementation follows the exact structure of the working TranzerCode example:
- Uses `generic` pass style (not `storeCard`)
- Uses `PKBarcodeFormatPDF417` barcodes
- Uses `iso-8859-1` encoding
- Includes required `locations` field

The passes generated with this approach successfully open in Apple Wallet. 