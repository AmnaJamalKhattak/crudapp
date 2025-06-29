#!/usr/bin/env python3
"""
Test runner script for Selenium tests.
This script can be used to run tests with different configurations.
"""

import subprocess
import sys
import os

def run_tests_with_pytest():
    """Run tests using pytest with various options"""
    
    # Basic test run
    print("Running Selenium tests...")
    result = subprocess.run([
        "pytest", 
        "test_users.py",
        "-v",  # Verbose output
        "--tb=short",  # Short traceback format
        "--strict-markers",
        "--disable-warnings"
    ], cwd=os.path.dirname(os.path.abspath(__file__)))
    
    return result.returncode

def run_tests_with_html_report():
    """Run tests and generate HTML report"""
    print("Running tests with HTML report...")
    result = subprocess.run([
        "pytest",
        "test_users.py",
        "--html=test_report.html",
        "--self-contained-html",
        "-v"
    ], cwd=os.path.dirname(os.path.abspath(__file__)))
    
    return result.returncode

def run_tests_with_coverage():
    """Run tests with coverage report"""
    print("Running tests with coverage...")
    result = subprocess.run([
        "pytest",
        "test_users.py",
        "--cov=.",
        "--cov-report=html",
        "--cov-report=term",
        "-v"
    ], cwd=os.path.dirname(os.path.abspath(__file__)))
    
    return result.returncode

def run_specific_test(test_name):
    """Run a specific test by name"""
    print(f"Running specific test: {test_name}")
    result = subprocess.run([
        "pytest",
        f"test_users.py::{test_name}",
        "-v"
    ], cwd=os.path.dirname(os.path.abspath(__file__)))
    
    return result.returncode

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == "html":
            exit_code = run_tests_with_html_report()
        elif command == "coverage":
            exit_code = run_tests_with_coverage()
        elif command == "specific" and len(sys.argv) > 2:
            exit_code = run_specific_test(sys.argv[2])
        else:
            print("Usage:")
            print("  python run_tests.py              # Run all tests")
            print("  python run_tests.py html         # Run with HTML report")
            print("  python run_tests.py coverage     # Run with coverage")
            print("  python run_tests.py specific TestUserManagement::test_01_page_load_and_elements_present")
            exit_code = 1
    else:
        exit_code = run_tests_with_pytest()
    
    sys.exit(exit_code) 