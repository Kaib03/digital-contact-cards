# Digital Contact Card Generator

This project generates a responsive, mobile-first website with digital contact cards for each team member. It's designed for easy sharing via NFC tags, QR codes, or direct links.

![Team Page Screenshot](https://user-images.githubusercontent.com/12345/some-image-url.png) <!-- Replace with an actual screenshot -->

## Features

- **Automated Generation**: Creates individual HTML contact pages from a simple `team_data.csv` file.
- **Central Team Page**: Generates a main `index.html` that links to all team members.
- **Sharable vCards**: Each contact page includes a "Save Contact" button to download a `.vcf` file.
- **Customizable**: Easily adapt templates and styles to match your brand.
- **GitHub Pages Ready**: Deploy the generated `output` directory directly to a `gh-pages` branch.

## How to Use

### 1. Update Team Data
Modify the `team_data.csv` file to add, remove, or update team member information. The required fields are `first_name`, `last_name`, and `email`.

You can also add optional fields like:
- `title`
- `phone`
- `linkedin_url`
- `twitter_handle`
- `avatar_url` (if you want to use a remote image)

### 2. Add Avatars (Optional)
For local avatar images, add them to the `assets/team/` directory. The script will automatically find them if they are named in the format `firstname-lastname.jpg` (or other common image formats).

### 3. Generate the Contact Cards
Run the generation script from the project root:
```bash
python3 scripts/generate_contact_cards.py
```

### 4. Review the Output
The generated website will be in the `output/` directory. You can open `output/index.html` in your browser to preview the team page.

### 5. Deploy
The contents of the `output/` directory are ready for deployment. You can host them on any web server or use GitHub Pages.

## Project Structure

- **`scripts/generate_contact_cards.py`**: The main Python script that builds the site.
- **`team_data.csv`**: Your team's contact information.
- **`templates/`**: Contains the HTML templates for the individual cards (`example.html`) and the main team page (`index_template.html`).
- **`assets/`**: Holds static assets like logos and team member avatars.
- **`output/`**: The destination for the generated website files. This is the directory you should deploy.
  - `index.html`: The main team page.
  - `html/`: Contains individual contact card pages.
  - `vcf/`: Contains the generated `.vcf` contact files.

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