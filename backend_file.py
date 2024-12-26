import time
import csv
import sys
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options

# Command-line arguments for scrolls and job title
scrolls = int(sys.argv[1])  # First argument: number of scrolls
job_ts = sys.argv[2]        # Second argument: job title to search for

# Setup WebDriver
driver_path = r"C:\Users\s\Downloads\edgedriver_win64\msedgedriver.exe"
service = Service(driver_path)
options = Options()
# options.add_argument('--headless')  # Uncomment if you don't want the browser UI
driver = webdriver.Edge(service=service, options=options)

# URL to scrape
url = "https://www.behance.net/joblist?tracking_source=nav20"
driver.get(url)

# Set up CSV file for storing data
with open('job_cards.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Job Title', 'Company', 'Location', 'Job URL', 'Image URL'])

    # Scroll and scrape job cards
    for _ in range(scrolls):
        time.sleep(3)  # Wait a bit for the page to load
        # Scroll down
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # Wait for new job cards to load
        time.sleep(2)

        # Find all job cards
        job_cards = driver.find_elements(By.CLASS_NAME, "JobCard-jobCard-mzZ")
        
        for job_card in job_cards:
            try:
                # Extract the job card details
                job_link = job_card.find_element(By.CLASS_NAME, "JobCard-jobCardLink-Ywm")
                job_title_text = job_link.get_attribute("aria-label").split(",")[0].split(":")[1].strip()
                company = job_card.find_element(By.CLASS_NAME, "JobCard-company-GQS").text
                location = job_card.find_element(By.CLASS_NAME, "JobCard-jobLocation-sjd").text
                
                # Extract the image URL (company logo)
                image_url = job_card.find_element(By.CLASS_NAME, "AvatarImage-avatarImage-PUL").get_attribute("src")
                
                # Write data to CSV
                writer.writerow([job_title_text, company, location, job_link.get_attribute("href"), image_url])

                if job_ts.lower() in company.lower():
                    print(f"Found matching job: {job_title_text} at {company}")
                    job_link.click()
                    time.sleep(5)
                    break
            except Exception as e:
                print(f"Error extracting job card info: {e}")

        if job_ts.lower() in company.lower():
            print(f"Found matching job: {job_title_text} at {company}")
            job_link.click()
            time.sleep(5)
            break  # Break out of the loop when the job is found

# Close the browser
driver.quit()

print("Job scraping complete, data saved to job_cards.csv")
