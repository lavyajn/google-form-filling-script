# Google Form Automation - Python (Selenium) Assignment

This project automates the process of filling a Google Form using Selenium WebDriver and sends the submission via email using Flask.

## 📋 Assignment Overview

**Company:** Medius Technologies  
**Position:** Selenium Web Scraper Developer  
**Task:** Create a Python script to automatically fill a Google Form and submit assignment via email

## 🎯 Features

- **Automated Form Filling:** Populates all form fields automatically using Selenium
- **Multiple XPath Strategies:** Robust element location with fallback strategies
- **CAPTCHA Handling:** Pauses for manual CAPTCHA verification
- **Screenshot Capture:** Automatically saves confirmation page screenshot
- **Email Submission:** Flask-based email sender with screenshot attachment
- **Error Handling:** Comprehensive logging and debug screenshots
- **Professional Output:** Clean, production-ready console logs

## 🛠️ Technologies Used

- Python 3.x
- Selenium WebDriver
- Chrome WebDriver (via webdriver-manager)
- Flask
- SMTP (Gmail)

## 📁 Project Structure

```
google-form-automation/
├── fill_form.py              # Main form automation script
├── send_submission.py        # Flask email submission script
├── requirements.txt          # Python dependencies
├── README.md                 # This file
├── confirmation.png          # Generated screenshot (after running)
└── debug_screenshots/        # Debug screenshots folder (auto-created)
```

## 🚀 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/lavyajn/google-form-filling-script.git
cd google-form-filling-script
```

### 2. Create Virtual Environment (Recommended)
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On Linux/Mac
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Install Chrome Browser
Make sure Google Chrome is installed on your system. The script will automatically download the appropriate ChromeDriver.

## ⚙️ Configuration

### Form Automation (`fill_form.py`)

Update the `YOUR_DATA` dictionary with your information from config.py which has to be created expilicitly:

```python
YOUR_DATA = {
    "Full Name": "Your Name",
    "Contact Number": "1234567890",
    "Email Id": "your.email@example.com",
    "Full Address": "Your complete address",
    "Pincode": "123456",
    "Date of Birth": "MM/DD/YYYY",
    "Gender": "Male"  # or "Female" or "Other"
}

FORM_URL = "https://forms.gle/YOUR_FORM_ID"
```

### Email Submission (`send_submission.py`)

Update email credentials and details:

```python
SENDER_EMAIL = "your.email@gmail.com"
SENDER_PASSWORD = "your-app-password"  # Use Gmail App Password

RECIPIENT_EMAIL = "your.recipient@gmail.com"
CC_EMAIL = "your.cc@gmail.com"

NAME = "Your Name"
GITHUB_REPO = "https://github.com/yourusername/your-repo"
RESUME_LINK = "https://your-resume-link.com"
PAST_WORK = "https://github.com/yourusername"
AVAILABILITY = "Your availability details"
```

**Note:** For Gmail, you need to create an [App Password](https://support.google.com/accounts/answer/185833) instead of using your regular password.

## 📖 Usage

### Step 1: Fill the Google Form

```bash
python fill_form.py
```

**What happens:**
1. Opens Chrome browser
2. Navigates to the Google Form
3. Automatically fills all fields
4. Waits for you to:
   - Select Gender (if not auto-filled)
   - Solve the CAPTCHA
   - Click Submit
5. Detects submission and saves screenshot as `confirmation.png`

**Console Output Example:**
```
======================================================================
GOOGLE FORM AUTOMATION SCRIPT
======================================================================

[CONFIG] Form data loaded:
  Full Name: Lavya Jain
  Contact Number: 9876543210
  ...

[LOADING] Opening form URL: https://forms.gle/...
[SUCCESS] Form loaded successfully
[FILLED] Full Name: Lavya Jain
[FILLED] Contact Number: 9876543210
...
[SUCCESS] All form fields filled successfully

======================================================================
MANUAL VERIFICATION REQUIRED
======================================================================
```

### Step 2: Send Email via Flask

**Method 1: Run Flask App**
```bash
flask --app send_submission run
```
Then open in browser: `http://127.0.0.1:5000/send-email`

**Method 2: Direct Execution**
```bash
python send_submission.py
```
Then open in browser: `http://127.0.0.1:5000/send-email`

**Email will include:**
- Screenshot of confirmation page
- All 6 required submission items

## 🔧 Technical Approach

### Form Field Location Strategy

The script uses a **multi-strategy approach** to locate form elements:

```python
# Strategy 1: Find by class and text
"//*[contains(text(), 'Label')]/ancestor::div[contains(@class, 'Qr7Oae')]//input"

# Strategy 2: Navigate through parent elements
"//*[contains(text(), 'Label')]/parent::*/parent::*/parent::*//input"

# Strategy 3: Use form viewer components
"//div[contains(@class, 'freebirdFormviewerComponentsQuestionTextRoot')]//input"

# Strategy 4: Following sibling approach
"//div[contains(., 'Label')]/following::input[1]"
```

This ensures **maximum compatibility** across different Google Form structures.

### Error Handling

- **Try-Catch blocks** for each field
- **Debug screenshots** saved on errors
- **Graceful degradation** - continues even if one field fails
- **Detailed logging** at every step

### CAPTCHA & Manual Verification

The script **pauses execution** after filling fields, allowing the user to:
1. Manually verify all filled data
2. Solve CAPTCHA/verification code
3. Click Submit button

The script **automatically detects** when the form is submitted by monitoring URL changes.

## 🐛 Troubleshooting

### Issue: Fields not filling
**Solution:** Check debug screenshots in `debug_screenshots/` folder to see the form structure.

### Issue: Chrome driver error
**Solution:** Update webdriver-manager:
```bash
pip install --upgrade webdriver-manager
```

### Issue: Email authentication failed
**Solution:** 
- Use Gmail App Password, not regular password
- Enable "Less secure app access" (if using old Gmail)
- Check credentials in `send_submission.py`

### Issue: Screenshot not found
**Solution:** Run `fill_form.py` first to generate `confirmation.png`

## 📝 Requirements File

```txt
selenium==4.15.2
webdriver-manager==4.0.1
flask==3.0.0
```

## 🎓 Learning Outcomes

This project demonstrates:
- Web automation using Selenium
- Robust element location strategies
- Error handling and logging
- Screenshot capture
- Email automation with attachments
- Flask web framework basics
- Professional code structure and documentation

## 👤 Author

**Lavya Jain**  
Email: lavyajain.dev@gmail.com  
GitHub: [@lavyajn](https://github.com/lavyajn)

## 📄 License

This project is created for the Medius Technologies assignment.

## 🙏 Acknowledgments

- Medius Technologies for the opportunity
- Selenium WebDriver documentation
- Python community

---



