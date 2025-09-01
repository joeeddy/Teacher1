#!/usr/bin/env python3
"""
Optional Dependencies Manager for Teacher1 Project

This module provides comprehensive management of optional dependencies,
including fallback mechanisms, installation guidance, and feature detection.
"""

import sys
import subprocess
import importlib
from typing import Dict, List, Tuple, Optional

class OptionalDependencyManager:
    """Manages optional dependencies for enhanced Teacher1 functionality."""
    
    def __init__(self):
        # Optional Dependencies Configuration: Define all optional packages with fallback mechanisms
        # Network-resilient: Each dependency has a clear fallback to ensure functionality
        self.dependency_specs = {
            'pyttsx3': {
                'pip_package': 'pyttsx3>=2.90',
                'description': 'Text-to-speech functionality',
                'category': 'audio',
                'system_deps': ['espeak', 'espeak-data'],
                'fallback': 'Text output only (no audio)',
                'install_cmd': 'pip install pyttsx3',
                'system_cmd': 'sudo apt-get install espeak espeak-data'
            },
            'speech_recognition': {
                'pip_package': 'SpeechRecognition>=3.10.0',
                'description': 'Speech input processing',
                'category': 'audio',
                'system_deps': [],
                'fallback': 'File-based audio processing only',
                'install_cmd': 'pip install SpeechRecognition',
                'system_cmd': None
            },
            'pyaudio': {
                'pip_package': 'pyaudio',
                'description': 'Real-time audio input/output',
                'category': 'audio',
                'system_deps': ['portaudio19-dev', 'python3-dev'],
                'fallback': 'File-based audio processing only',
                'install_cmd': 'pip install pyaudio',
                'system_cmd': 'sudo apt-get install portaudio19-dev python3-dev'
            },
            'transformers': {
                'pip_package': 'transformers>=4.21.0',
                'description': 'HuggingFace AI models for advanced chatbot',
                'category': 'ai',
                'system_deps': [],
                'fallback': 'Basic chatbot without AI model enhancement',
                'install_cmd': 'pip install transformers>=4.21.0',
                'system_cmd': None
            },
            'torch': {
                'pip_package': 'torch>=2.0.0',
                'description': 'PyTorch backend for AI/ML operations',
                'category': 'ai',
                'system_deps': [],
                'fallback': 'CPU-based AI processing only',
                'install_cmd': 'pip install torch>=2.0.0',
                'system_cmd': None
            },
            'espeak': {
                'pip_package': None,  # System package only
                'description': 'Text-to-speech audio output engine',
                'category': 'system',
                'system_deps': ['espeak', 'espeak-data'],
                'fallback': 'Text-only TTS output',
                'install_cmd': None,
                'system_cmd': 'sudo apt-get install espeak espeak-data'
            }
        }
    
    def check_dependency_status(self, dep_name: str) -> Dict:
        """Check if a specific dependency is available.
        
        Network-resilient: Safe checking with timeout and error handling.
        """
        spec = self.dependency_specs.get(dep_name)
        if not spec:
            return {'available': False, 'error': 'Unknown dependency'}
        
        result = {
            'name': dep_name,
            'available': False,
            'version': None,
            'error': None,
            'fallback_available': True,
            'spec': spec
        }
        
        try:
            if dep_name == 'espeak':
                # Network-resilient: Check system command with timeout
                try:
                    cmd_result = subprocess.run(['which', 'espeak'], 
                                              capture_output=True, text=True, timeout=10)
                    result['available'] = cmd_result.returncode == 0
                    if result['available']:
                        # Get espeak version with timeout
                        version_result = subprocess.run(['espeak', '--version'], 
                                                      capture_output=True, text=True, timeout=10)
                        if version_result.returncode == 0:
                            result['version'] = version_result.stdout.strip().split('\n')[0]
                    else:
                        result['error'] = 'espeak not found in system PATH'
                except subprocess.TimeoutExpired:
                    result['error'] = 'espeak check timed out'
                except Exception as e:
                    result['error'] = f'espeak check failed: {str(e)}'
            else:
                # Network-resilient: Check Python module with safe import and known problematic modules
                try:
                    # Special handling for modules known to cause import issues
                    if dep_name in ['transformers', 'torch']:
                        # Network-resilient: Use safer subprocess-based checking for problematic modules
                        import sys
                        check_result = subprocess.run([
                            sys.executable, '-c', f'import {dep_name}; print(getattr({dep_name}, "__version__", "unknown"))'
                        ], capture_output=True, text=True, timeout=15)
                        
                        if check_result.returncode == 0:
                            result['available'] = True
                            result['version'] = check_result.stdout.strip()
                        else:
                            result['error'] = f'Module import failed: {check_result.stderr.strip()}'
                    else:
                        # Standard import for stable modules
                        module = importlib.import_module(dep_name)
                        result['available'] = True
                        result['version'] = getattr(module, '__version__', 'unknown')
                except subprocess.TimeoutExpired:
                    result['error'] = f'{dep_name} import check timed out (likely compatibility issue)'
                except ImportError as e:
                    result['error'] = str(e)
                except Exception as e:
                    # Handle unexpected errors that might cause bus errors
                    result['error'] = f'Module check failed: {str(e)}'
        except Exception as e:
            # Network-resilient: Catch any unexpected errors
            result['error'] = f'Dependency check failed: {str(e)}'
        
        return result
    
    def get_all_dependencies_status(self) -> Dict:
        """Get status of all optional dependencies.
        
        Network-resilient: Safe checking with individual error handling.
        """
        results = {}
        for dep_name in self.dependency_specs.keys():
            try:
                # Network-resilient: Check each dependency individually with error isolation
                results[dep_name] = self.check_dependency_status(dep_name)
            except Exception as e:
                # Network-resilient: Isolate errors to prevent cascading failures
                results[dep_name] = {
                    'name': dep_name,
                    'available': False,
                    'version': None,
                    'error': f'Status check failed: {str(e)}',
                    'fallback_available': True,
                    'spec': self.dependency_specs.get(dep_name, {})
                }
        return results
    
    def get_summary_stats(self) -> Tuple[int, int, float]:
        """Get summary statistics: (working, total, percentage)."""
        status = self.get_all_dependencies_status()
        working = sum(1 for dep in status.values() if dep['available'])
        total = len(status)
        percentage = (working / total) * 100 if total > 0 else 0
        return working, total, percentage
    
    def print_detailed_report(self):
        """Print a comprehensive report of optional dependencies."""
        print("🎯 Optional Dependencies Manager - Detailed Report")
        print("=" * 60)
        
        status = self.get_all_dependencies_status()
        working, total, percentage = self.get_summary_stats()
        
        print(f"\n📊 Summary: {working}/{total} ({percentage:.0f}%) dependencies available")
        
        # Group by category
        categories = {}
        for dep_name, dep_status in status.items():
            category = dep_status['spec']['category']
            if category not in categories:
                categories[category] = []
            categories[category].append((dep_name, dep_status))
        
        for category, deps in categories.items():
            category_working = sum(1 for _, dep in deps if dep['available'])
            category_total = len(deps)
            category_percentage = (category_working / category_total) * 100
            
            print(f"\n🔧 {category.upper()} Dependencies: {category_working}/{category_total} ({category_percentage:.0f}%)")
            
            for dep_name, dep_status in deps:
                status_icon = "✅" if dep_status['available'] else "❌"
                version_str = f" ({dep_status['version']})" if dep_status['version'] else ""
                print(f"  {status_icon} {dep_name}{version_str}")
                print(f"      {dep_status['spec']['description']}")
                
                if not dep_status['available']:
                    print(f"      🔄 Fallback: {dep_status['spec']['fallback']}")
                    if dep_status['spec']['system_cmd']:
                        print(f"      📦 System: {dep_status['spec']['system_cmd']}")
                    if dep_status['spec']['install_cmd']:
                        print(f"      🐍 Python: {dep_status['spec']['install_cmd']}")
    
    def generate_installation_script(self) -> str:
        """Generate a bash script to install missing dependencies."""
        status = self.get_all_dependencies_status()
        script_lines = [
            "#!/bin/bash",
            "# Auto-generated installation script for Teacher1 optional dependencies",
            "echo '🎯 Installing Teacher1 Optional Dependencies'",
            ""
        ]
        
        # System packages first
        system_packages = set()
        for dep_status in status.values():
            if not dep_status['available'] and dep_status['spec']['system_deps']:
                system_packages.update(dep_status['spec']['system_deps'])
        
        if system_packages:
            script_lines.extend([
                "echo '📦 Installing system packages...'",
                f"sudo apt-get update",
                f"sudo apt-get install -y {' '.join(sorted(system_packages))}",
                ""
            ])
        
        # Python packages
        pip_packages = []
        for dep_name, dep_status in status.items():
            if not dep_status['available'] and dep_status['spec']['pip_package']:
                pip_packages.append(dep_status['spec']['pip_package'])
        
        if pip_packages:
            script_lines.extend([
                "echo '🐍 Installing Python packages...'",
                f"pip install {' '.join(pip_packages)}",
                ""
            ])
        
        script_lines.extend([
            "echo '✅ Installation complete!'",
            "echo 'Run python -c \"from optional_dependencies_manager import OptionalDependencyManager; OptionalDependencyManager().print_detailed_report()\" to verify'"
        ])
        
        return '\n'.join(script_lines)


def main():
    """Main function for command-line usage."""
    manager = OptionalDependencyManager()
    
    if len(sys.argv) > 1 and sys.argv[1] == '--generate-script':
        script = manager.generate_installation_script()
        with open('install_optional_dependencies.sh', 'w') as f:
            f.write(script)
        print("✅ Generated install_optional_dependencies.sh")
    else:
        manager.print_detailed_report()
        working, total, percentage = manager.get_summary_stats()
        
        if percentage == 100:
            print(f"\n🎉 Congratulations! All optional dependencies are working ({working}/{total})!")
        elif percentage >= 80:
            print(f"\n🌟 Excellent! Most optional dependencies are working ({working}/{total} - {percentage:.0f}%)")
        elif percentage >= 50:
            print(f"\n🔧 Good progress! Half of optional dependencies are working ({working}/{total} - {percentage:.0f}%)")
        else:
            print(f"\n🚀 Getting started! Some optional dependencies are working ({working}/{total} - {percentage:.0f}%)")
        
        print("\nRun with --generate-script to create an installation script.")


if __name__ == "__main__":
    main()