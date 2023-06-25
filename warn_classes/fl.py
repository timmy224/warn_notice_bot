import re

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException
import pandas as pd

from .base_warn import Warn

class FLWarn(Warn):
    url = "https://reactwarn.floridajobs.org/WarnList/Records?year=2023"
    state = "FL"

    def __init__(self, date=None):
        super().__init__(self.url, date)
        self.tags = "#jobs #layoffs #FL #florida"

    def _fetch_latest_notices(self) -> dict:
        layoffs = {}
        df = self.get_html_rows()[0]
        if df is None:
            return {}
        
        month, date, year = self.get_month_date_year(self._compare_date)
        curr_date = f"{month}-{date}-{year}"
        df = df[df["State Notification Date"] == curr_date]
        if len(df) == 0:
            return {}
        
        for _, row in df.iterrows():
            company_name = self.get_company_name(str(df["Company Name"]))
            if company_name is None:
                continue
            number_affected = row["Employees Affected"]
            if company_name not in layoffs:
                layoffs[company_name] = 0 
            layoffs[company_name] += number_affected

        return layoffs

    def get_html_rows(self) -> list:
        self.driver.get(self._url)
        delay = 10
        xpath = "//table[@id='DataTable']"
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

            table_html = self.driver.find_element(By.ID, "DataTable")\
                .get_attribute('outerHTML')
            dfs = pd.read_html(table_html)
            return dfs
        except:
            return None
