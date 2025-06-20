import os
from dotenv import load_dotenv
from linkedin_scraper import Person, actions
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

# Load environment variables from .env file
load_dotenv()

# Setup Chrome options
chrome_options = Options()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--disable-blink-features=AutomationControlled")
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_experimental_option('useAutomationExtension', False)

# Setup Chrome driver with automatic driver management
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

email = os.getenv("LINKEDIN_USER")
password = os.getenv("LINKEDIN_PASSWORD")

try:
    actions.login(driver, email, password) # if email and password isnt given, it'll prompt in terminal
    person = Person("https://www.linkedin.com/in/andre-iguodala-65b48ab5", driver=driver)
    
    print("Successfully scraped person data:")
    print(f"Name: {person.name}")
    print(f"Job Title: {person.job_title}")
    print(f"Company: {person.company}")
    print(f"Location: {getattr(person, 'location', 'N/A')}")
    print(f"About: {person.about}")
    
    # Optional: Export to CSV
    export_csv = input("\nWould you like to export this data to CSV? (y/n): ").lower().strip()
    if export_csv in ['y', 'yes']:
        try:
            csv_filename = person.to_csv()
            print(f"Data exported to: {csv_filename}")
        except Exception as csv_error:
            print(f"Error exporting to CSV: {csv_error}")
    
except Exception as e:
    print(f"Error occurred: {e}")
    print("You may need to manually verify your LinkedIn login or handle CAPTCHAs")
finally:
    driver.quit()
