from warn_classes import NYWarn

def handler(event, context):
    date = event.get('date')
    url = 'https://dol.ny.gov/warn-notices'
    print('Begin bot')
    warn_bot = NYWarn(url, date)
    print('Fetching warnings')
    layoffs = warn_bot.fetch_latest_notices()
    print(f'{len(layoffs)} layoffs found')
    if layoffs:
        print('Layoffs found')
        msgs = warn_bot.create_messages(layoffs)
        print('Post to Twitter')
        warn_bot.post_to_twitter(msgs)
    print('Completed')

