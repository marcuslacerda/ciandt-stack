"""Stack Unit Test."""
from config import Config
from stack import Stack
import unittest
import os
import mock_util

class StackTestCase(unittest.TestCase):
    """Stack Test Case."""

    def setUp(self):
        """Setup API settings for tests."""
        resource_path = os.path.join(
            os.path.split(__file__)[0], "resources/config.yaml")
        config = Config(resource_path)
        self.stack = Stack(config)

        id = 'kdkdkdkdkd-2012'
        self.mock_project = mock_util.build_project_jeb(id)
        mock_util.post(
            config.get('KNOWLEDGE_ELASTICSEARCH_HOST'),
            'project',
            'settings',
            self.mock_project['sheet_id'],
            self.mock_project
        )

    def tearDown(self):
        """Destroy settings created for tests."""
        # doc = build_marcus_doc()
        # self.profile.delete(doc['login'])

    def test_has_save_new_stack(self):
        """Stack: save new stack."""
        new_stack = {
            "key": 'kdkdkdkdkd-2012',
            "owner": 'VALE',
            "name": 'Stack-Test',
            "index": 0.92
        }
        saved_stack = self.stack.load_stack(new_stack)

        team_size = len(self.mock_project['team'])
        stack_size = len(self.mock_project['stack'])

        self.assertEquals(saved_stack['key'], new_stack['key'])
        self.assertGreaterEqual(len(saved_stack['stack']), stack_size)
        self.assertEquals(len(saved_stack['team']), team_size)
