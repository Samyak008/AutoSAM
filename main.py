from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import os
import time

def setup_driver():
    """Setup Chrome driver with user profile to maintain login session"""
    options = Options()
    
    # Use existing Chrome profile - MODIFY THIS PATH TO YOUR CHROME PROFILE
    # Common profile paths:
    # Windows: C:\\Users\\YourUsername\\AppData\\Local\\Google\\Chrome\\User Data\\Default
    # Mac: ~/Library/Application Support/Google/Chrome/Default
    # Linux: ~/.config/google-chrome/Default
    options.add_argument("user-data-dir=C:\\Users\\YourUsername\\AppData\\Local\\Google\\Chrome\\User Data")
    options.add_argument("profile-directory=Default")
    
    # Additional options for stability
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    
    service = Service()
    driver = webdriver.Chrome(service=service, options=options)
    driver.maximize_window()
    return driver

def fill_feedback(driver, course_index, is_theory=True):
    """Fill feedback for a specific course"""
    section_type = "Theory" if is_theory else "Practical"
    
    # Ratings to alternate between
    ratings = ["Excellent", "Very Good"]
    
    try:
        # Wait for the form to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "form-field-grid"))
        )
        
        # For each rating field (1-7 for your form)
        for field_num in range(1, 8):
            try:
                # Find all select2 containers in the current row
                select_containers = driver.find_elements(
                    By.CSS_SELECTOR,
                    f"tr:nth-child({course_index + 1}) .select2-container"
                )
                
                if field_num <= len(select_containers):
                    container = select_containers[field_num - 1]
                    
                    # Scroll to element
                    driver.execute_script(
                        "arguments[0].scrollIntoView({block: 'center'});", 
                        container
                    )
                    time.sleep(0.5)
                    
                    # Click to open dropdown
                    container.click()
                    time.sleep(0.5)
                    
                    # Select rating (alternating between Excellent and Very Good)
                    rating = ratings[field_num % 2]
                    
                    # Wait for dropdown and select option
                    dropdown_option = WebDriverWait(driver, 10).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, f"//div[@id='select2-drop']//li[contains(text(), '{rating}')]")
                        )
                    )
                    dropdown_option.click()
                    time.sleep(0.5)
                    
                    print(f"Set rating {rating} for field {field_num} in {section_type} course {course_index + 1}")
                    
            except Exception as e:
                print(f"Error setting rating for field {field_num}: {str(e)}")
        
        # Add comment
        try:
            comment = "Good teaching" if is_theory else "Good lab sessions"
            comment_field = driver.find_element(
                By.CSS_SELECTOR,
                f"tr:nth-child({course_index + 1}) textarea"
            )
            comment_field.send_keys(comment)
            print(f"Added comment for {section_type} course {course_index + 1}")
        except Exception as e:
            print(f"Error adding comment: {str(e)}")
            
    except Exception as e:
        print(f"Error processing {section_type} course {course_index + 1}: {str(e)}")

def main():
    driver = None
    try:
        driver = setup_driver()
        
        # Navigate directly to feedback page (use the already logged in session)
        driver.get("https://academia.srmist.edu.in/#Course_Feedback")
        print("Navigating to feedback page...")
        time.sleep(5)  # Wait for page load
        
        # Process theory courses
        print("\nProcessing Theory courses...")
        theory_rows = len(driver.find_elements(By.CSS_SELECTOR, "div:nth-child(1) > div.form-field-grid > table > tbody > tr"))
        for i in range(theory_rows):
            fill_feedback(driver, i, is_theory=True)
            
        # Process practical courses
        print("\nProcessing Practical courses...")
        practical_rows = len(driver.find_elements(By.CSS_SELECTOR, "div:nth-child(2) > div.form-field-grid > table > tbody > tr"))
        for i in range(practical_rows):
            fill_feedback(driver, i, is_theory=False)
            
        print("\nForm filling completed. Please review and submit manually.")
        input("Press Enter to close browser...")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
    finally:
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()