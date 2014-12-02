import unittest


class TestPlugins(unittest.TestCase):

    def setUp(self):
        pass

    def test_plugin_list(self):
        from fabfile.tasks import plugins
        print plugins


if __name__ == '__main__':
    unittest.main()
