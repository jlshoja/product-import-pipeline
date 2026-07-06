# 📚 Complete Command Reference - Image Processing System


## 🐍 Python Commands (Direct Execution)

### Activate Virtual Environment First

imagetools_env\Scripts\activate
```


### Download Images

python Fixed_Image_Downloader.py
```

#### Basic Processing
python unified_image_processor.py -i downloaded_images -o output
```

# All options
python unified_image_processor.py -i downloaded_images -o output -s 120 --remove-bg
```

---

### Utility Scripts

#### Check Excel File
```bash
python check_excel.py extracted_products.xlsx
```
Shows valid/empty rows and can create cleaned version

#### Debug Excel Reading
```bash
python debug_excel.py extracted_products.xlsx
```
Shows exactly what's being read from Excel

#### Test Download
```bash
python test_downloader.py
```
Quick test to see if downloader works

#### Direct Download Test
```bash
python direct_download_test.py
```
Run download with live output

#### Reset Download State
```bash
python reset_state.py
```
Clear download progress and start fresh

#### Fix Emoji Encoding
```bash
python fix_emoji_encoding.py
```
Remove emojis from Python files for Windows compatibility

---

### API Server (For Web Panel)

#### Start API Server
```bash
python api_server.py
```

Then open browser: http://localhost:5000

**API Endpoints:**

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Main web panel |
| GET | `/api/status` | Get current status |
| POST | `/api/step1/upload-excel` | Upload Excel file |
| POST | `/api/step1/start-download` | Start download |
| POST | `/api/step2/start-processing` | Start processing |
| GET | `/api/download-results` | Download ZIP |
| POST | `/api/reset` | Reset system |

---

## 📂 File Management

### Important Files

#### Input Files
```
extracted_products.xlsx    # Excel file with Product Name and Product URL columns
```

#### Python Scripts
```
Fixed_Image_Downloader.py      # Download images
unified_image_processor.py     # Process images
api_server.py                  # Backend API server
check_excel.py                 # Check Excel file
debug_excel.py                 # Debug Excel reading
test_downloader.py             # Test downloader
direct_download_test.py        # Direct test with live output
reset_state.py                 # Reset download state
fix_emoji_encoding.py          # Fix emoji issues
```

#### HTML Files
```
unified_web_panel.html         # Web interface
```

#### Batch Files
```
install.bat                    # Setup
download.bat                   # Simple download
download_advanced.bat          # Advanced download
process.bat                    # Simple processing
process_advanced.bat           # Advanced processing
complete_workflow.bat          # Full workflow
quick_start.bat                # Web panel
run.bat                        # Interactive menu
```

#### Output Folders
```
imagetools_env/                # Virtual environment
downloaded_images/             # Downloaded raw images
output/                        # Processed final images
uploads/                       # API uploaded files
```

#### State Files
```
download_state.json            # Download progress (auto-saved)
```

---

### File Operations

#### View Files in Folder
```bash
dir downloaded_images
dir output
```

#### Count Files
```bash
dir /b downloaded_images\*.* | find /c /v ""
dir /b output\*.webp | find /c /v ""
```

#### Delete State File
```bash
del download_state.json
```

#### Clear Output Folder
```bash
del /q output\*.*
```

#### Backup Files
```bash
xcopy downloaded_images downloaded_images_backup\ /E /I
xcopy output output_backup\ /E /I
```

---

## 🔍 Troubleshooting Commands

### Check Python Version
```bash
python --version
```

### Check Installed Packages
```bash
pip list
```

### Check Specific Package
```bash
pip show pandas
pip show rembg
pip show selenium
```

### Reinstall Package
```bash
pip uninstall pandas
pip install pandas
```

### Fix Missing Module
```bash
# If you get "No module named 'X'"
pip install X
```

**Common missing modules:**
```bash
pip install pandas
pip install openpyxl
pip install pillow
pip install selenium
pip install beautifulsoup4
pip install webdriver-manager
pip install "rembg[cpu]"
```

### Test Imports
```bash
python -c "import pandas; print('pandas OK')"
python -c "import PIL; print('PIL OK')"
python -c "import selenium; print('selenium OK')"
python -c "import rembg; print('rembg OK')"
```

