# main.py
import pandas as pd
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from config import EMAIL, PASSWORD, COLUMNS
from login import login
from click_watchlist import click_watchlist
from click_selectcolumns import click_selectcolumns
from select_columns import select_columns
from click_save import click_save
from table_extractor import extract_table_insert
from select_sector import select_sector

def main():
    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    
    try:
        starttime = datetime.now()

        login(driver, EMAIL, PASSWORD)
        # select_sector(driver)
        click_watchlist(driver)
        click_selectcolumns(driver)
        select_columns(driver,COLUMNS)
        click_save(driver)
        extract_table_insert(driver)
        endtime = datetime.now()
        print(f"Time taken by program = {(endtime-starttime).total_seconds()}")

    except Exception as e:
        print("Error:", e)

    finally:
        driver.quit()

if __name__ == "__main__":
    main()