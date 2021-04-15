pytest_plugins = ["errbot.backends.test"]
extra_plugin_dir = 'plugins/sdm'

def test_help_command(testbot):
    testbot.push_message("help")
    message = testbot.pop_message()
    assert "access to resource-name" in message
    assert "show available resources" in message
