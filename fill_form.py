import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# configuration for the data
YOUR_DATA = {
    "Full Name": "Lavya Jain",
    "Contact Number": "8218476656",
    "Email Id": "lavyajain.dev@gmail.com",
    "Full Address": "Nehru Nagar, Pimpri-Chinchwad, Maharashtra",
    "Pincode": "411018",
    "Date of Birth": "05/30/2004",
    "Gender": "Male"
}

FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLSdqYgND0WW6z1c0yeTRy-8SAKtgsI8ra3STzIqrTfQk5LmaeQ/viewform"
SCREENSHOT_FOLDER = "debug_screenshots"
CONFIRMATION_SCREENSHOT = "confirmation.png"

def take_screenshot(driver, step_name):
    """Take a screenshot for debugging purposes"""
    import os
    if not os.path.exists(SCREENSHOT_FOLDER):
        os.makedirs(SCREENSHOT_FOLDER)
    filename = f"{SCREENSHOT_FOLDER}/{step_name}_{int(time.time())}.png"
    driver.save_screenshot(filename)
    print(f"[INFO] Screenshot saved: {filename}")

def find_input_by_label(driver, label_text):
    """Find input field using multiple XPath strategies"""
    print(f"[DEBUG] Searching for input field: '{label_text}'")
    
    strategies = [
        f"//*[contains(text(), '{label_text}')]/ancestor::div[contains(@class, 'Qr7Oae')]//input",
        f"//*[contains(text(), '{label_text}')]/parent::*/parent::*/parent::*//input",
        f"//div[contains(@class, 'freebirdFormviewerComponentsQuestionTextRoot') and contains(., '{label_text}')]/ancestor::div[contains(@class, 'freebirdFormviewerComponentsQuestionBaseRoot')]//input",
        f"//div[contains(., '{label_text}') and not(contains(., 'Other'))]/following::input[1]",
    ]
    
    for i, xpath in enumerate(strategies, 1):
        try:
            element = driver.find_element(By.XPATH, xpath)
            print(f"[SUCCESS] Found input using strategy {i}")
            return element
        except Exception as e:
            print(f"[DEBUG] Strategy {i} failed: {str(e)[:80]}")
            continue
    
    raise Exception(f"Could not locate input field for label: {label_text}")

def find_textarea_by_label(driver, label_text):
    """Find textarea field using multiple XPath strategies"""
    print(f"[DEBUG] Searching for textarea field: '{label_text}'")
    
    strategies = [
        f"//*[contains(text(), '{label_text}')]/ancestor::div[contains(@class, 'Qr7Oae')]//textarea",
        f"//*[contains(text(), '{label_text}')]/parent::*/parent::*/parent::*//textarea",
        f"//div[contains(., '{label_text}')]/following::textarea[1]",
    ]
    
    for i, xpath in enumerate(strategies, 1):
        try:
            element = driver.find_element(By.XPATH, xpath)
            print(f"[SUCCESS] Found textarea using strategy {i}")
            return element
        except:
            continue
    
    raise Exception(f"Could not locate textarea field for label: {label_text}")

def find_date_input(driver, label_text):
    """Find date input field using multiple XPath strategies"""
    print(f"[DEBUG] Searching for date input field: '{label_text}'")
    
    strategies = [
        f"//*[contains(text(), '{label_text}')]/ancestor::div[contains(@class, 'Qr7Oae')]//input[@type='date']",
        f"//*[contains(text(), '{label_text}')]/parent::*/parent::*/parent::*//input[@type='date']",
        f"//div[contains(., '{label_text}')]/following::input[@type='date'][1]",
    ]
    
    for i, xpath in enumerate(strategies, 1):
        try:
            element = driver.find_element(By.XPATH, xpath)
            print(f"[SUCCESS] Found date input using strategy {i}")
            return element
        except:
            continue
    
    raise Exception(f"Could not locate date input field for label: {label_text}")

def find_radio_button(driver, label_text):
    """Find radio button by its aria-label attribute"""
    print(f"[DEBUG] Searching for radio button: '{label_text}'")
    try:
        xpath = f"//div[@role='radio' and @aria-label='{label_text}']"
        element = driver.find_element(By.XPATH, xpath)
        print(f"[SUCCESS] Found radio button")
        return element
    except Exception as e:
        print(f"[DEBUG] Radio button not found: {str(e)[:80]}")
        raise

