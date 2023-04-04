from warn_classes import NYWarn

def handler(event, context):
    url = 'https://dol.ny.gov/warn-notices'
    print('Begin bot')
    warn_bot = NYWarn(url)
    print('Fetching warnings')
    layoffs = warn_bot.fetch_latest_notices()
    print(f'{len(layoffs)} layoffs found')
    if layoffs:
        print('Layoffs found')
        msg = warn_bot.create_message(layoffs)
        print('Post to Twitter')
        warn_bot.post_to_twitter(msg)
    print('Completed')

