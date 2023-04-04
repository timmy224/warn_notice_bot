import re
from typing import List

from bs4 import BeautifulSoup
import requests
from .base_warn import Warn

class NYWarn(Warn):
    url = 'https://dol.ny.gov/warn-notices'

    def __init__(self):
        super().__init__(self.url)
        self.tags = "#warnact #layoffs #ny #newyork"

    def fetch_latest_notices(self) -> List[dict]:
        rows = self.get_rows()
        print(f"{len(rows)} row(s) found")
        layoffs = []
        for row in rows:
            posted_date = row.findNext('td').findNext('td').text
            if self._compare_date not in posted_date:
                continue

            # get pdf link
            pdf_link = None
            try:
                pdf_link = self.get_pdf_link(row)
            except: 
                print('error getting pdf_link')
                continue

            if pdf_link is None:
                print('pdf_link is None')
                continue

            try:
                pdf_text = self.get_pdf_text(pdf_link)
            except:
                print("error processing pdf_text")
                continue

            layoffs.append(self.process_pdf(pdf_text))
            print()
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
            print(pdf_link)
            return pdf_link

    def process_pdf(self, pdf_text) -> dict:
        company_name = re.search(r"(?:C\n?o\n?m\n?p\n?a\n?n\n?y: )\s+([^\n]+)", pdf_text).group(1)
        number_affected = int(re.search(r"N\n?u\n?m\n?b\n?e\n?r\s+A\s*f\n?f\n?e\n?c\n?t\n?e\n?d:\s*(\d+)", pdf_text).group(1))
        
        return {
            "company_name": company_name.strip(),
            "number_affected": number_affected,
        }
    