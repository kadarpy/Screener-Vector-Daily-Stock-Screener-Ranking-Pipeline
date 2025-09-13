#watchlist
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

#--------------click-on-watchlist---------

def click_watchlist(driver):
    try:
        watchlist = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR,'a.button.button-small')))
        watchlist.click()

        print("Clicked on Watchlist")
    except Exception as e:
        driver.save_screenshot("watchlistclickfailed.png")
        print("Failed to click Watchlist:", e)