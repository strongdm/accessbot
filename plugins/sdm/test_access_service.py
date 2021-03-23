from unittest.mock import patch

from access_service import service

def test_answer():
    help_message = service.help()
    assert "access to resource-name" in help_message