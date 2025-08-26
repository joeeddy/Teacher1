#!/usr/bin/env python3
"""
Teacher1 Functional Test Suite
=============================

This script tests the actual functionality of each module by mocking
dependencies and testing core logic.
"""

import os
import sys
import unittest
import tempfile
import json
from unittest.mock import Mock, patch, MagicMock
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

class TestStudentProfile(unittest.TestCase):
    """Test student profiling functionality"""
    
    def setUp(self):
        """Set up test environment"""
        # Import here to avoid import errors in the main scope
        import student_profile
        self.module = student_profile
    
    def test_student_profile_creation(self):
        """Test creating a student profile"""
        profile_data = {
            'student_id': 'test_001',
            'name': 'Test Student',
            'age': 7,
            'grade': 1
        }
        
        profile = self.module.StudentProfile(profile_data['student_id'])
        profile.update_profile(profile_data)
        
        self.assertEqual(profile.student_id, 'test_001')
        self.assertEqual(profile.profile_data['name'], 'Test Student')
        self.assertEqual(profile.profile_data['age'], 7)
    
    def test_learning_progress_tracking(self):
        """Test learning progress tracking"""
        profile = self.module.StudentProfile('test_002')
        
        # Add some learning activities
        profile.add_learning_activity('math', 'addition', 0.85, 'correct')
        profile.add_learning_activity('reading', 'phonics', 0.90, 'excellent')
        
        progress = profile.get_learning_progress()
        self.assertIn('math', progress)
        self.assertIn('reading', progress)
        self.assertTrue(progress['math']['average_score'] > 0)
    
    def test_profile_persistence(self):
        """Test saving and loading profiles"""
        with tempfile.TemporaryDirectory() as temp_dir:
            profile = self.module.StudentProfile('test_003')
            profile.profile_data = {'name': 'Test Student', 'age': 6}
            
            # Save profile
            save_path = Path(temp_dir) / 'test_profile.json'
            profile.save_profile(str(save_path))
            
            # Load profile
            new_profile = self.module.StudentProfile('test_003')
            new_profile.load_profile(str(save_path))
            
            self.assertEqual(new_profile.profile_data['name'], 'Test Student')
            self.assertEqual(new_profile.profile_data['age'], 6)

class TestKindergartenAssessment(unittest.TestCase):
    """Test kindergarten assessment functionality"""
    
    def setUp(self):
        """Set up test environment"""
        import kindergarten_assessment
        self.module = kindergarten_assessment
    
    def test_assessment_creation(self):
        """Test creating an assessment"""
        assessment = self.module.KindergartenAssessment()
        self.assertIsNotNone(assessment)
        self.assertTrue(hasattr(assessment, 'assessments'))
    
    def test_math_assessment(self):
        """Test math assessment functionality"""
        assessment = self.module.KindergartenAssessment()
        
        # Test number recognition
        result = assessment.assess_number_recognition(5, 5)
        self.assertTrue(result['correct'])
        self.assertEqual(result['score'], 1.0)
        
        # Test counting
        result = assessment.assess_counting([1, 2, 3], 3)
        self.assertTrue(result['correct'])
        self.assertEqual(result['score'], 1.0)
    
    def test_reading_assessment(self):
        """Test reading assessment functionality"""
        assessment = self.module.KindergartenAssessment()
        
        # Test letter recognition
        result = assessment.assess_letter_recognition('A', 'A')
        self.assertTrue(result['correct'])
        self.assertEqual(result['score'], 1.0)
        
        # Test phonics
        result = assessment.assess_phonics('cat', 'cat')
        self.assertTrue(result['correct'])
        self.assertEqual(result['score'], 1.0)
    
    def test_assessment_scoring(self):
        """Test assessment scoring system"""
        assessment = self.module.KindergartenAssessment()
        
        # Add some assessment results
        assessment.add_assessment_result('math', 'addition', True, 0.95)
        assessment.add_assessment_result('math', 'counting', True, 0.88)
        assessment.add_assessment_result('reading', 'letters', False, 0.45)
        
        report = assessment.generate_assessment_report()
        
        self.assertIn('math', report)
        self.assertIn('reading', report)
        self.assertTrue(report['math']['average_score'] > report['reading']['average_score'])

