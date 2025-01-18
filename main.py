from selenium import webdriver
from selenium.webdriver.common.by import By
import time

# Initialize the WebDriver
driver = webdriver.Chrome()  # Ensure the correct WebDriver is installed
driver.get("https://academia.srmist.edu.in/#Course_FeedbackURL_OF_YOUR_FORM_PAGE")  # Replace with the actual URL of your form
driver.maximize_window()

# Wait for the page to load
time.sleep(2)

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

# Loop through each field
for field_id, value_to_select in fields.items():
    try:
        # Locate the field container
        field_container = driver.find_element(By.ID, field_id)
        
        # Click to trigger the dropdown
        field_container.click()
        time.sleep(1)  # Allow the dropdown to load
        
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

# Add comments or other fields if needed
try:
    comments_field = driver.find_element(By.ID, "zc-Enter_Your_Feedback_Here_Theory-Comments-arialabel")
    comments_field.send_keys("NA")  # Replace with your desired comment
except Exception as e:
    print(f"Error adding comments: {e}")

# Wait to review before manually submitting
time.sleep(10)  # Adjust as needed or remove for automated submission

# Quit the driver
driver.quit()
