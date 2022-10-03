# Configure Alternative Emails for MS Teams Platform

If the users of your organization have multiple emails assigned and for some reason AccessBot is not able to find their accounts on strongDM you can add other emails to them on Azure Active Directory. These emails will be used to reach the strongDM account of the user.

In order to make this work, you'll need to register an Azure Active Directory App that AccessBot will use to retrieve the other emails from the users.

## Set Up Azure Active Directory App

1. Go to [Azure Portal](https://portal.azure.com/), click on the top search bar and type "Azure Active Directory", and then click on the resource:

![screenshot-1](https://user-images.githubusercontent.com/49597325/191571354-9f640b74-0110-4209-9084-f1ee36d4bb8b.png)

2. On the left side menu, click on "App registrations":

![screenshot-2](https://user-images.githubusercontent.com/49597325/191572298-d080d20e-02ec-4f17-81b9-c4d3ceb5c272.png)

3. Then click on "New registration":

![screenshot-3](https://user-images.githubusercontent.com/49597325/191572483-535490c6-5e3d-40ee-a4c1-27e9dce9ae97.png)

4. Define the name of the application, select the "Single Tenant" option for supported account types and under the "Redirect URL" select the "Web" option and paste `https://<directoryname>.onmicrosoft.com/MicrosoftGraphClient`, replacing `<directoryname>` with your Azure Directory name. Then click on "Register":

![screenshot-4](https://user-images.githubusercontent.com/49597325/191573066-a2cd2f59-b6f9-447f-9f43-d4cbe525d681.png)

5. After creating the resource, define the following environment variables using the specified values on the screenshot:
- `AZURE_AD_APP_ID` - Application (client) ID
- `AZURE_AD_TENANT_ID` - Active Directory Tenant ID

![screenshot-5](https://user-images.githubusercontent.com/49597325/191574079-b95371c4-be98-4196-a41b-512e5d2ad47e.png)

6. Now, go to "Certificates & secrets", click on the "Client secrets" tab and click on "New client secret":

![screenshot-6](https://user-images.githubusercontent.com/49597325/191575201-64c60ce9-8c1e-4ed6-82b7-0bab26bcc0de.png)

7. Type the description, select the wanted expiry time and then click on "Add":

![screenshot-7](https://user-images.githubusercontent.com/49597325/191576364-186c929b-7650-4d01-a8a0-fc7c2211164e.png)

8. Then, copy the secret and define it in the `AZURE_AD_APP_SECRET` environment variable:

![screenshot-8](https://user-images.githubusercontent.com/49597325/191576549-2ab0a47b-2248-46c2-af6a-29da580f5be2.png)

9. Now click on "API permissions":

![screenshot-9](https://user-images.githubusercontent.com/49597325/191584899-f0bd1d48-b712-42f8-b7ac-a5f0e1f2cd4d.png)

10. Click on "Add a permission":

![screenshot-10](https://user-images.githubusercontent.com/49597325/191585522-889c8b27-ba92-4537-a6fa-af1a2ded58f5.png)

11. On the side modal, click on "Microsoft Graph":

![screenshot-11](https://user-images.githubusercontent.com/49597325/191585682-59fec493-4c33-4464-a8e5-83d6ae685e81.png)

12. Click on "Application permissions", type "User.Read.All" in the search bar, expand the User permissions, click on the permission checkbox and click on "Add permissions":

![screenshot-12](https://user-images.githubusercontent.com/49597325/191585919-91fbf6f5-464b-4612-a26b-8f4501d334a0.png)

13. Then click on "Grant admin consent for &lt;directoryname&gt;" and click on "Yes":

![screenshot-14](https://user-images.githubusercontent.com/49597325/191586392-e607cf05-6ff7-43dc-b9c0-97bcce44bead.png)

That concludes the Azure Active Directory App configuration.

## Configuring Users Alternative Emails

Now, to add alternative emails to regular users, the admin of the Azure Active Directory must follow the next steps: 

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
