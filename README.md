This is a Docker setup for strongDM with errBot! To use it:

1. [Register a new "bot"] (https://api.slack.com/bot-users#installing-bot) in your Slack workspace. This will generate a Slack bot token.
2. Grant the bot permissions to send direct messages to all users, or at least communicate in a given channel, and to your admin user.
1. Clone this repo, or unpack the zip file provided.
2. Edit the DOCKERFILE and add Slack token, SDM API keys, Slack admin user handle, and timeout, optionally.
3. Build the image from the Dockerfile, set image tag.
4. Deploy the container with: `docker run -dit --rm --name grantbot <image tag>`
5. Container should start errbot automagically. If not, use `docker exec` to get in and run `errbot`.
5. There is an error log at `/errbot/errbot.log`.
6. In Slack, invite your bot (e.g. @grantbot) into your test channel.
7. Run !status to make sure you're connected.
8. Run `access to <resource>` to grant access to the calling user.
9. This will send a message to the defined admin user.
10. If the admin replies "yes" within TIMEOUT seconds, user will receive approval message.
11. Otherwise, request times out and both admin and user receive message to that effect.

---

V2:
- Removed command prefix (!)
- Successful grant gives same message 'chatops' used
- Fixed bug with spaces in resource name
- Script now pulls email from Slack user, rather than calculating it from Slack username
(6 Jan 2021)

---

V3:
- Moved most variables into DOCKERFILE.
- Added approval step for all requests.
(19 March 2021)