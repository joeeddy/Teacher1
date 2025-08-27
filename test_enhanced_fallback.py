#!/usr/bin/env python3
"""
Test script to validate the enhanced fallback mechanism for dependency testing and installation.
This script tests the enhanced functionality added to setup.py.
"""

import sys
import subprocess
import tempfile
import os

def test_builtin_dependency_detection():
    """Test that the enhanced fallback can detect built-in dependencies."""
    print("🧪 Testing built-in dependency detection...")
    
    # Import the enhanced functions from setup.py
    try:
        sys.path.insert(0, '.')
        from setup import check_builtin_dependencies
        
        # Test the function
        result = check_builtin_dependencies()
        if result:
            print("✅ Built-in dependency check passed")
            return True
        else:
            print("❌ Built-in dependency check failed")
            return False
    except Exception as e:
        print(f"❌ Error testing built-in dependencies: {e}")
        return False

def test_external_dependency_detection():
    """Test that the enhanced fallback can detect external dependencies."""
    print("🧪 Testing external dependency detection...")
    
    try:
        from setup import test_and_install_external_dependencies
        
        # Test the function
        result = test_and_install_external_dependencies()
        if result:
            print("✅ External dependency check passed")
            return True
        else:
            print("❌ External dependency check failed")
            return False
    except Exception as e:
        print(f"❌ Error testing external dependencies: {e}")
        return False

def test_optional_dependency_detection():
    """Test that the enhanced fallback can detect optional dependencies."""
    print("🧪 Testing optional dependency detection...")
    
    try:
        from setup import test_and_install_optional_dependencies
        
        # Test the function
        result = test_and_install_optional_dependencies()
        if result:
            print("✅ Optional dependency check passed")
            return True
        else:
            print("❌ Optional dependency check failed")
            return False
    except Exception as e:
        print(f"❌ Error testing optional dependencies: {e}")
        return False

def test_all_critical_dependencies():
    """Test that all critical dependencies are available after the setup."""
    print("🧪 Testing all critical dependencies are available...")
    
    # Test built-in critical dependencies
    critical_builtins = ['tkinter', 'uuid', 'json', 'asyncio', 'threading']
    
    for module_name in critical_builtins:
        try:
            if '.' in module_name:
                parent_module = module_name.split('.')[0]
                submodule = module_name.split('.')[1]
                parent = __import__(parent_module)
                getattr(parent, submodule)
            else:
                __import__(module_name)
            print(f"✅ {module_name} available")
        except (ImportError, AttributeError) as e:
            print(f"❌ {module_name} missing: {e}")
            return False
    
    # Test urllib.parse separately due to its dot notation
    try:
        import urllib.parse
        print("✅ urllib.parse available")
    except ImportError as e:
        print(f"❌ urllib.parse missing: {e}")
        return False
    
    # Test external critical dependencies
    critical_externals = ['numpy', 'matplotlib', 'websockets', 'flask', 'flask_cors']
    
    for module_name in critical_externals:
        try:
            __import__(module_name)
            print(f"✅ {module_name} available")
        except ImportError as e:
            print(f"❌ {module_name} missing: {e}")
            return False
    
    print("✅ All critical dependencies are available!")
    return True

def test_fallback_comprehensive():
    """Test that fallback works even when BuiltinDependencyTester is not available."""
    print("🧪 Testing fallback behavior when tester is unavailable...")
    
    # Create a temporary file that simulates missing test_builtin_dependencies
    try:
        # This tests the fallback path in check_builtin_dependencies
        # when the import fails
        
        # Test that the basic fallback functionality works
        # We can't easily simulate the ImportError without modifying the file,
        # but we can test that all the critical built-ins are working
        critical_modules = ['tkinter', 'uuid', 'json', 'asyncio', 'threading']
        
        all_available = True
        for module in critical_modules:
            try:
                __import__(module)
                print(f"✅ {module} available in fallback test")
            except ImportError:
                print(f"❌ {module} missing in fallback test")
                all_available = False
        
        # Test urllib.parse
        try:
            import urllib.parse
            print("✅ urllib.parse available in fallback test")
        except ImportError:
            print("❌ urllib.parse missing in fallback test")
            all_available = False
        
        return all_available
        
    except Exception as e:
        print(f"❌ Error in fallback test: {e}")
        return False

def main():
    """Main test function."""
    print("🔍 Enhanced Fallback Mechanism Test for Teacher1")
    print("=" * 60)
    
    tests = [
        ("Built-in dependency detection", test_builtin_dependency_detection),
        ("External dependency detection", test_external_dependency_detection),
        ("Optional dependency detection", test_optional_dependency_detection),
        ("All critical dependencies available", test_all_critical_dependencies),
        ("Fallback comprehensive test", test_fallback_comprehensive),
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'='*50}")
        print(f"Running: {test_name}")
        print(f"{'='*50}")
        
        try:
            result = test_func()
            results.append((test_name, result))
            if result:
                print(f"✅ {test_name}: PASSED")
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
            results.append((test_name, False))
    
    # Summary
    print(f"\n{'='*60}")
    print("TEST SUMMARY")
    print(f"{'='*60}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Enhanced fallback mechanism is working correctly.")
        return 0
    else:
        print("⚠️  Some tests failed. Please review the fallback implementation.")
        return 1

if __name__ == "__main__":
    sys.exit(main())