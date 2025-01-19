from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

# Initialize the WebDriver with webdriver-manager
service = Service(ChromeDriverManager().install())
options = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://academia.srmist.edu.in/#Course_Feedback")  # Replace with the actual login URL
driver.maximize_window()

try:
    # Wait for the page to load (adjust as needed)
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.NAME, "username"))
    )
    print("Login page loaded successfully. Please enter your credentials manually.")

    # Wait for user to log in manually
    input("Press Enter after logging in manually...")

    # Navigate to the feedback page (adjust URL if necessary)
    WebDriverWait(driver, 20).until(
        EC.url_contains("Course_Feedback")  # Update with the actual URL substring for the feedback form
    )
    print("Feedback page loaded.")

    # Field identifiers and the corresponding values to select
    fields = {
        "zc-Enter_Your_Feedback_Here_Theory-Punctuality-arialabel": "Excellent",
        "zc-Enter_Your_Feedback_Here_Theory-Sincerity-arialabel": "Very Good",
        "zc-Enter_Your_Feedback_Here_Theory-Subject_Knowledge-arialabel": "Good",
        "zc-Enter_Your_Feedback_Here_Theory-Lecture_Preparation-arialabel": "Excellent",
        "zc-Enter_Your_Feedback_Here_Theory-Communication_Presentation_Skills-arialabel": "Very Good",
        "zc-Enter_Your_Feedback_Here_Theory-Coverage_of_Syllabus_as_per_Schedule-arialabel": "Good",
        "zc-Enter_Your_Feedback_Here_Theory-Controlling_of_the_Classes-arialabel": "Very Good",
        "zc-Enter_Your_Feedback_Here_Theory-Standard_of_Test_Questions-arialabel": "Good",
        "zc-Enter_Your_Feedback_Here_Theory-Discussion_of_Test_Questions-arialabel": "Excellent",
        "zc-Enter_Your_Feedback_Here_Theory-Fairness_in_valuation-arialabel": "Very Good",
        "zc-Enter_Your_Feedback_Here_Theory-Interaction_Approachability-arialabel": "Good",
        "zc-Enter_Your_Feedback_Here_Theory-Helping_for_Clarification_of_Doubts-arialabel": "Excellent",
        "zc-Enter_Your_Feedback_Here_Theory-Knowledge_Gained_at_Present_on_the_Subject-arialabel": "Very Good",
        "zc-Enter_Your_Feedback_Here_Theory-Overall_Rating_of_the_Teacher-arialabel": "Excellent",
    }

    # Interact with each dropdown
    for field_id, value_to_select in fields.items():
        try:
            # Locate the field container
            field_container = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, field_id))
            )
            # Click to trigger the dropdown
            field_container.click()
            time.sleep(10)  # Allow the dropdown to load
            
            # Locate the dropdown options
            dropdown_options = driver.find_elements(By.CSS_SELECTOR, "#select2-drop ul.select2-results li")
            
            # Iterate through the options and select the desired value
            for option in dropdown_options:
                if value_to_select in option.text:
                    option.click()
                    time.sleep(0.5)  # Wait to ensure selection is registered
                    break
        except Exception as e:
            print(f"Error processing field {field_id}: {e}")

    # Add comments (optional)
    try:
        comments_field = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "zc-Enter_Your_Feedback_Here_Theory-Comments-arialabel"))
        )
        comments_field.send_keys("NA")  # Replace with your desired comment
    except Exception as e:
        print(f"Error adding comments: {e}")

    # Wait to review before submitting
    time.sleep(10)  # Adjust as needed or remove for automated submission

except Exception as e:
    print(f"An error occurred: {e}")

finally:
    # Quit the driver
    driver.quit()
