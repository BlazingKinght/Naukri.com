# login.py
from playwright.sync_api import Page
import config

def login(page: Page, email: str, password: str):
    """Logs into Naukri.com using given credentials."""
    
    print("[INFO] Logging in...")
    page.goto("https://www.naukri.com/")
    
    # Click on login button
    page.click("text=Login")
    page.wait_for_selector("input[type='text']", timeout=10000)  # Wait for login form
    
    # Enter email and password
    page.fill("input[placeholder='Enter your active Email ID / Username']", config.NAUKRI_EMAIL)
    page.fill("input[placeholder='Enter your password']", config.NAUKRI_PASSWORD)
    
    # Click submit
    page.click("button[type='submit']")
    

      # Wait for successful login (Profile icon or dashboard element)
    try:
        page.wait_for_selector("div[class*='user-name']", timeout=5000)  # Adjust timeout if needed
        print("[SUCCESS] Logged in successfully!")
    except:
        print("[ERROR] Login failed. Please check credentials.")

    