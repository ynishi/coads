from unittest import TestCase, mock
from coads.config import configs


class TestConfig(TestCase):

    def test_config(self):
        config = configs['test']
        self.assertEqual(config.USER, 'user1')
