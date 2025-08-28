#!/usr/bin/env python3
"""
Teacher1 Setup Script
--------------------
This script helps set up the Teacher1 project with Rasa chatbot integration.
"""

import os
import sys
import subprocess
from pathlib import Path

def run_command(command, cwd=None, check=True):
    """Run a shell command and return the result."""
    print(f"Running: {command}")
    try:
        result = subprocess.run(
            command.split(),
            cwd=cwd,
            check=check,
            capture_output=True,
            text=True
        )
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        return None

def check_python_version():
    """Check if Python version is compatible."""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("Error: Python 3.7+ is required")
        return False
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    # Note about Rasa compatibility
    if version.major == 3 and version.minor >= 12:
        print("⚠️  Note: Python 3.12+ may have limited Rasa compatibility")
        print("   For full Rasa support, consider using Python 3.8-3.11")
        print("   Core Teacher1 functionality works with current Python version")
    elif version.major == 3 and 8 <= version.minor <= 11:
        print("✅ Python version is fully compatible with all features including Rasa")
    else:
        print("✓ Python version compatible for core dependencies")
    return True

def install_system_package(package_name):
    """Attempt to install a system package using apt-get."""
    print(f"🔧 Attempting to install system package: {package_name}")
    try:
        result = run_command(f"sudo apt-get update", check=False)
        if result and result.returncode == 0:
            result = run_command(f"sudo apt-get install -y {package_name}", check=False)
            if result and result.returncode == 0:
                print(f"✅ Successfully installed {package_name}")
                return True
        print(f"❌ Failed to install {package_name}")
        return False
    except Exception as e:
        print(f"❌ Error installing {package_name}: {e}")
        return False

def install_pip_packages(packages):
    """Attempt to install missing pip packages."""
    if not packages:
        return True
    
    print(f"🔧 Attempting to install pip packages: {', '.join(packages)}")
    try:
        packages_str = ' '.join(packages)
        result = run_command(f"pip install {packages_str}", check=False)
        if result and result.returncode == 0:
            print(f"✅ Successfully installed pip packages")
            return True
        else:
            print(f"❌ Failed to install some pip packages")
            return False
    except Exception as e:
        print(f"❌ Error installing pip packages: {e}")
        return False

def test_and_install_optional_dependencies():
    """Test and optionally install non-critical dependencies."""
    print("\n🔍 Testing optional dependencies...")
    
    optional_packages = {
        'pyttsx3': 'pyttsx3>=2.90',
        'speech_recognition': 'SpeechRecognition>=3.10.0',
        'pyaudio': 'pyaudio'  # Note: may require system audio libraries
    }
    
    missing_packages = []
    
    for module_name, pip_package in optional_packages.items():
        try:
            __import__(module_name)
            print(f"✓ {module_name} available")
        except ImportError:
            print(f"? {module_name} missing (optional)")
            missing_packages.append(pip_package)
    
    if missing_packages:
        print(f"\n🔧 Attempting to install optional packages...")
        print("   Note: Some may fail due to system requirements (audio libraries, etc.)")
        print("   💡 For text-to-speech: sudo apt-get install espeak espeak-data")
        
        # Try to install each package individually for better error handling
        for package in missing_packages:
            try:
                module_name = package.split('>=')[0].replace('-', '_').lower()
                
                # Special handling for PyAudio which often has installation issues
                if module_name == 'pyaudio':
                    print(f"🔧 Attempting to install {package}...")
                    print(f"   Note: PyAudio requires system audio libraries (portaudio19-dev)")
                    print(f"   If installation fails, audio features will be limited but other functionality works")
                    
                result = run_command(f"pip install {package}", check=False)
                if result and result.returncode == 0:
                    try:
                        __import__(module_name)
                        print(f"✅ {module_name} successfully installed and available")
                    except ImportError:
                        print(f"⚠️  {module_name} installed but not available (may need system dependencies)")
                        if module_name == 'pyaudio':
                            print(f"   💡 Alternative: Speech recognition can work without PyAudio for file input")
                else:
                    if module_name == 'pyaudio':
                        print(f"⚠️  PyAudio installation failed (common due to system dependencies)")
                        print(f"   💡 Audio input features will be limited but file-based audio processing still works")
                        print(f"   💡 To fix: Install system packages: sudo apt-get install portaudio19-dev python3-dev")
                    else:
                        print(f"⚠️  Failed to install {package} (expected for some packages)")
            except Exception as e:
                print(f"⚠️  Error installing {package}: {e}")
    
    return True  # Optional dependencies don't affect overall success

