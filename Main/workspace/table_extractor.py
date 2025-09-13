#extract_table
import pandas as pd
from datetime import datetime,date
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from sqlalchemy import create_engine


def extract_table_insert(driver):
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "table.data-table")))
    
    soup = BeautifulSoup(driver.page_source, "html.parser")
    table = soup.find("table", class_="data-table")

    
    if table:
         print("Table found")
    else:
        raise Exception("Could not find table")
        

    header_row = table.find("tr")

    headers = [tableheader.get_text(strip=True).lower() for tableheader in header_row.find_all("th")]
    print(f"Found headers: {headers}")
    rows = []
    for tablerows in table.find_all("tr")[1:]:
        tabledata = tablerows.find_all("td")
        cells = [td.get_text(strip=True) for td in tabledata]
        if "" in cells:
                cells.remove("")
        if len(cells)==len(headers):
            rows.append(cells)
        

    if not rows:
        raise Exception("No valid rows extracted")

    df = pd.DataFrame(rows, columns=headers)
    df=df.drop(columns="s.no.",errors="ignore")
    df["date"] = date.today()
    df = df[["name", "cmprs.", "3mth return%", "6mth return%", "p/e", "mar caprs.cr.", "earnings yield%", "sales qtrrs.cr.", "pat qtrrs.cr.", "qtr sales var%",	"qtr profit var%"	,"roce%",	"debt / eq","roe%",	"date"]]
    df.to_csv("Screener.csv",index=False)

    try:
        engine = create_engine("postgresql+psycopg2://user:password@localhost:5432/database")
        with engine.connect() as conn:
            print("Connected to PostgreSQL",conn)
    except Exception as e:
        print("Failed to connect!",e)

    try:
        df.to_sql("screener",engine, if_exists="append", index=False)
        print("Data for today appended.")
    except Exception as e:
        print("Error inserting data")

