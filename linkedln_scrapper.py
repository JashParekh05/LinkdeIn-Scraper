from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import csv

def validate_linkedin_url(url):
    return url.startswith("https://www.linkedin.com/in/")

def extract_profile(driver):
    profile = {}
    try:
        # Extract the name
        profile['Name'] = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1.text-heading-xlarge.inline.t-24.v-align-middle.break-words"))
        ).text

        # Extract the headline
        profile['Headline'] = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.text-body-medium.break-words"))
        ).text

    except Exception as e:
        print("Profile elements not found or different structure.")
        print(f"Error: {e}")
    
    return profile

def save_to_csv(data, filename):
    with open(filename, 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=data.keys())
        writer.writeheader()
        writer.writerow(data)

def main():
    linkedin_url = input("Enter the LinkedIn profile URL: ")
    
    if not validate_linkedin_url(linkedin_url):
        print("Invalid LinkedIn profile URL. Please enter a valid URL.")
        return
    
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")  # Ensure the window is maximized

    driver_path = "/Users/jashparekh/Desktop/LInkelin Scrapper/chromedriver-mac-arm64/chromedriver"  # Update this path if needed
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    try:
        # First, navigate to LinkedIn login page
        driver.get("https://www.linkedin.com/login")
        time.sleep(2)  # Let the login page load

        # Find the username and password fields and enter credentials
        # Enter Personal Username and Password to start Chromewebdriver login
        driver.find_element(By.ID, "username").send_keys("************")
        driver.find_element(By.ID, "password").send_keys("************")

        # Click the Sign In button
        driver.find_element(By.XPATH, "//button[@type='submit']").click()
        
        time.sleep(3)  # Wait for login to complete and profile to load

        # Now navigate to the LinkedIn profile
        driver.get(linkedin_url)
        time.sleep(3)  # Pause for 3 seconds to allow page to load
        
        profile_data = extract_profile(driver)
        
        print("Extracted Profile Data:")
        print(profile_data)
        
        save_to_csv(profile_data, "linkedin_profile.csv")
        print("Data saved to linkedin_profile.csv")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    main()
