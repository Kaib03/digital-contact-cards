#!/usr/bin/env python3
"""
Configuration file for Apple Wallet Pass Generator

Update these values before generating passes:
1. Get Pass Type ID and Team ID from your Apple Developer Account holder
2. Update GitHub Pages URL to match your actual deployment
3. Customize styling and organization details as needed
"""

# =============================================================================
# CRITICAL: UPDATE THESE VALUES BEFORE GENERATING PASSES
# =============================================================================

# Apple Developer Account Information (GET FROM YOUR COLLEAGUE)
PASS_TYPE_IDENTIFIER = "pass.com.yourteam.scalewave.contact"  # REQUIRED: Replace with actual Pass Type ID
TEAM_IDENTIFIER = "YOUR_TEAM_ID"  # REQUIRED: Replace with actual Apple Team ID

# GitHub Pages URL (UPDATE TO MATCH YOUR DEPLOYMENT)
GITHUB_PAGES_URL = "https://kaib03.github.io/digital-contact-cards/"  # REQUIRED: Update with actual URL

# =============================================================================
# ORGANIZATION & BRANDING
# =============================================================================

ORGANIZATION_NAME = "Scalewave"
PASS_DESCRIPTION = "Scalewave Team Contact"

# =============================================================================
# VISUAL STYLING
# =============================================================================

# Clean White Theme (Like Professional Apple Wallet Passes)
PASS_STYLING = {
    "backgroundColor": "rgb(255, 255, 255)",    # Clean white background
    "foregroundColor": "rgb(15, 33, 255)",      # INNOVACIÓN blue (#0b21ff) for text
    "labelColor": "rgb(102, 102, 102)",         # Medium gray for labels
}

# Alternative Scalewave color schemes (uncomment to use):

# Original Scalewave Blue Theme:
# PASS_STYLING = {
#     "backgroundColor": "rgb(15, 33, 255)",      # INNOVACIÓN blue (#0b21ff)
#     "foregroundColor": "rgb(247, 255, 236)",    # PROFESIONALISMO light (#f7ffec)
#     "labelColor": "rgb(185, 244, 132)",         # CONFIANZA green (#b9f484)
# }

# Dark Professional Theme:
# PASS_STYLING = {
#     "backgroundColor": "rgb(31, 75, 140)",      # FORMALIDAD dark blue (#1f4b8c)
#     "foregroundColor": "rgb(247, 255, 236)",    # PROFESIONALISMO light (#f7ffec)
#     "labelColor": "rgb(185, 244, 132)",         # CONFIANZA green (#b9f484)
# }

# Clean Light Theme:
# PASS_STYLING = {
#     "backgroundColor": "rgb(247, 255, 236)",    # PROFESIONALISMO light (#f7ffec)
#     "foregroundColor": "rgb(31, 75, 140)",      # FORMALIDAD dark blue (#1f4b8c)
#     "labelColor": "rgb(15, 33, 255)",           # INNOVACIÓN blue (#0b21ff)
# }

# High Contrast Theme:
# PASS_STYLING = {
#     "backgroundColor": "rgb(31, 75, 140)",      # FORMALIDAD dark blue (#1f4b8c)
#     "foregroundColor": "rgb(255, 255, 255)",    # Pure white
#     "labelColor": "rgb(185, 244, 132)",         # CONFIANZA green (#b9f484)
# }

# Original color schemes for reference:

# Dark theme (original default)
# PASS_STYLING = {
#     "backgroundColor": "rgb(25, 25, 25)",
#     "foregroundColor": "rgb(255, 255, 255)", 
#     "labelColor": "rgb(200, 200, 200)",
# }

# Professional Blue Theme:
# PASS_STYLING = {
#     "backgroundColor": "rgb(0, 51, 102)",     # Navy blue
#     "foregroundColor": "rgb(255, 255, 255)",  # White text
#     "labelColor": "rgb(173, 216, 230)",       # Light blue labels
# }

# Clean White Theme:
# PASS_STYLING = {
#     "backgroundColor": "rgb(255, 255, 255)",  # White background
#     "foregroundColor": "rgb(33, 33, 33)",     # Dark gray text
#     "labelColor": "rgb(102, 102, 102)",       # Medium gray labels
# }

# Corporate Green Theme:
# PASS_STYLING = {
#     "backgroundColor": "rgb(0, 100, 0)",      # Forest green
#     "foregroundColor": "rgb(255, 255, 255)",  # White text
#     "labelColor": "rgb(144, 238, 144)",       # Light green labels
# }

# =============================================================================
# ADVANCED OPTIONS (OPTIONAL)
# =============================================================================

# Pass updates via web service (leave None if not using)
WEB_SERVICE_URL = None  # Example: "https://yourserver.com/passes/"
AUTHENTICATION_TOKEN = None  # Example: "your-auth-token-here"

# Image specifications (you usually don't need to change these)
IMAGE_SPECS = {
    "icon.png": (29, 29),
    "icon@2x.png": (58, 58),
    "icon@3x.png": (87, 87),
    "logo.png": (160, 50),
    "logo@2x.png": (320, 100),
    "logo@3x.png": (480, 150)
}

# =============================================================================
# VALIDATION FUNCTION
# =============================================================================

def validate_config():
    """Validate that required configuration values are set."""
    errors = []
    
    if PASS_TYPE_IDENTIFIER == "pass.com.yourteam.scalewave.contact":
        errors.append("PASS_TYPE_IDENTIFIER must be updated with actual Pass Type ID from Apple Developer Account")
    
    if TEAM_IDENTIFIER == "YOUR_TEAM_ID":
        errors.append("TEAM_IDENTIFIER must be updated with actual Team ID from Apple Developer Account")
    
    if GITHUB_PAGES_URL == "https://your-username.github.io/your-repo-name":
        errors.append("GITHUB_PAGES_URL must be updated with your actual GitHub Pages URL")
    
    if errors:
        print("❌ Configuration Errors:")
        for error in errors:
            print(f"   • {error}")
        print("\n📝 Please update config_wallet_passes.py before generating passes.")
        return False
    
    print("✅ Configuration looks good!")
    return True

# =============================================================================
# INSTRUCTIONS
# =============================================================================

INSTRUCTIONS = """
🔧 Configuration Instructions:

1. PASS_TYPE_IDENTIFIER: 
   - Get this from your Apple Developer Account holder
   - Format: pass.com.yourcompany.yourapp.type
   - Example: pass.com.scalewave.contacts.team

2. TEAM_IDENTIFIER:
   - This is the Team ID from the Apple Developer Account
   - It's a 10-character string like "ABC123DEFG"
   - Found in Apple Developer portal under "Membership"

3. GITHUB_PAGES_URL:
   - Your actual GitHub Pages URL where contact cards are hosted
   - Example: https://scalewave.github.io/team-contacts

4. Test the configuration:
   - Run: python config_wallet_passes.py
   - This will validate your settings

5. Generate passes:
   - Run: python scripts/generate_wallet_passes.py
   - This will create pass bundles ready for signing
"""

if __name__ == "__main__":
    print("🔧 Apple Wallet Pass Configuration")
    print("=" * 50)
    print(INSTRUCTIONS)
    print("\n🔍 Validating current configuration...")
    validate_config() 