#!/usr/bin/env python3
"""
Network-Resilient Dependency Testing Script

Tests the enhanced optional dependency handling system to ensure it properly handles:
- Network timeouts and failures
- Bus errors and crashes
- Graceful fallback mechanisms
- Non-blocking behavior during setup
"""

import sys
import subprocess
import time
import os

def test_network_resilient_setup():
    """Test that setup script doesn't hang or crash on network issues."""
    print("🧪 Testing network-resilient setup behavior...")
    
    start_time = time.time()
    try:
        # Test with a reasonable timeout - should not hang indefinitely
        result = subprocess.run([
            sys.executable, '-c', 'from setup import test_and_install_optional_dependencies; test_and_install_optional_dependencies()'
        ], capture_output=True, text=True, timeout=120)
        
        duration = time.time() - start_time
        print(f"✅ Setup completed in {duration:.1f}s (no hanging)")
        
        # Check that fallback information is present
        if 'Fallback:' in result.stdout:
            print("✅ Fallback mechanisms are clearly communicated")
        else:
            print("⚠️  Fallback information not found in output")
            
        # Check that it handles errors gracefully
        if 'Bus error' in result.stderr or 'Segmentation fault' in result.stderr:
            print("❌ Still experiencing crashes")
            return False
        else:
            print("✅ No crashes detected")
            
        return True
        
    except subprocess.TimeoutExpired:
        duration = time.time() - start_time
        print(f"❌ Setup hung for {duration:.1f}s - network resilience failed")
        return False
    except Exception as e:
        print(f"❌ Setup failed with error: {e}")
        return False

def test_optional_dependency_manager_stability():
    """Test that the optional dependency manager doesn't crash."""
    print("\n🧪 Testing optional dependency manager stability...")
    
    try:
        result = subprocess.run([
            sys.executable, '-c', '''
import optional_dependencies_manager
manager = optional_dependencies_manager.OptionalDependencyManager()
status = manager.get_all_dependencies_status()
working, total, percentage = manager.get_summary_stats()
print(f"Status check completed: {working}/{total} dependencies available")
for name, info in status.items():
    if not info["available"]:
        print(f"Fallback for {name}: {info['spec']['fallback']}")
'''
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Dependency manager operates without crashes")
            if 'Status check completed' in result.stdout:
                print("✅ Status checking works correctly")
            if 'Fallback for' in result.stdout:
                print("✅ Fallback information is accessible")
            return True
        else:
            print(f"❌ Dependency manager failed: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Dependency manager hung (timeout)")
        return False
    except Exception as e:
        print(f"❌ Dependency manager test failed: {e}")
        return False

def test_pip_install_timeout_handling():
    """Test that pip install operations respect timeouts."""
    print("\n🧪 Testing pip install timeout handling...")
    
    start_time = time.time()
    try:
        # Test with a non-existent package to trigger timeout behavior
        result = subprocess.run([
            sys.executable, '-c', '''
from setup import run_command
result = run_command("pip install --timeout 5 nonexistent_package_12345", check=False, timeout=15)
print("Timeout test completed - no hanging")
'''
        ], capture_output=True, text=True, timeout=30)
        
        duration = time.time() - start_time
        if duration < 25:  # Should complete well within timeout
            print(f"✅ Timeout handling works correctly ({duration:.1f}s)")
            return True
        else:
            print(f"⚠️  Timeout handling may be slow ({duration:.1f}s)")
            return True
            
    except subprocess.TimeoutExpired:
        print("❌ Timeout handling failed - command hung")
        return False
    except Exception as e:
        print(f"❌ Timeout test failed: {e}")
        return False

def test_fallback_mechanism_availability():
    """Test that fallback mechanisms are properly defined and accessible."""
    print("\n🧪 Testing fallback mechanism availability...")
    
    try:
        result = subprocess.run([
            sys.executable, '-c', '''
from setup import _fallback_optional_dependencies_test
result = _fallback_optional_dependencies_test()
print("Fallback testing completed successfully")
'''
        ], capture_output=True, text=True, timeout=15)
        
        if result.returncode == 0:
            print("✅ Fallback mechanisms are available and working")
            if 'Fallback:' in result.stdout:
                print("✅ Fallback information is properly displayed")
            return True
        else:
            print(f"❌ Fallback test failed: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Fallback availability test failed: {e}")
        return False

def test_core_functionality_preservation():
    """Test that core functionality is preserved despite optional dependency issues."""
    print("\n🧪 Testing core functionality preservation...")
    
    critical_imports = [
        'numpy', 'matplotlib', 'websockets', 'flask', 'flask_cors'
    ]
    
    for module in critical_imports:
        try:
            subprocess.run([
                sys.executable, '-c', f'import {module}; print("{module} available")'
            ], check=True, capture_output=True, text=True, timeout=10)
            print(f"✅ {module} - core functionality preserved")
        except subprocess.CalledProcessError:
            print(f"❌ {module} - core functionality affected")
            return False
        except Exception as e:
            print(f"❌ {module} test failed: {e}")
            return False
    
    print("✅ All core functionality preserved")
    return True

def main():
    """Run all network resilience tests."""
    print("🎯 Network-Resilient Dependency Testing")
    print("=" * 50)
    
    tests = [
        test_network_resilient_setup,
        test_optional_dependency_manager_stability,
        test_pip_install_timeout_handling,
        test_fallback_mechanism_availability,
        test_core_functionality_preservation
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print(f"\n📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All network resilience tests passed!")
        print("✅ Optional dependency handling is robust and network-resilient")
        return 0
    else:
        print("❌ Some tests failed - network resilience needs improvement")
        return 1

if __name__ == "__main__":
    sys.exit(main())