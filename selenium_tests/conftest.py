import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import chromedriver_binary  # This will add ChromeDriver to PATH
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

@pytest.fixture(scope="session")
def driver():
    """
    Fixture to create and manage Chrome WebDriver instance.
    Using session scope to reuse the same browser for all tests.
    """
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")  # Run in headless mode for Docker
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")

    try:
        # Initialize WebDriver
        service = Service()
        driver = webdriver.Chrome(service=service, options=chrome_options)
        yield driver
    finally:
        driver.quit()

@pytest.fixture(scope="session")
def base_url():
    """Get the base URL for the frontend application."""
    return os.getenv("FRONTEND_URL", "http://localhost:5173")

@pytest.fixture(scope="session")
def api_url():
    """Get the base URL for the backend API."""
    return os.getenv("BACKEND_URL", "http://localhost:3000/api")

@pytest.fixture
def test_data():
    """
    Fixture to provide test data for user operations.
    """
    return {
        "valid_user": {
            "name": "John Doe",
            "email": "john.doe@test.com",
            "age": "30"
        },
        "updated_user": {
            "name": "John Updated",
            "email": "john.updated@test.com",
            "age": "31"
        },
        "invalid_user": {
            "name": "",
            "email": "invalid-email",
            "age": "150"
        },
        "duplicate_email": {
            "name": "Jane Doe",
            "email": "john.doe@test.com",  # Same email as valid_user
            "age": "25"
        }
    } 