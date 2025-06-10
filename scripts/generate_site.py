#!/usr/bin/env python3
"""
Digital Contact Cards Site Generator

A clean, maintainable script for generating HTML contact cards and VCF files
using Jinja2 templating and centralized configuration.

Usage:
    python scripts/generate_site.py

Requirements:
    - Jinja2
    - team_data.csv file in the root directory
    - config.json for settings
    - Templates in templates/ directory
"""

import csv
import json
import os
import re
import shutil
import time
import subprocess
import sys
from pathlib import Path
from jinja2 import Environment, FileSystemLoader, select_autoescape


class ContactCardSiteGenerator:
    """Main class for generating the digital contact cards website."""
    
    def __init__(self, base_dir=None):
        """Initialize the generator with configuration and paths."""
        if base_dir is None:
            base_dir = Path(__file__).parent.parent
        else:
            base_dir = Path(base_dir)
        
        self.base_dir = base_dir
        self.config = self._load_config()
        self._setup_paths()
        self._setup_jinja()
        
    def _load_config(self):
        """Load configuration from config.json."""
        config_file = self.base_dir / "config.json"
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Configuration file not found: {config_file}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in config file: {e}")
    
    def _setup_paths(self):
        """Setup all file and directory paths from configuration."""
        paths = self.config['paths']
        self.csv_file = self.base_dir / paths['csv_file']
        self.templates_dir = self.base_dir / paths['templates_dir']
        self.output_dir = self.base_dir / paths['output_dir']
        self.html_output_dir = self.base_dir / paths['html_output_dir']
        self.vcf_output_dir = self.base_dir / paths['vcf_output_dir']
        self.assets_dir = self.base_dir / paths['assets_dir']
        self.passes_output_dir = self.base_dir / paths['passes_output_dir']
        self.signed_passes_dir = self.base_dir / paths['signed_passes_dir']
        
        # Create output directories
        self.html_output_dir.mkdir(parents=True, exist_ok=True)
        self.vcf_output_dir.mkdir(parents=True, exist_ok=True)
        self.passes_output_dir.mkdir(parents=True, exist_ok=True)
    
    def _setup_jinja(self):
        """Setup Jinja2 environment for templating."""
        self.jinja_env = Environment(
            loader=FileSystemLoader(self.templates_dir),
            autoescape=select_autoescape(['html', 'xml']),
            trim_blocks=True,
            lstrip_blocks=True
        )
    
    def copy_assets_to_output(self):
        """Copy assets directory to output directory for deployment."""
        output_assets_dir = self.output_dir / "assets"
        
        # Remove existing assets directory in output if it exists
        if output_assets_dir.exists():
            shutil.rmtree(output_assets_dir)
        
        # Copy the entire assets directory
        if self.assets_dir.exists():
            shutil.copytree(self.assets_dir, output_assets_dir)
            print("📁 Copied assets directory to output folder")
            return True
        else:
            print("⚠️  Warning: Assets directory not found")
            return False
    
    def clean_filename(self, first_name, last_name):
        """Generate a clean filename from first and last name."""
        # Handle multi-word first names properly
        first_name_clean = first_name.replace(' ', '').lower()
        last_name_clean = last_name.lower()
        filename = f"{first_name_clean}-{last_name_clean}"
        
        # Remove special characters and normalize
        filename = re.sub(r'[^a-z0-9\-]', '', filename)
        filename = re.sub(r'-+', '-', filename)
        return filename.strip('-')
    
    def format_phone(self, phone):
        """Format phone number for display."""
        if not phone:
            return ""
        
        # Remove all non-digit characters except +
        cleaned = re.sub(r'[^\d+]', '', phone)
        
        # Format US numbers
        if cleaned.startswith('+1') and len(cleaned) == 12:
            return f"+1 ({cleaned[2:5]}) {cleaned[5:8]}-{cleaned[8:]}"
        
        return phone
    
    def get_phone_clean(self, phone):
        """Get clean phone number for tel: links."""
        if not phone:
            return ""
        return re.sub(r'[^\d+]', '', phone)
    
    def check_avatar_exists(self, first_name, last_name):
        """Check if avatar image exists in assets/team/ directory."""
        filename = self.clean_filename(first_name, last_name)
        team_dir = self.assets_dir / "team"
        
        if not team_dir.exists():
            return None
            
        # Check for common image extensions
        for ext in ['.jpg', '.jpeg', '.png', '.gif', '.webp']:
            avatar_path = team_dir / f"{filename}{ext}"
            if avatar_path.exists():
                # Return absolute path for deployment
                return f"{self.config['deployment']['base_url']}/assets/team/{filename}{ext}"
        return None
    
    def read_csv_data(self):
        """Read team data from CSV file."""
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                return list(reader)
        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file not found: {self.csv_file}")
    
    def validate_member_data(self, member_data, row_num):
        """Validate and prepare member data."""
        required_fields = self.config['required_fields']
        
        # Check required fields
        missing_fields = [field for field in required_fields 
                         if not member_data.get(field, '').strip()]
        if missing_fields:
            print(f"⚠️  Skipping row {row_num}: Missing required fields: {', '.join(missing_fields)}")
            return None
        
        # Apply defaults for optional fields
        defaults = self.config['defaults']
        for field, default_value in defaults.items():
            if field not in member_data or not member_data[field].strip():
                member_data[field] = default_value
        
        return member_data
    
    def prepare_member_data(self, member_data):
        """Prepare member data with computed fields for templates."""
        prepared = member_data.copy()
        
        # Generate filename
        prepared['filename'] = self.clean_filename(
            member_data['first_name'], 
            member_data['last_name']
        )
        
        # Phone formatting
        prepared['phone_formatted'] = self.format_phone(member_data['phone'])
        prepared['phone_clean'] = self.get_phone_clean(member_data['phone'])
        
        # Avatar path (now returns absolute URL)
        prepared['avatar_path'] = self.check_avatar_exists(
            member_data['first_name'], 
            member_data['last_name']
        )
        
        # Ensure Twitter handle format
        twitter = member_data.get('twitter_handle', '').strip()
        if twitter and not twitter.startswith('@'):
            prepared['twitter_handle'] = f"@{twitter}"
        
        return prepared
    
    def generate_contact_card(self, member_data, cache_buster):
        """Generate HTML contact card for a single member."""
        template = self.jinja_env.get_template('contact-card.html')
        
        prepared_member = self.prepare_member_data(member_data)
        
        html_content = template.render(
            member=prepared_member,
            config=self.config,
            cache_buster=cache_buster
        )
        
        # Write HTML file
        filename = prepared_member['filename']
        html_file = self.html_output_dir / f"{filename}.html"
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        return filename
    
    def generate_vcf_file(self, member_data):
        """Generate VCF file for a member."""
        prepared_member = self.prepare_member_data(member_data)
        filename = prepared_member['filename']
        
        vcf_content = self._build_vcf_content(prepared_member)
        
        # Write VCF file
        vcf_file = self.vcf_output_dir / f"{filename}.vcf"
        with open(vcf_file, 'w', encoding='utf-8') as f:
            f.write(vcf_content)
        
        return filename
    
    def _build_vcf_content(self, member):
        """Build VCF content for a member."""
        vcf_lines = [
            "BEGIN:VCARD",
            "VERSION:3.0",
            f"FN:{member['first_name']} {member['last_name']}",
            f"N:{member['last_name']};{member['first_name']};;;"
        ]
        
        if member['title']:
            vcf_lines.append(f"TITLE:{member['title']}")
        
        if member['company_name']:
            vcf_lines.append(f"ORG:{member['company_name']}")
        
        if member['phone']:
            vcf_lines.append(f"TEL;TYPE=WORK,VOICE:{member['phone_clean']}")
        
        if member['email']:
            vcf_lines.append(f"EMAIL;TYPE=WORK:{member['email']}")
        
        if member['linkedin_url']:
            vcf_lines.append(f"URL;TYPE=LinkedIn:{member['linkedin_url']}")
        
        if member['twitter_handle']:
            twitter_url = f"https://twitter.com/{member['twitter_handle'].lstrip('@')}"
            vcf_lines.append(f"URL;TYPE=Twitter:{twitter_url}")
        
        # Add avatar if exists (already absolute URL)
        if member['avatar_path']:
            vcf_lines.append(f"PHOTO;VALUE=URL:{member['avatar_path']}")
        
        vcf_lines.append("END:VCARD")
        return '\n'.join(vcf_lines)
    
    def generate_index_page(self, team_members, cache_buster):
        """Generate the main index.html page."""
        template = self.jinja_env.get_template('index.html')
        
        # Prepare team members data
        prepared_members = [self.prepare_member_data(member) for member in team_members]
        
        html_content = template.render(
            team_members=prepared_members,
            config=self.config,
            cache_buster=cache_buster
        )
        
        # Write index file
        index_file = self.output_dir / "index.html"
        with open(index_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"📄 Generated: index.html")
    
    def check_apple_wallet_requirements(self):
        """Check if Apple Wallet generation requirements are met."""
        requirements_met = {
            'certificates': False,
            'assets': False,
            'script': False
        }
        
        # Check certificates
        cert_path = self.base_dir / "certs" / "YourPassTypeID.p12"
        wwdr_path = self.base_dir / "certs" / "WWDR.pem"
        requirements_met['certificates'] = cert_path.exists() and wwdr_path.exists()
        
        # Check assets
        assets_dir = self.base_dir / "assets" / "images"
        required_assets = ["icon.png", "icon@2x.png", "logo.png", "logo@2x.png"]
        requirements_met['assets'] = assets_dir.exists() and all(
            (assets_dir / asset).exists() for asset in required_assets
        )
        
        # Check script
        wallet_script = self.base_dir / "create_wallet_passes_working.py"
        requirements_met['script'] = wallet_script.exists()
        
        return requirements_met
    
    def generate_apple_wallet_passes(self):
        """Generate Apple Wallet passes by running the wallet script."""
        print("\n🍎 Generating Apple Wallet passes...")
        print("─" * 50)
        
        # Check requirements
        requirements = self.check_apple_wallet_requirements()
        
        if not all(requirements.values()):
            print("⚠️  Apple Wallet requirements not met:")
            if not requirements['certificates']:
                print("   Missing: Apple Developer certificates in certs/ directory")
            if not requirements['assets']:
                print("   Missing: Required assets (icon.png, logo.png, etc.) in assets/images/")
            if not requirements['script']:
                print("   Missing: create_wallet_passes_working.py script")
            print("   Skipping wallet pass generation...")
            return False
        
        # Run the wallet pass generation script
        wallet_script = self.base_dir / "create_wallet_passes_working.py"
        
        try:
            # Change to base directory to run the script
            original_dir = Path.cwd()
            
            try:
                # Change to the project root directory
                import os
                os.chdir(self.base_dir)
                
                # Run the wallet script
                result = subprocess.run(
                    [sys.executable, str(wallet_script)], 
                    capture_output=True, 
                    text=True,
                    cwd=str(self.base_dir)
                )
                
                if result.returncode == 0:
                    print("✅ Apple Wallet passes generated successfully")
                    
                    # Copy passes to output directory
                    return self.copy_passes_to_output()
                else:
                    print(f"❌ Apple Wallet generation failed:")
                    print(f"   Error: {result.stderr}")
                    return False
                    
            finally:
                # Always return to original directory
                os.chdir(original_dir)
                
        except Exception as e:
            print(f"❌ Error running Apple Wallet script: {e}")
            return False
    
    def copy_passes_to_output(self):
        """Copy generated wallet passes from signed_passes/ to output/passes/."""
        if not self.signed_passes_dir.exists():
            print("❌ signed_passes directory not found")
            return False
        
        # Find all .pkpass files
        pkpass_files = list(self.signed_passes_dir.glob("*.pkpass"))
        
        if not pkpass_files:
            print("⚠️  No .pkpass files found in signed_passes directory")
            return False
        
        # Copy each .pkpass file to output/passes/
        copied_count = 0
        for pkpass_file in pkpass_files:
            destination = self.passes_output_dir / pkpass_file.name
            try:
                shutil.copy2(pkpass_file, destination)
                copied_count += 1
                print(f"📱 Copied: {pkpass_file.name}")
            except Exception as e:
                print(f"❌ Failed to copy {pkpass_file.name}: {e}")
        
        if copied_count > 0:
            print(f"✅ Successfully copied {copied_count} wallet passes to output/passes/")
            return True
        else:
            print("❌ No wallet passes were copied")
            return False
    
    def generate_all(self):
        """Generate all HTML and VCF files from CSV data, plus Apple Wallet passes."""
        print("🚀 Starting Digital Contact Cards Site Generation...")
        print("=" * 60)
        
        # Copy assets to output directory first
        self.copy_assets_to_output()
        
        # Read CSV data
        try:
            csv_data = self.read_csv_data()
        except FileNotFoundError as e:
            print(f"❌ Error: {e}")
            return False
        
        if not csv_data:
            print("❌ Error: No data found in CSV file")
            return False
        
        print(f"📊 Found {len(csv_data)} team members in CSV")
        
        # Generate cache buster if enabled
        cache_buster = str(int(time.time())) if self.config.get('cache_busting') else ""
        
        # Process each team member
        valid_members = []
        generated_count = 0
        
        for i, member in enumerate(csv_data, 1):
            # Validate member data
            validated_member = self.validate_member_data(member, i)
            if not validated_member:
                continue
            
            valid_members.append(validated_member)
            
            try:
                # Generate contact card and VCF
                filename = self.generate_contact_card(validated_member, cache_buster)
                self.generate_vcf_file(validated_member)
                
                # Check avatar status
                prepared = self.prepare_member_data(validated_member)
                avatar_status = "✅ with avatar" if prepared['avatar_path'] else "📷 no avatar"
                
                print(f"{avatar_status} Generated: {filename}.html and {filename}.vcf")
                generated_count += 1
                
            except Exception as e:
                print(f"❌ Error processing {validated_member['first_name']} {validated_member['last_name']}: {e}")
                continue
        
        # Generate index page
        if valid_members:
            self.generate_index_page(valid_members, cache_buster)
        
        # Generate Apple Wallet passes
        wallet_success = self.generate_apple_wallet_passes()
        
        # Summary
        print("\n" + "=" * 60)
        print(f"🎉 Successfully generated {generated_count} contact cards!")
        print(f"📁 HTML files: {self.html_output_dir}")
        print(f"📁 VCF files: {self.vcf_output_dir}")
        print(f"🌐 Index page: {self.output_dir}/index.html")
        print(f"📁 Assets copied to: {self.output_dir}/assets")
        
        if wallet_success:
            print(f"📱 Apple Wallet passes: {self.passes_output_dir}")
        else:
            print("⚠️  Apple Wallet passes: Skipped (requirements not met)")
        
        if generated_count > 0:
            print("\n💡 Next steps:")
            print("1. Review generated files in the output/ directory")
            print("2. Test VCF files on mobile devices")
            if wallet_success:
                print("3. Test .pkpass files on iOS devices")
                print("4. Deploy to GitHub Pages with: ./deploy.sh")
            else:
                print("3. Deploy to GitHub Pages with: ./deploy.sh")
        
        return generated_count > 0


def main():
    """Main function to run the site generator."""
    try:
        generator = ContactCardSiteGenerator()
        success = generator.generate_all()
        
        if not success:
            print("\n❌ Site generation failed. Please check the error messages above.")
            return 1
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        return 1


if __name__ == "__main__":
    exit(main()) 