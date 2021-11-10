# Configure MS Teams

- Create the App in Azure Portal
- Using Azure Studio generate App Zip - Enter bot id!!!
- Add the app in https://admin.teams.microsoft.com/
- Add it to your teams org

## Limitations

Due to some MS Teams current limitations, the following features are not supported:

- Admins channel: it is not possible to add an application inside a private channel. Because of that, the bot
will communicate with all the administrators via direct messages.
- Request access commands via direct messages (DM): it is not possible to send messages to the admins when the bot
receives a message via DM, therefore all the commands that request access are disabled via DM.