class TestPersonalizedChatbot(unittest.TestCase):
    """Test personalized chatbot functionality"""
    
    def setUp(self):
        """Set up test environment"""
        import personalized_chatbot
        self.module = personalized_chatbot
    
    def test_chatbot_initialization(self):
        """Test chatbot initialization"""
        chatbot = self.module.PersonalizedChatbot('test_student')
        self.assertEqual(chatbot.student_id, 'test_student')
        self.assertIsNotNone(chatbot.conversation_history)
    
    def test_message_processing(self):
        """Test message processing"""
        chatbot = self.module.PersonalizedChatbot('test_student')
        
        # Test basic message processing
        response = chatbot.process_message("Hello")
        self.assertIsInstance(response, str)
        self.assertTrue(len(response) > 0)
        
        # Test educational content detection
        response = chatbot.process_message("I want to learn math")
        self.assertIsInstance(response, str)
        self.assertTrue('math' in response.lower() or 'learn' in response.lower())
    
    def test_personalization(self):
        """Test personalization features"""
        chatbot = self.module.PersonalizedChatbot('test_student')
        
        # Set some preferences
        chatbot.update_student_preferences({
            'favorite_subject': 'math',
            'difficulty_level': 'beginner',
            'learning_style': 'visual'
        })
        
        preferences = chatbot.get_student_preferences()
        self.assertEqual(preferences['favorite_subject'], 'math')
        self.assertEqual(preferences['difficulty_level'], 'beginner')
    
    def test_conversation_history(self):
        """Test conversation history tracking"""
        chatbot = self.module.PersonalizedChatbot('test_student')
        
        # Have a conversation
        chatbot.process_message("Hi")
        chatbot.process_message("I like math")
        chatbot.process_message("What is 2+2?")
        
        history = chatbot.get_conversation_history()
        self.assertTrue(len(history) >= 3)

class TestWebInterfaceConfig(unittest.TestCase):
    """Test web interface configuration"""
    
    def setUp(self):
        """Set up test environment"""
        import web_interface.config
        self.module = web_interface.config
    
    def test_domain_validation(self):
        """Test domain whitelist validation"""
        config = self.module.WebInterfaceConfig()
        
        # Test allowed domains
        self.assertTrue(config.is_domain_allowed('https://en.wikipedia.org/wiki/Science'))
        self.assertTrue(config.is_domain_allowed('https://www.khanacademy.org/math'))
        
        # Test disallowed domains
        self.assertFalse(config.is_domain_allowed('https://malicious-site.com'))
        self.assertFalse(config.is_domain_allowed('http://evil.example.com'))
    
    def test_url_sanitization(self):
        """Test URL sanitization"""
        config = self.module.WebInterfaceConfig()
        
        # Test valid URLs
        clean_url = config.sanitize_url('https://en.wikipedia.org/wiki/Science')
        self.assertTrue(clean_url.startswith('https://'))
        
        # Test invalid URLs
        with self.assertRaises((ValueError, TypeError)):
            config.sanitize_url('javascript:alert("xss")')
    
    def test_security_headers(self):
        """Test security header configuration"""
        config = self.module.WebInterfaceConfig()
        headers = config.get_security_headers()
        
        self.assertIn('Content-Security-Policy', headers)
        self.assertIn('X-Content-Type-Options', headers)
        self.assertIn('X-Frame-Options', headers)

class TestFractalModules(unittest.TestCase):
    """Test fractal modules functionality (without numpy)"""
    
    def setUp(self):
        """Set up test environment with mocked numpy"""
        # Mock numpy to test logic without the dependency
        self.numpy_mock = Mock()
        self.numpy_mock.array = lambda x: x
        self.numpy_mock.zeros = lambda shape: [0] * (shape if isinstance(shape, int) else shape[0])
        self.numpy_mock.random.random = lambda shape=None: 0.5
        self.numpy_mock.exp = lambda x: 2.718 ** x if isinstance(x, (int, float)) else [2.718 ** i for i in x]
        self.numpy_mock.tanh = lambda x: (2.718**(2*x) - 1) / (2.718**(2*x) + 1) if isinstance(x, (int, float)) else [(2.718**(2*i) - 1) / (2.718**(2*i) + 1) for i in x]
        
        with patch.dict('sys.modules', {'numpy': self.numpy_mock}):
            import fractal_modules
            self.module = fractal_modules
    
    def test_leaky_relu_function(self):
        """Test leaky ReLU activation function"""
        with patch.dict('sys.modules', {'numpy': self.numpy_mock}):
            # Test positive value
            result = self.module.param_vector_leaky_relu([1.0], alpha=0.01)
            self.assertTrue(result[0] == 1.0)  # Should pass through unchanged
            
            # Test negative value
            result = self.module.param_vector_leaky_relu([-1.0], alpha=0.01)
            self.assertTrue(result[0] == -0.01)  # Should be scaled by alpha
    
    def test_dynamic_neighborhood(self):
        """Test dynamic neighborhood calculation"""
        with patch.dict('sys.modules', {'numpy': self.numpy_mock}):
            # Test with simple parameters
            neighborhood = self.module.get_dynamic_neighborhood(
                current_state=[0.5, 0.5],
                history_var=0.1,
                state_dim=2
            )
            
            self.assertIsNotNone(neighborhood)
            self.assertTrue(len(neighborhood) == 2)

