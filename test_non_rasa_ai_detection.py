#!/usr/bin/env python3
"""
Non-Rasa AI Framework Detection Tests
====================================
Focused test suite to specifically identify non-Rasa AI frameworks and implementations
in the Teacher1 repository, as requested in the problem statement.

This test focuses specifically on detecting AI code that is NOT related to Rasa.
"""

import unittest
import sys
import os
from pathlib import Path
from test_ai_framework_detection import AIFrameworkDetector

class TestNonRasaAIDetection(unittest.TestCase):
    """
    Test suite specifically for detecting non-Rasa AI frameworks and implementations.
    """
    
    def setUp(self):
        """Set up test environment."""
        self.repo_path = Path(os.getcwd())
        self.detector = AIFrameworkDetector(str(self.repo_path))
        self.findings = self.detector.scan_repository()
        
        # Define Rasa-related libraries that should be excluded from non-Rasa findings
        self.rasa_related_libs = {
            'rasa', 'rasa-sdk', 'spacy'  # spaCy is primarily used by Rasa in this context
        }
    
    def test_non_rasa_ai_libraries_detected(self):
        """Test that non-Rasa AI libraries are detected."""
        non_rasa_imports = []
        
        for import_finding in self.findings.get('ai_imports', []):
            detected_lib = import_finding['detected_library']
            if detected_lib not in self.rasa_related_libs:
                non_rasa_imports.append(import_finding)
        
        # Should detect NumPy, Matplotlib, TensorFlow (even though TF is Rasa dependency, 
        # it's also a standalone ML framework)
        self.assertGreater(len(non_rasa_imports), 0, 
                          "Should detect at least some non-Rasa AI library imports")
        
        # Check for specific expected libraries
        detected_libs = {f['detected_library'] for f in non_rasa_imports}
        
        expected_non_rasa_libs = {'numpy', 'matplotlib', 'tensorflow'}
        found_expected = detected_libs.intersection(expected_non_rasa_libs)
        
        self.assertGreater(len(found_expected), 0,
                          f"Should detect at least one of {expected_non_rasa_libs}, found: {detected_libs}")
    
    def test_custom_ai_implementations_detected(self):
        """Test that custom AI implementations are detected."""
        custom_ai_classes = self.findings.get('custom_ai_classes', [])
        
        # Should detect the FractalEmergentAI class
        fractal_ai_detected = any(
            'FractalEmergentAI' in finding['class_name'] 
            for finding in custom_ai_classes
        )
        
        self.assertTrue(fractal_ai_detected, 
                       "Should detect the custom FractalEmergentAI class")
        
        # Should detect at least one custom AI class
        self.assertGreater(len(custom_ai_classes), 0,
                          "Should detect at least one custom AI class implementation")
    
    def test_ai_function_implementations_detected(self):
        """Test that AI-related functions are detected."""
        ai_functions = self.findings.get('ai_functions', [])
        
        # Should detect AI-related functions from fractal_modules.py
        expected_functions = {
            'apply_hierarchical_attention',
            'meta_learn_params', 
            'predictive_coding_update'
        }
        
        detected_functions = {f['function_name'] for f in ai_functions}
        found_expected = detected_functions.intersection(expected_functions)
        
        self.assertGreater(len(found_expected), 0,
                          f"Should detect AI functions like {expected_functions}, found: {detected_functions}")
    
    def test_non_rasa_dependencies_detected(self):
        """Test that non-Rasa AI dependencies are detected in requirements."""
        ai_deps = self.findings.get('ai_dependencies', [])
        
        non_rasa_deps = []
        for dep in ai_deps:
            detected_lib = dep['detected_library']
            if detected_lib not in self.rasa_related_libs:
                non_rasa_deps.append(dep)
        
        # Should detect NumPy, Matplotlib, TensorFlow, etc.
        self.assertGreater(len(non_rasa_deps), 0,
                          "Should detect non-Rasa AI dependencies in requirements.txt")
        
        detected_dep_libs = {d['detected_library'] for d in non_rasa_deps}
        expected_deps = {'numpy', 'matplotlib', 'tensorflow'}
        
        found_deps = detected_dep_libs.intersection(expected_deps)
        self.assertGreater(len(found_deps), 0,
                          f"Should find dependencies like {expected_deps}, found: {detected_dep_libs}")
    
    def test_fractal_ai_system_detected(self):
        """Test that the custom fractal AI system is properly detected."""
        # Check for fractal AI files
        ai_files = set()
        
        for finding_type in ['ai_imports', 'custom_ai_classes', 'ai_functions']:
            for finding in self.findings.get(finding_type, []):
                file_path = finding['file']
                if 'fractal' in file_path.lower():
                    ai_files.add(file_path)
        
        # Should detect both fractal_emergent_ai_gen10.py and fractal_modules.py
        expected_files = ['fractal_emergent_ai_gen10.py', 'fractal_modules.py']
        
        detected_fractal_files = []
        for ai_file in ai_files:
            for expected_file in expected_files:
                if expected_file in ai_file:
                    detected_fractal_files.append(expected_file)
        
        self.assertGreater(len(detected_fractal_files), 0,
                          f"Should detect fractal AI files: {expected_files}")
    
    def test_numpy_usage_detected(self):
        """Test that NumPy usage is detected (non-Rasa AI library)."""
        numpy_findings = []
        
        # Check imports
        for import_finding in self.findings.get('ai_imports', []):
            if 'numpy' in import_finding['detected_library']:
                numpy_findings.append(import_finding)
        
        # Check dependencies
        for dep_finding in self.findings.get('ai_dependencies', []):
            if 'numpy' in dep_finding['detected_library']:
                numpy_findings.append(dep_finding)
        
        self.assertGreater(len(numpy_findings), 0,
                          "Should detect NumPy usage as a non-Rasa AI library")
    
    def test_tensorflow_detected_as_non_rasa(self):
        """Test that TensorFlow is detected (even though it's a Rasa dependency)."""
        tensorflow_findings = []
        
        for dep_finding in self.findings.get('ai_dependencies', []):
            if 'tensorflow' in dep_finding['detected_library']:
                tensorflow_findings.append(dep_finding)
        
        self.assertGreater(len(tensorflow_findings), 0,
                          "Should detect TensorFlow as it's also a standalone ML framework")
    
    def test_no_other_major_ai_frameworks(self):
        """Test that no other major AI frameworks (PyTorch, scikit-learn, etc.) are present."""
        major_frameworks = {'torch', 'pytorch', 'sklearn', 'scikit-learn', 'openai', 'transformers'}
        
        detected_libs = set()
        for import_finding in self.findings.get('ai_imports', []):
            detected_libs.add(import_finding['detected_library'])
        
        for dep_finding in self.findings.get('ai_dependencies', []):
            detected_libs.add(dep_finding['detected_library'])
        
        found_major_frameworks = detected_libs.intersection(major_frameworks)
        
        # This test verifies that we're not using other major AI frameworks
        self.assertEqual(len(found_major_frameworks), 0,
                        f"Unexpected major AI frameworks detected: {found_major_frameworks}")

