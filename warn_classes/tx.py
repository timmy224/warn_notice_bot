import re

import pandas as pd
from .base_warn import Warn

class TXWarn(Warn):
    url = 'https://www.twc.texas.gov/files/news/warn-act-listings-2023-twc.xlsx'
    state = "TX"

    def __init__(self, date=None):
        super().__init__(self.url, date)
        self.tags = "#warnact #layoffs #TX #texas"

    def _fetch_latest_notices(self) -> dict:
        layoffs = {}

        df = pd.read_excel(self.url, sheet_name='Sheet1')
        df["NOTICE_DATE"] = df["NOTICE_DATE"].dt.strftime('%-m/%-d/%-y')
        df = df[df["NOTICE_DATE"] == self._compare_date]

        for _, row in df.iterrows():
            company_name = row['JOB_SITE_NAME'].strip()
            number_affected = row['TOTAL_LAYOFF_NUMBER']
            if company_name not in layoffs:
                layoffs[company_name] = 0 
            layoffs[company_name] += number_affected
        return layoffs