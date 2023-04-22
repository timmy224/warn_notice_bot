from bs4 import BeautifulSoup
import requests
import pandas as pd

from .base_warn import Warn

class NCWarn(Warn):
    url = "https://www.commerce.nc.gov/data-tools-reports/labor-market-data-tools/workforce-warn-reports/report-workforce-warn-listings-2023/open"
    state = "NC"

    def __init__(self, date=None):
        super().__init__(self.url, date)
        self.tags = "#jobs #layoffs #NC #northcarolina"

    def _fetch_latest_notices(self) -> dict:
        layoffs = {}
        
        dfs = self.get_pdf_tables(
            self._url, 
            stream=True
        )
        df = pd.DataFrame()
        for i_df in dfs:
            if len(df) == 0: 
                df = i_df
                continue

            if len(i_df.columns) == len(df.columns):
                df = pd.concat([df, i_df])
        if len(df) == 0:
            return layoffs
        
        df = df.reset_index(drop="index").T.reset_index().T # shift header down
        df = df.iloc[:, [2, 4, 7]]
        df.columns = ["Notice Date", "Company Name", "Number Affected"]
        df = df[df["Notice Date"] == self._compare_date]
        if len(df) == 0:
            return {}
        
        for _, row in df.iterrows():
            company_name = row["Company Name"]
            number_affected = int(row["Number Affected"])
            if company_name not in layoffs:
                layoffs[company_name] = 0
            layoffs[company_name] += number_affected

        return layoffs
    