# Selenium Test Suite for CRUD Application

This directory contains comprehensive Selenium test cases for the User Management CRUD application. The tests are designed to run in headless Chrome mode, making them suitable for CI/CD pipelines on AWS EC2 and Jenkins.

## Features

- **12+ Comprehensive Test Cases** covering all CRUD operations
- **Headless Chrome Support** for CI/CD environments
- **Page Object Model** design pattern for maintainable tests
- **Cross-platform compatibility** (Windows, Linux, macOS)
- **Jenkins/AWS EC2 ready** configuration
- **HTML and coverage reports** support

## Test Cases Overview

1. **Page Load and Elements** - Verify application loads correctly
2. **Add User Successfully** - Test valid user creation
3. **Duplicate Email Handling** - Test duplicate email validation
4. **Invalid Data Validation** - Test form validation
5. **Edit User** - Test user update functionality
6. **Delete User** - Test user deletion
7. **Form Validation** - Test form clearing and validation
8. **Multiple Users** - Test operations with multiple users
9. **Data Persistence** - Test data persistence after page refresh
10. **API Integration** - Verify UI-API data consistency
11. **Edge Cases** - Test boundary conditions and error handling
12. **Performance** - Test application responsiveness

## Prerequisites

- Python 3.8 or higher
- Chrome browser installed
- Node.js application running (frontend on port 5173, backend on port 3000)

## Installation

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Ensure your application is running:
   ```bash
   # Terminal 1 - Start backend
   cd server
   npm start
   
   # Terminal 2 - Start frontend
   cd client
   npm run dev
   ```

## Running Tests

### Basic Test Run
```bash
pytest test_users.py -v
```

### Using the Test Runner Script
```bash
# Run all tests
python run_tests.py

# Run with HTML report
python run_tests.py html

# Run with coverage
python run_tests.py coverage

# Run specific test
python run_tests.py specific TestUserManagement::test_01_page_load_and_elements_present
```

### Direct Pytest Commands
```bash
# Run with verbose output
pytest test_users.py -v

# Run with HTML report
pytest test_users.py --html=test_report.html --self-contained-html

# Run with coverage
pytest test_users.py --cov=. --cov-report=html

# Run specific test class
pytest test_users.py::TestUserManagement -v

# Run tests in parallel (requires pytest-xdist)
pytest test_users.py -n 4
```

## Configuration

### Environment Variables
You can configure the test URLs using environment variables:

```bash
export BASE_URL="http://localhost:5173"
export API_URL="http://localhost:3000/api"
```

### Chrome Options
The tests are configured for headless Chrome with the following options:
- `--headless` - Run without GUI
- `--no-sandbox` - Disable sandbox for CI environments
- `--disable-dev-shm-usage` - Overcome limited resource problems
- `--disable-gpu` - Disable GPU hardware acceleration
- `--window-size=1920,1080` - Set window size

## Test Structure

```
selenium_tests/
├── test_users.py              # Main test file with 12 test cases
├── run_tests.py               # Test runner script
├── requirements.txt           # Python dependencies
├── conftest.py               # Pytest configuration and fixtures
├── pages/                    # Page Object Model classes
│   ├── base_page.py          # Base page class
│   └── user_management_page.py # User management page class
└── README.md                 # This file
```

## Page Object Model

The tests use the Page Object Model design pattern for better maintainability:

- **BasePage**: Common Selenium operations and utilities
- **UserManagementPage**: Specific page interactions for the user management interface

## CI/CD Integration

### Jenkins Pipeline Example
```groovy
stage('Selenium Tests') {
    steps {
        script {
            // Install Python dependencies
            sh 'pip install -r selenium_tests/requirements.txt'
            
            // Run Selenium tests
            sh 'cd selenium_tests && pytest test_users.py -v --html=test_report.html'
            
            // Publish test results
            publishHTML([
                allowMissing: false,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'selenium_tests',
                reportFiles: 'test_report.html',
                reportName: 'Selenium Test Report'
            ])
        }
    }
}
```

### AWS EC2 Setup
1. Install Chrome and ChromeDriver:
   ```bash
   # Install Chrome
   sudo apt-get update
   sudo apt-get install -y google-chrome-stable
   
   # Install ChromeDriver (or use webdriver-manager)
   sudo apt-get install -y chromium-chromedriver
   ```

2. Install Python dependencies:
   ```bash
   pip install -r selenium_tests/requirements.txt
   ```

3. Run tests:
   ```bash
   cd selenium_tests
   pytest test_users.py -v
   ```

## Troubleshooting

### Common Issues

1. **Chrome not found**: Ensure Chrome is installed and accessible
2. **Port already in use**: Check if your application is running on the correct ports
3. **Element not found**: Verify the application is fully loaded before running tests
4. **Timeout errors**: Increase implicit wait times in the test configuration

### Debug Mode
To run tests in non-headless mode for debugging:
```python
# In test_users.py, comment out the headless option:
# options.add_argument("--headless")
```

### Screenshots
Tests automatically take screenshots on failure. Check the `screenshots/` directory.

## Test Data

The tests use the following test data patterns:
- Valid users with proper email formats
- Invalid data for validation testing
- Duplicate emails for error handling
- Edge cases with long names and boundary ages

## Reporting

### HTML Reports
Generate detailed HTML reports:
```bash
pytest test_users.py --html=test_report.html --self-contained-html
```

### Coverage Reports
Generate coverage reports:
```bash
pytest test_users.py --cov=. --cov-report=html --cov-report=term
```

## Contributing

When adding new test cases:
1. Follow the existing naming convention: `test_XX_descriptive_name`
2. Add proper docstrings explaining the test purpose
3. Use the Page Object Model for element interactions
4. Include both positive and negative test scenarios
5. Add appropriate assertions and error messages

## License

This test suite is part of the CRUD application project and follows the same license terms. 