#select_columns
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#-------------Select-checkboxes-by-label--------------

def select_columns(driver,COLUMNS):
    
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "ratio")))

        columnnames = driver.find_elements(By.CLASS_NAME, "ratio")
        matched = 0

        for columnname in columnnames:
            column_names = columnname.text.strip()
            checkbox = columnname.find_element(By.TAG_NAME, "input")
    
            if column_names in COLUMNS:
                if not checkbox.is_selected():
                    driver.execute_script("arguments[0].click();", checkbox)
                    print(f"Selected column: {column_names}")
                matched += 1
            else:
                if checkbox.is_selected():
                    driver.execute_script("arguments[0].click();", checkbox)
                    print(f"Deselect columns: {column_names}")


        print(f"Total columns matched and selected: {matched}")
        print(matched)

        if matched == 0:
            print("None of the desired columns matched.")

    except Exception as e:
        driver.save_screenshot("error_screenshot2.png")
        print("Failed to select columns:", e)