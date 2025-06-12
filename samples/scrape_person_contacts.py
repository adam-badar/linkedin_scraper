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
chrome_options.add_argument("--disable-web-security")
chrome_options.add_argument("--allow-running-insecure-content")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-plugins")
chrome_options.add_argument("--disable-images")
chrome_options.add_argument("--disable-javascript")
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
    person = Person("https://www.linkedin.com/in/adrian0350", contacts=[], driver=driver)
    
    print("Successfully scraped person contacts:")
    print("Person: " + person.name)
    print("Person contacts: ")
    
    for contact in person.contacts:
        print("Contact: " + contact.name + " - " + contact.occupation + " -> " + contact.url)
        
except Exception as e:
    print(f"Error occurred: {e}")
    print("You may need to manually verify your LinkedIn login or handle CAPTCHAs")
finally:
    driver.quit()
