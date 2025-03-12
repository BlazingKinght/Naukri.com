# main.py
from playwright.sync_api import sync_playwright
import config
from naukri_login import login
from job_search import search_jobs
from job_apply import apply_jobs
from utils import wait

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Run in headful mode
        page = browser.new_page()
        
        login(page, config.NAUKRI_EMAIL, config.NAUKRI_PASSWORD)
        wait(2)
        
        def close_popups(page):
            try:
                # Example selectors for popups (modify as needed)
                if page.locator("div.modal-content").is_visible():
                    page.click("button[aria-label='Close']")
                    print("[INFO] Closed popup.")
                
                if page.locator("div[role='dialog']").is_visible():
                    page.click("button[aria-label='Dismiss']")
                    print("[INFO] Closed modal dialog.")

            except:
                print("[INFO] No popups found.")

        # Call close_popups() after login but before search
        close_popups(page)
        search_jobs(page, config.SEARCH_QUERY, config.LOCATION, config.EXPERIENCE)

        
        apply_jobs(page)
        
        browser.close()
        print("[DONE] Job application process completed!")

if __name__ == "__main__":
    main()
