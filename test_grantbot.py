pytest_plugins = ["errbot.backends.test"]

extra_plugin_dir = 'plugins/sdm'

def test_help_command(testbot):
    testbot.push_message('help')
    assert "access to resource-name" in testbot.pop_message()
