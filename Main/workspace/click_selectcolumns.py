#select_columns
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#-----------------click-on-select-columns--------

def click_selectcolumns(driver):
    
    try:
        selct_col = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'a.button.button-small.button-secondary')))
        selct_col.click()

        print("Clicked on Edit Columns!")
    except Exception as e:
        driver.save_screenshot("clickselectcolfailed.png")
        print("Failed to click Edit Columns:", e)