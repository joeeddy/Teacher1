#!/usr/bin/env python3
"""
Quick dependency test for Teacher1 project.
This script provides a fast way to check if all dependencies are available.
"""

def quick_dependency_check():
    """Quick check of critical dependencies."""
    
    print("🚀 Quick Dependency Check for Teacher1")
    print("=" * 45)
    
    critical_deps = [
        ('numpy', 'Core mathematical operations'),
        ('matplotlib', 'Plotting and visualization'),
        ('websockets', 'WebSocket communication'),
        ('flask', 'Web interface'),
        ('tkinter', 'GUI applications'),
    ]
    
    optional_deps = [
        ('speech_recognition', 'Voice input'),
        ('pyttsx3', 'Text-to-speech'),
        ('tensorflow', 'AI/ML features'),
        ('rasa', 'Chatbot framework'),
    ]
    
    missing_critical = []
    missing_optional = []
    
    print("\n✅ Critical Dependencies:")
    for dep, description in critical_deps:
        try:
            if dep == 'speech_recognition':
                # Check for the actual package, not local file
                import speech_recognition
                if hasattr(speech_recognition, 'Recognizer'):
                    print(f"  ✓ {dep}: {description}")
                else:
                    raise ImportError("Local file, not package")
            else:
                __import__(dep)
                print(f"  ✓ {dep}: {description}")
        except ImportError:
            print(f"  ✗ {dep}: {description} - MISSING")
            missing_critical.append(dep)
    
    print("\n🔧 Optional Dependencies:")
    for dep, description in optional_deps:
        try:
            __import__(dep)
            print(f"  ✓ {dep}: {description}")
        except ImportError:
            print(f"  ? {dep}: {description} - Missing")
            missing_optional.append(dep)
    
    print(f"\n📊 Summary:")
    print(f"  Critical missing: {len(missing_critical)}")
    print(f"  Optional missing: {len(missing_optional)}")
    
    if missing_critical:
        print(f"\n❌ Cannot run project - missing critical dependencies:")
        for dep in missing_critical:
            print(f"     • {dep}")
        print(f"\n💡 To install: pip install {' '.join(missing_critical)}")
        return False
    else:
        print(f"\n✅ All critical dependencies available!")
        if missing_optional:
            print(f"   Optional features may not work due to missing: {', '.join(missing_optional)}")
        return True

if __name__ == "__main__":
    success = quick_dependency_check()
    exit(0 if success else 1)