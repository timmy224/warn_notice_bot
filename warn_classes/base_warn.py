from datetime import datetime
import os
from typing import List

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

import pandas as pd
from PyPDF2 import PdfReader
from pytwitter import Api
import pytz
import requests
from tabula import read_pdf
from tempfile import mkdtemp


class Warn:
    REQUEST_TOKEN_URL = "https://api.twitter.com/oauth/request_token?oauth_callback=oob&x_auth_access_type=write"
    MAX_MSG_LEN = 280

    def __init__(self, url:str=None, date:str=None):
        self.driver = None
        self.tags = ""
        self._url = url
        self._compare_date = date if date else self.compare_date()
        self._api = None
        
    def create_messages(self, layoffs: dict) -> str:
        print("Creating messages...")
        msgs = []
        temp_str = ""

        # header
        header = f"{self.state} Posted Date: {self._compare_date}\n"
        temp_str += header

        layoffs = list(layoffs.items())

        # create tweet
        max_iter = len(layoffs) - 1
        for i in range(len(layoffs)):
            company_name, number_affected = layoffs[i]
            msg = f"{company_name}: {number_affected}\n"
            curr_msg_len = len(msg)
            if len(temp_str) + curr_msg_len + len(self.tags) <= self.MAX_MSG_LEN:
                temp_str += msg
            else:
                temp_str += self.tags
                msgs.append(temp_str)
                temp_str = header
                temp_str += msg

            if i == max_iter:
                temp_str += self.tags
                msgs.append(temp_str)

        print("Finished creating messages")
        return msgs
    
    def fetch_latest_notices(self) -> List[dict]: 
        print("Fetching layoff notices...")
        
        self._get_web_driver()

        layoffs = self._fetch_latest_notices()
        print(f"{len(layoffs)} layoffs found")

        self._close_web_driver()

        return layoffs

    def _fetch_latest_notices(self) -> List[dict]:
        raise NotImplementedError
    
    def _get_web_driver(self) -> webdriver:
        if self.driver is None:
            options = Options()
            if os.environ.get('ENV') == "production":
                options.add_argument('--headless')
                options.add_argument('--no-sandbox')
                options.add_argument("--disable-gpu")
                options.add_argument("--window-size=1280x1696")
                options.add_argument("--single-process")
                options.add_argument("--disable-dev-shm-usage")
                options.add_argument("--disable-dev-tools")
                options.add_argument("--no-zygote")
                options.add_argument(f"--user-data-dir={mkdtemp()}")
                options.add_argument(f"--data-path={mkdtemp()}")
                options.add_argument(f"--disk-cache-dir={mkdtemp()}")
                options.add_argument("--remote-debugging-port=9222")
                options.binary_location = '/opt/chrome/chrome'
                self.driver = webdriver.Chrome(
                    "/opt/chromedriver",
                    options=options
                )
            else:
                self.driver = webdriver.Chrome(
                    ChromeDriverManager().install(),
                    options=options
                )
        return self.driver
    
    def _close_web_driver(self) -> None:
        if self.driver:
            self.driver.close()

    def get_pdf_tables(self, pdf_link:str, **kwargs) -> List[pd.DataFrame]:
        dfs = read_pdf(pdf_link, pages="all", **kwargs)
        return dfs

    def get_pdf_text(self, pdf_link:str) -> str:
        print(f'Requesting PDF for {pdf_link}...')
        response = requests.get(pdf_link)

        file_name = '/tmp/temp.pdf'
        with open(file_name, 'wb') as f:
            f.write(response.content)

        reader = PdfReader(file_name)
        page = reader.pages[0]
        text = page.extract_text()
        print(f"Finished extracting text from PDF")
        return text
    
    def create_twitter_client(self) -> Api:
        print("Creating Twitter client...")
        api = Api(
            consumer_key=os.environ.get('consumer_key'),
            consumer_secret=os.environ.get('consumer_secret'),
            access_token=os.environ.get('access_token'),
            access_secret=os.environ.get('access_token_secret')
        )
        print("Created twitter client")
        self._api = api
    
    def post_to_twitter(self, msgs: List[str]) -> None:
        if not msgs:
            return 

        if os.environ.get('ENV') == "production":
            if self._api is None:
                self.create_twitter_client()
        
            for msg in msgs:
                self._api.create_tweet(text=msg)
            print("Posted messages to Twitter")
    
    def compare_date(self) -> str:
        curr_date = datetime.now(pytz.timezone("America/New_York"))
        curr_date = curr_date.strftime("%-m/%-d/%Y")
        print(curr_date)
        return curr_date