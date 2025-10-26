import smtplib
import os
from dotenv import load_dotenv 
from email.message import EmailMessage
from flask import Flask

load_dotenv()

# email configuration
SENDER_EMAIL = "lavyajain.dev@gmail.com"
SENDER_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

RECIPIENT_EMAIL = "your.recipient@gmail.com"
CC_EMAIL = "your.cc@gmail.com"

# details to be sent
NAME = "Lavya Jain"
GITHUB_REPO = "https://github.com/lavyajn/google-form-filling-script"
RESUME_LINK = "https://drive.google.com/file/d/1AgDvl3d-KQE-O4zjgxoqRDCJzlfM_kr7/view?usp=drive_link"
PAST_WORK = "https://expense-tracker-frontend-five-iota.vercel.app/login"
AVAILABILITY = "I am only available to work part time from (5pm - 9pm) as i am currently a 5th semster engineering student"

# screenshot of file path
SCREENSHOT_FILE = "confirmation.png"

# initializing Flask App
app = Flask(__name__)

EMAIL_BODY = f"""Dear Hiring Team,

Please find my submission for the Python (Selenium) Assignment.

As requested, my submission includes the following 6 items:

1. Screenshot of Confirmation: Attached to this email ({SCREENSHOT_FILE}).
2. Source Code (GitHub): {GITHUB_REPO}
3. Brief Documentation: The GitHub repository includes a README.md file explaining my approach. The script 'fill_form.py' automates all data entry and pauses for the user to manually solve the CAPTCHA and submit. The 'send_submission.py' script (which sent this email) is a Flask application built to handle the email submission as per the task requirements.
4. My Resume: {RESUME_LINK}
5. Past Work Samples: {PAST_WORK}
6. Availability Confirmation: {AVAILABILITY}

Thank you for the opportunity.

Best regards,
{NAME}
"""

@app.route('/send-email')
def send_email():
    """
    Flask route to send assignment submission email with screenshot attachment
    Access via: http://127.0.0.1:5000/send-email
    """
    print("="*70)
    print("FLASK EMAIL SUBMISSION")
    print("="*70)
    
    print("\n[CONFIG] Email configuration:")
    print(f"  From: {SENDER_EMAIL}")
    print(f"  To: {RECIPIENT_EMAIL}")
    print(f"  CC: {CC_EMAIL}")
    print(f"  Subject: Python (Selenium) Assignment - {NAME}")
    
    # creating email message
    print("\n[INIT] Creating email message...")
    msg = EmailMessage()
    msg['Subject'] = f"Python (Selenium) Assignment - {NAME}"
    msg['From'] = SENDER_EMAIL
    msg['To'] = RECIPIENT_EMAIL
    msg['Cc'] = CC_EMAIL
    msg.set_content(EMAIL_BODY)
    
    # screenshot attatched
    print(f"[ATTACH] Attaching screenshot: {SCREENSHOT_FILE}")
    try:
        if not os.path.exists(SCREENSHOT_FILE):
            error_msg = f"Screenshot file not found: {SCREENSHOT_FILE}"
            print(f"[ERROR] {error_msg}")
            print("[INFO] Please run fill_form.py first to generate the screenshot")
            return f"Error: {error_msg}", 500
        
        with open(SCREENSHOT_FILE, 'rb') as f:
            file_data = f.read()
        
        msg.add_attachment(file_data, maintype='image', subtype='png', filename=SCREENSHOT_FILE)
        print(f"[SUCCESS] Screenshot attached successfully ({len(file_data)} bytes)")
        
    except Exception as e:
        error_msg = f"Failed to attach screenshot: {e}"
        print(f"[ERROR] {error_msg}")
        return f"Error: {error_msg}", 500
    
    # sending email via gmail SMTP
    print("\n[SMTP] Connecting to Gmail SMTP server...")
    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            print("[AUTH] Authenticating...")
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)
            print("[AUTH] Login successful")
            
            print("[SENDING] Sending email...")
            smtp.send_message(msg)
            print("[SUCCESS] Email sent successfully")
        
        success_msg = f"Submission email sent successfully to {RECIPIENT_EMAIL}"
        print(f"\n[COMPLETE] {success_msg}")
        print("="*70)
        
        return success_msg, 200
        
    except smtplib.SMTPAuthenticationError:
        error_msg = "SMTP Authentication failed. Check email and app password."
        print(f"[ERROR] {error_msg}")
        return f"Error: {error_msg}", 500
        
    except Exception as e:
        error_msg = f"Failed to send email: {e}"
        print(f"[ERROR] {error_msg}")
        import traceback
        traceback.print_exc()
        return f"Error: {error_msg}", 500

@app.route('/')
def index():
    """Default route with instructions"""
    return """
    <h1>Python (Selenium) Assignment - Email Submission</h1>
    <p>To send the submission email, visit: <a href="/send-email">/send-email</a></p>
    <p>Or run from terminal:</p>
    <pre>flask --app send_submission run</pre>
    <p>Then open: <a href="http://127.0.0.1:5000/send-email">http://127.0.0.1:5000/send-email</a></p>
    """

if __name__ == "__main__":
    print("\n" + "="*70)
    print("FLASK APPLICATION STARTING")
    print("="*70)
    print("\nInstructions:")
    print("  1. Make sure 'confirmation.png' exists (run fill_form.py first)")
    print("  2. Open browser and go to: http://127.0.0.1:5000/send-email")
    print("  3. Email will be sent automatically\n")
    print("="*70 + "\n")
    
    app.run(debug=True)