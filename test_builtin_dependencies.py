#!/usr/bin/env python3
"""
Test Built-in Dependencies for Teacher1
---------------------------------------
This script specifically tests for Python built-in modules that should be available
but might be missing due to minimal Python installations or system package issues.

Built-in dependencies are different from external dependencies listed in requirements.txt
because they should come with Python but sometimes require separate system packages.
"""

import sys
import importlib
from typing import Dict, List, Tuple


class BuiltinDependencyTester:
    """Test for missing built-in Python dependencies"""
    
    def __init__(self):
        # Built-in modules that Teacher1 requires
        self.builtin_dependencies = {
            'tkinter': {
                'description': 'GUI framework for big_text_gui.py',
                'system_package': 'python3-tk',
                'required_for': ['big_text_gui.py', 'GUI applications'],
                'is_critical': True
            },
            'sqlite3': {
                'description': 'Database support (potential future use)',
                'system_package': 'python3-sqlite3 (usually included)',
                'required_for': ['Database operations'],
                'is_critical': False
            },
            'uuid': {
                'description': 'UUID generation for websocket communication',
                'system_package': 'Built-in (should always be available)',
                'required_for': ['websocket_communication.py', 'student_profile.py'],
                'is_critical': True
            },
            'json': {
                'description': 'JSON handling for configuration and API',
                'system_package': 'Built-in (should always be available)',
                'required_for': ['Multiple modules'],
                'is_critical': True
            },
            'asyncio': {
                'description': 'Async operations for WebSocket communication',
                'system_package': 'Built-in (should always be available)',
                'required_for': ['websocket_communication.py', 'fractal_emergent_ai.py'],
                'is_critical': True
            },
            'threading': {
                'description': 'Thread support for concurrent operations',
                'system_package': 'Built-in (should always be available)',
                'required_for': ['fractal_emergent_ai.py', 'websocket_demo.py'],
                'is_critical': True
            },
            'urllib.parse': {
                'description': 'URL parsing for web interface',
                'system_package': 'Built-in (should always be available)',
                'required_for': ['web_interface/app.py'],
                'is_critical': True
            }
        }
    
    def test_builtin_dependency(self, module_name: str) -> Tuple[bool, str]:
        """Test if a built-in module can be imported"""
        try:
            importlib.import_module(module_name)
            return True, "Available"
        except ImportError as e:
            return False, str(e)
    
    def test_all_builtin_dependencies(self) -> Dict[str, Dict]:
        """Test all built-in dependencies and return detailed results"""
        results = {}
        
        for module_name, info in self.builtin_dependencies.items():
            available, error_msg = self.test_builtin_dependency(module_name)
            
            results[module_name] = {
                'available': available,
                'error': error_msg if not available else None,
                'description': info['description'],
                'system_package': info['system_package'],
                'required_for': info['required_for'],
                'is_critical': info['is_critical']
            }
        
        return results
    
    def get_missing_critical_dependencies(self, results: Dict[str, Dict]) -> List[str]:
        """Get list of missing critical built-in dependencies"""
        missing = []
        for module_name, result in results.items():
            if not result['available'] and result['is_critical']:
                missing.append(module_name)
        return missing
    
    def get_installation_instructions(self, missing_modules: List[str]) -> Dict[str, str]:
        """Get installation instructions for missing modules"""
        instructions = {}
        for module_name in missing_modules:
            if module_name in self.builtin_dependencies:
                instructions[module_name] = self.builtin_dependencies[module_name]['system_package']
        return instructions
    
    def print_detailed_report(self):
        """Print a detailed report of built-in dependency status"""
        print("🔍 Built-in Dependencies Test for Teacher1")
        print("=" * 60)
        print(f"Python version: {sys.version}")
        print()
        
        results = self.test_all_builtin_dependencies()
        missing_critical = self.get_missing_critical_dependencies(results)
        
        # Print status for each dependency
        for module_name, result in results.items():
            status = "✓" if result['available'] else "✗"
            criticality = "CRITICAL" if result['is_critical'] else "optional"
            
            print(f"{status} {module_name} ({criticality})")
            print(f"   Description: {result['description']}")
            print(f"   Required for: {', '.join(result['required_for'])}")
            
            if not result['available']:
                print(f"   ❌ Error: {result['error']}")
                print(f"   💡 Install: {result['system_package']}")
            
            print()
        
        # Summary
        if missing_critical:
            print("❌ MISSING CRITICAL BUILT-IN DEPENDENCIES")
            print("-" * 50)
            for module in missing_critical:
                info = self.builtin_dependencies[module]
                print(f"• {module}: {info['description']}")
                print(f"  Install with: {info['system_package']}")
            
            print()
            print("🔧 QUICK FIX:")
            if 'tkinter' in missing_critical:
                print("sudo apt-get update && sudo apt-get install python3-tk")
            
        else:
            print("✅ All critical built-in dependencies are available!")
        
        return len(missing_critical) == 0


def main():
    """Main test function"""
    tester = BuiltinDependencyTester()
    all_ok = tester.print_detailed_report()
    
    return 0 if all_ok else 1


if __name__ == "__main__":
    sys.exit(main())