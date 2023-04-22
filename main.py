import boto3
import inspect
import os
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

    errors = []
    for i in range(len(clsmembers)):
        bot_name = clsmembers[i][0]
        print(f'Begin {bot_name} bot')
        try:
            warn_bot = clsmembers[i][1](date)
            layoffs = warn_bot.fetch_latest_notices()
            if layoffs:
                msgs = warn_bot.create_messages(layoffs)
                warn_bot.post_to_twitter(msgs)
            print(f'{bot_name} has completed')
            print()
        except:
            errors.append(bot_name)
            
    if errors:
        msg = f"Errors fetching for the following states: {', '.join(errors)}"
        print(msg)
        send_email_alert(msg)

def send_email_alert(message):
    if os.environ.get("ENV") == "production":
        client = boto3.client('sns')
        _response = client.publish (
            TargetArn = os.environ.get('SNS_ARN'),
            Message = message,
            Subject = f"WarnNoticeBot Alert"
        )

if __name__ == "__main__":
    handler()
