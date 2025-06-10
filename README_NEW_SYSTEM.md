# Digital Contact Cards - Refactored System

This project generates beautiful HTML digital contact cards and Apple Wallet passes for team members from a simple CSV file.

## 🎉 What's New (Refactored System)

The HTML generation system has been completely refactored to be **clean, maintainable, and robust**:

### ✅ **Key Improvements**
- **Proper Templating**: Uses Jinja2 instead of brittle string replacement
- **External CSS**: Single stylesheet with CSS custom properties for easy theming
- **Configuration-Driven**: Centralized settings in `config.json`
- **Clean Code**: Well-organized, class-based architecture
- **Better Error Handling**: Comprehensive validation and user-friendly messages
- **Smaller Files**: ~75% reduction in HTML file sizes
- **Easy Maintenance**: Change CSS once, applies everywhere

### 🗂️ **New File Structure**
```
digital-contact-cards/
├── assets/
│   ├── css/
│   │   └── style.css           # Single external stylesheet
│   ├── images/                 # Company logos, etc.
│   └── team/                   # Team member avatars (optional)
├── templates/
│   ├── base.html              # Base template with common structure
│   ├── contact-card.html      # Individual contact card template
│   ├── index.html             # Team index page template
│   └── vcard_template.vcf     # VCF template (unchanged)
├── scripts/
│   ├── generate_site.py       # New clean generation script
│   └── (old scripts preserved)
├── output/
│   ├── html/                  # Generated HTML contact cards
│   ├── vcf/                   # Generated VCF files
│   └── index.html             # Team index page
├── config.json                # Centralized configuration
├── team_data.csv              # Team member data
└── requirements.txt           # Dependencies (includes Jinja2)
```

## 🚀 **Simple Workflow**

### **1. Update Team Data**
Edit `team_data.csv` with team member information:
```csv
first_name,last_name,title,company_name,phone,email,linkedin_url,twitter_handle
John,Doe,Software Engineer,ScaleWave,+1234567890,john@scalewave.es,https://linkedin.com/in/johndoe,@johndoe
```

### **2. Generate Website**
Run the generation script:
```bash
python scripts/generate_site.py
```

### **3. Deploy (Optional)**
Upload the `output/` directory to your web server or GitHub Pages.

That's it! 🎉

## 📋 **Requirements**

### **Python Dependencies**
Install once:
```bash
pip install Jinja2==3.1.2
```

### **Required CSV Fields**
- `first_name` - Person's first name
- `last_name` - Person's last name  
- `email` - Email address

### **Optional CSV Fields**
- `title` - Job title
- `company_name` - Company name (defaults to ScaleWave)
- `phone` - Phone number
- `linkedin_url` - LinkedIn profile URL
- `twitter_handle` - Twitter handle (with or without @)

## ⚙️ **Configuration**

All settings are centralized in `config.json`:

```json
{
  "company": {
    "name": "ScaleWave",
    "logo_url": "https://kaib03.github.io/digital-contact-cards/assets/images/logo_hi-res.png"
  },
  "deployment": {
    "github_pages_url": "https://kaib03.github.io/digital-contact-cards",
    "base_url": "https://kaib03.github.io/digital-contact-cards"
  },
  "defaults": {
    "company_name": "ScaleWave",
    "title": "Team Member"
  }
}
```

### **Easy Customization**
- **Company branding**: Update `company.name` and `company.logo_url`
- **Deployment URLs**: Update `deployment` section for your GitHub Pages
- **Default values**: Modify `defaults` for missing CSV fields

## 🎨 **Styling & Theming**

All styles are in `assets/css/style.css` with CSS custom properties for easy theming:

```css
:root {
  --primary-color: #1f4b8c;      /* Main brand color */
  --secondary-color: #2d5aa0;    /* Secondary brand color */
  --card-background: #ffffff;    /* Card background */
  /* ... more variables */
}
```

**To change the theme**: Simply update the CSS custom properties and regenerate!

## 🖼️ **Team Avatars (Optional)**

Place team member photos in `assets/team/` using the format:
- `firstname-lastname.jpg` (or .png, .gif, .webp)
- Example: `john-doe.jpg` for John Doe

The system automatically detects and includes avatars when available.

## 📱 **Apple Wallet Integration**

The Apple Wallet generation (`create_wallet_passes_working.py`) remains unchanged and continues to work perfectly with the new HTML system. The QR codes in wallet passes link to the generated HTML contact cards.

## 🔧 **Advanced Usage**

### **Custom Templates**
Modify templates in `templates/` directory:
- `base.html` - Common HTML structure
- `contact-card.html` - Individual contact cards
- `index.html` - Team index page

### **Multiple Environments**
Create different `config.json` files for development/production:
```bash
cp config.json config-dev.json
# Edit config-dev.json for development URLs
```

## 🆚 **Comparison: Old vs New**

| Aspect | Old System | New System |
|--------|------------|------------|
| **Templating** | String replacement | Jinja2 templates |
| **CSS** | Inline (150+ lines per file) | External stylesheet |
| **Configuration** | Hard-coded values | Centralized config.json |
| **Code Structure** | 347-line monolithic script | Clean class-based architecture |
| **File Size** | ~4.5KB per HTML file | ~1.2KB per HTML file |
| **Maintainability** | Difficult to modify | Easy to maintain and extend |
| **Error Handling** | Basic | Comprehensive validation |

## 🏗️ **For Developers**

### **Project Structure**
- `ContactCardSiteGenerator` class handles all generation logic
- Jinja2 templates provide clean separation of content and presentation
- Configuration-driven approach makes the system flexible
- Comprehensive error handling and validation

### **Key Methods**
- `generate_all()` - Main generation method
- `generate_contact_card()` - Individual card generation
- `generate_index_page()` - Team index page
- `validate_member_data()` - Data validation

### **Adding New Fields**
1. Add field to CSV
2. Update `config.json` defaults if needed
3. Modify templates to display the new field
4. Regenerate site

## 🎯 **Benefits Achieved**

✅ **Eliminated redundancy** - Removed duplicate template files  
✅ **Improved code structure** - Clean, class-based architecture  
✅ **Proper templating** - Jinja2 instead of string replacement  
✅ **Centralized styling** - Single external stylesheet  
✅ **Easy workflow** - Simple 3-step process  
✅ **Better maintenance** - Easy to modify and extend  
✅ **Smaller files** - 75% reduction in HTML file sizes  
✅ **Professional grade** - Industry-standard templating system  

---

## 🔗 **Related Files**

- **Apple Wallet Generation**: `create_wallet_passes_working.py` (unchanged)
- **Original System**: `scripts/generate_contact_cards.py` (preserved for reference)
- **Team Data**: `team_data.csv`
- **Assets**: `assets/` directory

The new system maintains full compatibility with existing Apple Wallet functionality while providing a dramatically improved HTML generation experience. 