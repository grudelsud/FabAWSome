import unittest


class TestPlugins(unittest.TestCase):

    def setUp(self):
        pass

    def test_plugin_list(self):
        from fabfile.tasks import plugins, tasks
        print plugins
        print tasks


if __name__ == '__main__':
    unittest.main()
