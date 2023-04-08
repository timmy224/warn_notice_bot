import inspect
import sys

import warn_classes

def handler(event, context):
    clsmembers = inspect.getmembers(sys.modules[warn_classes.__name__], inspect.isclass)

    for i in range(len(clsmembers)):
        bot_name = clsmembers[i][0]
        print(f'Begin {bot_name} bot')
        warn_bot = clsmembers[i][1]()
        print('Fetching warnings')
        layoffs = warn_bot.fetch_latest_notices()
        print(f'{len(layoffs)} layoffs found')
        if layoffs:
            print('Layoffs found')
            msgs = warn_bot.create_messages(layoffs)
            print('Post to Twitter')
            warn_bot.post_to_twitter(msgs)
        print('Completed')
        print()

if __name__ == "__main__":
    handler(None, None)