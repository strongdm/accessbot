help_message = """
NAME: 
    **accessbot** - Manage access to strongDM resources via chat

UTIL COMMANDS:
    **!status** - Show bot health status
    **!whoami** - Show details of your identifier. Useful to debug requester's information

BOT COMMANDS:
    **help** - Show help
    **access to resource-name** - Grant access to a resource (using the requester's email address)
    **show available resources** - Show all available resources
"""

class HelpHelper:
    def execute(self):
        yield help_message
