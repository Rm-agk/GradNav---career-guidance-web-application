from django.test import TestCase
from django.urls import reverse
from django.test import TestCase, Client
from unittest.mock import patch
import json

class ChatWithGPTTests(TestCase):
    def setUp(self):
        # Set up a client to use in tests
        self.client = Client()

    def test_post_request_with_message(self):
        # Test the view with a valid POST request
        with patch('requests.post') as mock_post:
            mock_post.return_value.status_code = 200
            mock_post.return_value.json.return_value = {
                'choices': [{'message': {'content': 'Hello, how can I help you?'}}]
            }
            
            response = self.client.post(reverse('chat_with_gpt'), {'message': 'Hello'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {'response': 'Hello, how can I help you?'})
    

    def test_get_request_rejected(self):
        # Ensure that GET requests are rejected
        response = self.client.get(reverse('chat_with_gpt'))
        self.assertNotEqual(response.status_code, 200)

    def test_api_failure_handling(self):
        # Test the API failure scenario
        with patch('requests.post') as mock_post:
            mock_post.return_value.status_code = 400
            mock_post.return_value.json.return_value = {}
            
            response = self.client.post(reverse('chat_with_gpt'), {'message': 'Test'})
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json(), {'response': 'Failed to get response from OpenAI API'})

    def test_exception_handling(self):
        # Test exception handling in the view
        with patch('requests.post') as mock_post:
            mock_post.side_effect = Exception("Some error")
            
            response = self.client.post(reverse('chat_with_gpt'), {'message': 'Test'})
            self.assertEqual(response.status_code, 200)
            self.assertTrue('An error occurred' in response.json()['response'])



