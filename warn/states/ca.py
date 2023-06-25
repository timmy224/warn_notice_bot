import re
from typing import List

import pandas as pd
from ..warn_base import Warn

class CAWarn(Warn):
    url = 'https://edd.ca.gov/siteassets/files/jobs_and_training/warn/warn_report.xlsx'
    state = "CA"

    def __init__(self, date=None):
        super().__init__(self.url, date)
        self.tags = "#jobs #layoffs #CA #california"

    def _fetch_latest_notices(self) -> dict:
        df = pd.read_excel(self.url, sheet_name='Sheet1', dtype=str)
        if 'Received\nDate' not in df.columns:
            df = pd.read_excel(self.url, sheet_name='Sheet1', dtype=str, skiprows=1)
        df['Received\nDate'] = df['Received\nDate'].astype(str)

        month, date, year = self.get_month_date_year(self._compare_date)
        match_date = f'{year}-{month}-{date} 00:00:00'
        df = df[df['Received\nDate'] == match_date]

        layoffs = {}
        for _, row in df.iterrows():
            company_name = row['Company'].strip()
            number_affected = row['No. Of\nEmployees']
            if company_name not in layoffs:
                layoffs[company_name] = 0 
            layoffs[company_name] += int(number_affected)
        return layoffs
