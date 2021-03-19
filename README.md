This is a Docker setup for strongDM with errBot! To use it:

1. Clone the repo.
2. Edit config.py and add a valid Slack bot token (replace "REDACTED)", and user account as admin.
2. Edit sdm/grantbot.py and add SDM API key/secret at top of file.
3. Build the image from the Dockerfile, set image tag.
4. Deploy the container with: `docker run -dit --rm --name grantbot <image tag>`
5. Container should start errbot automagically. If not, use `docker exec` to get in and run `errbot`.
5. There is an error log at `/errbot/errbot.log`.
6. In Slack, invite @grantbot into your test channel.
7. Run !status to make sure you're connected.
8. Run `access to <resource>` to grant access to the calling user.

---

V2:
- Removed command prefix (!)
- Successful grant gives same message 'chatops' used
- Fixed bug with spaces in resource name
- Script now pulls email from Slack user, rather than calculating it from Slack username
(6 Jan 2021)