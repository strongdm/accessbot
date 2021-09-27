# Configure Alternative Emails

This configuration is to set up a field in Slack to say the StrongDM Account email of a user that the Slack Account email is not the same of the StrongDM Account.

Follow these steps to configure in your Slack Workspace:

1. Go to the top left side dropdown button (with your workspace name), click in `Settings & Administration > Customize <workspace-name>`:

- 

2. Go to the `Profile` tab and click on `Edit your workspace's profile fields` button:

- 

3. Click in the `Create a custom field` button:

- 

4. Select the `Text` option:

- 

5. Put the label of the custom slack field and its hint (we suggest using `StrongDM Email` and `StrongDM's account email` for label and hint, respectively):

- 

6. Now, back to your Slack window and, in the top-right profile icon, click and after open, click in `Edit Profile`:

- 

7. And when it opens, put your StrongDM Account email in the added profile field:

- 

Ps.: It'll not work if the `SDM_EMAIL_SLACK_FIELD` env var wasn't defined.
