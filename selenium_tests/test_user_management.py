import os
import sys
import pytest
import time
import requests
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# Add the project root directory to the Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from selenium_tests.pages.user_management_page import UserManagementPage

@pytest.fixture(scope="session")
def test_data():
    """Test data for user management tests."""
    return {
        "valid_user": {
            "name": "John Doe",
            "email": "john.doe@gmail.com",
            "age": "25"
        },
        "duplicate_email": {
            "name": "Jane Doe",
            "email": "john.doe@test.com",
            "age": "30"
        },
        "invalid_user": {
            "name": "",  # Empty name
            "email": "invalid-email",  # Invalid email format
            "age": "-1"  # Invalid age
        },
        "updated_user": {
            "name": "John Updated",
            "email": "john.updated@test.com",
            "age": "26"
        }
    }

class TestUserManagement:
    """
    Test suite for User Management CRUD operations using Selenium.
    Contains 10+ comprehensive test cases covering all functionality.
    """
    
    def setup_method(self):
        """Setup method run before each test."""
        time.sleep(2)  # Wait between tests
    
    def test_01_page_load_and_elements_present(self, driver, base_url):
        """
        Test Case 1: Verify page loads correctly and all essential elements are present.
        """
        # Navigate to the application
        driver.get(base_url)
        
        # Create page object
        page = UserManagementPage(driver)
        
        # Verify page title
        assert "DevOps Assignment 2" in driver.title
        
        # Verify form is present
        assert page.is_element_present(*page.NAME_INPUT), "Name input should be present"
        assert page.is_element_present(*page.EMAIL_INPUT), "Email input should be present"
        assert page.is_element_present(*page.AGE_INPUT), "Age input should be present"
        assert page.is_element_present(*page.SUBMIT_BUTTON), "Submit button should be present"
        
        # Verify users table is present
        assert page.is_element_present(*page.USER_TABLE), "Users table should be present"
        
        # Verify submit button text
        submit_button = page.find_element(*page.SUBMIT_BUTTON)
        assert submit_button.text == "Add user", "Submit button should show 'Add user'"
    
    def test_02_add_new_user_successfully(self, driver, base_url, test_data):
        """
        Test Case 2: Add a new user with valid data successfully.
        """
        driver.get(base_url)
        page = UserManagementPage(driver)
        
        # Get initial user count
        initial_count = page.get_users_count()
        
        # Add new user
        user = test_data["valid_user"]
        page.add_user(user["name"], user["email"], user["age"])
        
        # Wait for user to appear in table
        assert page.wait_for_user_to_appear(user["email"]), "User should appear in table"
        
        # Verify user count increased
        final_count = page.get_users_count()
        assert final_count == initial_count + 1, f"User count should increase from {initial_count} to {initial_count + 1}"
        
        # Verify user data in table
        user_row_index = page.find_user_by_email(user["email"])
        assert user_row_index >= 0, "User should be found in table"
        
        user_data_from_table = page.get_user_data_from_table(user_row_index)
        assert user_data_from_table["name"] == user["name"]
        assert user_data_from_table["email"] == user["email"]
        assert user_data_from_table["age"] == user["age"] + " Year's"
        
        # Verify form is cleared after submission
        form_values = page.get_form_field_values()
        assert form_values["name"] == "", "Name field should be cleared"
        assert form_values["email"] == "", "Email field should be cleared"
        assert form_values["age"] == "", "Age field should be cleared"
    
    def test_03_add_user_with_duplicate_email(self, driver, base_url, test_data):
        """
        Test Case 3: Attempt to add user with duplicate email and verify error handling.
        """
        driver.get(base_url)
        page = UserManagementPage(driver)
        
        # Add first user
        user = test_data["valid_user"]
        page.add_user(user["name"], user["email"], user["age"])
        
        # Wait for first user to appear
        assert page.wait_for_user_to_appear(user["email"])
        
        # Try to add user with same email
        duplicate_user = test_data["duplicate_email"]
        page.add_user(duplicate_user["name"], duplicate_user["email"], duplicate_user["age"])
        
        # Check for alert message
        alert = driver.switch_to.alert
        assert alert is not None, "Alert should appear for duplicate email"
        assert "Email already exists" in alert.text, "Alert should mention duplicate email"
        alert.accept()
        
        # Verify only one user with that email exists
        user_count = page.get_users_count()
        email_count = 0
        for i in range(user_count):
            user_data_from_table = page.get_user_data_from_table(i)
            if user_data_from_table and user_data_from_table["email"] == user["email"]:
                email_count += 1
        
        assert email_count == 1, "Only one user with duplicate email should exist"
    
    def test_04_add_user_with_invalid_data(self, driver, base_url, test_data):
        """
        Test Case 4: Attempt to add user with invalid data and verify validation.
        """
        driver.get(base_url)
        page = UserManagementPage(driver)
        
        # Get initial user count
        initial_count = page.get_users_count()
        
        # Try to add user with empty name
        invalid_user = test_data["invalid_user"]
        page.add_user(invalid_user["name"], invalid_user["email"], invalid_user["age"])
        
        # Check for alert message
        alert = driver.switch_to.alert
        assert alert is not None, "Alert should appear for invalid data"
        assert "Please fill in all fields" in alert.text, "Alert should mention missing fields"
        alert.accept()
        
        # Verify user count didn't change
        final_count = page.get_users_count()
        assert final_count == initial_count, "User count should not change for invalid data"
    
    def test_05_edit_existing_user(self, driver, base_url, test_data):
        """
        Test Case 5: Edit an existing user and verify changes are saved.
        """
        driver.get(base_url)
        page = UserManagementPage(driver)
        
        # Add a user first
        user = test_data["valid_user"]
        page.add_user(user["name"], user["email"], user["age"])
        
        # Wait for user to appear
        assert page.wait_for_user_to_appear(user["email"])
        
        # Find user row and edit
        user_row_index = page.find_user_by_email(user["email"])
        assert user_row_index >= 0, "User should be found for editing"
        
        # Click edit button
        page.edit_user(user_row_index)
        
        # Verify form is populated with user data
        form_values = page.get_form_field_values()
        assert form_values["name"] == user["name"]
        assert form_values["email"] == user["email"]
        assert form_values["age"] == user["age"]
        
        # Update user data
        updated_user = test_data["updated_user"]
        page.fill_user_form(updated_user["name"], updated_user["email"], updated_user["age"])
        page.submit_form()
        
        # Wait for updated user to appear
        assert page.wait_for_user_to_appear(updated_user["email"])
        
        # Verify user data was updated
        updated_row_index = page.find_user_by_email(updated_user["email"])
        assert updated_row_index >= 0, "Updated user should be found in table"
        
        updated_data = page.get_user_data_from_table(updated_row_index)
        assert updated_data["name"] == updated_user["name"]
        assert updated_data["email"] == updated_user["email"]
        assert updated_data["age"] == updated_user["age"] + " Year's"
    
    def test_06_delete_existing_user(self, driver, base_url, test_data):
        """
        Test Case 6: Delete an existing user and verify removal.
        """
        driver.get(base_url)
        page = UserManagementPage(driver)
        
        # Add a user first
        user = test_data["valid_user"]
        page.add_user(user["name"], user["email"], user["age"])
        
        # Wait for user to appear
        assert page.wait_for_user_to_appear(user["email"])
        
        # Get user count before deletion
        initial_count = page.get_users_count()
        
        # Find user row and delete
        user_row_index = page.find_user_by_email(user["email"])
        assert user_row_index >= 0, "User should be found for deletion"
        
        # Click delete button
        page.delete_user(user_row_index)
        
        # Wait for user to disappear
        assert page.wait_for_user_to_disappear(user["email"]), "User should be removed from table"
        
        # Verify user count decreased
        final_count = page.get_users_count()
        assert final_count == initial_count - 1, f"User count should decrease from {initial_count} to {initial_count - 1}"
        
        # Verify user is not in table
        user_row_index_after = page.find_user_by_email(user["email"])
        assert user_row_index_after == -1, "User should not be found after deletion"
    
    def test_07_form_validation_and_clearing(self, driver, base_url):
        """
        Test Case 7: Test form validation and clearing functionality.
        """
        driver.get(base_url)
        page = UserManagementPage(driver)
        
        # Test form clearing
        page.fill_user_form("Test Name", "test@email.com", "25")
        page.clear_user_form()
        
        form_values = page.get_form_field_values()
        assert form_values["name"] == "", "Name field should be cleared"
        assert form_values["email"] == "", "Email field should be cleared"
        assert form_values["age"] == "", "Age field should be cleared"
        
        # Test partial form submission (should fail)
        page.fill_user_form("Test Name", "", "25")
        page.submit_form()
        
        alert_text = page.get_alert_text()
        assert alert_text is not None, "Alert should appear for incomplete form"
        assert "Please fill in all fields" in alert_text, "Alert should mention missing fields"
    
    def test_08_multiple_users_operations(self, driver, base_url):
        """
        Test Case 8: Test operations with multiple users.
        """
        driver.get(base_url)
        page = UserManagementPage(driver)
        
        # Add multiple users
        users = [
            {"name": "User 1", "email": "user1@test.com", "age": "25"},
            {"name": "User 2", "email": "user2@test.com", "age": "30"},
            {"name": "User 3", "email": "user3@test.com", "age": "35"}
        ]
        
        for user in users:
            page.add_user(user["name"], user["email"], user["age"])
            assert page.wait_for_user_to_appear(user["email"]), f"User {user['email']} should appear"
        
        # Verify all users are in table
        final_count = page.get_users_count()
        assert final_count == len(users), f"Should have {len(users)} users in table"
        
        # Get all users data
        all_users_data = page.get_all_users_data()
        assert len(all_users_data) == len(users), "All users should be retrieved"
        
        # Verify each user data
        for user in users:
            user_found = any(u["email"] == user["email"] for u in all_users_data)
            assert user_found, f"User {user['email']} should be in table data"
    
    def test_09_page_refresh_and_data_persistence(self, driver, base_url, test_data):
        """
        Test Case 9: Test data persistence after page refresh.
        """
        driver.get(base_url)
        page = UserManagementPage(driver)
        
        # Add a user
        user = test_data["valid_user"]
        page.add_user(user["name"], user["email"], user["age"])
        
        # Wait for user to appear
        assert page.wait_for_user_to_appear(user["email"])
        
        # Refresh page
        page.refresh_page()
        
        # Verify user still exists after refresh
        assert page.is_user_in_table(user["name"], user["email"]), "User should persist after page refresh"
        
        # Verify user data is correct
        user_row_index = page.find_user_by_email(user["email"])
        user_data_from_table = page.get_user_data_from_table(user_row_index)
        assert user_data_from_table["name"] == user["name"]
        assert user_data_from_table["email"] == user["email"]
        assert user_data_from_table["age"] == user["age"] + " Year's"
    
    def test_10_api_integration_verification(self, driver, base_url, api_url, test_data):
        """
        Test Case 10: Verify API integration by checking data consistency between UI and API.
        """
        driver.get(base_url)
        page = UserManagementPage(driver)
        
        # Add user through UI
        user = test_data["valid_user"]
        page.add_user(user["name"], user["email"], user["age"])
        
        # Wait for user to appear in UI
        assert page.wait_for_user_to_appear(user["email"])
        
        # Get user data from UI
        user_row_index = page.find_user_by_email(user["email"])
        ui_user_data = page.get_user_data_from_table(user_row_index)
        
        # Verify user exists in API
        try:
            response = requests.get(f"{api_url}/users")
            assert response.status_code == 200, "API should return 200 status"
            
            api_users = response.json()
            api_user = None
            for user in api_users:
                if user.get("email") == user["email"]:
                    api_user = user
                    break
            
            assert api_user is not None, "User should exist in API response"
            
            # Verify data consistency
            assert api_user["name"] == ui_user_data["name"], "Name should match between UI and API"
            assert api_user["email"] == ui_user_data["email"], "Email should match between UI and API"
            assert api_user["age"] == ui_user_data["age"] + " Year's", "Age should match between UI and API"
            
        except requests.RequestException as e:
            pytest.fail(f"API request failed: {e}")
    
    def test_11_edge_cases_and_error_handling(self, driver, base_url):
        """
        Test Case 11: Test edge cases and error handling scenarios.
        """
        driver.get(base_url)
        page = UserManagementPage(driver)
        
        # Test with very long name
        long_name = "A" * 100
        page.add_user(long_name, "longname@test.com", "25")
        
        # Test with special characters in name
        special_name = "John O'Connor-Smith"
        page.add_user(special_name, "special@test.com", "30")
        
        # Test with very young age
        page.add_user("Young User", "young@test.com", "18")
        
        # Test with maximum age
        page.add_user("Old User", "old@test.com", "70")
        
        # Verify all users were added
        assert page.wait_for_user_to_appear("longname@test.com")
        assert page.wait_for_user_to_appear("special@test.com")
        assert page.wait_for_user_to_appear("young@test.com")
        assert page.wait_for_user_to_appear("old@test.com")
    
    def test_12_performance_and_responsiveness(self, driver, base_url):
        """
        Test Case 12: Test application performance and responsiveness.
        """
        driver.get(base_url)
        page = UserManagementPage(driver)
        
        # Measure page load time
        start_time = time.time()
        page.wait_for_page_load()
        load_time = time.time() - start_time
        
        assert load_time < 5, f"Page should load within 5 seconds, took {load_time:.2f} seconds"
        
        # Test form responsiveness
        start_time = time.time()
        page.fill_user_form("Performance Test", "perf@test.com", "25")
        form_fill_time = time.time() - start_time
        
        assert form_fill_time < 2, f"Form filling should be responsive, took {form_fill_time:.2f} seconds"
        
        # Test table rendering
        start_time = time.time()
        page.get_users_count()
        table_render_time = time.time() - start_time
        
        assert table_render_time < 1, f"Table rendering should be fast, took {table_render_time:.2f} seconds" 