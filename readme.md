# Warn Notice Bot

[Twitter: WarnNoticeBot](https://twitter.com/WarnNoticeBot/)

The Warn Notice Layoff Twitter Bot is a Python-based bot that automatically tweets updates about companies that have issued WARN (Worker Adjustment and Retraining Notification) notices. WARN notices are legally required notifications that employers in the United States must provide to employees in the event of mass layoffs or plant closures. 

This Twitter bot utilizes web scraping techniques to gather information from publicly available sources, such as state government websites, to identify companies that have issued WARN notices. It then automatically generates tweets containing relevant details, such as the state, company name, number of employees impacted, and the date of notice.

## States
 1. NY
 2. CA

## Example Tweet

> CA Posted Date: 4/5/2023 
> International Vitamin Corporation IVC: 52 
> Childhelp Inc.: 110 
> Salesforce, Inc.: 86 
> Roku, Inc.: 91 
> Zume, Inc.: 58
> [#warnact](https://twitter.com/hashtag/warnact?src=hashtag_click)  [#layoffs](https://twitter.com/hashtag/layoffs?src=hashtag_click)  [#ca](https://twitter.com/hashtag/ca?src=hashtag_click)  [#california](https://twitter.com/hashtag/california?src=hashtag_click)

## Installation
1. Create virtual environment
 ```console
python -m venv env 
 ```
2. Activate virtual environment
```console
. env/bin/activate 
 ```
 3. Install dependencies
```console
pip install -r requirements.txt 
 ```

## Project Directory
```console
warn_notice_bot
├── Dockerfile
├── __init__.py
├── main.py            # entry
├── readme.md
├── requirements.txt
└── warn_classes       # individual classes
```

## Required credentials
Twitter

 - access_token
 - access_token_secret
 - consumer_key
 - consumer_secret



