"""
Test for gitlab_exporter.py
"""
import os
import unittest
from unittest.mock import Mock, patch

from gitlab_downloader.main import GitlabExporter

headers = {
    "Private-Token": "1234"
}


class TestExportProject(unittest.TestCase):
    """
    Test exporter class
    """
    def setUp(self):
        """
        Setup process
        """
        self.project_name = "test_project"
        self.export_folder = "./gitlab_exports"
        self.gitlab_exporter = GitlabExporter(self.project_name)

        if not os.path.exists(self.export_folder):
            os.makedirs(self.export_folder)

    def tearDown(self):
        """
        Tear Down process
        """
        if os.path.exists(self.export_folder):
            for file in os.listdir(self.export_folder):
                os.remove(os.path.join(self.export_folder, file))
            os.rmdir(self.export_folder)

    @patch('requests.post')
    @patch('requests.get')
    @patch('builtins.open', new_callable=unittest.mock.mock_open)
    def test_export_project_success(self, mock_open, mock_get, mock_post):
        """
        Test export project success
        """
        mock_post.return_value = Mock(status_code=202)

        mock_get.side_effect = [
            Mock(status_code=200,
                 json=lambda: [{"id": 1, "name": "test_project",
                                "path_with_namespace": "namespace/test_project"}]),
            Mock(status_code=200, json=lambda: {"export_status": "queued"}),
            Mock(status_code=200,
                 json=lambda: {"export_status": "finished",
                               "_links": {"api_url": "http://download_url"}}),
            Mock(status_code=200,
                 iter_content=lambda chunk_size: [b'content_chunk1',
                                                  b'content_chunk2', b'content_chunk3'])
        ]

        # Call the function to export the project
        self.gitlab_exporter.export_project_by_name()

        # Construct the expected file path based on actual implementation
        expected_file_path = f"{self.export_folder}/test_project_export.tar.gz"

        # Check if the file was opened for writing
        mock_open.assert_called_once_with(expected_file_path, 'wb')

        # Check that data was written
        handle = mock_open()
        self.assertTrue(handle.write.called, "No data was written to the file.")

        # Ensure correct API calls were made
        mock_post.assert_called_once()
        self.assertEqual(mock_get.call_count, 4)


if __name__ == '__main__':
    unittest.main()
