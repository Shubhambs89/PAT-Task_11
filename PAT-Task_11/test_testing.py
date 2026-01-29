import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.fixture
def driver():
    #Setup Headless Mode
    chrome_options = Options()
    chrome_options.add_argument("--headless=new") 
    chrome_options.add_argument("--incognito")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get("https://www.guvi.in/")
    yield driver
    driver.quit()

# --- Positive Test Cases ---

# Validate the URL of the login button to be https://www.guvi.in/sign-in/
def test_login_button_url(driver):
    wait = WebDriverWait(driver, 10)
    
    login_button = wait.until(EC.element_to_be_clickable((By.ID, "login-btn")))
    login_button.click()
    
    wait.until(EC.url_contains("sign-in"))

    current_url = driver.current_url
    assert current_url == "https://www.guvi.in/sign-in/?sourceUri=http%3A%2F%2Fwww.guvi.in%2F"


#Validate the username and password boxes are visible and enabled
def test_login_fields_visibility(driver):
    wait = WebDriverWait(driver, 10)
    
    # Navigate to login page
    wait.until(EC.element_to_be_clickable((By.ID, "login-btn"))).click()
    
    email_field = wait.until(EC.visibility_of_element_located((By.ID, "email")))
    password_field = wait.until(EC.visibility_of_element_located((By.ID, "password")))
    
    assert email_field.is_displayed() and email_field.is_enabled()
    assert password_field.is_displayed() and password_field.is_enabled()

#validate that the submit button is working properly
def test_submit_button_functionality(driver):
    wait = WebDriverWait(driver, 10)
    
    wait.until(EC.element_to_be_clickable((By.ID, "login-btn"))).click()
    
    wait.until(EC.visibility_of_element_located((By.ID, "email"))).send_keys("sb1249952@gmail.com")
    wait.until(EC.visibility_of_element_located((By.ID, "password"))).send_keys("4AI12me101@")
    
    submit_button = driver.find_element(By.ID, "login-btn")
    submit_button.click()
    
    assert submit_button.is_enabled()

# --- Negative Test Case ---

def test_invalid_login(driver):
    wait = WebDriverWait(driver, 10)
    
    wait.until(EC.element_to_be_clickable((By.ID, "login-btn"))).click()
    
    wait.until(EC.visibility_of_element_located((By.ID, "email"))).send_keys("invalid@example.com")
    wait.until(EC.visibility_of_element_located((By.ID, "password"))).send_keys("wrongpassword")
    
    driver.find_element(By.ID, "login-btn").click()

    # Wait specifically for the error message to appear in the DOM
    error_message = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "invalid-feedback")))
    
    assert error_message.is_displayed()
    assert "Incorrect Email or Password" in error_message.text