import re
from typing import List, Tuple

from bs4 import BeautifulSoup
import requests
import pandas as pd

from .base_warn import Warn

class SCWarn(Warn):
    url = "https://scworks.org/employer/employer-programs/risk-closing/layoff-notification-reports"
    state = "SC"

    def __init__(self, date=None):
        super().__init__(self.url, date)
        self.tags = "#warnact #layoffs #sc #southcarolina"

    def _fetch_latest_notices(self) -> dict:
        layoffs = {}
        
        pdf_link = self.get_pdf_link(self._url)
        dfs = self.get_pdf_tables(pdf_link)
        df = pd.DataFrame()
        for i_df in dfs:
            df = pd.concat([df, i_df])
        
        df = df[~df["Notice Date"] == self._compare_date]
        for _, row in df.iterrows():
            company_name = row["Company"]
            number_affected = int(row["Impacted"])
            if company_name not in layoffs:
                layoffs[company_name] = 0
            layoffs[company_name] += number_affected

        return layoffs
        
    def get_pdf_link(self, url=None) -> str:
        if url is None:
            url = self._url

        try:
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            class_pattern = "clearfix text-formatted field field--name-body"\
            " field--type-text-with-summary field--label-hidden field__item"
            li = soup.find(class_=class_pattern).find_all("li")[0]
        except:
            print("Can't get PDF link")

        curr_date = self._compare_date.replace("/", "-")
        if li and curr_date in li.text:
            a_href = li.find("a", href=True)
            pdf_link = "https://scworks.org" + a_href['href']
            return pdf_link
        return None

    def process_pdf(self, pdf_text:str) -> Tuple[str, str]:
        company_pattern = r"(?:C\n?o\n?m\n?p\n?a\n?n\n?y: )\s+([^\n]+)"
        company_name = re.search(company_pattern, pdf_text).group(1)

        number_pattern = r"N\n?u\n?m\n?b\n?e\n?r\s+A\s*f\n?f\n?e\n?c\n?t\n?e\n?d:\s*(\d+)"
        number_affected = int(re.search(number_pattern, pdf_text).group(1))
        
        return company_name.strip(), number_affected
    