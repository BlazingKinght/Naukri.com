import logging
from playwright.sync_api import Page, TimeoutError as PlaywrightTimeoutError

def apply_jobs(page: Page):
    """Applies to job listings on all pages."""
    logging.info("Starting job application process...")
    applied_count = 0
    current_page = 1
    max_retries = 3  # Maximum retries for job listings

    while True:
        logging.info(f"Processing page {current_page}...")

        # Increase timeout and handle exceptions better
        retries = 0
        while retries < max_retries:
            try:
                page.wait_for_selector("div.jobTuple", timeout=15000)  # Increased timeout
                break  # Exit loop if successful
            except PlaywrightTimeoutError:
                logging.error(f"Timeout while waiting for job listings to load. Retrying ({retries+1}/{max_retries})...")
                page.reload()
                retries += 1
        
        if retries == max_retries:
            logging.error("Max retries reached. Skipping page...")
            break  # Stop script if page doesn't load

        job_listings = page.query_selector_all("div.jobTuple")

        if not job_listings:
            logging.warning("No job listings found on this page. Ending process.")
            break  # Stop if no jobs are found

        for job in job_listings:
            try:
                job_link = job.locator("a.title")
                if job_link.count() == 0:
                    logging.warning("No job link found inside job listing. Skipping...")
                    continue

                # Open job in a new tab
                with page.expect_popup() as popup_info:
                    job_link.first.click()
                job_page = popup_info.value

                # Apply for the job in the new tab
                apply_for_job_in_tab(job_page)

                applied_count += 1
                logging.info(f"Applied for job {applied_count}")

                job_page.close()
            except PlaywrightTimeoutError:
                logging.error("Timeout while waiting for job details to load.")
            except Exception as e:
                logging.error(f"Could not apply for job: {e}")

        # Go to the next page
        try:
            next_page_button = page.locator("a.styles_btn-secondary__2AsIP:has-text('Next')")
            if next_page_button.is_visible():
                next_page_button.click()
                page.wait_for_selector("div.jobTuple", timeout=15000)  # Ensure next page loads before continuing
                current_page += 1
            else:
                logging.info("No more pages to process. Ending job application.")
                break
        except Exception as e:
            logging.error(f"Could not navigate to next page: {e}")
            break

    logging.info(f"Job applications completed. Total applied: {applied_count}")
