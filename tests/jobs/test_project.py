"""Project Unit Test."""
from tests import mock_util, config_resource_path
from config import Config
from knowledge import Project
import unittest
import os


class ProjectTestCase(unittest.TestCase):
    """Project Tests Cases."""

    def setUp(self):
        """Setup API settings for tests."""
        config = Config(config_resource_path, False)
        self.project = Project(config)

        id = "12MK2sfe8qwkyLFi7KWudnAsyYF2kteUCWNk4hX2fB4Y"
        self.doc = mock_util.build_project_jeb(id)
        mock_util.post(
            config.get('KNOWLEDGE_ELASTICSEARCH_HOST'),
            'project',
            'settings',
            self.doc['sheet_id'],
            self.doc
        )

    def test_get_technology_list(self):
        """Project: get technolgy list from sheet_id."""
        tech_list = self.project.get_technology_list(self.doc['sheet_id'])
        self.assertGreater(len(tech_list), 0)