### Clear Python Cache
```bash
del /s /q __pycache__
del /s /q *.pyc
```

### Kill Process on Port 5000
```bash
# Find process
netstat -ano | findstr :5000

# Kill process (replace PID with actual number)
taskkill /PID <PID> /F
```

---

## 🎯 Common Workflows

### Workflow 1: First Time Setup
```bash
1. install.bat
2. Place extracted_products.xlsx in folder
3. download.bat
4. process.bat
```

### Workflow 2: Quick Process
```bash
1. download.bat
2. process.bat (choose y for background removal)
```

### Workflow 3: Custom Settings
```bash
1. download_advanced.bat
2. process_advanced.bat
   - Enter custom size: 80
   - Color detection: y
   - Background removal: y
```

### Workflow 4: Complete Automation
```bash
complete_workflow.bat
# Just sit back and wait 50-70 minutes
```

### Workflow 5: Web Panel
```bash
1. quick_start.bat
2. Upload Excel in browser
3. Click "Start Download"
4. Click "Start Processing"
5. Click "Download ZIP"
```

### Workflow 6: Resume Interrupted Download
```bash
# Download was interrupted
download_advanced.bat
# Choose: Resume from last position? y
```

---

## 📊 Expected Output

### Download Output
```
downloaded_images/
├── 4729a.jpg
├── 4729b.jpg
├── 4729c.webp
├── 5707a.png
├── 5707b.jpg
└── ...
```

### Processing Output
```
output/
├── 4729a_black.webp
├── 4729b_blue.webp
├── 5707a_white.webp
└── ...
```

**Naming Convention:**
- Format: `{SKU}{letter}_{color}.webp`
- Example: `4729a_black.webp`
  - `4729` = Product SKU (from Product Name column)
  - `a` = Image variant (a, b, c, d, e, f...)
  - `black` = Detected color
  - `.webp` = Format

---

## ⚙️ Configuration

### Change Max File Size
```bash
# In batch file: Edit default value
# In Python:
python unified_image_processor.py -s 150  # 150KB
```

### Disable Color Detection
```bash
python unified_image_processor.py --no-color
```

### Enable Background Removal
```bash
python unified_image_processor.py --remove-bg
```

### Change Output Folder
```bash
python unified_image_processor.py -o my_output
```

---

## 🆘 Quick Help

### Command Not Found?
```bash
# Make sure virtual environment is activated
imagetools_env\Scripts\activate

# Check if Python is in PATH
python --version
```

### Module Not Found?
```bash
pip install <module-name>
```

### Download Not Starting?
```bash
# Check Excel file exists
dir extracted_products.xlsx

# Test downloader
python test_downloader.py
```

### Processing Not Working?
```bash
# Check input folder exists
dir downloaded_images

# Check images exist
dir downloaded_images\*.*
```

### Web Panel Not Loading?
```bash
# Make sure API server is running
python api_server.py

# Open browser manually
start http://localhost:5000
```

---

## 📝 Notes

### File Requirements
- Excel file must be named `extracted_products.xlsx`
- Must have columns: `Product Name` and `Product URL`
- At least one valid URL required

### System Requirements
- Python 3.12+
- Windows 10/11
- 2GB+ RAM
- 500MB+ free disk space
- Internet connection

### Performance Tips
- Use SSD for faster processing
- Close unnecessary programs
- Use resume feature for large downloads
- Process in batches if system is slow

---

## 🔗 Quick Links

**Essential Files:**
- `extracted_products.xlsx` - Your product links
- `Fixed_Image_Downloader.py` - Download script
- `unified_image_processor.py` - Processing script
- `download_advanced.bat` - Download
- `process_advanced.bat` - Process

**Useful Files:**
- `check_excel.py` - Verify Excel file
- `reset_state.py` - Start fresh
- `run.bat` - Interactive menu

**Advanced:**
- `api_server.py` - Backend server
- `unified_web_panel.html` - Web interface
- `complete_workflow.bat` - Full automation

---

## 📞 Support

If you encounter issues:

1. Check this reference guide
2. Look at error messages
3. Try troubleshooting commands
4. Check that all files are in place
5. Verify virtual environment is activated

---

**Last Updated:** 2026-01-04
**Version:** 2.0
**Author:** Claude + User Collaboration
