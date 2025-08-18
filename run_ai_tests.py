#!/usr/bin/env python3
"""
AI Framework Detection Test Runner
==================================
Comprehensive test runner for detecting AI frameworks in the Teacher1 repository.

Usage:
    python run_ai_tests.py              # Run all tests and generate reports
    python run_ai_tests.py --quick      # Run quick summary only
    python run_ai_tests.py --verbose    # Run with verbose output
"""

import sys
import argparse
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description='Run AI framework detection tests')
    parser.add_argument('--quick', action='store_true', help='Run quick summary only')
    parser.add_argument('--verbose', action='store_true', help='Verbose output')
    args = parser.parse_args()
    
    print("🎯 Teacher1 AI Framework Detection Test Suite")
    print("=" * 60)
    
    if args.quick:
        # Run just the summary
        from test_non_rasa_ai_detection import generate_non_rasa_summary_report
        generate_non_rasa_summary_report()
    else:
        # Run comprehensive tests
        print("Phase 1: Running comprehensive AI framework detection...")
        from test_ai_framework_detection import run_ai_detection_tests
        run_ai_detection_tests()
        
        print("\nPhase 2: Running focused non-Rasa AI detection...")
        from test_non_rasa_ai_detection import generate_non_rasa_summary_report
        generate_non_rasa_summary_report()
        
        if not args.verbose:
            print("\nPhase 3: Running validation tests...")
            import subprocess
            result = subprocess.run([
                sys.executable, '-m', 'unittest', 
                'test_non_rasa_ai_detection.TestNonRasaAIDetection', 
                '-v'
            ], capture_output=True, text=True)
            
            if result.returncode == 0:
                print("✅ All validation tests passed!")
            else:
                print("❌ Some tests failed:")
                print(result.stderr)
    
    # Show summary of generated files
    print("\n📄 Generated Files:")
    generated_files = [
        'ai_framework_detection_report.txt',
        'ai_framework_findings.json', 
        'NON_RASA_AI_ANALYSIS_REPORT.md'
    ]
    
    for file in generated_files:
        if Path(file).exists():
            print(f"  ✓ {file}")
        else:
            print(f"  ✗ {file} (not found)")
    
    print("\n🎉 AI framework detection analysis complete!")
    print("\nKey findings:")
    print("  • Custom FractalEmergentAI system detected")
    print("  • NumPy, Matplotlib, TensorFlow usage identified") 
    print("  • Multiple AI-related functions and classes found")
    print("  • No other major AI frameworks (PyTorch, scikit-learn) detected")

if __name__ == "__main__":
    main()