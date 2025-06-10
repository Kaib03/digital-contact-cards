#!/usr/bin/env python3
"""
Digital Contact Card Generator

This script automates the creation of individual HTML digital contact cards 
and VCF files for multiple team members from a CSV data source.

Usage:
    python generate_contact_cards.py

Requirements:
    - team_data.csv file in the root directory
    - example.html template in the templates directory
"""

import csv
import os
import re
from pathlib import Path
import time


class ContactCardGenerator:
    def __init__(self, base_dir=None):
        """Initialize the generator with directory paths."""
        if base_dir is None:
            base_dir = Path(__file__).parent.parent
        else:
            base_dir = Path(base_dir)
        
        self.base_dir = base_dir
        self.templates_dir = base_dir / "templates"
        self.output_dir = base_dir / "output"
        self.html_output_dir = self.output_dir / "html"
        self.vcf_output_dir = self.output_dir / "vcf"
        self.csv_file = base_dir / "team_data.csv"
        self.template_file = self.templates_dir / "example.html"
        self.index_template_file = self.templates_dir / "index_template.html"
        
        # Create output directories
        self.html_output_dir.mkdir(parents=True, exist_ok=True)
        self.vcf_output_dir.mkdir(parents=True, exist_ok=True)
    
    def clean_filename(self, first_name, last_name):
        """Generate a clean filename from first and last name."""
        filename = f"{first_name}-{last_name}".lower()
        # Remove special characters and replace spaces with hyphens
        filename = re.sub(r'[^a-z0-9\-]', '', filename)
        # Remove multiple consecutive hyphens
        filename = re.sub(r'-+', '-', filename)
        return filename.strip('-')
    
    def format_phone(self, phone):
        """Format phone number for display."""
        if not phone:
            return ""
        # Remove all non-digit characters except +
        cleaned = re.sub(r'[^\d+]', '', phone)
        if cleaned.startswith('+1') and len(cleaned) == 12:
            # US format: +1 (XXX) XXX-XXXX
            return f"+1 ({cleaned[2:5]}) {cleaned[5:8]}-{cleaned[8:]}"
        return phone
    
    def read_template(self):
        """Read the HTML template file."""
        try:
            with open(self.template_file, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"Template file not found: {self.template_file}")
    
    def read_csv_data(self):
        """Read team data from CSV file."""
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                return list(reader)
        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file not found: {self.csv_file}")
    
    def check_avatar_exists(self, first_name, last_name):
        """Check if avatar image exists in assets/team/ directory."""
        filename = self.clean_filename(first_name, last_name)
        # Check for common image extensions
        for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
            avatar_path = self.base_dir / "assets" / "team" / f"{filename}{ext}"
            if avatar_path.exists():
                return f"../assets/team/{filename}{ext}"
        return None
    
    def generate_html(self, template, member_data):
        """Generate HTML content by replacing placeholders in template."""
        html_content = template
        
        # Create filename for this member
        filename = self.clean_filename(member_data['first_name'], member_data['last_name'])
        
        # Format phone number
        formatted_phone = self.format_phone(member_data['phone'])
        
        # Check if avatar exists locally
        local_avatar_path = self.check_avatar_exists(member_data['first_name'], member_data['last_name'])
        
        # Add a cache-busting query parameter
        cache_buster = str(int(time.time()))

        # Replace placeholders in template
        replacements = {
            # Cache buster for logo
            '{CACHE_BUSTER}': cache_buster,

            # Page title
            'Jane Doe – Acme Startup': f"{member_data['first_name']} {member_data['last_name']} – {member_data['company_name']}",
            
            # Header name and title
            '<h1>Jane Doe</h1>': f"<h1>{member_data['first_name']} {member_data['last_name']}</h1>",
            '<h2>Product Manager</h2>': f"<h2>{member_data['title']}</h2>",
            
            # Company logo - use absolute GitHub Pages URL for better compatibility
            'https://your-org.github.io/team-contacts/assets/logo.png': 'https://kaib03.github.io/digital-contact-cards/assets/images/logo_hi-res.png',
            'Acme Startup Logo': f"{member_data['company_name']} Logo",
            
            # Avatar image alt text
            'alt="Jane Doe"': f'alt="{member_data["first_name"]} {member_data["last_name"]}"',
            
            # VCF download link - use relative path to vcf directory
            'jane-doe.vcf': f'../vcf/{filename}.vcf',
            
            # Contact information with new structure
            'href="tel:+1234567890"': f'href="tel:{member_data["phone"].replace(" ", "").replace("(", "").replace(")", "").replace("-", "")}"',
            '<span class="label">+1 (234) 567-890</span>': f'<span class="label">{formatted_phone}</span>',
            'href="mailto:jane.doe@acme.com"': f'href="mailto:{member_data["email"]}"',
            '<span class="label">jane.doe@acme.com</span>': f'<span class="label">{member_data["email"]}</span>',
            'href="https://linkedin.com/in/jane-doe"': f'href="{member_data["linkedin_url"]}"',
            'href="https://twitter.com/jane_doe"': f'href="https://twitter.com/{member_data["twitter_handle"].lstrip("@")}"',
            '<span class="label">@jane_doe</span>': f'<span class="label">{member_data["twitter_handle"] if member_data["twitter_handle"].startswith("@") else "@" + member_data["twitter_handle"]}</span>'
        }
        
        # Apply replacements
        for old, new in replacements.items():
            if new:  # Only replace if new value is not empty
                html_content = html_content.replace(old, new)
        
        # Handle avatar image - use local path if exists, otherwise hide the image
        if local_avatar_path:
            html_content = html_content.replace('https://your-org.github.io/team-contacts/assets/jane.jpg', local_avatar_path)
        else:
            # Remove the avatar image element entirely if no local avatar exists
            avatar_pattern = r'<img class="avatar"[^>]*>'
            html_content = re.sub(avatar_pattern, '', html_content)
            # Also remove the comment line above it
            html_content = html_content.replace('<!-- Avatar/photo -->', '')
        
        # Handle optional Twitter section (remove if no Twitter handle)
        if not member_data['twitter_handle']:
            # Remove the entire Twitter contact item
            twitter_pattern = r'<a class="contact-item" href="https://twitter\.com/[^"]*"[^>]*>.*?</a>'
            html_content = re.sub(twitter_pattern, '', html_content, flags=re.DOTALL)
        
        return html_content
    
    def generate_index_page(self, team_data, cache_buster):
        """Generates the main index.html page from a template."""
        try:
            with open(self.index_template_file, 'r', encoding='utf-8') as f:
                index_template = f.read()
        except FileNotFoundError:
            print(f"❌ Index template not found: {self.index_template_file}")
            return

        team_grid_html = ""
        for member in team_data:
            filename = self.clean_filename(member['first_name'], member['last_name'])
            team_grid_html += f"""
            <div class="member-card">
                <h3>{member['first_name']} {member['last_name']}</h3>
                <p>{member['title']}</p>
                <a href="html/{filename}.html" class="view-button">View Contact Card</a>
            </div>
            """
        
        # Replace placeholders
        final_index_html = index_template.replace('{TEAM_GRID}', team_grid_html)
        final_index_html = final_index_html.replace('{CACHE_BUSTER}', cache_buster)

        # Save the index file to the root of the output directory
        index_file_path = self.output_dir / "index.html"
        with open(index_file_path, 'w', encoding='utf-8') as f:
            f.write(final_index_html)
        print(f"📄 Generated: index.html")

    def generate_vcf(self, member_data):
        """Generate VCF content for a team member."""
        filename = self.clean_filename(member_data['first_name'], member_data['last_name'])
        
        vcf_content = [
            "BEGIN:VCARD",
            "VERSION:3.0",
            f"FN:{member_data['first_name']} {member_data['last_name']}",
            f"N:{member_data['last_name']};{member_data['first_name']};;;",
        ]
        
        if member_data['title']:
            vcf_content.append(f"TITLE:{member_data['title']}")
        
        if member_data['company_name']:
            vcf_content.append(f"ORG:{member_data['company_name']}")
        
        if member_data['phone']:
            clean_phone = member_data['phone'].replace(' ', '').replace('(', '').replace(')', '').replace('-', '')
            vcf_content.append(f"TEL;TYPE=WORK,VOICE:{clean_phone}")
        
        if member_data['email']:
            vcf_content.append(f"EMAIL;TYPE=WORK:{member_data['email']}")
        
        if member_data['linkedin_url']:
            vcf_content.append(f"URL;TYPE=LinkedIn:{member_data['linkedin_url']}")
        
        if member_data['twitter_handle']:
            twitter_url = f"https://twitter.com/{member_data['twitter_handle'].lstrip('@')}"
            vcf_content.append(f"URL;TYPE=Twitter:{twitter_url}")
        
        # Use local avatar path if it exists
        local_avatar_path = self.check_avatar_exists(member_data['first_name'], member_data['last_name'])
        if local_avatar_path:
            # For VCF, we need the full URL when deployed to GitHub Pages
            github_avatar_url = f"https://your-username.github.io/your-repo-name/{local_avatar_path.lstrip('../')}"
            vcf_content.append(f"PHOTO;VALUE=URL:{github_avatar_url}")
        
        vcf_content.append("END:VCARD")
        
        return '\n'.join(vcf_content)
    
    def validate_csv_data(self, data):
        """Validate CSV data and required fields."""
        required_fields = ['first_name', 'last_name', 'email']
        
        for i, row in enumerate(data, 1):
            missing_fields = [field for field in required_fields if not row.get(field, '').strip()]
            if missing_fields:
                print(f"Warning: Row {i} is missing required fields: {', '.join(missing_fields)}")
                return False
        return True
    
    def generate_all(self):
        """Generate all HTML and VCF files from CSV data."""
        print("🚀 Starting Digital Contact Card Generation...")
        
        # Read template and data
        try:
            template = self.read_template()
            csv_data = self.read_csv_data()
        except FileNotFoundError as e:
            print(f"❌ Error: {e}")
            return False
        
        if not csv_data:
            print(f"❌ Error: No data found in CSV file")
            return False
        
        print(f"📊 Found {len(csv_data)} team members in CSV")
        
        cache_buster = str(int(time.time()))

        # Generate files for each team member
        generated_count = 0
        for i, member in enumerate(csv_data, 1):
            try:
                # Fill missing optional fields with empty strings
                member.setdefault('company_name', 'Scalewave')
                member.setdefault('title', '')
                member.setdefault('phone', '')
                member.setdefault('linkedin_url', '')
                member.setdefault('twitter_handle', '')
                member.setdefault('avatar_url', '')
                member.setdefault('company_logo_url', 'https://kaib03.github.io/digital-contact-cards/assets/images/logo_hi-res.png')
                
                # Skip if missing required fields
                if not member.get('first_name') or not member.get('last_name') or not member.get('email'):
                    print(f"⚠️  Skipping row {i}: Missing required fields (first_name, last_name, or email)")
                    continue
                
                filename = self.clean_filename(member['first_name'], member['last_name'])
                
                # Check if avatar exists locally
                local_avatar = self.check_avatar_exists(member['first_name'], member['last_name'])
                avatar_status = "✅ with avatar" if local_avatar else "📷 no avatar"
                
                # Generate HTML file
                html_content = self.generate_html(template, member)
                html_file = self.html_output_dir / f"{filename}.html"
                with open(html_file, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                # Generate VCF file
                vcf_content = self.generate_vcf(member)
                vcf_file = self.vcf_output_dir / f"{filename}.vcf"
                with open(vcf_file, 'w', encoding='utf-8') as f:
                    f.write(vcf_content)
                
                print(f"{avatar_status} Generated: {filename}.html and {filename}.vcf")
                generated_count += 1
                
            except Exception as e:
                print(f"❌ Error processing row {i}: {e}")
                continue
        
        # Generate the main index page
        self.generate_index_page(csv_data, cache_buster)

        print(f"\n🎉 Successfully generated {generated_count} contact cards and index page!")
        print(f"📁 HTML files saved to: {self.html_output_dir}")
        print(f"📁 VCF files saved to: {self.vcf_output_dir}")
        
        return generated_count > 0


def main():
    """Main function to run the contact card generator."""
    generator = ContactCardGenerator()
    
    # Check if required files exist
    if not generator.csv_file.exists():
        print(f"❌ Error: CSV file not found at {generator.csv_file}")
        print("Please create a 'team_data.csv' file with your team member data.")
        return
    
    if not generator.template_file.exists():
        print(f"❌ Error: Template file not found at {generator.template_file}")
        print("Please ensure 'example.html' exists in the templates directory.")
        return
    
    # Generate contact cards
    success = generator.generate_all()
    
    if success:
        print("\n💡 Next steps:")
        print("1. Review the generated HTML files in the output/html/ directory")
        print("2. Test the VCF files by downloading them on a mobile device")
        print("3. Deploy the HTML files to your web server or GitHub Pages")
        print("4. Update VCF avatar URLs with your actual GitHub Pages URL after deployment")
    else:
        print("\n❌ Contact card generation failed. Please check the error messages above.")


if __name__ == "__main__":
    main() 