# Configure Alternative Emails

This configuration is to set up a field in Slack to say the StrongDM Account email of a user that the Slack Account email is not the same of the StrongDM Account.

**_This functionality is only available in pro workspace plan._**

Follow these steps to configure in your Slack Workspace:

1. Go to the top left side dropdown button (with your workspace name), click in `Settings & Administration > Customize <workspace-name>`:

![workspace dropdown button](https://user-images.githubusercontent.com/49597325/134933901-3e032c8c-8e83-426c-84da-46fd045cba52.jpg)


2. Go to the `Profile` tab and click on the `Edit your workspace's profile fields` button:

![custom profile fields tab](https://user-images.githubusercontent.com/49597325/134933956-1632c5e8-44ff-4aba-ba54-2b4502ae20f1.jpg)


3. Click on the `Create a custom field` button:

![custom profile field](https://user-images.githubusercontent.com/49597325/134933991-b50ce39b-1e37-4e8f-b5f1-37620f925cdb.jpg)


4. Select the `Text` option:

![text custom profile field](https://user-images.githubusercontent.com/49597325/134934042-a3853b7f-899a-4a1c-a22b-2e55da92d803.jpg)

5. Put the label of the custom slack field and its hint (we suggest using `StrongDM Email` and `StrongDM's account email` for label and hint, respectively) and click on the `Create` button:

![create custom profile field](https://user-images.githubusercontent.com/49597325/134934088-4c7b29bb-28bb-4af1-a714-f1f21cc60150.jpg)


6. Now, back to your Slack window and, in the top-right profile icon, click and after open, click on `Edit Profile`:

![go to edit profile](https://user-images.githubusercontent.com/49597325/134934145-9bef28ec-d084-4d79-830d-bb764a8b5023.jpg)

7. And when it opens, put your StrongDM Account email in the added profile field:

![set StrongDM account email](https://user-images.githubusercontent.com/49597325/134934179-3f299cb1-9416-4c90-a02a-b052b1bb207a.jpg)

Ps.: It'll not work if the `SDM_EMAIL_SLACK_FIELD` env var wasn't defined.
