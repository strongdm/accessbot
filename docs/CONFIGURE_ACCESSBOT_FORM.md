# Configure AccessBot Form

## Set Environment Variable

To request access to a StrongDM resource through AccessBot using a form set the environment variable `SDM_ACCESS_FORM_BOT_NICKNAME` in your `env-file`.

To know the value you should put in the environment variable, run the following command in the terminal (in the project root):

```
python3 tools/get-slack-handle.py -d "AccessBot Form" 
```
After running this command, you should be able to see something like this in the terminal:

```
The nick for that user is: @wb_bot_a03muafcvm1
```

After that, use this nickname to set the environment variable mentioned above.

## Usage Example

The following gif shows an example of how to use the AccessBot form to request a resource from StrongDM.

![accessbot-form](https://user-images.githubusercontent.com/82273420/163173633-243771d8-a31c-4f79-aaf6-102eb4265286.gif)