class TestSpeechAndAudio(unittest.TestCase):
    """Test speech recognition and text-to-speech (mocked)"""
    
    def test_text_to_speech_interface(self):
        """Test text-to-speech interface"""
        # Mock the TTS engine
        with patch('pyttsx3.init') as mock_init:
            mock_engine = Mock()
            mock_init.return_value = mock_engine
            
            import text_to_speech
            
            # Test speaking functionality
            text_to_speech.speak("Hello, this is a test")
            
            # Verify the engine was called
            mock_init.assert_called_once()
    
    def test_speech_recognition_interface(self):
        """Test speech recognition interface"""
        # Mock the speech recognition
        with patch('speech_recognition.Recognizer') as mock_recognizer:
            with patch('speech_recognition.Microphone') as mock_microphone:
                mock_recognizer.return_value.listen = Mock()
                mock_recognizer.return_value.recognize_google = Mock(return_value="test speech")
                
                import speech_recognition as sr_module
                
                # Test basic functionality exists
                self.assertTrue(hasattr(sr_module, 'recognize_speech'))

class TestWebSocketCommunication(unittest.TestCase):
    """Test WebSocket communication logic (mocked)"""
    
    def setUp(self):
        """Set up test environment with mocked websockets"""
        # Mock websockets module
        self.websockets_mock = Mock()
        self.websockets_mock.serve = Mock()
        self.websockets_mock.connect = Mock()
        
        with patch.dict('sys.modules', {'websockets': self.websockets_mock}):
            import websocket_communication
            self.module = websocket_communication
    
    def test_message_creation(self):
        """Test message creation and formatting"""
        with patch.dict('sys.modules', {'websockets': self.websockets_mock}):
            communicator = self.module.WebSocketCommunicator(
                name="test_communicator",
                server_port=8765,
                target_port=8766
            )
            
            message = communicator.create_message("Hello", "question")
            
            self.assertIsInstance(message, dict)
            self.assertEqual(message['content'], "Hello")
            self.assertEqual(message['type'], "question")
            self.assertIn('id', message)
            self.assertIn('timestamp', message)
    
    def test_message_deduplication(self):
        """Test message deduplication logic"""
        with patch.dict('sys.modules', {'websockets': self.websockets_mock}):
            communicator = self.module.WebSocketCommunicator(
                name="test_communicator",
                server_port=8765,
                target_port=8766
            )
            
            # Test duplicate detection
            msg_id = "test_message_001"
            
            # First time should not be duplicate
            self.assertFalse(communicator._is_duplicate_message(msg_id))
            
            # Add to cache
            communicator.message_cache.add(msg_id)
            
            # Second time should be duplicate
            self.assertTrue(communicator._is_duplicate_message(msg_id))
    
    def test_communication_stats(self):
        """Test communication statistics tracking"""
        with patch.dict('sys.modules', {'websockets': self.websockets_mock}):
            communicator = self.module.WebSocketCommunicator(
                name="test_communicator",
                server_port=8765,
                target_port=8766
            )
            
            stats = communicator.get_stats()
            
            self.assertIsInstance(stats, dict)
            self.assertIn('cache_size', stats)
            self.assertIn('conversation_state', stats)

def run_functional_tests():
    """Run all functional tests"""
    print("🧪 Teacher1 Functional Test Suite")
    print("=" * 50)
    
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    test_classes = [
        TestStudentProfile,
        TestKindergartenAssessment,
        TestPersonalizedChatbot,
        TestWebInterfaceConfig,
        TestFractalModules,
        TestSpeechAndAudio,
        TestWebSocketCommunication
    ]
    
    for test_class in test_classes:
        tests = loader.loadTestsFromTestCase(test_class)
        suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 50)
    print("FUNCTIONAL TEST SUMMARY")
    print("=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\nFAILURES ({len(result.failures)}):")
        for test, traceback in result.failures:
            print(f"  ❌ {test}")
    
    if result.errors:
        print(f"\nERRORS ({len(result.errors)}):")
        for test, traceback in result.errors:
            print(f"  💥 {test}")
    
    # Determine overall result
    if len(result.failures) == 0 and len(result.errors) == 0:
        print(f"\n🎉 ALL FUNCTIONAL TESTS PASSED!")
        return True
    else:
        print(f"\n⚠️  Some functional tests failed. See details above.")
        return False

if __name__ == "__main__":
    success = run_functional_tests()
    sys.exit(0 if success else 1)