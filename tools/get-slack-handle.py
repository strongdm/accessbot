import os
import sys
import argparse

from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

# $ python tools/get-slack-handle.py -e rodolfo@strongdm.com
# The nick for that user is: @rodolfo
# $ python tools/get-slack-handle.py -d "Rodolfo Campos"
# The nick for that user is: @rodolfo

slack_token = os.environ["SLACK_BOT_TOKEN"]
client = WebClient(token=slack_token)
USERS_PAGE_LIMIT = 500

def get_user_by_email(email):
    user = client.users_lookupByEmail(email=email)["user"]
    return user

def get_user_by_name(name):
    def get_users(**kwargs):
        response = client.users_list(**kwargs)
        members = response['members']
        next_cursor = response['response_metadata']['next_cursor']
        return members, next_cursor

    def find_user_by_name_fields(data, value):
        for item in data:
            if item.get("display_name") == value or item.get("real_name") == value:
                return item

    next_cursor = None
    user = None
    while not user:
        members, next_cursor = get_users(limit = USERS_PAGE_LIMIT, cursor = next_cursor)
        user = find_user_by_name_fields(members, name)
        if not next_cursor:
            break
    return  user

def print_slack_handle(user):
    if user is None:
        print("User not found.")
    else:
        name = user["name"]
        print(f"The nick for that user is: @{name}")   

def main(arguments):

    parser = argparse.ArgumentParser(
        epilog="""Example:\n python get-slack-handle.py <email@gmail.com> 
        The script will get the slack handle by user's email passed as argument.""",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument("-e", "--email", help="A valid email.")
    parser.add_argument("-d","--display_name", help="A valid display name.")
    args = parser.parse_args(arguments)
    
    if not (args.email or args.display_name):
        parser.error('Please, provide an email or display name. Use -h for help.')

    try:
        user = None
        if args.email:
            user = get_user_by_email(args.email)
        elif args.display_name:
            user = get_user_by_name(args.display_name)
        print_slack_handle(user)
    except SlackApiError as e:
        print("Slack API error {}".format(e))
    except Exception as e:
        print("Error {}".format(e))


if __name__ == "__main__":
    main(sys.argv[1:])