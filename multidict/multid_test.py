import unittest
from multidict import MultiDict


class MultiDTest(unittest.TestCase):
    config = MultiDict(filename='./test.conf')
    data = config.data

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_config_is_dict(self):
        self.assertIsInstance(self.data, dict)

    def test_key_count(self):
        self.assertEqual(2, len(self.data.keys()))

    def test_sub_key_accessible(self):
        self.assertEqual('foo-bar-two', self.data.foo.bar.two)