def test_and_install_external_dependencies():
    """Test and install critical external dependencies."""
    print("\n🔍 Testing critical external dependencies...")
    
    critical_packages = {
        'numpy': 'numpy>=2.3.0',
        'matplotlib': 'matplotlib>=3.10.0', 
        'websockets': 'websockets>=15.0',
        'flask': 'flask>=3.1.0',
        'flask_cors': 'flask-cors>=6.0.0'
    }
    
    missing_packages = []
    
    for module_name, pip_package in critical_packages.items():
        try:
            __import__(module_name)
            print(f"✓ {module_name} available")
        except ImportError:
            print(f"❌ {module_name} missing")
            missing_packages.append(pip_package)
    
    if missing_packages:
        print(f"\n🔧 Installing missing critical packages...")
        if install_pip_packages(missing_packages):
            # Verify installation
            still_missing = []
            for module_name, pip_package in critical_packages.items():
                try:
                    __import__(module_name)
                    print(f"✓ {module_name} now available")
                except ImportError:
                    still_missing.append(module_name)
            
            if still_missing:
                print(f"❌ Still missing after installation: {', '.join(still_missing)}")
                return False
        else:
            return False
    
    print("✅ All critical external dependencies available")
    return True

def check_builtin_dependencies():
    """Check for missing built-in Python dependencies and attempt to install them."""
    print("\n🔍 Checking built-in dependencies...")
    
    # Import our built-in dependency tester
    try:
        from test_builtin_dependencies import BuiltinDependencyTester
        tester = BuiltinDependencyTester()
        results = tester.test_all_builtin_dependencies()
        missing_critical = tester.get_missing_critical_dependencies(results)
        
        if missing_critical:
            print("❌ Missing critical built-in dependencies:")
            for module in missing_critical:
                info = tester.builtin_dependencies[module]
                print(f"  • {module}: {info['description']}")
                print(f"    Install: {info['system_package']}")
            
            # Attempt to install missing critical dependencies
            install_success = True
            for module in missing_critical:
                info = tester.builtin_dependencies[module]
                system_package = info['system_package']
                
                # Only attempt to install if it's an actual system package
                if system_package and not system_package.startswith('Built-in'):
                    if 'python3-tk' in system_package:
                        if install_system_package('python3-tk'):
                            # Verify the installation worked
                            try:
                                import tkinter
                                print(f"✅ {module} now available after installation")
                            except ImportError:
                                print(f"❌ {module} still not available after installation")
                                install_success = False
                        else:
                            install_success = False
                            
            return install_success
        else:
            print("✓ All critical built-in dependencies available")
            return True
            
    except ImportError:
        print("⚠️  Built-in dependency tester not available")
        # Enhanced fallback: test critical built-in modules manually
        critical_builtins = {
            'tkinter': 'python3-tk',
            'uuid': None,
            'json': None,
            'asyncio': None,
            'threading': None,
            'urllib.parse': None
        }
        
        missing_critical = []
        for module_name, system_package in critical_builtins.items():
            try:
                if '.' in module_name:
                    # Handle modules like urllib.parse
                    parent_module = module_name.split('.')[0]
                    submodule = module_name.split('.')[1]
                    parent = __import__(parent_module)
                    getattr(parent, submodule)
                else:
                    __import__(module_name)
                print(f"✓ {module_name} available")
            except (ImportError, AttributeError):
                print(f"❌ {module_name} missing")
                if system_package:
                    missing_critical.append((module_name, system_package))
        
        # Attempt to install missing packages
        if missing_critical:
            install_success = True
            for module_name, system_package in missing_critical:
                if install_system_package(system_package):
                    # Verify installation
                    try:
                        __import__(module_name)
                        print(f"✅ {module_name} now available after installation")
                    except ImportError:
                        print(f"❌ {module_name} still not available after installation")
                        install_success = False
                else:
                    install_success = False
            return install_success
        else:
            return True

def install_dependencies():
    """Install project dependencies."""
    print("\n📦 Installing dependencies...")
    requirements_file = "requirements.txt"
    
    if not os.path.exists(requirements_file):
        print("Error: requirements.txt not found")
        return False
    
    # Check if we're using conda environment
    python_path = sys.executable
    if "miniconda" in python_path or "conda" in python_path:
        print(f"Using conda Python: {python_path}")
        print("📋 Core dependencies are already installed via conda:")
        
        # Test core dependencies
        try:
            import numpy, matplotlib, websockets, flask, flask_cors
            print("  ✓ numpy, matplotlib, websockets, flask, flask_cors - Available")
        except ImportError as e:
            print(f"  ✗ Some core dependencies missing: {e}")
            return False
            
        print("\n⚠️  Rasa installation requires Python 3.8-3.11 compatibility")
        print("   Current Python 3.13.5 may not support rasa>=3.6.0")
        print("   Please use Python 3.10 environment for full Rasa support")
        return True
    else:
        # Try normal pip install
        result = run_command("pip install -r requirements.txt")
        return result is not None

