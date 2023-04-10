import re
from typing import List

import pandas as pd
from .base_warn import Warn

class CAWarn(Warn):
    url = 'https://edd.ca.gov/siteassets/files/jobs_and_training/warn/warn_report.xlsx'
    state = "CA"

    def __init__(self, date=None):
        super().__init__(self.url, date)
        self.tags = "#jobs #layoffs #CA #california"

    def _fetch_latest_notices(self) -> dict:
        df = pd.read_excel(self.url, sheet_name='Sheet1', dtype=str)
        month, date, year = self.get_month_date_year(self._compare_date)
        match_date = f'{year}-{month}-{date} 00:00:00'
        df['Received\nDate'] = df['Received\nDate'].astype(str)
        df = df[df['Received\nDate'] == match_date]

        layoffs = {}
        for _, row in df.iterrows():
            company_name = row['Company'].strip()
            number_affected = row['No. Of\nEmployees']
            if company_name not in layoffs:
                layoffs[company_name] = 0 
            layoffs[company_name] += number_affected
        return layoffs

    def get_month_date_year(self, date:str):
        date_regex = re.compile(r'(\d{1,2})/(\d{1,2})/(\d{1,4})')
        match = date_regex.search(date)
        if match:
            month = match.group(1)
            date = match.group(2)
            year = match.group(3)

            if len(month) == 1:
                month = "0" + month
            if len(date) == 1:
                date = "0" + date

        return month, date, year
