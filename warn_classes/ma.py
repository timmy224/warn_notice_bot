import re

import pandas as pd
from .base_warn import Warn

class MAWarn(Warn):
    url = 'https://www.mass.gov/service-details/worker-adjustment-and-retraining-act-warn-weekly-report'
    state = "MA"

    def __init__(self, date=None):
        super().__init__(self.url, date)
        self.tags = "#warnact #layoffs #MA #massachusetts"

    def _fetch_latest_notices(self) -> dict:
        layoffs = {}
        month, day, year = self._compare_date.split('/')
        
        formatted_date = "-".join([
            month.zfill(2), 
            day.zfill(2),
            year[-2:]])
        
        download_url = f"https://www.mass.gov/doc/warn-report-for-the-week-ending-{formatted_date}/download"
        try:
            reader = pd.ExcelFile(download_url)
        except:
            print("File not found: updated each Friday")
            return {}
        
        sheet_names = [s for s in reader.sheet_names]
        df = pd.DataFrame()
        for sheet_name in sheet_names:
            try:
                temp_df = pd.read_excel(
                    download_url, 
                    header=2, 
                    sheet_name=sheet_name
                )

                temp_df['Date Received'] = temp_df['Date Received'].dt.strftime('%-m/%-d/%Y')
                temp_df = temp_df[temp_df['Date Received'] == self._compare_date]
            except:
                temp_df = None
            
            if temp_df is not None:
                df = pd.concat([df, temp_df])
        
        if len(df) == 0:
            return {}
        
        for _, row in df.iterrows():
            company_name = row['Company Name'].strip()
            number_str = str(row['# Affected']).split(" ")

            try:
                number_affected = int(number_str[-1])
            except:
                number_affected = int(number_str[0])

            if company_name not in layoffs:
                layoffs[company_name] = 0 
            layoffs[company_name] += number_affected

        return layoffs