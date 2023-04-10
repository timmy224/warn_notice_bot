from typing import List

from bs4 import BeautifulSoup
import pandas as pd
import requests
from .base_warn import Warn

class MIWarn(Warn):
    url = "https://milmi.org/warn/"
    state = "MI"

    def __init__(self, date=None):
        super().__init__(self.url, date)
        self.tags = "#jobs #layoffs #MI #michigan"

    def _fetch_latest_notices(self) -> dict:
        layoffs = {}
        df = self._get_html_table(self._url)
        if df is None:
            return {}
        
        df = df[df["Date Received"] == self._compare_date]
        if len(df) == 0:
            return {}
        
        for _, row in df.iterrows():
            company_name = row["Company Name"]
            number_affected = row["Number of Layoffs"]
            if company_name not in layoffs:
                layoffs[company_name] = 0 
            layoffs[company_name] += number_affected
        return layoffs
  
    def _get_html_table(self, url:str=None) -> List:
        if url is None:
            url = self._url

        try:
            response = requests.get(self._url)
            soup = BeautifulSoup(response.text, 'html.parser')
            table_html = soup.find(
                "table", {
                "class": "table tablewarn table-striped table-branded"
            })

            df = pd.read_html(str(table_html))[0]
            return df
        except Exception:
            return None

        
    