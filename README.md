# Digital Contact Cards

Create beautiful HTML digital contact cards and Apple Wallet passes for your team from a simple CSV file.

## Project Overview

This project generates:
- **📱 Apple Wallet Passes**: QR code-enabled business cards for iOS devices
- **🌐 HTML Contact Cards**: Beautiful, responsive web pages for each team member
- **📇 VCF Files**: Downloadable contact files for easy importing
- **🔗 Team Index Page**: A central hub showcasing all team members

**Live Example**: [https://kaib03.github.io/digital-contact-cards/](https://kaib03.github.io/digital-contact-cards/)

## Repository Structure

### **Branches**
- **`main`**: Contains the source code, templates, and configuration
- **`gh-pages`**: Contains the generated website files (auto-deployed)

### **Key Directories**
```
digital-contact-cards/
├── assets/
│   ├── css/style.css           # External stylesheet with CSS variables
│   ├── images/                 # Company logos and graphics
│   └── team/                   # Team member avatars (optional)
├── templates/
│   ├── base.html              # Base Jinja2 template
│   ├── contact-card.html      # Individual contact card template
│   ├── index.html             # Team index page template
│   └── vcard_template.vcf     # VCF file template
├── scripts/
│   ├── generate_site.py       # Main site generation script
│   └── generate_passes.py     # Apple Wallet pass generation
├── output/                    # Generated website files (auto-created)
│   ├── html/                  # Individual contact card pages
│   ├── vcf/                   # VCF download files
│   └── passes/                # Apple Wallet .pkpass files
├── signed_passes/             # Temporary wallet pass storage
├── certs/                     # Apple Developer certificates (required for wallet)
├── config.json                # Centralized configuration
└── team_data.csv              # Team member information
```

## Requirements for Apple Wallet

To generate Apple Wallet passes, you must have:

### **1. Apple Developer Account**
- Active Apple Developer Program membership ($99/year)
- Access to Apple Developer Portal

### **2. Required Certificates**
Place these files in the `certs/` directory:

- **`YourPassTypeID.p12`** - Your Pass Type ID certificate
  - Created in Apple Developer Portal under "Certificates, Identifiers & Profiles"
  - Must be exported as .p12 file with a password
  - Update the password in `create_wallet_passes_working.py` if different from default

- **`WWDR.pem`** - Apple Worldwide Developer Relations certificate
  - Download from Apple Developer Portal
  - Convert from .cer to .pem format using: `openssl x509 -inform der -in wwdr.cer -out WWDR.pem`

### **3. Required Assets**
Place these files in `assets/images/`:
- `icon.png` (29×29 pixels)
- `icon@2x.png` (58×58 pixels) 
- `logo.png` (160×50 pixels max)
- `logo@2x.png` (320×100 pixels max)

### **4. System Requirements**
- **OpenSSL** installed on your system
- **Python 3.x** with required dependencies

**⚠️ Note**: If these requirements aren't met, the system will automatically skip wallet pass generation and only create the website.

## How to Update Team Info (Step-by-Step Guide)

### **1. Edit Team Data**

Open `team_data.csv` in any text editor or spreadsheet application:

```csv
first_name,last_name,title,company_name,phone,email,linkedin_url,twitter_handle
John,Doe,Software Engineer,ScaleWave,+1234567890,john@scalewave.es,https://linkedin.com/in/johndoe,@johndoe
```

**Column Descriptions:**
- **`first_name`** *(required)*: Person's first name
- **`last_name`** *(required)*: Person's last name
- **`title`**: Job title (e.g., "Software Engineer", "CEO")
- **`company_name`**: Company name (defaults to "ScaleWave")
- **`phone`**: Phone number in any format (+1234567890, (123) 456-7890)
- **`email`** *(required)*: Email address
- **`linkedin_url`**: Full LinkedIn profile URL
- **`twitter_handle`**: Twitter handle (with or without @)

### **2. Add Team Member Avatars (Optional)**

To add profile photos:

1. **Create the directory** (if it doesn't exist):
   ```bash
   mkdir -p assets/team/
   ```

2. **Add images using this naming convention**:
   - Format: `firstname-lastname.extension`
   - Supported formats: `.jpg`, `.jpeg`, `.png`, `.gif`, `.webp`
   - Example: `john-doe.jpg` for John Doe
   - Example: `juanbautista-beyhaut.png` for Juan Bautista Beyhaut

3. **Image recommendations**:
   - Size: 300x300 pixels or larger (square format)
   - File size: Under 500KB for web performance

### **3. Customize Company Branding (Optional)**

Edit `config.json` to update company information:

```json
{
  "company": {
    "name": "Your Company Name",
    "logo_url": "https://your-site.github.io/your-repo/assets/images/logo.png"
  },
  "deployment": {
    "github_pages_url": "https://your-username.github.io/your-repo",
    "base_url": "https://your-username.github.io/your-repo"
  }
}
```

## Running the Project

### **Prerequisites**

1. **Install Python dependencies**:
   ```bash
   pip install Jinja2==3.1.2
   ```

2. **Make the deployment script executable** (one-time setup):
   ```bash
   chmod +x deploy.sh
   ```

3. **Set up Apple Wallet certificates** (optional - see Requirements section above)

### **One-Click Deployment**

After updating your team data, run the automation script:

```bash
./deploy.sh
```

This single command will:
1. ✅ Generate the website from your CSV data
2. ✅ Generate Apple Wallet passes (if certificates available)
3. ✅ Commit changes to the main branch
4. ✅ Deploy everything to GitHub Pages
5. ✅ Provide you with live URLs

**That's it!** Your website and wallet passes will be live in 1-2 minutes at:
- **Website**: `https://your-username.github.io/your-repo/`
- **Wallet Passes**: `https://your-username.github.io/your-repo/passes/[name].pkpass`

### **Manual Process (Alternative)**

If you prefer to run commands individually:

```bash
# 1. Generate the website and wallet passes
python scripts/generate_site.py

# 2. Commit and push changes
git add .
git commit -m "Update team data and regenerate site + wallet passes"
git push origin main

# 3. Deploy to GitHub Pages
git subtree push --prefix output origin gh-pages
```

## Apple Wallet Integration

### **Accessing Wallet Passes**

Once deployed, your Apple Wallet passes are available at:
```
https://your-username.github.io/your-repo/passes/[firstname-lastname].pkpass
```

**Examples:**
- `https://kaib03.github.io/digital-contact-cards/passes/john-doe.pkpass`
- `https://kaib03.github.io/digital-contact-cards/passes/samer-roz.pkpass`

### **Installing Wallet Passes**

**On iOS devices:**
1. **Safari**: Navigate to the .pkpass URL → Tap "Add to Apple Wallet"
2. **AirDrop**: Send .pkpass file to iOS device → Tap to open → Add to Wallet
3. **Email/Messages**: Attach .pkpass file → Recipient taps to add to Wallet

**Features:**
- QR codes link directly to HTML contact cards
- Professional Scalewave branding
- Contact information on the back of the pass
- Automatic updates when you redeploy

### **Generate Wallet Passes Only**

To create wallet passes without updating the website:

```bash
python create_wallet_passes_working.py
```

**Requirements:**
- Apple Developer certificates (see requirements section)
- OpenSSL installed on your system

## Customization

### **Styling and Themes**

All styles are centralized in `assets/css/style.css` with CSS custom properties:

```css
:root {
  --primary-color: #1f4b8c;      /* Main brand color */
  --secondary-color: #2d5aa0;    /* Secondary brand color */
  --card-background: #ffffff;    /* Card background */
  /* ... more variables */
}
```

**To change the theme**: Update the CSS variables and redeploy.

### **Templates**

Modify the Jinja2 templates in `templates/`:
- `base.html` - Common HTML structure
- `contact-card.html` - Individual contact cards
- `index.html` - Team index page

### **Configuration**

Update `config.json` for:
- Company branding
- Deployment URLs
- Default values for missing CSV fields

## Troubleshooting

### **Site Not Updating**

1. **Check GitHub Pages settings**:
   - Go to repository Settings > Pages
   - Ensure source is set to `gh-pages` branch, `/ (root)` folder

2. **Force browser refresh**:
   - Chrome/Firefox: `Ctrl+F5` (Windows) or `Cmd+Shift+R` (Mac)
   - Or try an incognito/private window

### **Missing Avatars**

- Verify image filename matches: `firstname-lastname.extension`
- Check image is in `assets/team/` directory
- Supported formats: jpg, jpeg, png, gif, webp

### **CSV Errors**

- Ensure required fields are present: `first_name`, `last_name`, `email`
- Check for special characters in names (use quotes if needed)
- Verify CSV format is correct

### **Apple Wallet Issues**

1. **Certificates not found**:
   - Verify `YourPassTypeID.p12` and `WWDR.pem` are in `certs/` directory
   - Check certificate password in `create_wallet_passes_working.py`

2. **Wallet passes not generating**:
   - Ensure OpenSSL is installed: `openssl version`
   - Check that required assets exist in `assets/images/`

3. **Passes not adding to Wallet**:
   - Verify pass URLs are accessible
   - Test with Safari on iOS (other browsers may not work)
   - Check that certificates haven't expired

## Technical Details

### **System Architecture**
- **Static Site Generator**: Jinja2-based templating system
- **Styling**: External CSS with custom properties for easy theming
- **Deployment**: GitHub Pages with git subtree
- **File Structure**: Clean separation of source and generated files
- **Apple Wallet**: PKPass format with TranzerCode-compatible structure

### **Performance Features**
- External CSS reduces HTML file sizes by ~75%
- Cache busting for reliable updates
- Responsive design for all device sizes
- Optimized images and assets

### **Security**
- No server-side processing required
- Static files only
- HTTPS enabled via GitHub Pages
- Apple Wallet passes signed with official certificates

## Contributing

When making changes to the project:

1. Update CSV data or templates as needed
2. Test locally by running `python scripts/generate_site.py`
3. Use `./deploy.sh` for deployment
4. Monitor the live site for proper updates

## Support

For issues or questions:
1. Check this README for common solutions
2. Review `APPLE_WALLET_CHECKLIST.md` for wallet-specific help
3. Verify your CSV data format
4. Ensure all required dependencies are installed

---

**Project Status**: ✅ Production Ready  
**Last Updated**: June 2025  
**Version**: 2.0 (Refactored with Jinja2 + Apple Wallet Integration) 