from bs4 import BeautifulSoup
import pandas as pd
import requests

from .base_warn import Warn

class OHWarn(Warn):
    url = "https://jfs.ohio.gov/warn/current.stms"
    state = "OH"

    def __init__(self, date=None):
        super().__init__(self.url, date)
        self.tags = "#warnact #layoffs #OH #ohio"

    def _fetch_latest_notices(self) -> dict:
        layoffs = {}
        df = self._get_html_table(self._url)
        if df is None:
            return {}

        month, day, year = self._compare_date.split("/")
        curr_date = "/".join([
            month.zfill(2),
            day.zfill(2),
            year
        ])

        df = df[df["Date Received"] == curr_date]
        if len(df) == 0:
            return {}

        for _, row in df.iterrows():
            company_name = row["Company"]
            number_affected = row["Potential Number Affected"]
            if company_name not in layoffs:
                layoffs[company_name] = 0 
            layoffs[company_name] += number_affected
        return layoffs
  
    def _get_html_table(self, url:str=None) -> pd.DataFrame:
        if url is None:
            url = self._url 
        
        try:
            response = requests.get(self._url)
            soup = BeautifulSoup(response.text, 'html.parser')
            html_table = soup.find('table', {"class": "warnTable"})
            dfs = pd.read_html(str(html_table))
            return dfs[0]
        except:
            return None

        

    