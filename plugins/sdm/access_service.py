help_message = """
NAME: 
    accessbot - Manages access to strongDM resources via chatbots

COMMANDS:
    access to resource-name       - Grant access to a resource (using the requester's email address)
"""

class AccessService:
    def help(self):
        """
        Returns bot help
        """
        return help_message

service = AccessService()