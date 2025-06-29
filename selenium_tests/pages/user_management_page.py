from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from .base_page import BasePage
import time

class UserManagementPage(BasePage):
    """Page Object Model for User Management page"""
    
    # Page URL
    URL = "http://localhost:5173"  # Frontend Vite development server URL
    
    # Locators
    NAME_INPUT = (By.NAME, "name")
    EMAIL_INPUT = (By.NAME, "email")
    AGE_INPUT = (By.NAME, "age")
    SUBMIT_BUTTON = (By.CSS_SELECTOR, "button[type='submit']")
    USER_TABLE = (By.CLASS_NAME, "table")
    USER_ROWS = (By.CSS_SELECTOR, "tbody tr")
    EDIT_BUTTON = (By.CLASS_NAME, "edit_btn")
    DELETE_BUTTON = (By.CLASS_NAME, "delete_btn")
    SUCCESS_MESSAGE = (By.CLASS_NAME, "success-message")
    ERROR_MESSAGE = (By.CLASS_NAME, "error-message")
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def add_user(self, name, email, age):
        """Add a new user with the given details."""
        self.fill_user_form(name, email, age)
        self.submit_form()
    
    def fill_user_form(self, name, email, age):
        """Fill the user form with the given details."""
        self.find_element(*self.NAME_INPUT).clear()
        self.find_element(*self.NAME_INPUT).send_keys(name)
        
        self.find_element(*self.EMAIL_INPUT).clear()
        self.find_element(*self.EMAIL_INPUT).send_keys(email)
        
        self.find_element(*self.AGE_INPUT).clear()
        self.find_element(*self.AGE_INPUT).send_keys(age)
    
    def submit_form(self):
        """Submit the user form."""
        submit_button = self.find_element(*self.SUBMIT_BUTTON)
        if submit_button:
            submit_button.click()
            time.sleep(1)  # Wait for form submission
    
    def get_success_message(self):
        """Get the success message text."""
        try:
            return self.find_element(*self.SUCCESS_MESSAGE).text
        except NoSuchElementException:
            return None
    
    def get_error_message(self):
        """Get the error message text."""
        try:
            return self.find_element(*self.ERROR_MESSAGE).text
        except NoSuchElementException:
            return None
    
    def is_user_in_table(self, name, email):
        """Check if a user with the given email exists in the table."""
        try:
            rows = self.find_elements(*self.USER_ROWS)
            for row in rows:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) >= 3 and cells[1].text == name and cells[2].text == email:
                    return True
            return False
        except NoSuchElementException:
            return False
    
    def get_users_count(self):
        """Get the number of users in the table."""
        try:
            rows = self.find_elements(*self.USER_ROWS)
            return len(rows)
        except NoSuchElementException:
            return 0
    
    def find_user_by_email(self, email):
        """Find a user's row index by email."""
        try:
            rows = self.find_elements(*self.USER_ROWS)
            for i, row in enumerate(rows):
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) >= 3 and cells[2].text == email:
                    return i
            return -1
        except NoSuchElementException:
            return -1
    
    def get_user_data_from_table(self, row_index):
        """Get user data from the specified row."""
        try:
            rows = self.find_elements(*self.USER_ROWS)
            if 0 <= row_index < len(rows):
                cells = rows[row_index].find_elements(By.TAG_NAME, "td")
                return {
                    "name": cells[1].text,
                    "email": cells[2].text,
                    "age": cells[3].text
                }
            return None
        except NoSuchElementException:
            return None
    
    def edit_user(self, row_index):
        """Click the edit button for the user at the specified row."""
        try:
            rows = self.find_elements(*self.USER_ROWS)
            if 0 <= row_index < len(rows):
                edit_button = rows[row_index].find_element(By.CLASS_NAME, "edit_btn")
                edit_button.click()
                time.sleep(1)  # Wait for form to be populated
        except NoSuchElementException:
            pass
    
    def delete_user(self, row_index):
        """Click the delete button for the user at the specified row."""
        try:
            rows = self.find_elements(*self.USER_ROWS)
            if 0 <= row_index < len(rows):
                delete_button = rows[row_index].find_element(By.CLASS_NAME, "delete_btn")
                delete_button.click()
                time.sleep(1)  # Wait for deletion
        except NoSuchElementException:
            pass
    
    def clear_user_form(self):
        """Clear all form fields."""
        self.find_element(*self.NAME_INPUT).clear()
        self.find_element(*self.EMAIL_INPUT).clear()
        self.find_element(*self.AGE_INPUT).clear()
    
    def get_form_field_values(self):
        """Get the current values of all form fields."""
        return {
            "name": self.find_element(*self.NAME_INPUT).get_attribute("value"),
            "email": self.find_element(*self.EMAIL_INPUT).get_attribute("value"),
            "age": self.find_element(*self.AGE_INPUT).get_attribute("value")
        }
    
    def refresh_page(self):
        """Refresh the current page."""
        self.driver.refresh()
        time.sleep(2)  # Wait for page to reload
    
    def wait_for_user_to_appear(self, email, timeout=10):
        """Wait for a user with the given email to appear in the table."""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: self.find_user_by_email(email) >= 0
            )
            return True
        except TimeoutException:
            return False
    
    def wait_for_user_to_disappear(self, email, timeout=10):
        """Wait for a user with the given email to disappear from the table."""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: self.find_user_by_email(email) == -1
            )
            return True
        except TimeoutException:
            return False
    
    def get_page_title(self):
        """Get the page title."""
        return self.get_element_text(*self.PAGE_TITLE)
    
    def is_form_present(self):
        """Check if the user form is present."""
        return self.is_element_present(*self.FORM)
    
    def is_users_table_present(self):
        """Check if the users table is present."""
        return self.is_element_present(*self.USER_TABLE)
    
    def get_submit_button_text(self):
        """Get the text of the submit button."""
        return self.get_element_text(*self.SUBMIT_BUTTON)
    
    def get_users_count(self):
        """Get the number of users in the table."""
        rows = self.find_elements(*self.USER_ROWS)
        return len(rows)
    
    def get_user_data_from_table(self, row_index=0):
        """Get user data from a specific row in the table."""
        rows = self.find_elements(*self.USER_ROWS)
        if row_index < len(rows):
            row = rows[row_index]
            cells = row.find_elements(By.TAG_NAME, "td")
            if len(cells) >= 4:
                return {
                    "id": cells[0].text,
                    "name": cells[1].text,
                    "email": cells[2].text,
                    "age": cells[3].text.replace(" Year's", "")
                }
        return None
    
    def get_validation_errors(self):
        """Get validation error messages"""
        try:
            errors = self.driver.find_elements(*self.VALIDATION_ERROR)
            return [error.text for error in errors]
        except NoSuchElementException:
            return []
    
    def is_form_cleared(self):
        """Check if the form is cleared"""
        name_value = self.driver.find_element(*self.NAME_INPUT).get_attribute("value")
        email_value = self.driver.find_element(*self.EMAIL_INPUT).get_attribute("value")
        age_value = self.driver.find_element(*self.AGE_INPUT).get_attribute("value")
        return not (name_value or email_value or age_value)
    
    def get_user_count(self):
        """Get the total number of users"""
        table = self.driver.find_element(*self.USER_TABLE)
        rows = table.find_elements(By.TAG_NAME, "tr")
        return len(rows) - 1  # Subtract header row
    
    def user_exists(self, email):
        """Check if a user exists"""
        return self.find_user_by_email(email) >= 0
    
    def get_page_load_time(self):
        """Measure page load time in milliseconds"""
        start_time = time.time()
        self.navigate()
        end_time = time.time()
        return (end_time - start_time) * 1000
    
    def get_current_time(self):
        """Get current time in milliseconds"""
        return int(time.time() * 1000)
    
    def get_operation_result(self):
        """Get the result of the last operation"""
        try:
            # Wait for success or error message
            message = self.wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "message"))
            ).text
            
            # Check if operation was successful based on message
            success = "success" in message.lower()
            status_code = 200 if success else 400
            
            return self.OperationResult(success, message, status_code)
        except TimeoutException:
            return self.OperationResult(False, "Operation timed out")
    
    class OperationResult:
        """Class to hold operation results"""
        def __init__(self, success, message, status_code=None):
            self.success = success
            self.message = message
            self.status_code = status_code 