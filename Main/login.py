#login
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import LOGIN_PAGE

#------------loggin-----------

def login(driver, email, password):
    driver.get(LOGIN_PAGE)
    
    try:
        user = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "username")))
        user.send_keys(email)

        pas = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password")))
        pas.send_keys(password)

        submit = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "button.button-primary")))
        submit.click()

        print("Loged in!")

    except Exception as error:
        print("failed to login!",error)