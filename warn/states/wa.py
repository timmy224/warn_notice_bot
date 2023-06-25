from bs4 import BeautifulSoup
import pandas as pd
import requests

from ..warn_base import Warn

class WAWarn(Warn):
    url = "https://fortress.wa.gov/esd/file/warn/Public/SearchWARN.aspx"
    state = "WA"

    def __init__(self, date=None):
        super().__init__(self.url, date)
        self.tags = "#jobs #layoffs #WA #washington"

    def _fetch_latest_notices(self) -> dict:
        layoffs = {}
        df = self._get_html_table(self._url)
        if df is None:
            return {}
        
        df = df[df["Received Date"] == self._compare_date]
        if len(df) == 0:
            return {}

        for _, row in df.iterrows():
            company_name = row["Company"]
            number_affected = row["# of Workers"]
            if company_name not in layoffs:
                layoffs[company_name] = 0 
            layoffs[company_name] += int(number_affected)
        return layoffs
  
    def _get_html_table(self, url:str=None) -> pd.DataFrame:
        if url is None:
            url = self._url 
        
        try:
            response = requests.get(self._url)
            soup = BeautifulSoup(response.text, 'html.parser')
            html_table = soup.find('table', {"id": "ucPSW_gvMain"})
            df = pd.read_html(str(html_table), match='Company')[0]
            df = df.rename(columns=df.iloc[1])
            df = df.iloc[2:]
            return df
        except:
            return None
