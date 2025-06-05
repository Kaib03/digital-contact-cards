#!/usr/bin/env python3
"""
Apple Wallet Pass Preview Generator

This script creates a visual preview of what your Apple Wallet passes will look like
before sending them for signing. This helps you verify the design, colors, and layout.

Usage:
    python preview_wallet_pass.py

Output:
    - Visual mockup images of the passes
    - Shows how they'll appear in Apple Wallet
"""

import csv
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import qrcode

# Import configuration
sys.path.append(str(Path(__file__).parent.parent))
try:
    import config_wallet_passes as config
except ImportError:
    print("❌ Error: config_wallet_passes.py not found!")
    print("Please make sure config_wallet_passes.py exists in the project root.")
    sys.exit(1)


class PassPreviewGenerator:
    def __init__(self, base_dir=None):
        """Initialize the preview generator."""
        if base_dir is None:
            base_dir = Path(__file__).parent.parent
        else:
            base_dir = Path(base_dir)
        
        self.base_dir = base_dir
        self.output_dir = base_dir / "pass_previews"
        self.csv_file = base_dir / "team_data.csv"
        self.fonts_dir = base_dir / "assets" / "fonts"
        
        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
        # Apple Wallet pass dimensions (portrait orientation) - 4X RESOLUTION for maximum quality
        self.scale_factor = 4
        self.pass_width = 375 * self.scale_factor
        self.pass_height = 471 * self.scale_factor
        
        # Pass background color (typically white or very light from config)
        self.pass_bg_color_rgb = self.parse_rgb_color(config.PASS_STYLING["backgroundColor"])
        # Ensure it has alpha for compositing if needed, default to opaque
        self.pass_bg_color_rgba = self.pass_bg_color_rgb + (255,) if len(self.pass_bg_color_rgb) == 3 else self.pass_bg_color_rgb

        # Text colors from config
        self.text_color_name = self.parse_rgb_color(config.PASS_STYLING.get("primaryTextColor", "rgb(15,33,255)")) # Scalewave Blue
        self.text_color_title = self.parse_rgb_color(config.PASS_STYLING.get("secondaryTextColor", "rgb(50,50,50)")) # Darker Gray
        
        label_color_tuple = self.parse_rgb_color(config.PASS_STYLING.get("labelColor", "rgb(102,102,102)"))
        self.label_color_transparent = label_color_tuple + (int(255 * 0.7),) # ~70% Opacity for labels
        self.qr_label_color_solid = self.parse_rgb_color(config.PASS_STYLING.get("qrLabelColor", "rgb(70,70,70)")) # Solid color for QR Label
        
        # Load Scalewave logo
        self.logo_image = self.load_scalewave_logo()
    
    def parse_rgb_color(self, color_str):
        """Parse RGB color string like 'rgb(255, 255, 255)' to tuple."""
        try:
            color_values = color_str.replace('rgb(', '').replace(')', '').split(',')
            return tuple(int(val.strip()) for val in color_values)
        except: return (0,0,0)
    
    def load_scalewave_logo(self):
        """Load the actual Scalewave logo."""
        # Prioritize the cropped version as it might be specifically prepared
        logo_paths = [
            self.base_dir / "assets" / "images" / "logo_scalewave_cropped.png",
            self.base_dir / "assets" / "images" / "logo_scalewave.png", # Original full logo
            self.base_dir / "assets" / "images" / "logo@3x.png",
            self.base_dir / "assets" / "logo.png", 
        ]
        
        for logo_path in logo_paths:
            if logo_path.exists():
                try:
                    logo_img = Image.open(logo_path)
                    if logo_img.mode != 'RGBA':
                        logo_img = logo_img.convert('RGBA')
                    print(f"✓ Loaded Scalewave logo: {logo_path}")
                    return logo_img
                except Exception as e:
                    print(f"⚠️  Warning: Could not load logo file {logo_path}: {e}")
        
        print("❌ Error: Crucial Scalewave logo files not found! Please check assets/images.")
        # Create a placeholder if no logo found to avoid crashing
        placeholder = Image.new('RGBA', (80*self.scale_factor, 30*self.scale_factor), (0,0,0,0)) 
        d = ImageDraw.Draw(placeholder)
        try: 
            fnt = ImageFont.truetype("Arial.ttf", 10*self.scale_factor)
            d.text((5,5), "Logo Missing", font=fnt, fill=(255,0,0,255))
        except: pass # Ignore if font fails for placeholder
        return placeholder
    
    def get_font(self, size, weight="Regular", font_name="Merculia"):
        # Simplified font loading, assuming standard system fonts or specific files
        # This would ideally use a more robust font management or specific font files for Merculia
        font_map = {
            "Merculia-Bold": self.fonts_dir / "Merculia-Bold.otf",
            "Merculia-Medium": self.fonts_dir / "Merculia-Medium.ttf",
            "Merculia-Regular": self.fonts_dir / "Merculia-Medium.ttf", # Fallback Regular to Medium
            "Merculia-Semibold": self.fonts_dir / "Merculia-Semibold.ttf",
            "Merculia-Black": self.fonts_dir / "Merculia-Black.ttf",
            "Helvetica-Bold": "HelveticaNeue-Bold.ttf", # System fallback
            "Helvetica-Regular": "HelveticaNeue.ttf",   # System fallback
        }
        font_key = f"{font_name}-{weight}"
        font_path_obj = font_map.get(font_key)
        # If specific Merculia weight not found, try Merculia-Medium as a default for Merculia
        if font_name == "Merculia" and not (font_path_obj and font_path_obj.exists()):
            font_path_obj = font_map.get("Merculia-Medium") # Default to Medium for Merculia if specific weight missing
        
        font_path_str = str(font_path_obj) if font_path_obj and font_path_obj.exists() else f"{font_name.replace(' ', '')}{weight}.ttf"

        try:
            return ImageFont.truetype(font_path_str, size)
        except IOError:
            print(f"⚠️ Font '{font_path_str}' not found. Trying Arial.")
            try: return ImageFont.truetype("Arial.ttf", size)
            except IOError: return ImageFont.load_default()

    def clean_filename(self, first_name, last_name):
        """Generate a clean filename from first and last name."""
        filename = f"{first_name}-{last_name}".lower()
        import re
        filename = re.sub(r'[^a-z0-9\-]', '', filename)
        filename = re.sub(r'-+', '-', filename)
        return filename.strip('-')
    
    def read_csv_data(self):
        """Read team data from CSV file."""
        try:
            with open(self.csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                return list(reader)
        except FileNotFoundError:
            raise FileNotFoundError(f"CSV file not found: {self.csv_file}")
    
    def create_qr_code(self, url, box_size=6, border=4):
        """Create a QR code for the given URL."""
        qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, 
                           box_size=box_size, border=border)
        qr.add_data(url)
        qr.make(fit=True)
        
        # Create QR code image with white background
        qr_image = qr.make_image(fill_color='black', back_color='white')
        # Convert to RGBA to ensure proper pasting
        if qr_image.mode != 'RGBA':
            qr_image = qr_image.convert('RGBA')
        return qr_image
    
    def draw_rounded_rectangle(self, draw, xy, radius, fill, outline=None, width=1):
        """Draw a rounded rectangle."""
        x1, y1, x2, y2 = [int(round(c)) for c in xy]
        radius = int(round(radius))
        if outline: # Draw outline first if specified
            outline_color = outline[0:3] + (outline[3] if len(outline) > 3 else 255,)
            draw.rounded_rectangle((x1,y1,x2,y2), radius=radius, fill=None, outline=outline_color, width=int(round(width)))
        fill_color = fill[0:3] + (fill[3] if len(fill) > 3 else 255,)
        draw.rounded_rectangle((x1,y1,x2,y2), radius=radius, fill=fill_color)
    
    def create_pass_preview(self, member_data):
        """Create a visual preview of the Apple Wallet pass."""
        filename = self.clean_filename(member_data['first_name'], member_data['last_name'])
        sf = self.scale_factor

        # Page background (light gray, distinct from the white pass card)
        page_bg_color = (230, 230, 230, 255) 
        image = Image.new('RGBA', (self.pass_width, self.pass_height), page_bg_color)
        
        # Pass card properties
        card_width = 335 * sf # Slightly narrower than full width for padding/shadow effect
        card_height = 450 * sf # Adjusted height
        card_x1 = (self.pass_width - card_width) // 2
        card_y1 = (self.pass_height - card_height) // 2
        card_x2 = card_x1 + card_width
        card_y2 = card_y1 + card_height
        card_radius = 15 * sf 

        # Simple shadow for the card
        shadow_offset = 4 * sf
        shadow_color = (0, 0, 0, 30) # Softer shadow
        self.draw_rounded_rectangle(ImageDraw.Draw(image), 
                                  (card_x1 + shadow_offset, card_y1 + shadow_offset, 
                                   card_x2 + shadow_offset, card_y2 + shadow_offset), 
                                   card_radius, fill=shadow_color)

        # Draw the actual pass card on top
        draw = ImageDraw.Draw(image)
        self.draw_rounded_rectangle(draw, (card_x1, card_y1, card_x2, card_y2), card_radius, fill=self.pass_bg_color_rgba)

        # Content padding inside the card
        content_padding_x = 20 * sf
        content_padding_top = 20 * sf
        content_padding_bottom = 20 * sf
        content_x_start = card_x1 + content_padding_x
        content_width_actual = card_width - (2 * content_padding_x)
        
        current_y = float(card_y1 + content_padding_top) # Start current_y as float for precision, cast to int for drawing

        # --- TOP ROW: Logo (Left) & "CONTACT CARD" (Right) ---
        logo_max_height = 50 * sf # Max height for logo (equiv. 50px @1x)
        actual_logo_width, actual_logo_height = 0, 0
        if self.logo_image:
            img_w, img_h = self.logo_image.size
            aspect_ratio = img_w / img_h if img_h > 0 else 1
            
            actual_logo_height = min(logo_max_height, int(round(img_h * sf))) if img_h * sf < logo_max_height else logo_max_height
            actual_logo_width = int(round(actual_logo_height * aspect_ratio))

            if actual_logo_width > 0 and actual_logo_height > 0:
                logo_to_draw = self.logo_image.resize((actual_logo_width, actual_logo_height), Image.Resampling.LANCZOS)
                image.paste(logo_to_draw, (content_x_start, int(round(current_y))), logo_to_draw)
            else: # Placeholder or missing logo might have 0 dimensions
                actual_logo_width, actual_logo_height = 0,0 # Ensure these are zero if no logo drawn
        
        header_font_size = 13 * sf 
        header_font = self.get_font(header_font_size, "Medium")
        header_text = "CONTACT CARD"
        header_bbox = draw.textbbox((0,0), header_text, font=header_font)
        header_text_width = header_bbox[2] - header_bbox[0]
        header_text_height = header_bbox[3] - header_bbox[1]
        header_x = card_x2 - content_padding_x - int(round(header_text_width))
        
        # Attempt to vertically align header text with logo space, or just place it if no logo
        effective_top_row_item_height = actual_logo_height if actual_logo_height > 0 else header_text_height
        header_y = current_y + (effective_top_row_item_height - header_text_height) / 2
        if actual_logo_height == 0: header_y = current_y # if no logo, header is at current_y

        draw.text((header_x, int(round(header_y))), header_text, font=header_font, fill=self.label_color_transparent)
        current_y += max(actual_logo_height, header_text_height) + (25 * sf) # Space after top row

        # --- NAME --- (Left Aligned)
        name_font_size = 26 * sf 
        name_font = self.get_font(name_font_size, "Bold")
        name_label_font_size = 11*sf
        name_label_font = self.get_font(name_label_font_size, "Medium")
        name_label_text = "NAME"
        name_label_bbox = draw.textbbox((0,0), name_label_text, font=name_label_font)
        draw.text((content_x_start, int(round(current_y))), name_label_text, font=name_label_font, fill=self.label_color_transparent)
        current_y += (name_label_bbox[3] - name_label_bbox[1]) + (8 * sf) # Increased space after label
        
        name_text = f"{member_data['first_name']} {member_data['last_name']}"
        draw.text((content_x_start, int(round(current_y))), name_text, font=name_font, fill=self.text_color_name)
        name_bbox = draw.textbbox((0,0),name_text,font=name_font)
        current_y += (name_bbox[3]-name_bbox[1]) + (18 * sf) # Space after name value

        # --- TITLE --- (Left Aligned)
        title_font_size = 20 * sf
        title_font = self.get_font(title_font_size, "Medium")
        title_label_font_size = 11*sf
        title_label_font = self.get_font(title_label_font_size, "Medium")
        title_label_text = "TITLE"
        title_label_bbox = draw.textbbox((0,0), title_label_text, font=title_label_font)
        draw.text((content_x_start, int(round(current_y))), title_label_text, font=title_label_font, fill=self.label_color_transparent)
        current_y += (title_label_bbox[3] - title_label_bbox[1]) + (8 * sf) # Increased space after label

        title_text = member_data['title']
        draw.text((content_x_start, int(round(current_y))), title_text, font=title_font, fill=self.text_color_title)
        title_bbox = draw.textbbox((0,0),title_text,font=title_font)
        current_y += (title_bbox[3]-title_bbox[1]) + (30 * sf) # Space after title, before QR
        
        # --- QR CODE & LABEL --- (Centered)
        qr_content_size = int(round(content_width_actual * 0.55)) # QR code ~55% of content width
        qr_box_size = qr_content_size // 38 if qr_content_size // 38 >=1 else 1
        qr_border = 2 # Smaller border for QR
        qr_image_pil = self.create_qr_code(f"{config.GITHUB_PAGES_URL}html/{filename}.html", 
                                           box_size=qr_box_size, # box_size must be >=1
                                           border=qr_border)
        
        # Calculate actual QR image size generated by library (it adds border etc)
        actual_qr_pil_size = qr_image_pil.size[0]
        # Resize it to fit our target qr_content_size using NEAREST to keep sharpness
        qr_display_size = qr_content_size 
        qr_image_resized = qr_image_pil.resize((qr_display_size, qr_display_size), Image.Resampling.NEAREST)
        
        qr_x = content_x_start + (content_width_actual - qr_display_size) // 2
        # Ensure QR code does not overflow card bottom
        available_space_for_qr_and_label = card_y2 - current_y - content_padding_bottom
        qr_label_font_size = 11 * sf
        qr_label_font = self.get_font(qr_label_font_size, "Medium")
        qr_label_text = "SCAN TO CONNECT"
        qr_label_bbox = draw.textbbox((0,0), qr_label_text, font=qr_label_font)
        qr_label_height = qr_label_bbox[3] - qr_label_bbox[1]
        qr_label_spacing = 6 * sf

        if available_space_for_qr_and_label < (qr_display_size + qr_label_height + qr_label_spacing):
            reduction = (qr_display_size + qr_label_height + qr_label_spacing) - available_space_for_qr_and_label
            qr_display_size -= int(round(reduction))
            qr_display_size = max(qr_display_size, 40 * sf) 
            qr_image_resized = qr_image_pil.resize((qr_display_size, qr_display_size), Image.Resampling.NEAREST)
            qr_x = content_x_start + (content_width_actual - qr_display_size) // 2
        
        # QR Background Bubble
        bubble_padding = 8 * sf
        bubble_x1 = qr_x - bubble_padding
        bubble_y1 = current_y - bubble_padding
        bubble_x2 = qr_x + qr_display_size + bubble_padding
        bubble_y2 = current_y + qr_display_size + bubble_padding
        bubble_radius = 5 * sf 
        self.draw_rounded_rectangle(draw, (bubble_x1, bubble_y1, bubble_x2, bubble_y2), bubble_radius, fill=(255,255,255,255)) # Opaque white bubble
        
        # Paste QR code without using itself as mask to avoid transparency issues
        image.paste(qr_image_resized, (int(round(qr_x)), int(round(current_y))))
        current_y += qr_display_size + qr_label_spacing

        qr_label_width = qr_label_bbox[2] - qr_label_bbox[0]
        qr_label_x = content_x_start + (content_width_actual - int(round(qr_label_width))) // 2
        draw.text((int(round(qr_label_x)), int(round(current_y))), qr_label_text, font=qr_label_font, fill=self.qr_label_color_solid)

        # --- FINAL RESIZE FOR OUTPUT ---
        final_output_width = 375
        final_output_height = 471 # This is the target for the *page*, card is smaller
        final_image = image.resize((final_output_width, final_output_height), Image.Resampling.LANCZOS)
        
        preview_path = self.output_dir / f"{filename}_wallet_pass_preview.png"
        final_image.save(preview_path, 'PNG', optimize=True, compress_level=6) # Good balance
        
        print(f"✓ Preview generated (Top-Left Logo Design): {preview_path}")
        return preview_path
    
    def generate_all_previews(self):
        """Generate previews for all team members."""
        print("🎨 Generating Apple Wallet Pass Previews (Top-Left Logo Design)...")
        print(f"📁 Output directory: {self.output_dir}")
        print(f"📄 Reading data from: {self.csv_file}")
        
        if config.GITHUB_PAGES_URL == "https://your-username.github.io/your-repo-name":
            print("\n❌ Config Error: GITHUB_PAGES_URL needs to be updated in config_wallet_passes.py")
            return []
        print("✅ GitHub Pages URL configured.")
        
        print(f"\n🎨 Pass Design (Using 4x internal rendering):")
        print(f"   Background: {config.PASS_STYLING['backgroundColor']}")
        print(f"   Text: {config.PASS_STYLING['foregroundColor']}")
        print(f"   Labels: {config.PASS_STYLING['labelColor']} (rendered with ~70% alpha)")
        
        try:
            csv_data = self.read_csv_data()
            print(f"\n📋 Found {len(csv_data)} team members.")
        except FileNotFoundError:
            print(f"\n❌ Error: Could not find {self.csv_file}")
            return []
        
        generated_previews = []
        print("\n🔄 Generating previews...")
        for i, member_data in enumerate(csv_data, 1):
            try:
                print(f"   {i}/{len(csv_data)} Processing: {member_data['first_name']} {member_data['last_name']}")
                preview_path = self.create_pass_preview(member_data)
                generated_previews.append(preview_path)
            except Exception as e:
                print(f"❌ Error for {member_data.get('first_name', 'Unknown')}: {e}")
                import traceback
                traceback.print_exc()
                continue
        
        print(f"\n✅ Generated {len(generated_previews)} pass previews!")
        return generated_previews


def main():
    """Main function."""
    try:
        print("🔍 Apple Wallet Pass Preview Generator (Top-Left Logo Attempt)")
        print("=" * 60)
        generator = PassPreviewGenerator()
        previews = generator.generate_all_previews()
        
        if previews:
            print(f"\n🎉 Success! Generated {len(previews)} previews in: {generator.output_dir}")
            print("   Previews reflect top-left logo, top-right header, no line.")
        else:
            print("\n❌ No previews generated. Check errors above.")
            
    except FileNotFoundError as e:
        print(f"❌ Error: {e}")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main() 