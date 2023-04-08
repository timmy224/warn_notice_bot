import re
from typing import List, Tuple

from bs4 import BeautifulSoup
import requests
from .base_warn import Warn

class NYWarn(Warn):
    url = "https://dol.ny.gov/warn-notices"
    tags = "#warnact #layoffs #ny #newyork"
    state = "NY"

    def __init__(self, date=None):
        super().__init__(self.url, date)

    def _fetch_latest_notices(self) -> dict:
        rows = self.get_rows()
        layoffs = {}
        for row in rows:
            posted_date = row.findNext('td').findNext('td').text
            if self._compare_date not in posted_date:
                continue

            # get pdf link
            pdf_link = None
            try:
                pdf_link = self.get_pdf_link(row)
            except: 
                print('Error finding PDF link')
                continue

            if pdf_link is None:
                print('No PDF link was found')
                continue

            try:
                pdf_text = self.get_pdf_text(pdf_link)
            except:
                print("Error processing pdf text")
                continue

            company_name, number_affected = self.process_pdf(pdf_text)
            if company_name not in layoffs:
                layoffs[company_name] = 0 
            layoffs[company_name] += number_affected
        return layoffs
  
    def get_rows(self) -> List:
        response = requests.get(self._url)
        soup = BeautifulSoup(response.text, 'html.parser')
        rows = soup.find('table').find_all("tr")
        return rows

    def get_pdf_link(self, row) -> str:
        url_concat = self._url.split("/warn-notices")[0]
        links = row.find_all('a', href=True)
        for link in links:
            pdf_link = url_concat + "/" + link['href']
            pdf_link = pdf_link.strip()
            return pdf_link

    def process_pdf(self, pdf_text) -> Tuple[str, str]:
        company_pattern = r"(?:C\n?o\n?m\n?p\n?a\n?n\n?y: )\s+([^\n]+)"
        company_name = re.search(company_pattern, pdf_text).group(1)

        number_pattern = r"N\n?u\n?m\n?b\n?e\n?r\s+A\s*f\n?f\n?e\n?c\n?t\n?e\n?d:\s*(\d+)"
        number_affected = int(re.search(number_pattern, pdf_text).group(1))
        
        return company_name.strip(), number_affected
    