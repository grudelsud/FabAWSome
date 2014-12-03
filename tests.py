import unittest


class TestPlugins(unittest.TestCase):
  def setUp(self):
    pass

  def test_config_loader(self):
    from fabfile.conf import Configurator
    c = Configurator('sample')

    conf = c.get_conf()
    self.assertEqual(conf['PROJECT_NAME'], 'Test')

    ec2conf = c.get_instance_descriptor('test')
    self.assertEqual(ec2conf['region'], 'eu-west-1')

  def test_plugin_list(self):
    from fabfile.tasks import plugins, tasks
    # print '%s' % tasks['django']['reload']

    self.assertEqual(plugins, ['django', 'instance', 'nginx', 'supervisor', 'wsgi'])
    self.assertEqual(tasks['django'].keys(), ['compile', 'reload'])


if __name__ == '__main__':
  unittest.main()
