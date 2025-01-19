from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
import time

# Initialize WebDriver
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.add_argument('--log-level=3')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(service=service, options=options)
driver.maximize_window()

try:
    print("Opening website...")
    driver.get("https://academia.srmist.edu.in/#Course_Feedback")
    
    print("Please log in manually when the page loads.")
    input("After logging in, press Enter to continue...")
    
    # Wait for page load
    print("Waiting for page to load completely...")
    time.sleep(5)
    
    # Feedback mapping
    feedback_fields = {
        "Punctuality": "Excellent",
        "Sincerity": "Very Good",
        "Subject_Knowledge": "Excellent",
        "Lecture_Preparation": "Very Good",
        "Communication_Presentation_Skills": "Excellent",
        "Coverage_of_Syllabus_as_per_Schedule": "Very Good",
        "Controlling_of_the_Classes": "Excellent",
        "Standard_of_Test_Questions": "Very Good",
        "Discussion_of_Test_Questions": "Excellent",
        "Fairness_in_valuation": "Very Good",
        "Interaction_Approachability": "Excellent",
        "Helping_for_Clarification_of_Doubts": "Very Good",
        "Knowledge_Gained_at_Present_on_the_Subject": "Excellent",
        "Overall_Rating_of_the_Teacher": "Very Good"
    }
    
    def select_dropdown_value(field_name, value):
        try:
            # First try to find the select container
            select_container = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, f'div[id*="{field_name}"][class*="select2-container"]'))
            )
            
            # Scroll into view
            driver.execute_script("arguments[0].scrollIntoView({behavior: 'auto', block: 'center'});", select_container)
            time.sleep(1)
            
            # Click the container to open dropdown
            actions = ActionChains(driver)
            actions.move_to_element(select_container).click().perform()
            time.sleep(1)
            
            # Wait for dropdown to appear and select option
            dropdown = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#select2-drop'))
            )
            
            # Find and click the desired option
            option = WebDriverWait(dropdown, 10).until(
                EC.presence_of_element_located((By.XPATH, f"//div[@id='select2-drop']//li[contains(text(), '{value}')]"))
            )
            option.click()
            print(f"Successfully selected {value} for {field_name}")
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Error selecting {value} for {field_name}: {str(e)}")
    
    # Process each field
    for field_name, value in feedback_fields.items():
        print(f"\nProcessing: {field_name}")
        select_dropdown_value(field_name, value)
    
    # Add comments if needed
    try:
        comments_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'textarea[id*="Comments"]'))
        )
        comments_field.send_keys("NA")
        print("\nAdded comments successfully")
    except Exception as e:
        print(f"Error adding comments: {str(e)}")
    
    print("\nForm filling completed. Please review and submit manually.")
    input("Press Enter to close the browser...")

except Exception as e:
    print(f"An error occurred: {str(e)}")

finally:
    driver.quit()