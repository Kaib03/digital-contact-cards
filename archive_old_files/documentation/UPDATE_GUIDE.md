# 🚀 Complete Update Guide for Digital Contact Cards

## ✅ **Logo Update Complete!**
- **Home page logo**: Now 300px (50% bigger)
- **Contact card logos**: Now 200px (43% bigger)
- **Much more prominent branding** across the entire site

---

## 📝 **When You Want to Update Contact Information**

### **Step 1: Edit Your Data**
1. Open `team_data.csv` in any text editor or Excel
2. Update contact information (names, emails, phone numbers, etc.)
3. Save the file

### **Step 2: Regenerate & Deploy**
Run the deployment script:
```bash
./documentation/deploy.sh
```

This automatically:
- ✅ Regenerates all HTML contact cards
- ✅ Regenerates all VCF files  
- ✅ Copies files to the correct directories for GitHub Pages

### **Step 3: Commit to GitHub**
```bash
git add .
git commit -m "Update contact information"
git push origin main
```

### **Step 4: Verify Live Site**
- **Wait 2-5 minutes** for GitHub Pages to rebuild
- **Check your site**: `https://Kaib03.github.io/digital-contact-cards/`
- **Hard refresh** browser (Ctrl+Shift+R or Cmd+Shift+R) if needed

---

## 📸 **Adding Team Photos**

### **Step 1: Prepare Photos**
1. **Resize photos** to 400x400px or smaller (for web performance)
2. **Name them correctly** using the same format as contact cards:
   - `jane-doe.jpg` for Jane Doe
   - `john-smith.png` for John Smith  
   - `sarah-johnson.jpeg` for Sarah Johnson
   - etc.

### **Step 2: Place Photos**
Put photos in: `assets/team/` directory

### **Step 3: Regenerate**
```bash
./deploy.sh
git add .
git commit -m "Add team photos"
git push origin main
```

Photos will automatically appear in contact cards!

---

## 🎨 **Making Design Changes**

### **Template Changes** (affects all contact cards)
1. **Edit**: `templates/example.html`
2. **Regenerate**: `./deploy.sh`
3. **Commit**: Follow Step 3 above

### **Home Page Changes**
1. **Edit**: `index.html` directly
2. **Commit**: Follow Step 3 above (no need to regenerate)

---

## 🔧 **Troubleshooting GitHub Pages**

### **If Changes Don't Show Up Online:**

1. **Wait longer** - GitHub Pages can take up to 10 minutes
2. **Hard refresh** your browser (Ctrl+Shift+F5)
3. **Try incognito/private mode** to bypass browser cache
4. **Force rebuild** by making a tiny change:
   ```bash
   # Add a comment to index.html, then:
   git add .
   git commit -m "Force rebuild"
   git push origin main
   ```

### **Check GitHub Pages Status:**
1. Go to your GitHub repository
2. Click **Settings** → **Pages**
3. Ensure it shows: "Your site is published at..."

---

## 📋 **Complete Workflow Checklist**

When updating contact information:

- [ ] Edit `team_data.csv`
- [ ] Run `./deploy.sh`
- [ ] Run `git add .`
- [ ] Run `git commit -m "Update contact information"`
- [ ] Run `git push origin main`
- [ ] Wait 2-5 minutes
- [ ] Hard refresh browser and test live site
- [ ] Verify contact cards and VCF downloads work

---

## 🎯 **Quick Commands Reference**

### **Full Update Workflow:**
```bash
# 1. Edit team_data.csv first, then:
./documentation/deploy.sh
git add .
git commit -m "Update contact information"
git push origin main
```

### **Emergency Rebuild:**
```bash
git add .
git commit -m "Force rebuild" --allow-empty
git push origin main
```

### **Check What's Changed:**
```bash
git status
git diff
```

---

## 🌐 **Your Live URLs**

- **Home Page**: `https://Kaib03.github.io/digital-contact-cards/`
- **Individual Cards**: `https://Kaib03.github.io/digital-contact-cards/html/[name].html`

Example: `https://Kaib03.github.io/digital-contact-cards/html/jane-doe.html`

---

## 💡 **Pro Tips**

1. **Always test locally first** - open `html/jane-doe.html` in your browser
2. **Keep backups** of your `team_data.csv` file
3. **Use descriptive commit messages** for easy tracking
4. **Test VCF downloads** on mobile devices after updates
5. **Update one person at a time** for large changes to avoid errors

Your contact cards are now ready with **much bigger logos** and you have a bulletproof update process! 🎉 