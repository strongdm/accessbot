# Configure Alternative Emails for MS Teams Platform

If the users of your organization have multiple emails assigned and for some reason AccessBot is not able to find their accounts on strongDM you can add other emails to them on Azure Active Directory. These emails will be used to reach the strongDM account of the user.

In order to make this work, you'll need to register an Azure Active Directory App that AccessBot will use to retrieve the other emails from the users. Please, refer to the docs that will teach you [how to configure an Active Directory app](CONFIGURE_AZURE_ACTIVE_DIRECTORY.md).

## Configuring Users Alternative Emails

After configuring the Azure Active Directory app, the admin of the Azure Active Directory must follow the next steps to add alternative emails to regular users: 

1. Go to Azure Active Directory page and click on "Users":

![screenshot-9](https://user-images.githubusercontent.com/49597325/191577812-d26be998-a417-4773-a69a-acfef6a66971.png)

2. Find and click on a user:

![screenshot-10](https://user-images.githubusercontent.com/49597325/191578258-2c5bb5d8-214c-4f37-b0e9-652b9edd82d7.png)

3. Click on "Edit properties":

![screenshot-11](https://user-images.githubusercontent.com/49597325/191578511-8a8b798e-7919-4194-8ac7-89a23c3a32c0.png)

4. Click on the "Contact information" tab and click on "Add email"

![screenshot-12](https://user-images.githubusercontent.com/49597325/191581070-97628af9-a03c-4249-a2ed-1d4040345b2f.png)

5. Click on "Add", type the user's strongDM account email (registered on the strongDM organization) and click on "Save":

![screenshot-13](https://user-images.githubusercontent.com/49597325/191581401-3d3f038a-12e9-4c24-b340-bdb796bd7ce0.png)

6. Then click on "Save" again:

![screenshot-14](https://user-images.githubusercontent.com/49597325/191581673-2e73c3bb-b343-4615-8fb4-42944a374e3e.png)

That's it! Now the account other emails will be used to reach the strongDM account.
