from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch, MagicMock
import json
import os


class ChatAPITestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.chat_url = reverse('chat_api')
        
    def test_get_request_returns_error(self):
        """Test that GET requests return an error"""
        response = self.client.get(self.chat_url)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data['error'], 'Invalid request method')
    
    def test_post_without_api_key(self):
        """Test POST request when OpenAI API key is not configured"""
        with patch.dict(os.environ, {}, clear=True):
            response = self.client.post(
                self.chat_url,
                data=json.dumps({'message': 'Hello'}),
                content_type='application/json'
            )
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data['status'], 'error')
            self.assertIn('OpenAI API key not configured', data['response'])
    
    @patch('main.views.OpenAI')
    def test_successful_api_call(self, mock_openai_class):
        """Test successful API call with valid OpenAI API key"""
        # Mock the OpenAI client and response
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        mock_response = MagicMock()
        mock_response.choices = [MagicMock()]
        mock_response.choices[0].message = MagicMock()
        mock_response.choices[0].message.content = "Test response from GPT"
        
        mock_client.chat.completions.create.return_value = mock_response
        
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-api-key'}):
            response = self.client.post(
                self.chat_url,
                data=json.dumps({'message': 'Hello, how are you?'}),
                content_type='application/json'
            )
            
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data['status'], 'success')
            self.assertEqual(data['response'], 'Test response from GPT')
            
            # Verify OpenAI client was called correctly
            mock_openai_class.assert_called_once_with(api_key='test-api-key')
            mock_client.chat.completions.create.assert_called_once()
            
            # Check the arguments passed to the API call
            call_args = mock_client.chat.completions.create.call_args
            self.assertEqual(call_args[1]['model'], 'gpt-3.5-turbo')
            self.assertEqual(call_args[1]['max_tokens'], 500)
            self.assertEqual(len(call_args[1]['messages']), 2)
            self.assertEqual(call_args[1]['messages'][0]['role'], 'system')
            self.assertEqual(call_args[1]['messages'][1]['role'], 'user')
            self.assertEqual(call_args[1]['messages'][1]['content'], 'Hello, how are you?')
    
    @patch('main.views.OpenAI')
    def test_invalid_api_key_error(self, mock_openai_class):
        """Test handling of invalid API key error"""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        # Simulate OpenAI invalid API key error
        mock_client.chat.completions.create.side_effect = Exception("invalid_api_key: Invalid API key")
        
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'invalid-key'}):
            response = self.client.post(
                self.chat_url,
                data=json.dumps({'message': 'Hello'}),
                content_type='application/json'
            )
            
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data['status'], 'error')
            self.assertIn('API key is invalid', data['response'])
    
    @patch('main.views.OpenAI')
    def test_rate_limit_error(self, mock_openai_class):
        """Test handling of rate limit error"""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        # Simulate OpenAI rate limit error
        mock_client.chat.completions.create.side_effect = Exception("rate_limit exceeded")
        
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            response = self.client.post(
                self.chat_url,
                data=json.dumps({'message': 'Hello'}),
                content_type='application/json'
            )
            
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data['status'], 'error')
            self.assertIn('quota exceeded or rate limit hit', data['response'])
    
    @patch('main.views.OpenAI')
    def test_general_exception_fallback(self, mock_openai_class):
        """Test handling of general exceptions with fallback response"""
        mock_client = MagicMock()
        mock_openai_class.return_value = mock_client
        
        # Simulate a general exception
        mock_client.chat.completions.create.side_effect = Exception("Network error")
        
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            with patch('random.choice') as mock_choice:
                mock_choice.return_value = "I'm temporarily unavailable. Please try your question again in a moment."
                
                response = self.client.post(
                    self.chat_url,
                    data=json.dumps({'message': 'Hello'}),
                    content_type='application/json'
                )
                
                self.assertEqual(response.status_code, 200)
                data = response.json()
                self.assertEqual(data['status'], 'fallback')
                self.assertEqual(data['response'], "I'm temporarily unavailable. Please try your question again in a moment.")
    
    def test_invalid_json_request(self):
        """Test handling of invalid JSON in request body"""
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
            response = self.client.post(
                self.chat_url,
                data="invalid json",
                content_type='application/json'
            )
            
            # Should return fallback response due to JSON parsing error
            self.assertEqual(response.status_code, 200)
            data = response.json()
            self.assertEqual(data['status'], 'fallback')
    
    def test_empty_message(self):
        """Test handling of empty message"""
        with patch('main.views.OpenAI') as mock_openai_class:
            mock_client = MagicMock()
            mock_openai_class.return_value = mock_client
            
            mock_response = MagicMock()
            mock_response.choices = [MagicMock()]
            mock_response.choices[0].message = MagicMock()
            mock_response.choices[0].message.content = "How can I help you?"
            
            mock_client.chat.completions.create.return_value = mock_response
            
            with patch.dict(os.environ, {'OPENAI_API_KEY': 'test-key'}):
                response = self.client.post(
                    self.chat_url,
                    data=json.dumps({'message': ''}),
                    content_type='application/json'
                )
                
                self.assertEqual(response.status_code, 200)
                data = response.json()
                self.assertEqual(data['status'], 'success')
                
                # Verify empty string was passed to API
                call_args = mock_client.chat.completions.create.call_args
                self.assertEqual(call_args[1]['messages'][1]['content'], '')


class HomepageViewTestCase(TestCase):
    """Test cases for the homepage view and background elements"""
    
    def setUp(self):
        self.client = Client()
        self.homepage_url = reverse('homepage')
    
    def test_homepage_renders_successfully(self):
        """Test that homepage renders without errors"""
        response = self.client.get(self.homepage_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'GPT Chat Assistant')
    
    def test_background_shapes_included(self):
        """Test that background shapes are included in homepage template - Issue #5"""
        response = self.client.get(self.homepage_url)
        self.assertEqual(response.status_code, 200)
        
        # Verify all 5 background shape divs are present
        for i in range(1, 6):
            self.assertContains(response, f'bg-shape bg-shape-{i}')
        
        # Verify background shapes comment is present
        self.assertContains(response, 'Floating organic shapes for minimalist background')
    
    def test_css_styles_loaded(self):
        """Test that CSS styles are properly loaded"""
        response = self.client.get(self.homepage_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'main/css/style.css')