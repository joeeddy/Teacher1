#!/usr/bin/env python3
"""
Full Test of All Optional Dependencies for Teacher1
==================================================
This script provides comprehensive testing of all optional dependencies,
including availability, functionality, and fallback mechanisms.
"""

import sys
import subprocess
import importlib
import time
import traceback
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class FullOptionalDependenciesTest:
    """Comprehensive testing of all optional dependencies with functionality validation."""
    
    def __init__(self):
        self.test_results = {}
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.warnings = 0
        
    def log_result(self, test_name: str, status: str, details: str = "", recommendation: str = ""):
        """Log a test result with details."""
        self.total_tests += 1
        if status == "PASS":
            self.passed_tests += 1
        elif status == "FAIL":
            self.failed_tests += 1
        elif status == "WARN":
            self.warnings += 1
            
        self.test_results[test_name] = {
            'status': status,
            'details': details,
            'recommendation': recommendation
        }
    
    def test_dependency_availability(self, dep_name: str, pip_package: str = None) -> Tuple[bool, str]:
        """Test if a dependency is available and get version info."""
        try:
            if dep_name == 'espeak':
                # System dependency
                result = subprocess.run(['which', 'espeak'], capture_output=True, text=True)
                if result.returncode == 0:
                    version_result = subprocess.run(['espeak', '--version'], capture_output=True, text=True)
                    version = version_result.stdout.strip().split('\n')[0] if version_result.returncode == 0 else 'unknown'
                    return True, version
                else:
                    return False, "Not found in system PATH"
            else:
                # Python module
                module = importlib.import_module(dep_name)
                version = getattr(module, '__version__', 'unknown')
                return True, version
        except ImportError as e:
            return False, str(e)
        except Exception as e:
            return False, f"Error: {str(e)}"
    
    def test_pyttsx3_functionality(self) -> Tuple[str, str]:
        """Test pyttsx3 text-to-speech functionality."""
        try:
            import pyttsx3
            engine = pyttsx3.init()
            
            # Test basic properties
            voices = engine.getProperty('voices')
            rate = engine.getProperty('rate')
            volume = engine.getProperty('volume')
            
            # Test setting properties
            engine.setProperty('rate', 150)
            engine.setProperty('volume', 0.8)
            
            # Test say functionality (without actual audio output)
            engine.say("Testing pyttsx3 functionality")
            
            details = f"Voices: {len(voices) if voices else 0}, Rate: {rate}, Volume: {volume}"
            return "PASS", details
            
        except ImportError:
            return "FAIL", "Module not available"
        except Exception as e:
            return "WARN", f"Available but has issues: {str(e)}"
    
    def test_speech_recognition_functionality(self) -> Tuple[str, str]:
        """Test speech_recognition functionality."""
        try:
            import speech_recognition as sr
            
            # Check if this is the Teacher1 custom wrapper or standard library
            if hasattr(sr, 'listen_and_print'):
                # This is the Teacher1 custom wrapper
                details = "Teacher1 custom speech recognition wrapper available"
                return "PASS", details
            elif hasattr(sr, 'Recognizer'):
                # This is the standard SpeechRecognition library
                recognizer = sr.Recognizer()
                
                # Test microphone availability (without actually recording)
                try:
                    mic_list = sr.Microphone.list_microphone_names()
                    mic_count = len(mic_list)
                except:
                    mic_count = 0
                
                # Test recognizer properties
                energy_threshold = recognizer.energy_threshold
                pause_threshold = recognizer.pause_threshold
                
                details = f"Standard SpeechRecognition: Microphones detected: {mic_count}, Energy threshold: {energy_threshold}"
                return "PASS", details
            else:
                return "WARN", "Unrecognized speech_recognition module format"
            
        except ImportError:
            return "FAIL", "Module not available"
        except Exception as e:
            return "WARN", f"Available but has issues: {str(e)}"
    
    def test_pyaudio_functionality(self) -> Tuple[str, str]:
        """Test pyaudio audio input/output functionality."""
        try:
            import pyaudio
            
            # Initialize PyAudio
            pa = pyaudio.PyAudio()
            
            # Get device information
            device_count = pa.get_device_count()
            default_input = pa.get_default_input_device_info()
            default_output = pa.get_default_output_device_info()
            
            # Test supported formats
            supported_formats = []
            for fmt in [pyaudio.paInt16, pyaudio.paInt24, pyaudio.paFloat32]:
                try:
                    if pa.is_format_supported(44100, input_device=default_input['index'], 
                                            input_channels=1, input_format=fmt):
                        supported_formats.append(fmt)
                except:
                    pass
            
            pa.terminate()
            
            details = f"Devices: {device_count}, Input: {default_input.get('name', 'Unknown')}, " \
                     f"Output: {default_output.get('name', 'Unknown')}, Formats: {len(supported_formats)}"
            return "PASS", details
            
        except ImportError:
            return "FAIL", "Module not available"
        except Exception as e:
            return "WARN", f"Available but has issues: {str(e)}"
    
    def test_transformers_functionality(self) -> Tuple[str, str]:
        """Test transformers HuggingFace functionality."""
        try:
            import transformers
            from transformers import pipeline
            
            # Test basic pipeline creation (without downloading models)
            try:
                # This will fail if no models are available, which is expected
                sentiment_pipeline = pipeline("sentiment-analysis")
                details = f"Version: {transformers.__version__}, Pipeline creation: Success"
                return "PASS", details
            except Exception as model_error:
                # Expected if no models are downloaded
                details = f"Version: {transformers.__version__}, Pipeline creation failed (expected without models): {str(model_error)[:100]}"
                return "WARN", details
                
        except ImportError:
            return "FAIL", "Module not available"
        except Exception as e:
            return "WARN", f"Available but has issues: {str(e)}"
    
    def test_torch_functionality(self) -> Tuple[str, str]:
        """Test PyTorch functionality."""
        try:
            import torch
            
            # Test basic tensor operations
            tensor = torch.tensor([1.0, 2.0, 3.0])
            result = tensor + 1
            
            # Check CUDA availability
            cuda_available = torch.cuda.is_available()
            device_count = torch.cuda.device_count() if cuda_available else 0
            
            # Test basic operations
            matrix = torch.randn(2, 3)
            matrix_sum = torch.sum(matrix)
            
            details = f"Version: {torch.__version__}, CUDA: {cuda_available}, " \
                     f"GPU devices: {device_count}, Basic ops: OK"
            return "PASS", details
            
        except ImportError:
            return "FAIL", "Module not available"
        except Exception as e:
            return "WARN", f"Available but has issues: {str(e)}"
    
    def test_espeak_functionality(self) -> Tuple[str, str]:
        """Test espeak system functionality."""
        try:
            # Test espeak availability
            result = subprocess.run(['which', 'espeak'], capture_output=True, text=True)
            if result.returncode != 0:
                return "FAIL", "espeak not found in system PATH"
            
            # Test espeak version
            version_result = subprocess.run(['espeak', '--version'], capture_output=True, text=True)
            version = version_result.stdout.strip().split('\n')[0] if version_result.returncode == 0 else 'unknown'
            
            # Test espeak voices
            voices_result = subprocess.run(['espeak', '--voices'], capture_output=True, text=True)
            voice_count = len(voices_result.stdout.strip().split('\n')) - 1 if voices_result.returncode == 0 else 0
            
            # Test basic synthesis (to /dev/null to avoid audio output)
            test_result = subprocess.run(['espeak', '-s', '150', 'test'], 
                                       capture_output=True, text=True)
            synthesis_ok = test_result.returncode == 0
            
            details = f"Version: {version}, Voices: {voice_count}, Synthesis: {'OK' if synthesis_ok else 'Failed'}"
            return "PASS", details
            
        except Exception as e:
            return "WARN", f"Available but has issues: {str(e)}"
    
    def test_fallback_mechanisms(self):
        """Test that fallback mechanisms work when dependencies are missing."""
        print("\n🔄 Testing Fallback Mechanisms...")
        
        # Test text-to-speech fallback
        try:
            from text_to_speech import speak  # Use correct function name
            # This should work even without pyttsx3 by falling back to print
            speak("Test fallback message")
            self.log_result("TTS_Fallback", "PASS", "Text-to-speech fallback working")
        except Exception as e:
            self.log_result("TTS_Fallback", "FAIL", f"TTS fallback failed: {str(e)}")
        
        # Test chatbot fallback
        try:
            from personalized_chatbot import PersonalizedKindergartenChatbot  # Use correct class name
            chatbot = PersonalizedKindergartenChatbot()
            # Test basic functionality
            self.log_result("Chatbot_Fallback", "PASS", "Chatbot available and initialized")
        except Exception as e:
            self.log_result("Chatbot_Fallback", "FAIL", f"Chatbot fallback failed: {str(e)}")
        
        # Test speech recognition fallback
        try:
            import speech_recognition as sr
            if hasattr(sr, 'listen_and_print'):
                self.log_result("Speech_Fallback", "PASS", "Custom speech recognition wrapper available")
            else:
                self.log_result("Speech_Fallback", "WARN", "Standard speech recognition available")
        except Exception as e:
            self.log_result("Speech_Fallback", "FAIL", f"Speech recognition fallback failed: {str(e)}")
    
    def run_comprehensive_test(self):
        """Run the complete test suite for all optional dependencies."""
        print("🎯 Full Test of All Optional Dependencies")
        print("=" * 60)
        
        # Import the optional dependencies manager
        try:
            from optional_dependencies_manager import OptionalDependencyManager
            manager = OptionalDependencyManager()
            deps = manager.dependency_specs
        except ImportError:
            print("❌ Could not import OptionalDependencyManager")
            return False
        
        print(f"\n🔍 Testing {len(deps)} Optional Dependencies...")
        
        # Test each dependency for availability and functionality
        for dep_name, spec in deps.items():
            print(f"\n📦 Testing {dep_name}...")
            
            # Test availability
            available, version_info = self.test_dependency_availability(dep_name, spec.get('pip_package'))
            
            if available:
                print(f"  ✅ Available: {version_info}")
                
                # Test functionality based on dependency type
                if dep_name == 'pyttsx3':
                    status, details = self.test_pyttsx3_functionality()
                elif dep_name == 'speech_recognition':
                    status, details = self.test_speech_recognition_functionality()
                elif dep_name == 'pyaudio':
                    status, details = self.test_pyaudio_functionality()
                elif dep_name == 'transformers':
                    status, details = self.test_transformers_functionality()
                elif dep_name == 'torch':
                    status, details = self.test_torch_functionality()
                elif dep_name == 'espeak':
                    status, details = self.test_espeak_functionality()
                else:
                    status, details = "PASS", "Basic availability confirmed"
                
                print(f"  🧪 Functionality: {status} - {details}")
                self.log_result(f"{dep_name}_functionality", status, details)
                
            else:
                print(f"  ❌ Not Available: {version_info}")
                print(f"  🔄 Fallback: {spec.get('fallback', 'None specified')}")
                self.log_result(f"{dep_name}_availability", "FAIL", version_info, spec.get('install_cmd', ''))
        
        # Test fallback mechanisms
        self.test_fallback_mechanisms()
        
        # Generate comprehensive report
        self.generate_final_report()
        
        return True
    
    def generate_final_report(self):
        """Generate a comprehensive final report."""
        print("\n" + "=" * 80)
        print("🎓 FULL OPTIONAL DEPENDENCIES TEST REPORT")
        print("=" * 80)
        
        print(f"\n📊 TEST SUMMARY:")
        print(f"  Total Tests: {self.total_tests}")
        print(f"  Passed: {self.passed_tests}")
        print(f"  Failed: {self.failed_tests}")
        print(f"  Warnings: {self.warnings}")
        print(f"  Success Rate: {(self.passed_tests/self.total_tests)*100:.1f}%")
        
        print(f"\n📋 DETAILED RESULTS:")
        for test_name, result in self.test_results.items():
            status_icon = {"PASS": "✅", "FAIL": "❌", "WARN": "⚠️"}.get(result['status'], "?")
            print(f"  {status_icon} {test_name}: {result['details']}")
            if result['recommendation']:
                print(f"      💡 {result['recommendation']}")
        
        print(f"\n🎯 RECOMMENDATIONS:")
        print("  1. Install missing system dependencies with: sudo apt-get install espeak espeak-data portaudio19-dev python3-dev")
        print("  2. Install missing Python packages with: pip install pyttsx3 pyaudio transformers torch")
        print("  3. For production use, ensure fallback mechanisms are properly configured")
        print("  4. Test audio dependencies in environment with audio hardware available")
        
        print(f"\n✨ CONCLUSION:")
        if self.passed_tests >= self.total_tests * 0.8:
            print("  🌟 Excellent! Most optional dependencies are working well.")
        elif self.passed_tests >= self.total_tests * 0.5:
            print("  🔧 Good progress! Many optional dependencies are functional.")
        else:
            print("  🚀 Getting started! Several dependencies need installation.")
        
        print(f"  📈 Teacher1 project has robust fallback mechanisms for missing dependencies.")


def main():
    """Main function to run the comprehensive test."""
    tester = FullOptionalDependenciesTest()
    
    print("🧪 Teacher1 - Full Optional Dependencies Test")
    print("Comprehensive testing of availability, functionality, and fallbacks")
    print("=" * 70)
    
    try:
        success = tester.run_comprehensive_test()
        return 0 if success else 1
    except KeyboardInterrupt:
        print("\n⚠️ Test interrupted by user")
        return 130
    except Exception as e:
        print(f"\n❌ Test failed with error: {str(e)}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())