def setup_rasa():
    """Set up and train the Rasa model."""
    print("\n🤖 Setting up Rasa chatbot...")
    
    rasa_dir = Path("rasa_bot")
    if not rasa_dir.exists():
        print("Error: rasa_bot directory not found")
        return False
    
    # Check if Rasa is available
    try:
        import rasa
        print(f"Rasa {rasa.__version__} is available")
    except ImportError:
        import sys
        version = sys.version_info
        print("⚠️  Rasa is not installed in current environment")
        if version.major == 3 and version.minor >= 12:
            print(f"   This is expected with Python {version.major}.{version.minor}.{version.micro}")
            print("   Rasa currently supports Python 3.8-3.11")
            print("   💡 Solutions:")
            print("   1. Use Python 3.8-3.11 environment (recommended)")
            print("   2. Wait for Rasa updates supporting Python 3.12+")
            print("   3. Use core Teacher1 functionality (works without Rasa)")
        else:
            print("   Install Rasa with: pip install rasa>=3.6.0 rasa-sdk>=3.6.0")
        return False
    
    # Train the Rasa model
    print("Training Rasa model...")
    result = run_command("rasa train", cwd=str(rasa_dir))
    
    if result:
        print("Rasa model trained successfully! ✓")
        return True
    else:
        print("Failed to train Rasa model")
        return False

def test_components():
    """Test individual components."""
    print("\n🧪 Testing components...")
    
    # Test imports
    test_imports = [
        ("numpy", "import numpy as np; print('NumPy:', np.__version__)"),
        ("text_to_speech", "from text_to_speech import speak; print('TTS: Available')"),
        ("fractal_modules", "import fractal_modules; print('Fractal modules: Available')"),
    ]
    
    for name, test_code in test_imports:
        try:
            result = subprocess.run(
                [sys.executable, "-c", test_code],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                print(f"{name}: ✓")
                if result.stdout.strip():
                    print(f"  {result.stdout.strip()}")
            else:
                print(f"{name}: ✗")
                if result.stderr:
                    print(f"  Error: {result.stderr.strip()}")
        except Exception as e:
            print(f"{name}: ✗ (Exception: {e})")

def show_usage_examples():
    """Show usage examples."""
    print("\n📚 Usage Examples:")
    print("="*50)
    
    examples = [
        ("GUI Application", "python big_text_gui.py"),
        ("Text-to-Speech Demo", "python text_to_speech.py"),
        ("Speech Recognition Demo", "python speech_recognition_demo.py"),
        ("Fractal AI System", "python fractal_emergent_ai.py"),
        ("Chatbot (with TTS)", "python rasa_bot/chatbot_integration.py"),
        ("Chatbot (text only)", "python rasa_bot/chatbot_integration.py --no-tts"),
        ("Rasa Shell", "cd rasa_bot && rasa shell"),
    ]
    
    for name, command in examples:
        print(f"\n{name}:")
        print(f"  {command}")

def main():
    """Main setup function."""
    print("🎓 Teacher1 Setup Script")
    print("="*40)
    
    # Check Python version
    if not check_python_version():
        return 1
    
    # Test and install built-in dependencies
    builtin_ok = check_builtin_dependencies()
    if not builtin_ok:
        print("⚠️  Some built-in dependencies could not be installed")
        print("   GUI functionality may be limited")
        print("   You may need to manually install: sudo apt-get install python3-tk")
    
    # Test and install external dependencies
    external_ok = test_and_install_external_dependencies()
    if not external_ok:
        print("❌ Failed to install some critical external dependencies")
        print("   Trying manual pip install from requirements.txt...")
        # Fallback to original installation method
        if not install_dependencies():
            print("❌ Failed to install dependencies via requirements.txt")
            return 1
    
    # Test and install optional dependencies
    test_and_install_optional_dependencies()
    
    # Setup Rasa
    if not setup_rasa():
        print("❌ Failed to setup Rasa")
        print("Note: You can manually train later with: cd rasa_bot && rasa train")
    
    # Test components
    test_components()
    
    # Show usage examples
    show_usage_examples()
    
    # Final dependency status check
    print("\n🔍 Final dependency status check...")
    final_builtin_ok = check_builtin_dependencies()
    final_external_ok = test_and_install_external_dependencies()
    
    if final_builtin_ok and final_external_ok:
        print("\n✅ Setup complete! All critical dependencies are available.")
    else:
        print("\n⚠️  Setup complete but some dependencies may still be missing.")
        print("    Core functionality should still work.")
    
    print("\nTo get started:")
    print("  python rasa_bot/chatbot_integration.py")
    
    return 0

if __name__ == "__main__":
    exit(main())