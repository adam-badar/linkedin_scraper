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
    
    # Scrape a person's data
    person = Person("https://www.linkedin.com/in/andre-iguodala-65b48ab5", driver=driver)
    
    print("Successfully scraped person data:")
    print(f"Name: {person.name}")
    print(f"Job Title: {person.job_title}")
    print(f"Company: {person.company}")
    print(f"Location: {getattr(person, 'location', 'N/A')}")
    print(f"About: {person.about}")
    
    # Export to CSV
    print("\nExporting to CSV...")
    csv_filename = person.to_csv()
    print(f"Data exported to: {csv_filename}")
    
    # Also demonstrate dictionary export
    person_dict = person.to_dict()
    print(f"\nSample data structure:")
    for key, value in list(person_dict.items())[:10]:  # Show first 10 fields
        print(f"  {key}: {value}")
    print("  ...")
    
    # Example of exporting multiple people (if you want to scrape multiple profiles)
    # persons = [person]  # Add more Person objects here
    # Person.export_multiple_to_csv(persons, "multiple_persons.csv")
    
except Exception as e:
    print(f"Error occurred: {e}")
    print("You may need to manually verify your LinkedIn login or handle CAPTCHAs")
finally:
    driver.quit()
