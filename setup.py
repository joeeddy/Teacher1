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

def run_command(command, cwd=None, check=True, timeout=60):
    """Run a shell command and return the result.
    
    Enhanced with network-resilient timeout handling for optional dependency operations.
    """
    print(f"Running: {command}")
    try:
        result = subprocess.run(
            command.split(),
            cwd=cwd,
            check=check,
            capture_output=True,
            text=True,
            timeout=timeout  # Network-resilient: prevent hanging on network issues
        )
        if result.stdout:
            print(result.stdout)
        return result
    except subprocess.TimeoutExpired as e:
        print(f"⚠️  Command timed out after {timeout}s (likely network issue): {command}")
        return None
    except subprocess.CalledProcessError as e:
        print(f"Error running command: {e}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        return None

def check_espeak_availability():
    """Check if espeak is available for text-to-speech."""
    try:
        result = subprocess.run(['which', 'espeak'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✓ espeak system package available")
            return True
        else:
            print("? espeak missing (affects TTS audio output)")
            return False
    except Exception:
        print("? espeak status unknown")
        return False

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
    """Attempt to install missing pip packages with network-resilient retry logic."""
    if not packages:
        return True
    
    print(f"🔧 Attempting to install pip packages: {', '.join(packages)}")
    
    # Network-resilient: Use shorter timeout and retry failed packages individually
    packages_str = ' '.join(packages)
    
    try:
        # First attempt: try installing all packages together with timeout
        result = run_command(f"pip install --timeout 30 {packages_str}", check=False, timeout=120)
        if result and result.returncode == 0:
            print(f"✅ Successfully installed pip packages")
            return True
        else:
            print(f"⚠️  Batch installation failed, trying individual package installation...")
            
            # Network-resilient fallback: try each package individually
            success_count = 0
            for package in packages:
                try:
                    print(f"🔧 Installing {package} individually...")
                    result = run_command(f"pip install --timeout 30 {package}", check=False, timeout=60)
                    if result and result.returncode == 0:
                        print(f"✅ {package} installed successfully")
                        success_count += 1
                    else:
                        print(f"⚠️  {package} installation failed (network/dependency issue)")
                except Exception as e:
                    print(f"⚠️  Error installing {package}: {e}")
            
            if success_count > 0:
                print(f"✅ Partial success: {success_count}/{len(packages)} packages installed")
                return True
            else:
                print(f"❌ No packages could be installed due to network/dependency issues")
                return False
                
    except Exception as e:
        print(f"❌ Error installing pip packages: {e}")
        return False

def test_and_install_optional_dependencies():
    """Test and optionally install non-critical dependencies using the comprehensive manager.
    
    Network-resilient: Gracefully handles network failures and dependency check errors.
    Optional Dependencies Handling: All missing dependencies show clear fallback options.
    """
    print("\n🔍 Testing optional dependencies...")
    print("📝 Note: Network issues are handled gracefully - fallbacks ensure functionality")
    
    try:
        from optional_dependencies_manager import OptionalDependencyManager
        
        # Network-resilient: Safely create manager and handle potential crashes
        try:
            manager = OptionalDependencyManager()
            print("✅ Optional dependencies manager loaded successfully")
        except Exception as e:
            print(f"⚠️  Error creating optional dependencies manager: {e}")
            return _fallback_optional_dependencies_test()
        
        # Network-resilient: Safe status checking with error handling
        try:
            working, total, percentage = manager.get_summary_stats()
            print(f"📊 Current Status: {working}/{total} ({percentage:.0f}%) dependencies available")
        except Exception as e:
            print(f"⚠️  Error getting dependency stats: {e}")
            return _fallback_optional_dependencies_test()
        
        # Network-resilient: Safe detailed status check
        try:
            status = manager.get_all_dependencies_status()
        except Exception as e:
            print(f"⚠️  Error checking detailed dependency status: {e}")
            return _fallback_optional_dependencies_test()
        
        # Network-resilient: Process available dependencies with fallback info
        # Optional Dependencies Handling: Show fallback immediately to reassure users
        missing_packages = []
        for dep_name, dep_status in status.items():
            if dep_status['available']:
                print(f"✓ {dep_name} available")
            else:
                print(f"? {dep_name} missing (optional)")
                # Optional Dependencies Handling: Show fallback mechanism immediately
                fallback = dep_status.get('spec', {}).get('fallback', 'Basic functionality maintained')
                print(f"  💡 Fallback: {fallback}")
                if dep_status.get('spec', {}).get('pip_package'):
                    missing_packages.append(dep_status['spec']['pip_package'])
        
        if missing_packages:
            print(f"\n🔧 Attempting to install optional packages...")
            print("   Note: Network failures are expected and handled gracefully")
            print("   💡 Optional Dependencies Handling: Application will work with fallback mechanisms if installation fails")
            print("   💡 Use install_optional_dependencies.sh for comprehensive installation")
            
            # Network-resilient: Try to install packages with improved timeout handling
            success_count = 0
            for package in missing_packages[:3]:  # Limit to first 3 to prevent excessive timeouts
                try:
                    module_name = package.split('>=')[0].replace('-', '_').lower()
                    print(f"🔧 Attempting to install {package}...")
                    
                    # Network-resilient: Use timeout and graceful error handling
                    result = run_command(f"pip install --timeout 30 {package}", check=False, timeout=90)
                    if result and result.returncode == 0:
                        # Network-resilient: Safe import verification using subprocess for problematic modules
                        try:
                            if module_name in ['transformers', 'torch']:
                                # Use subprocess to avoid bus errors
                                import sys
                                verify_result = run_command(f"{sys.executable} -c \"import {module_name}; print('SUCCESS')\"", 
                                                          check=False, timeout=15)
                                if verify_result and verify_result.returncode == 0 and 'SUCCESS' in verify_result.stdout:
                                    print(f"✅ {module_name} successfully installed and available")
                                    success_count += 1
                                else:
                                    print(f"⚠️  {module_name} installed but not available (may need system dependencies or compatibility issues)")
                            else:
                                # Standard import for stable modules
                                __import__(module_name)
                                print(f"✅ {module_name} successfully installed and available")
                                success_count += 1
                        except ImportError:
                            print(f"⚠️  {module_name} installed but not available (may need system dependencies)")
                        except Exception as e:
                            print(f"⚠️  {module_name} verification failed: {e}")
                    else:
                        print(f"⚠️  {package} installation failed (network/system dependency issue)")
                        # Show fallback immediately to reassure user
                        dep_info = next((d for d in status.values() if d.get('spec', {}).get('pip_package') == package), None)
                        if dep_info:
                            print(f"   💡 Fallback: {dep_info['spec']['fallback']}")
                except Exception as e:
                    print(f"⚠️  Error installing {package}: {e}")
            
            if success_count > 0:
                print(f"✅ Successfully installed {success_count} optional packages")
            else:
                print("📝 No optional packages installed - application will use fallback mechanisms")
        
        # Network-resilient: Safe final status check
        try:
            final_working, final_total, final_percentage = manager.get_summary_stats()
            print(f"\n📊 Final Status: {final_working}/{final_total} ({final_percentage:.0f}%) dependencies available")
        except Exception as e:
            print(f"\n⚠️  Error getting final status (dependency check issue): {e}")
            print("📝 Optional dependencies may be partially available - application will use fallbacks")
        
        return True
    
    except ImportError:
        # Network-resilient: Fallback to basic implementation if manager not available
        print("⚠️  Optional dependencies manager not available, using basic implementation")
        return _fallback_optional_dependencies_test()


def _fallback_optional_dependencies_test():
    """Network-resilient fallback for optional dependency testing when manager fails."""
    print("🔄 Using fallback optional dependency testing...")
    
    basic_packages = {
        'pyttsx3': {'package': 'pyttsx3>=2.90', 'fallback': 'Text output only (no audio)'},
        'speech_recognition': {'package': 'SpeechRecognition>=3.10.0', 'fallback': 'File-based audio processing only'},
        'pyaudio': {'package': 'pyaudio', 'fallback': 'File-based audio processing only'},
    }
    
    missing_packages = []
    available_count = 0
    
    for module_name, info in basic_packages.items():
        try:
            __import__(module_name)
            print(f"✓ {module_name} available")
            available_count += 1
        except ImportError:
            print(f"? {module_name} missing (optional)")
            print(f"  💡 Fallback: {info['fallback']}")
            missing_packages.append(info['package'])
    
    print(f"\n📊 Basic Status: {available_count}/{len(basic_packages)} basic optional dependencies available")
    print("📝 Application will work with available dependencies and fallback mechanisms")
    return True


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
            
        print("\n⚠️  For audio input features, install PyAudio dependencies:")
        print("   sudo apt-get install portaudio19-dev python3-dev")
        print("   pip install pyaudio")
        return True
    else:
        # Network-resilient: Try normal pip install with timeout and retry logic
        print("Installing core dependencies from requirements.txt...")
        print("⚠️  Note: Network issues may cause timeouts - this is handled gracefully")
        
        result = run_command("pip install -r requirements.txt", timeout=300)  # 5 minute timeout
        if result is not None:
            print("✅ Core dependencies installation completed")
            return True
        else:
            print("⚠️  Installation from requirements.txt failed or timed out")
            print("🔄 Attempting fallback installation of critical packages...")
            
            # Network-resilient fallback: try core packages individually
            critical_packages = ['numpy>=2.3.0', 'matplotlib>=3.10.0', 'websockets>=15.0', 'flask>=3.1.0', 'flask-cors>=6.0.0']
            return install_pip_packages(critical_packages)



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
        ("Speech Recognition Demo", "python speech_recognition.py"),
        ("Fractal AI System", "python fractal_emergent_ai.py"),
        ("Personalized Chatbot", "python personalized_chatbot.py"),
        ("WebSocket Demo", "python websocket_demo.py"),
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
    print("  python text_to_speech.py")
    print("  python fractal_emergent_ai.py")
    print("  python websocket_demo.py")
    
    return 0

if __name__ == "__main__":
    exit(main())