def find_any_field_by_label(driver, label_text):
    """
    Find any type of field (input, textarea, select, radio) by label
    Returns tuple: (element, field_type)
    """
    print(f"[DEBUG] Searching for any field type with label: '{label_text}'")
    
    # Strategy 1: Trying to find input field
    input_strategies = [
        f"//*[contains(text(), '{label_text}')]/ancestor::div[contains(@class, 'Qr7Oae')]//input",
        f"//*[contains(text(), '{label_text}')]/parent::*/parent::*/parent::*//input",
        f"//div[contains(., '{label_text}')]/following::input[1]",
    ]
    
    for xpath in input_strategies:
        try:
            element = driver.find_element(By.XPATH, xpath)
            return (element, 'input')
        except:
            continue
    
    # Strategy 2: Trying to find textarea
    textarea_strategies = [
        f"//*[contains(text(), '{label_text}')]/ancestor::div[contains(@class, 'Qr7Oae')]//textarea",
        f"//div[contains(., '{label_text}')]/following::textarea[1]",
    ]
    
    for xpath in textarea_strategies:
        try:
            element = driver.find_element(By.XPATH, xpath)
            return (element, 'textarea')
        except:
            continue
    
    # Strategy 3: Trying to find select/dropdown
    select_strategies = [
        f"//*[contains(text(), '{label_text}')]/ancestor::div[contains(@class, 'Qr7Oae')]//select",
        f"//div[contains(., '{label_text}')]/following::select[1]",
    ]
    
    for xpath in select_strategies:
        try:
            element = driver.find_element(By.XPATH, xpath)
            return (element, 'select')
        except:
            continue
    
    raise Exception(f"Could not locate any field for label: {label_text}")

