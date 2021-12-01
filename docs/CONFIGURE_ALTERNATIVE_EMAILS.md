# Configure Alternative Emails

You can make access requests using alternative emails. This functionality is specially helpful when you need to make access requests using a different email address than the one you have configured in your Slack Profile. 

**_Custom profile fields are only available for Slack Business+ workspaces and Bolt API_**

Follow these steps to configure in your Slack Workspace:

1. Go to the top left hand side dropdown button (with your workspace name) and select `Settings & Administration > Customize <workspace-name>`:

![workspace dropdown button](https://user-images.githubusercontent.com/49597325/134933901-3e032c8c-8e83-426c-84da-46fd045cba52.jpg)


2. Go to the `Profile` tab and select `Edit your workspace's profile fields`:

![custom profile fields tab](https://user-images.githubusercontent.com/49597325/134933956-1632c5e8-44ff-4aba-ba54-2b4502ae20f1.jpg)


3. Click on the `Create a custom field` button:

![custom profile field](https://user-images.githubusercontent.com/49597325/134933991-b50ce39b-1e37-4e8f-b5f1-37620f925cdb.jpg)


4. Select the `Text` option:

![text custom profile field](https://user-images.githubusercontent.com/49597325/134934042-a3853b7f-899a-4a1c-a22b-2e55da92d803.jpg)


5. Enter the label of the custom slack field and its hint (we suggest using `StrongDM Email` and `StrongDM's account email` for label and hint, respectively) and click `Create`:

![create custom profile field](https://user-images.githubusercontent.com/49597325/134934088-4c7b29bb-28bb-4af1-a714-f1f21cc60150.jpg)


6. Go back to your Slack window and `Edit Profile`:

![go to edit profile](https://user-images.githubusercontent.com/49597325/134934145-9bef28ec-d084-4d79-830d-bb764a8b5023.jpg)


7. Enter your StrongDM Account email in the added profile field:

![set StrongDM account email](https://user-images.githubusercontent.com/49597325/134934179-3f299cb1-9416-4c90-a02a-b052b1bb207a.jpg)

IMPORTANT: Remember to setup the field name (e.g. `StrongDM Email`) in the environment variable `SDM_EMAIL_SLACK_FIELD`
