help_message = """
NAME: 
    accessbot - Manages access to strongDM resources via chat

COMMANDS:
    access to resource-name       - Grant access to a resource (using the requester's email address)
"""

class HelpHelper:
    def execute(self):
        yield help_message
