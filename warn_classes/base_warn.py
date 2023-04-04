from datetime import datetime, timedelta
import os
from typing import List

from PyPDF2 import PdfReader
from pytwitter import Api
import requests
import pytz

class Warn:
    REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"

    def __init__(self, url):
        self._url = url
        self._compare_date = self.compare_date()
        self.tags = ""
        self._api = None
        
    def create_message(self, layoffs: List[dict]) -> str:
        msg = f"Posted Date: {self._compare_date}\n"
        for layoff in layoffs:
            msg += f"{layoff['company_name']}: {layoff['number_affected']}\n"
        msg += self.tags
        return msg
    
    def fetch_latest_notices(self) -> List[dict]: 
        raise NotImplementedError
    
    def get_pdf_text(self, pdf_link) -> str:
        print('requesting pdf')
        response = requests.get(pdf_link)

        print('writing pdf')
        file_name = '/tmp/temp.pdf'
        with open(file_name, 'wb') as f:
            f.write(response.content)

        print('reading pdf')
        reader = PdfReader(file_name)
        page = reader.pages[0]
        print('extracting text')
        text = page.extract_text()
        return text
    
    def create_twitter_client(self) -> Api:
        print("Creating Twitter client")
        api = Api(
            consumer_key=os.environ.get('consumer_key'),
            consumer_secret=os.environ.get('consumer_secret'),
            access_token=os.environ.get('access_token'),
            access_secret=os.environ.get('access_token_secret')
        )
        print("Created twitter client")
        self._api = api
    
    def post_to_twitter(self, msg) -> None:
        if self._api is None:
            self.create_twitter_client()
        self._api.create_tweet(text=msg)
    
    def compare_date(self) -> str:
        curr_date = datetime.now(pytz.timezone("America/New_York"))
        curr_date = curr_date.strftime("%-m/%-d/%Y")
        print(f"current date: {curr_date}")
        return curr_date