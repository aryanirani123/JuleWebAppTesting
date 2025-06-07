import unittest
from unittest import mock
from google.cloud.firestore import SERVER_TIMESTAMP, Query

# Assuming firestore_service.py is in the parent directory or accessible in PYTHONPATH
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Will be populated in setUpClass after Client is mocked
firestore_service = None
add_feedback = None
get_feedback = None

# Removed class decorator @mock.patch('google.cloud.firestore.Client')
class TestFirestoreService(unittest.TestCase):

    mock_firestore_client_instance = None
    client_patcher = None # To hold the patcher object for start/stop

    @classmethod
    def setUpClass(cls):
        global firestore_service, add_feedback, get_feedback

        # Patch google.cloud.firestore.Client before importing firestore_service
        cls.client_patcher = mock.patch('google.cloud.firestore.Client')
        mock_client_constructor_class = cls.client_patcher.start() # Start the patch

        # mock_client_constructor_class is now the mock constructor for firestore.Client
        # Any call to firestore.Client() will use this mock.

        import firestore_service as fs_module # Import now that Client is mocked
        add_feedback = fs_module.add_feedback
        get_feedback = fs_module.get_feedback

        # fs_module.db should be an instance of the mocked Client
        cls.mock_firestore_client_instance = fs_module.db

        # Verify it's a mock instance
        if not isinstance(cls.mock_firestore_client_instance, mock.MagicMock):
            cls.client_patcher.stop() # Clean up patch
            actual_type = type(cls.mock_firestore_client_instance).__name__
            raise Exception(
                f"firestore_service.db is an instance of '{actual_type}', not a MagicMock as expected. "
                "Patching google.cloud.firestore.Client might have failed or been overridden."
            )

    @classmethod
    def tearDownClass(cls):
        if cls.client_patcher: # Ensure patcher exists before trying to stop
            cls.client_patcher.stop() # Stop the patch

    def setUp(self):
        # The instance fs_module.db (aliased as cls.mock_firestore_client_instance) is already a mock.
        # We just need to reset its state for each test.
        if not isinstance(self.mock_firestore_client_instance, mock.MagicMock):
            # This should not happen if setUpClass was successful
            raise Exception("firestore_service.db is not a mock at setUp. Check setUpClass.")

        self.fs_db_mock = self.mock_firestore_client_instance
        self.fs_db_mock.reset_mock()

        # Configure default behaviors for the mock instance
        self.mock_collection_ref = self.fs_db_mock.collection.return_value

        # Ensure add returns a tuple (timestamp, doc_ref) where doc_ref is a mock
        mock_doc_ref_for_add = mock.MagicMock(id="test_doc_id_from_add")
        self.mock_collection_ref.add.return_value = (None, mock_doc_ref_for_add)

        self.mock_query_instance = self.mock_collection_ref.order_by.return_value
        self.mock_query_instance.stream.return_value = []

    # Test methods no longer receive mock_gcloud_firestore_client_constructor
    def test_add_feedback_success(self):
        # Specific mock setup for this test if different from setUp defaults
        # Example: if add needs to return a specific new ID
        # mock_doc_ref = mock.MagicMock(id="new_id_for_this_test")
        # self.mock_collection_ref.add.return_value = (None, mock_doc_ref)

        add_feedback("Test User", "Great service!")

        self.fs_db_mock.collection.assert_called_once_with('feedback')
        self.mock_collection_ref.add.assert_called_once_with({
            'name': "Test User",
            'message': "Great service!",
            'timestamp': SERVER_TIMESTAMP
        })

    def test_add_feedback_empty_name(self):
        with self.assertRaises(ValueError) as context:
            add_feedback("", "A message")
        self.assertEqual(str(context.exception), "Name and message cannot be empty.")
        self.fs_db_mock.collection.assert_not_called()

    def test_add_feedback_empty_message(self):
        with self.assertRaises(ValueError) as context:
            add_feedback("A User", "")
        self.assertEqual(str(context.exception), "Name and message cannot be empty.")
        self.fs_db_mock.collection.assert_not_called()

    def test_get_feedback_success_multiple_items(self):
        mock_doc_1_data = {'name': 'User One', 'message': 'Msg 1', 'timestamp': '2023-01-01T12:00:00Z'}
        mock_doc_2_data = {'name': 'User Two', 'message': 'Msg 2', 'timestamp': '2023-01-01T13:00:00Z'}

        mock_doc_1 = mock.MagicMock()
        mock_doc_1.id = "doc1"
        mock_doc_1.to_dict.return_value = mock_doc_1_data

        mock_doc_2 = mock.MagicMock()
        mock_doc_2.id = "doc2"
        mock_doc_2.to_dict.return_value = mock_doc_2_data

        mock_stream_results = [mock_doc_1, mock_doc_2]
        self.mock_query_instance.stream.return_value = mock_stream_results

        feedback_list = get_feedback()

        self.fs_db_mock.collection.assert_called_once_with('feedback')
        self.mock_collection_ref.order_by.assert_called_once_with(
            'timestamp', direction=Query.DESCENDING
        )
        self.mock_query_instance.stream.assert_called_once()

        self.assertEqual(len(feedback_list), 2)
        self.assertEqual(feedback_list[0]['name'], 'User One')
        self.assertEqual(feedback_list[0]['id'], 'doc1')
        self.assertEqual(feedback_list[1]['name'], 'User Two')
        self.assertEqual(feedback_list[1]['id'], 'doc2')

    def test_get_feedback_no_items(self):
        self.mock_query_instance.stream.return_value = []

        feedback_list = get_feedback()

        self.fs_db_mock.collection.assert_called_once_with('feedback')
        self.mock_collection_ref.order_by.assert_called_once_with(
            'timestamp', direction=Query.DESCENDING
        )
        self.mock_query_instance.stream.assert_called_once()

        self.assertEqual(len(feedback_list), 0)

if __name__ == '__main__':
    unittest.main()