def fill_google_form():
    print("="*70)
    print("GOOGLE FORM AUTOMATION SCRIPT")
    print("="*70)
    
    print("\n[CONFIG] Form data loaded:")
    for key, value in YOUR_DATA.items():
        print(f"  {key}: {value}")
    
    print("\n[INIT] Setting up Chrome WebDriver...")
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    
    try:
        print(f"\n[LOADING] Opening form URL: {FORM_URL}")
        driver.get(FORM_URL)
        take_screenshot(driver, "01_form_opened")

        print("[WAITING] Waiting for form to load...")
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.TAG_NAME, "input"))
        )
        time.sleep(2)
        print("[SUCCESS] Form loaded successfully")
        take_screenshot(driver, "02_form_loaded")

        print("\n[PROCESS] Starting form field population...")
        print("-" * 70)
        
        # Full Name
        try:
            field = find_input_by_label(driver, "Full Name")
            field.clear()
            field.send_keys(YOUR_DATA["Full Name"])
            print(f"[FILLED] Full Name: {YOUR_DATA['Full Name']}")
            time.sleep(0.5)
        except Exception as e:
            print(f"[ERROR] Failed to fill Full Name: {e}")
            take_screenshot(driver, "error_fullname")
        
        # Contact Number
        try:
            contact_filled = False
            for label_variant in ["Contact Number", "Contact", "Phone Number", "Mobile Number"]:
                try:
                    print(f"[ATTEMPT] Trying label variant: '{label_variant}'")
                    field = find_input_by_label(driver, label_variant)
                    field.clear()
                    field.send_keys(YOUR_DATA["Contact Number"])
                    print(f"[FILLED] Contact Number: {YOUR_DATA['Contact Number']}")
                    contact_filled = True
                    break
                except:
                    continue
            
            if not contact_filled:
                raise Exception("Could not locate Contact Number field with any label variant")
            time.sleep(0.5)
        except Exception as e:
            print(f"[ERROR] Failed to fill Contact Number: {e}")
            take_screenshot(driver, "error_contact")
        
        # Email ID
        try:
            field = find_input_by_label(driver, "Email ID")
            field.clear()
            field.send_keys(YOUR_DATA["Email Id"])
            print(f"[FILLED] Email ID: {YOUR_DATA['Email Id']}")
            time.sleep(0.5)
        except Exception as e:
            print(f"[ERROR] Failed to fill Email ID: {e}")
            take_screenshot(driver, "error_email")
        
        # Full Address
        try:
            try:
                field = find_textarea_by_label(driver, "Full Address")
            except:
                field = find_input_by_label(driver, "Full Address")
            field.clear()
            field.send_keys(YOUR_DATA["Full Address"])
            print(f"[FILLED] Full Address: {YOUR_DATA['Full Address']}")
            time.sleep(0.5)
        except Exception as e:
            print(f"[ERROR] Failed to fill Full Address: {e}")
            take_screenshot(driver, "error_address")
        
        # Pin Code
        try:
            field = find_input_by_label(driver, "Pin Code")
            field.clear()
            field.send_keys(YOUR_DATA["Pincode"])
            print(f"[FILLED] Pin Code: {YOUR_DATA['Pincode']}")
            time.sleep(0.5)
        except Exception as e:
            print(f"[ERROR] Failed to fill Pin Code: {e}")
            take_screenshot(driver, "error_pincode")
        
        # Date of Birth
        try:
            field = find_date_input(driver, "Date of Birth")
            field.clear()
            field.send_keys(YOUR_DATA["Date of Birth"])
            print(f"[FILLED] Date of Birth: {YOUR_DATA['Date of Birth']}")
            time.sleep(0.5)
        except Exception as e:
            print(f"[ERROR] Failed to fill Date of Birth: {e}")
            take_screenshot(driver, "error_dob")
        
        # Gender (handles Radio Buttons, Input, or Dropdown automatically)
        try:
            gender_filled = False
            
            # Method 1: Trying for radio buttons 
            try:
                print(f"[DEBUG] Attempting Gender as radio button")
                radio = find_radio_button(driver, YOUR_DATA["Gender"])
                radio.click()
                print(f"[FILLED] Gender (radio button): {YOUR_DATA['Gender']}")
                gender_filled = True
            except:
                pass
            
            # Method 2: Trying for input/textarea/select
            if not gender_filled:
                print(f"[DEBUG] Trying Gender as input/textarea/dropdown")
                try:
                    element, field_type = find_any_field_by_label(driver, "Gender")
                    
                    if field_type == 'select':
                        from selenium.webdriver.support.ui import Select
                        Select(element).select_by_visible_text(YOUR_DATA["Gender"])
                        print(f"[FILLED] Gender (dropdown): {YOUR_DATA['Gender']}")
                    else:
                        element.clear()
                        element.send_keys(YOUR_DATA["Gender"])
                        print(f"[FILLED] Gender ({field_type}): {YOUR_DATA['Gender']}")
                    
                    gender_filled = True
                except Exception as inner_e:
                    print(f"[DEBUG] Failed to find Gender field: {str(inner_e)[:80]}")
            
            if not gender_filled:
                print(f"[WARNING] Could not automatically fill Gender field")
                print(f"[INFO] Please select/enter Gender manually: {YOUR_DATA['Gender']}")
                take_screenshot(driver, "warning_gender")
            
            time.sleep(0.5)
        except Exception as e:
            print(f"[ERROR] Gender field handling error: {str(e)[:80]}")
            take_screenshot(driver, "error_gender")
        
        print("-" * 70)
        print("[SUCCESS] All form fields filled successfully")
        take_screenshot(driver, "03_all_fields_filled")
        
        # Stop for CAPTCHA and Manual Fields
        print("\n" + "="*70)
        print("MANUAL VERIFICATION REQUIRED")
        print("="*70)
        print("Action required:")
        print("  1. Switch to the Chrome browser window")
        print("  2. Verify all fields are filled correctly")
        print("  3. Fill any remaining fields if needed (e.g., Gender if not auto-filled)")
        print("  4. Complete the CAPTCHA verification")
        print("  5. Click the SUBMIT button")
        print("\nWaiting for submission (timeout: 5 minutes)...")
        print("="*70 + "\n")

        # waiting  for submission
        try:
            WebDriverWait(driver, 300).until(
                EC.url_contains("formResponse")
            )
            
            print("[SUCCESS] Form submission detected")
            time.sleep(2)
            
            # Save confirmation screenshot to be sent with email
            driver.save_screenshot(CONFIRMATION_SCREENSHOT)
            print(f"[SUCCESS] Confirmation screenshot saved: {CONFIRMATION_SCREENSHOT}")
            
            # saving to debug folde aswell
            take_screenshot(driver, "04_confirmation_page")
            
        except Exception as e:
            print(f"[WARNING] Timeout waiting for submission")
            print("Please verify that the form was submitted manually")
            take_screenshot(driver, "error_timeout")
        
        print("\n[CLEANUP] Keeping browser open for 5 seconds...")
        time.sleep(5)

    except Exception as e:
        print(f"\n[CRITICAL ERROR] {e}")
        take_screenshot(driver, "critical_error")
        import traceback
        traceback.print_exc()
    
    finally:
        print("\n[CLEANUP] Closing browser...")
        driver.quit()
        print("[COMPLETE] Script execution finished")
        print(f"[INFO] Debug screenshots saved in: {SCREENSHOT_FOLDER}")
        print(f"[INFO] Confirmation screenshot: {CONFIRMATION_SCREENSHOT}")
        print("="*70)

if __name__ == "__main__":
    fill_google_form()