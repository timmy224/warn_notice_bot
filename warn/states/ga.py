import re

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import pandas as pd

from ..warn_base import Warn

class GAWarn(Warn):
    url = "https://www.tcsg.edu/warn-public-view/"
    state = "GA"

    def __init__(self, date=None):
        super().__init__(self.url, date)
        self.tags = "#jobs #layoffs #GA #georgia"

    def _fetch_latest_notices(self) -> dict:
        layoffs = {}
        rows = self.get_html_rows()
        if rows is None:
            return layoffs
        
        df = rows[0]
        if df is None:
            return {}
        df["Submitted Date"] = pd.to_datetime(
            df["Submitted Date"], 
            format="%B %d, %Y",
            errors="coerce"
        )
        df["Submitted Date"] = df["Submitted Date"].dt.strftime('%-m/%-d/%Y')
        df = df[df["Submitted Date"] == self._compare_date]
        if len(df) == 0:
            return {}
        
        for _, row in df.iterrows():
            company_name = self.get_company_name(str(df["Company Name"]))
            if company_name is None:
                continue
            number_affected = row["Total Number of Affected Employees"]
            if company_name not in layoffs:
                layoffs[company_name] = 0 
            layoffs[company_name] += number_affected

        return layoffs

    def get_html_rows(self) -> list:
        self.driver.get(self._url)
        delay = 5
        xpath = "//th[@aria-label='Submitted Date: activate to sort column ascending']"
        try:
            WebDriverWait(self.driver, delay)\
                .until(EC.presence_of_element_located((
                    By.XPATH,
                    xpath
                )))
            print('Page is ready')
        except TimeoutException:
            print('Timeout occurred before element loaded')
            return None

        try:
            submitted_date_filter = self.driver.find_element(By.XPATH, xpath)
            submitted_date_filter.click()
            WebDriverWait(self.driver, 2)

            table_html = self.driver.find_element(By.ID, "DataTables_Table_0")\
                .get_attribute('outerHTML')
            dfs = pd.read_html(table_html)
            return dfs
        except:
            return None
