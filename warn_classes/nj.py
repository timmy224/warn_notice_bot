import re

from typing import Tuple

from .base_warn import Warn

class NJWarn(Warn):
    url = "https://www.nj.gov/labor/assets/PDFs/WARN/2023_WARN_Notice_Archive.pdf"
    state = "NJ"

    def __init__(self, date=None):
        super().__init__(self.url, date)
        self.tags = "#jobs #layoffs #NJ #newjersey"

    def _fetch_latest_notices(self) -> dict:
        layoffs = {}
        try:
            df = self.get_pdf_tables(self._url)[0]
        except:
            print("Error processing pdf text")
            return {}
        
        df = df[df["Effective Date"] == self._compare_date]
        if len(df) == 0:
            return {}

        for _, row in df.iterrows():
            company_name = row["Company"]
            number_affected = row["Workforce Affected"]
            if company_name not in layoffs:
                layoffs[company_name] = 0
            layoffs[company_name] += number_affected

        return layoffs

    def process_pdf(self, pdf_text:str) -> Tuple[str, str]:

        company_pattern = r"(?:C\n?o\n?m\n?p\n?a\n?n\n?y: )\s+([^\n]+)"
        company_name = re.search(company_pattern, pdf_text).group(1)

        number_pattern = r"N\n?u\n?m\n?b\n?e\n?r\s+A\s*f\n?f\n?e\n?c\n?t\n?e\n?d:\s*(\d+)"
        number_affected = int(re.search(number_pattern, pdf_text).group(1))
        
        return company_name.strip(), number_affected
    