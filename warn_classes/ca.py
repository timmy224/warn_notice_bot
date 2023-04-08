import re
from typing import List

import pandas as pd
from .base_warn import Warn

class CAWarn(Warn):
    url = 'https://edd.ca.gov/siteassets/files/jobs_and_training/warn/warn_report.xlsx'

    def __init__(self):
        super().__init__(self.url)
        self.tags = "#warnact #layoffs #ca #california"

    def fetch_latest_notices(self) -> List[dict]:
        df = pd.read_excel(self.url, sheet_name='Sheet1', dtype="object")
        month, date, year = self.get_month_date_year(self._compare_date)
        match_date = f'{year}-{month}-{date} 00:00:00'
        df['Received\nDate'] = df['Received\nDate'].astype(str)
        df = df[df['Received\nDate'] == match_date]

        layoffs = []
        for _, row in df.iterrows():
            company_name = row['Company']
            number_affected = row['No. Of\nEmployees']
            layoffs.append({
                "company_name": company_name.strip(),
                "number_affected": number_affected,
            })
        return layoffs

    def get_month_date_year(self, date_str):
        date_regex = re.compile(r'(\d{1,2})/(\d{1,2})/(\d{1,4})')
        match = date_regex.search(date_str)
        if match:
            month = match.group(1)
            date = match.group(2)
            year = match.group(3)

            if len(month) == 1:
                month = "0" + month
            if len(date) == 1:
                date = "0" + date

        return month, date, year

    def process_pdf(self, pdf_text) -> dict:
        company_name = re.search(r"(?:C\n?o\n?m\n?p\n?a\n?n\n?y: )\s+([^\n]+)", pdf_text).group(1)
        number_affected = int(re.search(r"N\n?u\n?m\n?b\n?e\n?r\s+A\s*f\n?f\n?e\n?c\n?t\n?e\n?d:\s*(\d+)", pdf_text).group(1))
        
        return {
            "company_name": company_name.strip(),
            "number_affected": number_affected,
        }
    