def generate_non_rasa_summary_report():
    """
    Generate a focused summary report of non-Rasa AI code findings.
    """
    detector = AIFrameworkDetector(os.getcwd())
    findings = detector.scan_repository()
    
    rasa_related = {'rasa', 'rasa-sdk', 'spacy'}
    
    print("\n" + "="*80)
    print("NON-RASA AI CODE DETECTION SUMMARY")
    print("="*80)
    
    # Non-Rasa AI Libraries
    print("\n🔍 NON-RASA AI LIBRARIES DETECTED:")
    print("-" * 50)
    non_rasa_imports = []
    for import_finding in findings.get('ai_imports', []):
        if import_finding['detected_library'] not in rasa_related:
            non_rasa_imports.append(import_finding)
            print(f"  • {import_finding['detected_library']} in {Path(import_finding['file']).name}")
    
    if not non_rasa_imports:
        print("  No non-Rasa AI library imports detected.")
    
    # Custom AI Implementations
    print("\n🧠 CUSTOM AI IMPLEMENTATIONS:")
    print("-" * 50)
    custom_implementations = findings.get('custom_ai_classes', [])
    for impl in custom_implementations:
        print(f"  • Class '{impl['class_name']}' in {Path(impl['file']).name} (line {impl['line']})")
        print(f"    Description: Custom AI class matching pattern '{impl['pattern_matched']}'")
    
    if not custom_implementations:
        print("  No custom AI implementations detected.")
    
    # AI Functions
    print("\n⚙️  AI-RELATED FUNCTIONS:")
    print("-" * 50)
    ai_functions = findings.get('ai_functions', [])
    fractal_functions = [f for f in ai_functions if 'fractal' in f['file'].lower()]
    for func in fractal_functions:
        print(f"  • {func['function_name']}() in {Path(func['file']).name} (line {func['line']})")
    
    # Dependencies
    print("\n📦 NON-RASA AI DEPENDENCIES:")
    print("-" * 50)
    non_rasa_deps = []
    for dep in findings.get('ai_dependencies', []):
        if dep['detected_library'] not in rasa_related:
            non_rasa_deps.append(dep)
            print(f"  • {dep['dependency']}")
    
    if not non_rasa_deps:
        print("  No non-Rasa AI dependencies detected.")
    
    # Summary
    total_non_rasa = len(non_rasa_imports) + len(custom_implementations) + len(fractal_functions) + len(non_rasa_deps)
    print(f"\n📊 SUMMARY:")
    print(f"   Total non-Rasa AI findings: {total_non_rasa}")
    print(f"   - Non-Rasa AI libraries: {len(non_rasa_imports)}")
    print(f"   - Custom AI implementations: {len(custom_implementations)}")
    print(f"   - AI-related functions: {len(fractal_functions)}")
    print(f"   - Non-Rasa AI dependencies: {len(non_rasa_deps)}")
    
    return findings

if __name__ == "__main__":
    # Run the summary report
    generate_non_rasa_summary_report()
    
    # Run the unit tests
    print("\n" + "="*80)
    print("RUNNING NON-RASA AI DETECTION TESTS")
    print("="*80)
    unittest.main(verbosity=2)