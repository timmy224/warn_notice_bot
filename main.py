import inspect
import sys

import warn_classes

def handler(event={}, context=None) -> None:
    date = event.get("date")
    state = event.get("state")

    if state:
        module_name = state.lower()
        state = state.upper()
        clsmembers = [(
            f"{state}Warn",
            eval(f"warn_classes.{module_name}.{state}"+"Warn")
        )]
    else:
        clsmembers = inspect.getmembers(
            sys.modules[warn_classes.__name__], 
            inspect.isclass
        )

    for i in range(len(clsmembers)):
        bot_name = clsmembers[i][0]
        print(f'Begin {bot_name} bot')
        warn_bot = clsmembers[i][1](date)
        layoffs = warn_bot.fetch_latest_notices()
        if layoffs:
            msgs = warn_bot.create_messages(layoffs)
            warn_bot.post_to_twitter(msgs)
        print(f'{bot_name} has completed')
        print()

if __name__ == "__main__":
    handler()
