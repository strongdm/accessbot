import os
from slack_bolt import App
from modal import modal

app = App(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET")
)

slack_client = None
CHANNEL_ID = os.environ.get('SLACK_CHANNEL_ID')

@app.shortcut("open_access_form")
def open_access_form(ack, shortcut, client):
    global slack_client
    slack_client = client

    ack()

    client.views_open(
        trigger_id=shortcut["trigger_id"],
        view=modal
    )

@app.view("send_command")
def handle_view_events(ack, body, logger):
    global slack_client

    ack()
    command = get_command(body)

    try:
        slack_client.chat_postMessage(channel=CHANNEL_ID, link_names = True, text=command)
    except Exception as e:
        logger.exception(f"Failed to post a message {e}")

def get_command(body):
    values = body['view']['state']['values']
    
    # Required
    resource = values['resource_block']['resource']['value']
    # Optional
    duration = values['duration_block']['duration']['value']
    # Optional
    reason = values['reason_block']['reason']['value']
    # Required
    approver = values['approver_block']['approver']['value']
    username = body['user']['username']

    command = f'access to {resource}'

    if reason is not None:
        command = f'{command} --reason {approver} {reason}'

    if duration is not None:
        command = f'{command} --duration {duration}'

    command = f'{command} --requester @{username}'

    return command

if __name__ == "__main__":
    app.start(port=int(os.environ.get("PORT", 3000)))
