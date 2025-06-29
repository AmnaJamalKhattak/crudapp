from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

class BasePage:
    """
    Base page object class containing common methods for all page objects.
    """
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
    
    def find_element(self, by, value):
        """Find a single element with explicit wait"""
        try:
            return self.wait.until(
                EC.presence_of_element_located((by, value))
            )
        except TimeoutException:
            raise NoSuchElementException(f"Element not found with {by}={value}")
    
    def find_elements(self, by, value):
        """Find multiple elements with explicit wait"""
        try:
            return self.wait.until(
                EC.presence_of_all_elements_located((by, value))
            )
        except TimeoutException:
            return []
    
    def click_element(self, by, value):
        """Click an element with explicit wait"""
        try:
            element = self.wait.until(
                EC.element_to_be_clickable((by, value))
            )
            element.click()
            return True
        except TimeoutException:
            return False
    
    def send_keys_to_element(self, by, value, text):
        """Send keys to an element with explicit wait"""
        try:
            element = self.wait.until(
                EC.presence_of_element_located((by, value))
            )
            element.clear()
            element.send_keys(text)
            return True
        except TimeoutException:
            return False
    
    def is_element_present(self, by, value):
        """Check if an element is present"""
        try:
            self.find_element(by, value)
            return True
        except NoSuchElementException:
            return False
    
    def wait_for_element_visible(self, by, value, timeout=10):
        """Wait for an element to be visible"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, value))
            )
            return True
        except TimeoutException:
            return False
    
    def wait_for_element_invisible(self, by, value, timeout=10):
        """Wait for an element to be invisible"""
        try:
            WebDriverWait(self.driver, timeout).until(
                EC.invisibility_of_element_located((by, value))
            )
            return True
        except TimeoutException:
            return False
    
    def wait_for_page_load(self):
        """Wait for page to load completely"""
        try:
            self.wait.until(
                lambda driver: driver.execute_script("return document.readyState") == "complete"
            )
            return True
        except TimeoutException:
            return False
    
    def get_element_text(self, by, value):
        """Get text of an element with explicit wait"""
        try:
            element = self.wait.until(
                EC.presence_of_element_located((by, value))
            )
            return element.text
        except TimeoutException:
            return None
    
    def get_element_attribute(self, by, value, attribute):
        """Get attribute of an element with explicit wait"""
        try:
            element = self.wait.until(
                EC.presence_of_element_located((by, value))
            )
            return element.get_attribute(attribute)
        except TimeoutException:
            return None
    
    def take_screenshot(self, filename):
        """Take screenshot and save to file."""
        self.driver.save_screenshot(f"screenshots/{filename}.png")
    
    def get_alert_text(self):
        """Get text from alert dialog."""
        try:
            alert = self.driver.switch_to.alert
            text = alert.text
            alert.accept()
            return text
        except:
            return None
    
    def scroll_to_element(self, by, value):
        """Scroll to element."""
        element = self.find_element(by, value)
        self.driver.execute_script("arguments[0].scrollIntoView(true);", element)
        time.sleep(0.5)
    
    def wait_for_element_to_disappear(self, by, value, timeout=10):
        """Wait for element to disappear."""
        try:
            WebDriverWait(self.driver, timeout).until_not(
                EC.presence_of_element_located((by, value))
            )
            return True
        except TimeoutException:
            return False 