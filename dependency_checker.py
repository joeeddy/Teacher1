#!/usr/bin/env python3
"""
Comprehensive Dependency Checker for Teacher1 Project
Analyzes all dependencies and identifies missing packages without requiring installation.
"""

import sys
import subprocess
import importlib
import importlib.util
from pathlib import Path
import re
from dataclasses import dataclass
from typing import List, Dict, Optional, Tuple


@dataclass
class DependencyStatus:
    """Represents the status of a dependency."""
    name: str
    required_version: Optional[str]
    installed_version: Optional[str]
    available: bool
    critical: bool
    error_message: Optional[str]


class DependencyChecker:
    """Comprehensive dependency checker for the Teacher1 project."""
    
    def __init__(self):
        self.results = []
        self.requirements_file = Path("requirements.txt")
        
        # Define critical vs optional dependencies
        self.critical_deps = {
            'numpy', 'matplotlib', 'websockets', 'flask', 'flask-cors'
        }
        
        self.ai_deps = {
            'tensorflow', 'spacy', 'rasa', 'rasa-sdk'
        }
        
        self.audio_deps = {
            'speechrecognition', 'pyaudio', 'pyttsx3'
        }
        
        self.gui_deps = {
            'tkinter'
        }
        
        # Package name mapping (pip name -> import name)
        self.package_import_mapping = {
            'speechrecognition': 'speech_recognition',
            'rasa-sdk': 'rasa_sdk',
            'flask-cors': 'flask_cors'
        }
    
    def parse_requirements(self) -> Dict[str, str]:
        """Parse requirements.txt and extract package names and versions."""
        requirements = {}
        
        if not self.requirements_file.exists():
            print(f"❌ Requirements file not found: {self.requirements_file}")
            return requirements
        
        try:
            with open(self.requirements_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # Parse package name and version requirement
                        match = re.match(r'^([a-zA-Z0-9_-]+)([>=<~!].*)?\s*$', line)
                        if match:
                            package_name = match.group(1)
                            version_spec = match.group(2) or ""
                            requirements[package_name] = version_spec
                        else:
                            print(f"⚠️  Could not parse requirement: {line}")
        except Exception as e:
            print(f"❌ Error reading requirements file: {e}")
        
        return requirements
    
    def check_python_version(self) -> Tuple[bool, str]:
        """Check Python version compatibility."""
        version = sys.version_info
        version_str = f"{version.major}.{version.minor}.{version.micro}"
        
        # Check for known compatibility issues
        issues = []
        
        if version.major < 3:
            issues.append("Python 3.x is required")
        elif version.major == 3 and version.minor < 7:
            issues.append("Python 3.7+ is required for modern packages")
        
        # Check Rasa compatibility (known issue)
        if version.major == 3 and version.minor >= 11:
            issues.append("Rasa 3.6.0+ requires Python <3.11")
        
        if issues:
            return False, f"Python {version_str}: {'; '.join(issues)}"
        else:
            return True, f"Python {version_str}: Compatible"
    
    def check_dependency(self, package_name: str, version_spec: str = "") -> DependencyStatus:
        """Check if a specific dependency is available and get its version."""
        
        # Get the actual import name (handle package name variations)
        import_name = self.package_import_mapping.get(package_name, package_name)
        
        # Special case for tkinter (built-in module)
        if import_name == 'tkinter':
            try:
                import tkinter
                return DependencyStatus(
                    name=package_name,
                    required_version=version_spec,
                    installed_version="built-in",
                    available=True,
                    critical=package_name in self.critical_deps,
                    error_message=None
                )
            except ImportError as e:
                return DependencyStatus(
                    name=package_name,
                    required_version=version_spec,
                    installed_version=None,
                    available=False,
                    critical=package_name in self.critical_deps,
                    error_message=str(e)
                )
        
        # For other packages, try to import them
        try:
            # Try importing the module
            module = importlib.import_module(import_name)
            
            # Try to get version
            version = None
            for attr in ['__version__', 'VERSION', 'version']:
                if hasattr(module, attr):
                    version = str(getattr(module, attr))
                    break
            
            return DependencyStatus(
                name=package_name,
                required_version=version_spec,
                installed_version=version,
                available=True,
                critical=package_name in self.critical_deps,
                error_message=None
            )
            
        except ImportError as e:
            return DependencyStatus(
                name=package_name,
                required_version=version_spec,
                installed_version=None,
                available=False,
                critical=package_name in self.critical_deps,
                error_message=str(e)
            )
    
    def check_project_modules(self) -> List[DependencyStatus]:
        """Check if project-specific modules can be imported."""
        project_modules = [
            'big_text_gui',
            'fractal_modules',
            'text_to_speech',
            'speech_recognition',
            'websocket_communication'
        ]
        
        results = []
        for module_name in project_modules:
            if Path(f"{module_name}.py").exists():
                status = self.check_dependency(module_name)
                status.critical = True  # Project modules are critical
                results.append(status)
        
        return results
    
    def check_system_dependencies(self) -> List[str]:
        """Check for system-level dependencies that might be needed."""
        system_issues = []
        
        # Check for audio system dependencies (for pyaudio, etc.)
        audio_libs = [
            'portaudio19-dev',
            'libasound2-dev',
            'alsa-utils'
        ]
        
        # Check if we're in a containerized environment
        if Path('/.dockerenv').exists() or Path('/run/.containerenv').exists():
            system_issues.append("Running in containerized environment - audio features may be limited")
        
        return system_issues
    
    def analyze_compatibility_issues(self, requirements: Dict[str, str]) -> List[str]:
        """Analyze potential compatibility issues between dependencies."""
        issues = []
        
        # Check for known compatibility problems
        python_version = sys.version_info
        
        # Rasa compatibility issue
        if 'rasa' in requirements and python_version >= (3, 11):
            issues.append("Rasa requires Python <3.11, but Python 3.11+ is installed")
        
        # TensorFlow compatibility
        if 'tensorflow' in requirements and python_version >= (3, 12):
            issues.append("TensorFlow may have compatibility issues with Python 3.12+")
        
        return issues
    
    def run_comprehensive_check(self) -> Dict:
        """Run a comprehensive dependency check."""
        print("🔍 Teacher1 Comprehensive Dependency Check")
        print("=" * 60)
        
        # Check Python version
        python_ok, python_msg = self.check_python_version()
        print(f"🐍 {python_msg}")
        
        # Parse requirements
        requirements = self.parse_requirements()
        
        # Add tkinter since it's needed but not in requirements.txt
        requirements['tkinter'] = ""
        
        print(f"📋 Found {len(requirements)} requirements in {self.requirements_file}")
        if 'tkinter' in requirements:
            print("📋 Added tkinter (GUI dependency) to check list")
        
        # Check each requirement
        print("\n📦 Checking Package Dependencies:")
        print("-" * 40)
        
        critical_missing = []
        optional_missing = []
        available_packages = []
        
        for package_name, version_spec in requirements.items():
            status = self.check_dependency(package_name, version_spec)
            self.results.append(status)
            
            if status.available:
                icon = "✅"
                version_info = f" (v{status.installed_version})" if status.installed_version else ""
                print(f"{icon} {package_name}{version_info}")
                available_packages.append(package_name)
            else:
                icon = "❌" if status.critical else "⚠️ "
                print(f"{icon} {package_name}: {status.error_message}")
                
                if status.critical or package_name in self.ai_deps:
                    critical_missing.append(package_name)
                else:
                    optional_missing.append(package_name)
        
        # Check project modules
        print("\n🏗️  Checking Project Modules:")
        print("-" * 40)
        
        project_status = self.check_project_modules()
        for status in project_status:
            icon = "✅" if status.available else "❌"
            print(f"{icon} {status.name}")
            if not status.available:
                critical_missing.append(status.name)
        
        # Check for compatibility issues
        compatibility_issues = self.analyze_compatibility_issues(requirements)
        if compatibility_issues:
            print("\n⚠️  Compatibility Issues:")
            print("-" * 40)
            for issue in compatibility_issues:
                print(f"• {issue}")
        
        # Check system dependencies
        system_issues = self.check_system_dependencies()
        if system_issues:
            print("\n🖥️  System Environment Notes:")
            print("-" * 40)
            for issue in system_issues:
                print(f"• {issue}")
        
        # Summary
        print("\n📊 Summary:")
        print("=" * 60)
        
        total_deps = len(requirements)
        available_count = len(available_packages)
        critical_missing_count = len(critical_missing)
        optional_missing_count = len(optional_missing)
        
        print(f"Total dependencies: {total_deps}")
        print(f"Available packages: {available_count}")
        print(f"Critical missing: {critical_missing_count}")
        print(f"Optional missing: {optional_missing_count}")
        
        if critical_missing:
            print(f"\n❌ Critical dependencies missing:")
            for dep in critical_missing:
                print(f"   • {dep}")
        
        if optional_missing:
            print(f"\n⚠️  Optional dependencies missing:")
            for dep in optional_missing:
                print(f"   • {dep}")
        
        # Return summary data
        return {
            'python_compatible': python_ok,
            'total_dependencies': total_deps,
            'available_packages': available_packages,
            'critical_missing': critical_missing,
            'optional_missing': optional_missing,
            'compatibility_issues': compatibility_issues,
            'system_issues': system_issues,
            'all_results': self.results
        }
    
    def generate_installation_plan(self, summary: Dict) -> None:
        """Generate an installation plan for missing dependencies."""
        print("\n🚀 Installation Plan:")
        print("=" * 60)
        
        if not summary['critical_missing'] and not summary['optional_missing']:
            print("✅ All dependencies are available! No installation needed.")
            return
        
        # Basic packages that should install easily
        basic_packages = []
        problematic_packages = []
        
        all_missing = summary['critical_missing'] + summary['optional_missing']
        
        for package in all_missing:
            if package in ['rasa', 'rasa-sdk', 'tensorflow']:
                problematic_packages.append(package)
            elif package.endswith('.py'):  # Project modules
                continue
            else:
                basic_packages.append(package)
        
        if basic_packages:
            print("1. Install basic packages:")
            print(f"   pip install {' '.join(basic_packages)}")
        
        # Note about tkinter
        print("\n2. System packages that may need to be installed:")
        print("   # On Ubuntu/Debian:")
        print("   sudo apt-get install python3-tk")
        print("   # On CentOS/RHEL:")
        print("   sudo yum install tkinter")
        
        if problematic_packages:
            print("\n3. Install AI/ML packages (may require specific Python version):")
            for package in problematic_packages:
                if package == 'rasa':
                    print(f"   # {package} requires Python <3.11")
                    print(f"   pip install {package}")
                else:
                    print(f"   pip install {package}")
        
        if summary['compatibility_issues']:
            print("\n⚠️  Note: Compatibility issues detected:")
            for issue in summary['compatibility_issues']:
                print(f"   • {issue}")
            print("\n   Consider using a Python version manager (e.g., pyenv) to install Python 3.10")


def main():
    """Main function to run the dependency checker."""
    checker = DependencyChecker()
    summary = checker.run_comprehensive_check()
    checker.generate_installation_plan(summary)
    
    # Exit with appropriate code
    if summary['critical_missing']:
        print("\n❌ Critical dependencies are missing. Please install them before running the project.")
        return 1
    elif summary['compatibility_issues']:
        print("\n⚠️  Some compatibility issues detected, but project may still work.")
        return 0
    else:
        print("\n✅ All critical dependencies are available!")
        return 0


if __name__ == "__main__":
    exit(main())