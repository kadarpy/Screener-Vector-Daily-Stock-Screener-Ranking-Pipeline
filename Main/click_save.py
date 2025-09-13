#save
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time


#------Click-"Save-columns"-button------


def click_save(driver):
    
    try:
        save = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR,'button.button-primary')))
        

          # Scroll into view
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save)
        time.sleep(0.5)
        try:
            save.click()
        except:
            ActionChains(driver).move_to_element(save).click().perform()
        print("Clicked Save Columns!")
    except Exception as e:
        driver.save_screenshot("clicksavecolfailed.png")
        print("Failed to click Save Columns button:", e)