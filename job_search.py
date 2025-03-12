# job_search.py
from playwright.sync_api import Page
import config

def search_jobs(page: Page, query: str, location: str, experience: str):
    """Searches for jobs based on given parameters."""

    print(f"[INFO] Searching for jobs: {query}, Location: {location}, Experience: {experience} years")
    
    page.goto("https://www.naukri.com/")

    # Click the button using exact text
    page.click("text=Search jobs here")
    
    # Enter job title
    page.fill("input[placeholder='Enter keyword / designation / companies']", config.SEARCH_QUERY)

    # Enter location
    page.fill("input[placeholder='Enter location']", config.LOCATION)

    # Determine the correct experience value based on config.EXPERIENCE
    if config.EXPERIENCE == "1":
        experience_value = f"{config.EXPERIENCE} year"
    elif config.EXPERIENCE == "Fresher (less than 1 year)":
        experience_value = "Fresher (less than 1 year)"
    else:
        experience_value = f"{config.EXPERIENCE} years"

    # Click dropdown to open
    page.locator("#experienceDD").click()

    # Ensure dropdown is fully loaded
    page.wait_for_selector(".dropdownContainer.dropdownShow", state="visible")

    # Select the correct experience option using the formatted experience_value
    option = page.locator(f"ul.dropdown li").get_by_text(experience_value, exact=True)

    # Scroll into view and wait for visibility
    option.scroll_into_view_if_needed()
    option.wait_for(state="visible")

    # Click to select experience
    option.click()


    # Print selected value for verification
    selected_value = page.input_value("#experienceDD")
    print(f"Selected Experience: {selected_value}")


    # Find the search button by its class
    search_button = page.locator("button.nI-gNb-sb__icon-wrapper")

    # Wait for the button to be visible and enabled
    search_button.wait_for(state="visible")

    # Click the search button
    search_button.click()

        
    print("[SUCCESS] Job search completed!")
