# Digital Contact Card Generator

This tool automates the creation of individual HTML digital contact cards and VCF files for multiple team members from a CSV data source.

## Features

- ✅ Generates personalized HTML contact cards from CSV data
- ✅ Creates corresponding VCF files for "Save Contact" functionality
- ✅ Handles phone number formatting
- ✅ Supports optional Twitter integration
- ✅ Clean filename generation (e.g., "jane-doe.html")
- ✅ Organized output structure
- ✅ Error handling and validation

## Quick Start

1. **Prepare your data**: Edit `team_data.csv` with your team member information
2. **Run the generator**: `python scripts/generate_contact_cards.py`
3. **Find your files**: Generated files will be in `output/html/` and `output/vcf/`

## CSV File Structure

Your `team_data.csv` file should have the following columns:

| Column | Required | Description | Example |
|--------|----------|-------------|---------|
| `first_name` | ✅ | First name | Jane |
| `last_name` | ✅ | Last name | Doe |
| `email` | ✅ | Email address | jane.doe@scalewave.com |
| `title` | ❌ | Job title | Product Manager |
| `company_name` | ❌ | Company name | Scalewave |
| `phone` | ❌ | Phone number | +1234567890 |
| `linkedin_url` | ❌ | LinkedIn profile | https://linkedin.com/in/janedoe |
| `twitter_handle` | ❌ | Twitter handle | @jane_doe |
| `avatar_url` | ❌ | Profile image URL | https://example.com/jane.jpg |
| `company_logo_url` | ❌ | Company logo URL | https://example.com/logo.png |

### Sample CSV Content

```csv
first_name,last_name,title,company_name,phone,email,linkedin_url,twitter_handle,avatar_url,company_logo_url
Jane,Doe,Product Manager,Scalewave,+1234567890,jane.doe@scalewave.com,https://linkedin.com/in/janedoe,@jane_doe,https://scalewave.com/assets/team/jane.jpg,https://scalewave.com/assets/logo.png
John,Smith,Senior Developer,Scalewave,+1987654321,john.smith@scalewave.com,https://linkedin.com/in/johnsmith,@johnsmith_dev,https://scalewave.com/assets/team/john.jpg,https://scalewave.com/assets/logo.png
```

## Directory Structure

```
digital-contact-cards/
├── scripts/
│   └── generate_contact_cards.py    # Main generator script
├── templates/
│   └── example.html                 # HTML template
├── output/
│   ├── html/                        # Generated HTML files
│   └── vcf/                         # Generated VCF files
├── team_data.csv                    # Your team data
└── README.md                        # This file
```

## Usage

### Basic Usage

```bash
cd digital-contact-cards
python scripts/generate_contact_cards.py
```

### What the Script Does

1. **Reads** your `team_data.csv` file
2. **Processes** the HTML template (`templates/example.html`)
3. **Generates** individual HTML files for each team member
4. **Creates** corresponding VCF files for contact saving
5. **Organizes** output into `output/html/` and `output/vcf/` directories

### Generated Files

For a team member "Jane Doe", the script will create:
- `output/html/jane-doe.html` - The contact card webpage
- `output/vcf/jane-doe.vcf` - The vCard file for contact saving

## Phone Number Formatting

The script automatically formats US phone numbers:
- Input: `+1234567890` or `1234567890`
- Display: `+1 (234) 567-890`
- VCF: `+1234567890` (clean format for contact apps)

## Customization

### Modifying the HTML Template

Edit `templates/example.html` to customize:
- Styling and layout
- Additional contact fields
- Company branding

### Default Values

The script uses these defaults for missing data:
- `company_name`: "Scalewave"
- `company_logo_url`: Uses template default
- Optional fields are simply omitted if empty

## Error Handling

The script will:
- ✅ Skip rows with missing required fields (first_name, last_name, email)
- ✅ Show clear error messages for missing files
- ✅ Continue processing even if individual rows fail
- ✅ Report the total number of successfully generated files

## Deployment

### For Web Use
1. Upload HTML files to your web server
2. Ensure VCF files are accessible at the same relative path
3. Update image URLs in your CSV to point to hosted images

### For NFC Tags
1. Program NFC tags with the URLs to your hosted HTML files
2. Test on mobile devices to ensure VCF download works
3. Consider using URL shorteners for cleaner NFC programming

## Dependencies

This script uses only Python standard library modules:
- `csv` - For reading CSV files
- `os` - For file system operations
- `re` - For text processing
- `pathlib` - For path handling

No additional packages required!

## Troubleshooting

### Common Issues

**"CSV file not found"**
- Ensure `team_data.csv` exists in the root directory
- Check file name spelling

**"Template file not found"**
- Ensure `templates/example.html` exists
- Check that the templates directory is present

**"No files generated"**
- Check that your CSV has the required columns: first_name, last_name, email
- Verify your CSV data doesn't have empty required fields

**VCF files not downloading on mobile**
- Ensure your web server serves `.vcf` files with correct MIME type
- Test VCF files by opening them directly in a browser

### Getting Help

If you encounter issues:
1. Check the console output for specific error messages
2. Verify your CSV file format matches the expected structure
3. Ensure all required files are in the correct locations

## License

This project is open source. Feel free to modify and distribute as needed for your organization. 