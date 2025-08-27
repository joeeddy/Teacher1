#!/usr/bin/env python3
"""
Detailed analysis of missing dependencies and import issues.
"""

import sys
import importlib.util

def test_import_variations():
    """Test different import variations for packages."""
    
    print("🔍 Testing Import Variations")
    print("=" * 50)
    
    # Test speech recognition variations
    print("\n📢 Speech Recognition:")
    variations = ['speech_recognition', 'speechrecognition', 'SpeechRecognition']
    for var in variations:
        try:
            module = importlib.import_module(var)
            print(f"✅ {var}: Available (version: {getattr(module, '__version__', 'unknown')})")
        except ImportError as e:
            print(f"❌ {var}: {e}")
    
    # Test GUI variations
    print("\n🖥️ GUI:")
    gui_variations = ['tkinter', 'Tkinter', 'tk']
    for var in gui_variations:
        try:
            module = importlib.import_module(var)
            print(f"✅ {var}: Available")
        except ImportError as e:
            print(f"❌ {var}: {e}")
    
    # Test project modules
    print("\n🏗️ Project Modules:")
    project_modules = ['big_text_gui', 'fractal_modules', 'text_to_speech', 'websocket_communication']
    for module_name in project_modules:
        try:
            spec = importlib.util.spec_from_file_location(module_name, f"{module_name}.py")
            if spec is None:
                print(f"❌ {module_name}: File not found or not importable")
                continue
            
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            print(f"✅ {module_name}: Successfully imported")
        except Exception as e:
            print(f"❌ {module_name}: {e}")

def check_available_packages():
    """Check what packages are actually available in the environment."""
    
    print("\n📦 Available Python Packages")
    print("=" * 50)
    
    import subprocess
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', 'list'], 
                                capture_output=True, text=True, timeout=30)
        if result.returncode == 0:
            lines = result.stdout.split('\n')
            packages = []
            for line in lines[2:]:  # Skip header lines
                if line.strip():
                    parts = line.split()
                    if len(parts) >= 2:
                        packages.append((parts[0], parts[1]))
            
            print(f"Found {len(packages)} installed packages:")
            
            # Look for packages related to our requirements
            relevant_packages = []
            keywords = ['numpy', 'matplotlib', 'flask', 'websocket', 'speech', 'audio', 
                       'rasa', 'tensorflow', 'spacy', 'tkinter']
            
            for name, version in packages:
                for keyword in keywords:
                    if keyword.lower() in name.lower():
                        relevant_packages.append((name, version))
                        break
            
            if relevant_packages:
                print("\nPotentially relevant packages:")
                for name, version in relevant_packages:
                    print(f"  {name}: {version}")
            else:
                print("No packages matching our requirements found.")
                
        else:
            print(f"Error running pip list: {result.stderr}")
    except Exception as e:
        print(f"Error checking packages: {e}")

def analyze_import_paths():
    """Analyze Python import paths and module discovery."""
    
    print("\n🛤️ Python Import Path Analysis")
    print("=" * 50)
    
    print("Python executable:", sys.executable)
    print("Python version:", sys.version)
    print("\nImport paths:")
    for i, path in enumerate(sys.path, 1):
        print(f"  {i}. {path}")
    
    # Check if we can find specific modules
    print("\n🔍 Module Search:")
    modules_to_find = ['speech_recognition', 'numpy', 'tkinter']
    
    for module_name in modules_to_find:
        spec = importlib.util.find_spec(module_name)
        if spec:
            print(f"✅ {module_name}: Found at {spec.origin}")
        else:
            print(f"❌ {module_name}: Not found in import path")

if __name__ == "__main__":
    test_import_variations()
    check_available_packages()
    analyze_import_paths()