# Deploy Digital Contact Cards to GitHub Pages

This guide will help you deploy your digital contact cards to GitHub Pages for free hosting.

## Prerequisites

- A GitHub account
- Your digital contact cards project (this folder)
- Git installed on your computer

## Step 1: Prepare Your Repository

1. **Create a new repository on GitHub:**
   - Go to [github.com](https://github.com) and click "New repository"
   - Name it something like `team-contact-cards` or `digital-business-cards`
   - Make it **Public** (required for free GitHub Pages)
   - Don't initialize with README, .gitignore, or license

2. **Prepare your local files:**
   ```bash
   # Navigate to your project directory
   cd /path/to/your/digital-contact-cards
   
   # Initialize git repository (if not already done)
   git init
   
   # Add all files
   git add .
   
   # Commit files
   git commit -m "Initial commit: Digital contact cards project"
   
   # Add your GitHub repository as remote
   git remote add origin https://github.com/YOUR-USERNAME/YOUR-REPO-NAME.git
   
   # Push to GitHub
   git push -u origin main
   ```

## Step 2: Configure GitHub Pages

1. **Go to your repository on GitHub**
2. **Click on "Settings" tab**
3. **Scroll down to "Pages" in the left sidebar**
4. **Under "Source", select "Deploy from a branch"**
5. **Choose "main" branch**
6. **Choose "/ (root)" folder**
7. **Click "Save"**

## Step 3: Organize Files for GitHub Pages

GitHub Pages will serve files from your repository root. You need to organize your files properly:

1. **Create the proper directory structure:**
   ```
   your-repo/
   ├── assets/
   │   ├── logo.png
   │   └── team/
   │       ├── jane-doe.jpg
   │       ├── john-smith.jpg
   │       └── ... (other team photos)
   ├── html/
   │   ├── jane-doe.html
   │   ├── john-smith.html
   │   └── ... (other contact cards)
   ├── vcf/
   │   ├── jane-doe.vcf
   │   ├── john-smith.vcf
   │   └── ... (other VCF files)
   └── index.html (optional: landing page)
   ```

2. **Copy generated files to the correct locations:**
   ```bash
   # Copy generated HTML files to root html/ directory
   cp output/html/* html/
   
   # Copy generated VCF files to root vcf/ directory  
   cp output/vcf/* vcf/
   
   # Your assets should already be in assets/
   ```

## Step 4: Update VCF Files with GitHub Pages URLs

After deployment, update your VCF files to use the correct GitHub Pages URLs for avatar images:

1. **Find your GitHub Pages URL:**
   - It will be: `https://YOUR-USERNAME.github.io/YOUR-REPO-NAME/`

2. **Update the script to use your actual URL:**
   - Edit `scripts/generate_contact_cards.py`
   - Find the line with `github_avatar_url` (around line 158)
   - Replace `your-username` and `your-repo-name` with your actual values:
   ```python
   github_avatar_url = f"https://YOUR-USERNAME.github.io/YOUR-REPO-NAME/{local_avatar_path.lstrip('../')}"
   ```

3. **Regenerate VCF files:**
   ```bash
   python scripts/generate_contact_cards.py
   cp output/vcf/* vcf/
   ```

## Step 5: Add Team Photos (Optional)

If you have team photos, add them to improve the contact cards:

1. **Resize photos** to reasonable web sizes (e.g., 400x400px or smaller)
2. **Name them** using the same format as generated files:
   - `jane-doe.jpg` for Jane Doe
   - `john-smith.png` for John Smith
   - etc.
3. **Place them** in `assets/team/` directory
4. **Regenerate cards** to include the photos:
   ```bash
   python scripts/generate_contact_cards.py
   cp output/html/* html/
   ```

## Step 6: Create an Index Page (Optional)

Create a landing page that lists all your team members:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Team Contact Cards - Scalewave</title>
    <style>
        body { font-family: sans-serif; margin: 2rem; color: #333; }
        .container { max-width: 800px; margin: auto; text-align: center; }
        .team-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-top: 2rem; }
        .member-card { border: 1px solid #ddd; padding: 1rem; border-radius: 8px; }
        .member-card a { text-decoration: none; color: #007bff; font-weight: bold; }
    </style>
</head>
<body>
    <div class="container">
        <h1>Scalewave Team Contact Cards</h1>
        <p>Click on any team member to view their digital contact card</p>
        
        <div class="team-grid">
            <div class="member-card">
                <h3><a href="html/jane-doe.html">Jane Doe</a></h3>
                <p>Product Manager</p>
            </div>
            <div class="member-card">
                <h3><a href="html/john-smith.html">John Smith</a></h3>
                <p>Senior Developer</p>
            </div>
            <!-- Add more team members as needed -->
        </div>
    </div>
</body>
</html>
```

## Step 7: Deploy and Test

1. **Commit and push your changes:**
   ```bash
   git add .
   git commit -m "Organize files for GitHub Pages deployment"
   git push origin main
   ```

2. **Wait for deployment** (usually 5-10 minutes)

3. **Test your contact cards:**
   - Visit: `https://YOUR-USERNAME.github.io/YOUR-REPO-NAME/html/jane-doe.html`
   - Test the "Save Contact" button downloads
   - Test on mobile devices

## Step 8: Share Your Contact Cards

You can now share your contact cards using URLs like:
- `https://YOUR-USERNAME.github.io/YOUR-REPO-NAME/html/jane-doe.html`
- `https://YOUR-USERNAME.github.io/YOUR-REPO-NAME/html/john-smith.html`

These URLs can be:
- **Embedded in NFC tags**
- **Shared via QR codes**
- **Included in email signatures**
- **Shared directly via links**

## Troubleshooting

**Contact cards not showing up?**
- Check that files are in the `html/` directory at repository root
- Verify GitHub Pages is enabled in repository settings
- Wait a few minutes for deployment to complete

**Logo not showing?**
- Make sure `logo.png` exists in `assets/` directory
- Check the file path in your HTML files is `../assets/logo.png`

**VCF downloads not working?**
- Ensure VCF files are in the `vcf/` directory at repository root
- Check the relative path in HTML files is `../vcf/filename.vcf`

**Avatar images showing as broken?**
- If you don't have photos, the script will hide the avatar automatically
- If you have photos, make sure they're in `assets/team/` with correct filenames

## Updating Contact Cards

To update contact information:

1. **Update `team_data.csv`** with new information
2. **Run the generator script:** `python scripts/generate_contact_cards.py`
3. **Copy updated files:** 
   ```bash
   cp output/html/* html/
   cp output/vcf/* vcf/
   ```
4. **Commit and push changes:**
   ```bash
   git add .
   git commit -m "Update contact information"
   git push origin main
   ```

Your updates will be live within a few minutes! 