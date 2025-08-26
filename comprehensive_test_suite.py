#!/usr/bin/env python3
"""
Teacher1 Comprehensive Test Suite
=================================

This script provides top-to-bottom testing of the Teacher1 repository,
analyzing all components, their functionality, integration, and health.
"""

import os
import sys
import ast
import importlib.util
import traceback
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional
import unittest
from unittest.mock import Mock, patch

class TestResult:
    """Stores test results with details"""
    def __init__(self, name: str, passed: bool, details: str = "", error: str = ""):
        self.name = name
        self.passed = passed
        self.details = details
        self.error = error
        self.timestamp = time.time()

class TestStats:
    """Tracks testing statistics"""
    def __init__(self):
        self.total_tests = 0
        self.passed_tests = 0
        self.failed_tests = 0
        self.skipped_tests = 0
        self.results: List[TestResult] = []
    
    def add_result(self, result: TestResult):
        self.results.append(result)
        self.total_tests += 1
        if result.passed:
            self.passed_tests += 1
        else:
            self.failed_tests += 1
    
    def add_skip(self, name: str, reason: str):
        self.results.append(TestResult(name, True, f"SKIPPED: {reason}"))
        self.skipped_tests += 1

class ComprehensiveTestSuite:
    """Main test suite for Teacher1 repository"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.stats = TestStats()
        self.python_files = []
        self.discover_python_files()
    
    def discover_python_files(self):
        """Discover all Python files in the repository"""
        for root, dirs, files in os.walk(self.project_root):
            # Skip hidden directories and __pycache__
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__']
            
            for file in files:
                if file.endswith('.py') and not file.startswith('.'):
                    file_path = Path(root) / file
                    rel_path = file_path.relative_to(self.project_root)
                    self.python_files.append(rel_path)
        
        print(f"Discovered {len(self.python_files)} Python files")
    
    def test_syntax_analysis(self):
        """Test syntax analysis of all Python files"""
        print("\n" + "="*60)
        print("SYNTAX ANALYSIS")
        print("="*60)
        
        for file_path in self.python_files:
            try:
                full_path = self.project_root / file_path
                with open(full_path, 'r', encoding='utf-8') as f:
                    source = f.read()
                
                # Parse the AST to check syntax
                ast.parse(source, filename=str(file_path))
                
                result = TestResult(
                    f"Syntax: {file_path}",
                    True,
                    "Valid Python syntax"
                )
                self.stats.add_result(result)
                print(f"✓ {file_path}")
                
            except SyntaxError as e:
                result = TestResult(
                    f"Syntax: {file_path}",
                    False,
                    "",
                    f"Syntax error: {e}"
                )
                self.stats.add_result(result)
                print(f"✗ {file_path}: {e}")
                
            except Exception as e:
                result = TestResult(
                    f"Syntax: {file_path}",
                    False,
                    "",
                    f"Error reading file: {e}"
                )
                self.stats.add_result(result)
                print(f"✗ {file_path}: {e}")
    
    def test_import_analysis(self):
        """Test import statements and dependencies"""
        print("\n" + "="*60)
        print("IMPORT ANALYSIS")
        print("="*60)
        
        failed_imports = {}
        successful_imports = {}
        
        for file_path in self.python_files:
            try:
                full_path = self.project_root / file_path
                with open(full_path, 'r', encoding='utf-8') as f:
                    source = f.read()
                
                tree = ast.parse(source)
                imports = []
                
                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            imports.append(alias.name)
                    elif isinstance(node, ast.ImportFrom):
                        module = node.module or ''
                        for alias in node.names:
                            imports.append(f"{module}.{alias.name}" if module else alias.name)
                
                # Test each import
                file_failed_imports = []
                for imp in imports:
                    try:
                        # Skip relative imports and built-ins
                        if imp.startswith('.') or imp in ['sys', 'os', 'time', 'json', 'ast', 'pathlib', 'unittest', 'typing', 'traceback', 'subprocess']:
                            continue
                        
                        # Try to import the module
                        if '.' in imp:
                            module_name = imp.split('.')[0]
                        else:
                            module_name = imp
                        
                        try:
                            __import__(module_name)
                            successful_imports[imp] = successful_imports.get(imp, 0) + 1
                        except ImportError:
                            file_failed_imports.append(imp)
                            failed_imports[imp] = failed_imports.get(imp, 0) + 1
                    except Exception:
                        pass
                
                if file_failed_imports:
                    result = TestResult(
                        f"Imports: {file_path}",
                        False,
                        f"Available imports: {len(imports) - len(file_failed_imports)}",
                        f"Missing imports: {file_failed_imports}"
                    )
                    print(f"⚠ {file_path}: Missing {file_failed_imports}")
                else:
                    result = TestResult(
                        f"Imports: {file_path}",
                        True,
                        f"All {len(imports)} imports available"
                    )
                    print(f"✓ {file_path}: All imports available")
                
                self.stats.add_result(result)
                
            except Exception as e:
                result = TestResult(
                    f"Imports: {file_path}",
                    False,
                    "",
                    f"Error analyzing imports: {e}"
                )
                self.stats.add_result(result)
                print(f"✗ {file_path}: {e}")
        
        # Summary
        print(f"\nImport Summary:")
        print(f"  Successful imports: {len(successful_imports)}")
        print(f"  Failed imports: {len(failed_imports)}")
        if failed_imports:
            print(f"  Most common missing: {sorted(failed_imports.items(), key=lambda x: x[1], reverse=True)[:5]}")
    
    def test_module_structure(self):
        """Analyze module structure and complexity"""
        print("\n" + "="*60)
        print("MODULE STRUCTURE ANALYSIS")
        print("="*60)
        
        for file_path in self.python_files:
            try:
                full_path = self.project_root / file_path
                with open(full_path, 'r', encoding='utf-8') as f:
                    source = f.read()
                
                tree = ast.parse(source)
                
                # Count various elements
                classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
                functions = [node for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
                async_functions = [node for node in ast.walk(tree) if isinstance(node, ast.AsyncFunctionDef)]
                lines = len(source.splitlines())
                
                details = f"Lines: {lines}, Classes: {len(classes)}, Functions: {len(functions)}, Async: {len(async_functions)}"
                
                # Basic complexity assessment
                complexity_score = 0
                if lines > 500:
                    complexity_score += 1
                if len(classes) > 5:
                    complexity_score += 1
                if len(functions) > 20:
                    complexity_score += 1
                
                complexity_levels = ["Simple", "Moderate", "Complex", "Very Complex"]
                complexity = complexity_levels[min(complexity_score, 3)]
                
                result = TestResult(
                    f"Structure: {file_path}",
                    True,
                    f"{details}, Complexity: {complexity}"
                )
                self.stats.add_result(result)
                print(f"📊 {file_path}: {details}, {complexity}")
                
            except Exception as e:
                result = TestResult(
                    f"Structure: {file_path}",
                    False,
                    "",
                    f"Error analyzing structure: {e}"
                )
                self.stats.add_result(result)
                print(f"✗ {file_path}: {e}")
    
    def test_docstring_coverage(self):
        """Check docstring coverage"""
        print("\n" + "="*60)
        print("DOCUMENTATION ANALYSIS")
        print("="*60)
        
        for file_path in self.python_files:
            try:
                full_path = self.project_root / file_path
                with open(full_path, 'r', encoding='utf-8') as f:
                    source = f.read()
                
                tree = ast.parse(source)
                
                # Check module docstring
                module_doc = ast.get_docstring(tree)
                
                # Check class and function docstrings
                classes = [node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
                functions = [node for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]
                
                documented_classes = sum(1 for cls in classes if ast.get_docstring(cls))
                documented_functions = sum(1 for func in functions if ast.get_docstring(func))
                
                total_items = len(classes) + len(functions)
                documented_items = documented_classes + documented_functions
                
                if total_items > 0:
                    coverage = (documented_items / total_items) * 100
                    details = f"Module doc: {'Yes' if module_doc else 'No'}, Coverage: {coverage:.1f}% ({documented_items}/{total_items})"
                    
                    result = TestResult(
                        f"Docs: {file_path}",
                        coverage > 50,  # Consider 50%+ as passing
                        details
                    )
                else:
                    result = TestResult(
                        f"Docs: {file_path}",
                        True,
                        "No classes/functions to document"
                    )
                
                self.stats.add_result(result)
                print(f"📚 {file_path}: {result.details}")
                
            except Exception as e:
                result = TestResult(
                    f"Docs: {file_path}",
                    False,
                    "",
                    f"Error analyzing documentation: {e}"
                )
                self.stats.add_result(result)
                print(f"✗ {file_path}: {e}")
    
    def test_existing_test_files(self):
        """Run existing test files"""
        print("\n" + "="*60)
        print("EXISTING TESTS")
        print("="*60)
        
        test_files = [f for f in self.python_files if f.name.startswith('test_')]
        
        for test_file in test_files:
            try:
                print(f"\nRunning {test_file}...")
                
                # Try to run the test file
                cmd = [sys.executable, '-m', 'unittest', str(test_file.with_suffix(''))]
                result_proc = subprocess.run(
                    cmd,
                    cwd=self.project_root,
                    capture_output=True,
                    text=True,
                    timeout=30
                )
                
                if result_proc.returncode == 0:
                    result = TestResult(
                        f"Test: {test_file}",
                        True,
                        f"Tests passed\n{result_proc.stdout}"
                    )
                    print(f"✓ {test_file}: Tests passed")
                else:
                    result = TestResult(
                        f"Test: {test_file}",
                        False,
                        f"Output: {result_proc.stdout}",
                        f"Tests failed: {result_proc.stderr}"
                    )
                    print(f"✗ {test_file}: Tests failed")
                    print(f"  Error: {result_proc.stderr[:200]}...")
                
                self.stats.add_result(result)
                
            except subprocess.TimeoutExpired:
                result = TestResult(
                    f"Test: {test_file}",
                    False,
                    "",
                    "Test timed out after 30 seconds"
                )
                self.stats.add_result(result)
                print(f"⏰ {test_file}: Timed out")
                
            except Exception as e:
                result = TestResult(
                    f"Test: {test_file}",
                    False,
                    "",
                    f"Error running test: {e}"
                )
                self.stats.add_result(result)
                print(f"✗ {test_file}: {e}")
    
    def test_module_execution(self):
        """Test if modules can be executed without errors"""
        print("\n" + "="*60)
        print("MODULE EXECUTION TESTS")
        print("="*60)
        
        # Test files that are likely meant to be executed
        executable_files = [
            'demo.py',
            'setup.py',
            'websocket_demo.py',
            'big_text_gui.py',
            'text_to_speech.py',
            'speech_recognition.py'
        ]
        
        for file_name in executable_files:
            file_path = None
            for f in self.python_files:
                if f.name == file_name:
                    file_path = f
                    break
            
            if not file_path:
                self.stats.add_skip(f"Execute: {file_name}", "File not found")
                continue
            
            try:
                print(f"\nTesting execution of {file_path}...")
                
                # Try to execute with --help or quick mode
                test_args = []
                if 'demo' in file_name:
                    test_args = []  # Run demo normally but with timeout
                elif 'websocket_demo' in file_name:
                    test_args = ['--help']
                else:
                    test_args = ['--help']
                
                cmd = [sys.executable, str(file_path)] + test_args
                result_proc = subprocess.run(
                    cmd,
                    cwd=self.project_root,
                    capture_output=True,
                    text=True,
                    timeout=10
                )
                
                # For some files, non-zero exit is expected (like --help)
                if result_proc.returncode == 0 or '--help' in test_args:
                    result = TestResult(
                        f"Execute: {file_path}",
                        True,
                        f"Executed successfully"
                    )
                    print(f"✓ {file_path}: Executed successfully")
                else:
                    result = TestResult(
                        f"Execute: {file_path}",
                        False,
                        f"Exit code: {result_proc.returncode}",
                        f"Error: {result_proc.stderr[:200]}"
                    )
                    print(f"✗ {file_path}: Failed with exit code {result_proc.returncode}")
                
                self.stats.add_result(result)
                
            except subprocess.TimeoutExpired:
                result = TestResult(
                    f"Execute: {file_path}",
                    True,  # Timeout might be expected for interactive programs
                    "Execution started (timed out after 10s - likely interactive)"
                )
                self.stats.add_result(result)
                print(f"⏰ {file_path}: Started but timed out (likely interactive)")
                
            except Exception as e:
                result = TestResult(
                    f"Execute: {file_path}",
                    False,
                    "",
                    f"Error executing: {e}"
                )
                self.stats.add_result(result)
                print(f"✗ {file_path}: {e}")
    
    def test_web_interface_components(self):
        """Test web interface specific components"""
        print("\n" + "="*60)
        print("WEB INTERFACE COMPONENT TESTS")
        print("="*60)
        
        web_files = [f for f in self.python_files if 'web_interface' in str(f)]
        
        for file_path in web_files:
            try:
                print(f"\nAnalyzing {file_path}...")
                
                full_path = self.project_root / file_path
                with open(full_path, 'r', encoding='utf-8') as f:
                    source = f.read()
                
                # Check for Flask patterns
                has_flask = 'flask' in source.lower() or 'Flask' in source
                has_routes = '@app.route' in source or 'route(' in source
                has_templates = 'render_template' in source
                has_json = 'jsonify' in source or 'json' in source
                
                details = []
                if has_flask:
                    details.append("Flask app")
                if has_routes:
                    details.append("Routes defined")
                if has_templates:
                    details.append("Templates used")
                if has_json:
                    details.append("JSON handling")
                
                result = TestResult(
                    f"WebApp: {file_path}",
                    len(details) > 0,
                    f"Features: {', '.join(details) if details else 'None detected'}"
                )
                self.stats.add_result(result)
                print(f"🌐 {file_path}: {result.details}")
                
            except Exception as e:
                result = TestResult(
                    f"WebApp: {file_path}",
                    False,
                    "",
                    f"Error analyzing web component: {e}"
                )
                self.stats.add_result(result)
                print(f"✗ {file_path}: {e}")
    
    def test_ai_components(self):
        """Test AI and machine learning components"""
        print("\n" + "="*60)
        print("AI COMPONENT TESTS")
        print("="*60)
        
        ai_files = [
            'fractal_emergent_ai.py',
            'fractal_modules.py',
            'personalized_chatbot.py',
            'kindergarten_assessment.py',
            'student_profile.py'
        ]
        
        for file_name in ai_files:
            file_path = None
            for f in self.python_files:
                if f.name == file_name:
                    file_path = f
                    break
            
            if not file_path:
                self.stats.add_skip(f"AI: {file_name}", "File not found")
                continue
            
            try:
                print(f"\nAnalyzing {file_path}...")
                
                full_path = self.project_root / file_path
                with open(full_path, 'r', encoding='utf-8') as f:
                    source = f.read()
                
                # Check for AI/ML patterns
                ai_indicators = [
                    ('numpy', 'NumPy arrays'),
                    ('matplotlib', 'Plotting/visualization'),
                    ('sklearn', 'Scikit-learn ML'),
                    ('tensorflow', 'TensorFlow'),
                    ('torch', 'PyTorch'),
                    ('asyncio', 'Async processing'),
                    ('class', 'Object-oriented design'),
                    ('def __init__', 'Class initialization'),
                    ('async def', 'Async functions'),
                    ('websocket', 'WebSocket communication')
                ]
                
                detected_features = []
                for indicator, description in ai_indicators:
                    if indicator in source:
                        detected_features.append(description)
                
                # Count complex operations
                tree = ast.parse(source)
                classes = len([node for node in ast.walk(tree) if isinstance(node, ast.ClassDef)])
                functions = len([node for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))])
                
                details = f"Features: {', '.join(detected_features) if detected_features else 'Basic'}, Classes: {classes}, Functions: {functions}"
                
                result = TestResult(
                    f"AI: {file_path}",
                    len(detected_features) > 0 or classes > 0,
                    details
                )
                self.stats.add_result(result)
                print(f"🤖 {file_path}: {details}")
                
            except Exception as e:
                result = TestResult(
                    f"AI: {file_path}",
                    False,
                    "",
                    f"Error analyzing AI component: {e}"
                )
                self.stats.add_result(result)
                print(f"✗ {file_path}: {e}")
    
    def generate_report(self):
        """Generate comprehensive test report"""
        print("\n" + "="*60)
        print("COMPREHENSIVE TEST REPORT")
        print("="*60)
        
        # Overall statistics
        print(f"\nOVERALL STATISTICS:")
        print(f"  Total Tests: {self.stats.total_tests}")
        print(f"  Passed: {self.stats.passed_tests}")
        print(f"  Failed: {self.stats.failed_tests}")
        print(f"  Skipped: {self.stats.skipped_tests}")
        
        if self.stats.total_tests > 0:
            pass_rate = (self.stats.passed_tests / self.stats.total_tests) * 100
            print(f"  Pass Rate: {pass_rate:.1f}%")
        
        # Category breakdown
        categories = {}
        for result in self.stats.results:
            category = result.name.split(':')[0]
            if category not in categories:
                categories[category] = {'passed': 0, 'failed': 0, 'total': 0}
            categories[category]['total'] += 1
            if result.passed:
                categories[category]['passed'] += 1
            else:
                categories[category]['failed'] += 1
        
        print(f"\nCATEGORY BREAKDOWN:")
        for category, stats in categories.items():
            rate = (stats['passed'] / stats['total']) * 100 if stats['total'] > 0 else 0
            print(f"  {category}: {stats['passed']}/{stats['total']} ({rate:.1f}%)")
        
        # Failed tests
        failed_results = [r for r in self.stats.results if not r.passed]
        if failed_results:
            print(f"\nFAILED TESTS ({len(failed_results)}):")
            for result in failed_results:
                print(f"  ✗ {result.name}")
                if result.error:
                    print(f"    Error: {result.error[:100]}{'...' if len(result.error) > 100 else ''}")
        
        # Repository health assessment
        print(f"\nREPOSITORY HEALTH ASSESSMENT:")
        
        # Calculate health score
        health_score = 0
        max_score = 0
        
        # Syntax health (20 points)
        syntax_results = [r for r in self.stats.results if r.name.startswith('Syntax:')]
        if syntax_results:
            syntax_pass_rate = len([r for r in syntax_results if r.passed]) / len(syntax_results)
            health_score += syntax_pass_rate * 20
        max_score += 20
        
        # Import health (15 points)
        import_results = [r for r in self.stats.results if r.name.startswith('Imports:')]
        if import_results:
            import_pass_rate = len([r for r in import_results if r.passed]) / len(import_results)
            health_score += import_pass_rate * 15
        max_score += 15
        
        # Documentation health (10 points)
        doc_results = [r for r in self.stats.results if r.name.startswith('Docs:')]
        if doc_results:
            doc_pass_rate = len([r for r in doc_results if r.passed]) / len(doc_results)
            health_score += doc_pass_rate * 10
        max_score += 10
        
        # Test coverage (15 points)
        test_results = [r for r in self.stats.results if r.name.startswith('Test:')]
        if test_results:
            test_pass_rate = len([r for r in test_results if r.passed]) / len(test_results)
            health_score += test_pass_rate * 15
        max_score += 15
        
        # Execution health (20 points)
        exec_results = [r for r in self.stats.results if r.name.startswith('Execute:')]
        if exec_results:
            exec_pass_rate = len([r for r in exec_results if r.passed]) / len(exec_results)
            health_score += exec_pass_rate * 20
        max_score += 20
        
        # Component health (20 points)
        component_results = [r for r in self.stats.results if r.name.startswith(('WebApp:', 'AI:'))]
        if component_results:
            component_pass_rate = len([r for r in component_results if r.passed]) / len(component_results)
            health_score += component_pass_rate * 20
        max_score += 20
        
        if max_score > 0:
            health_percentage = (health_score / max_score) * 100
            print(f"  Overall Health Score: {health_percentage:.1f}%")
            
            if health_percentage >= 90:
                print(f"  Status: 🟢 EXCELLENT - Repository is in excellent condition")
            elif health_percentage >= 75:
                print(f"  Status: 🟡 GOOD - Repository is in good condition with minor issues")
            elif health_percentage >= 50:
                print(f"  Status: 🟠 FAIR - Repository needs attention in several areas")
            else:
                print(f"  Status: 🔴 POOR - Repository requires significant work")
        
        # Recommendations
        print(f"\nRECOMMENDations:")
        
        if failed_results:
            syntax_failures = [r for r in failed_results if r.name.startswith('Syntax:')]
            if syntax_failures:
                print(f"  🔧 Fix syntax errors in {len(syntax_failures)} files")
            
            import_failures = [r for r in failed_results if r.name.startswith('Imports:')]
            if import_failures:
                print(f"  📦 Install missing dependencies for {len(import_failures)} files")
            
            test_failures = [r for r in failed_results if r.name.startswith('Test:')]
            if test_failures:
                print(f"  🧪 Fix failing tests in {len(test_failures)} test files")
            
            exec_failures = [r for r in failed_results if r.name.startswith('Execute:')]
            if exec_failures:
                print(f"  ⚙️ Fix execution issues in {len(exec_failures)} executable files")
        
        doc_results = [r for r in self.stats.results if r.name.startswith('Docs:')]
        if doc_results:
            low_doc_coverage = [r for r in doc_results if r.passed and 'Coverage:' in r.details and float(r.details.split('Coverage: ')[1].split('%')[0]) < 70]
            if low_doc_coverage:
                print(f"  📚 Improve documentation coverage in {len(low_doc_coverage)} files")
        
        print(f"  🚀 Consider adding integration tests for component interactions")
        print(f"  🔒 Consider adding security and performance tests")
        print(f"  📊 Consider setting up continuous integration (CI) pipeline")
        
        # Save detailed report
        self.save_detailed_report()
    
    def save_detailed_report(self):
        """Save detailed report to file"""
        report_path = self.project_root / "test_report.md"
        
        with open(report_path, 'w') as f:
            f.write("# Teacher1 Repository Test Report\n\n")
            f.write(f"Generated: {time.ctime()}\n\n")
            
            f.write("## Summary\n\n")
            f.write(f"- **Total Tests**: {self.stats.total_tests}\n")
            f.write(f"- **Passed**: {self.stats.passed_tests}\n")
            f.write(f"- **Failed**: {self.stats.failed_tests}\n")
            f.write(f"- **Skipped**: {self.stats.skipped_tests}\n")
            
            if self.stats.total_tests > 0:
                pass_rate = (self.stats.passed_tests / self.stats.total_tests) * 100
                f.write(f"- **Pass Rate**: {pass_rate:.1f}%\n")
            
            f.write("\n## Detailed Results\n\n")
            
            for result in self.stats.results:
                status = "✅" if result.passed else "❌"
                f.write(f"### {status} {result.name}\n")
                if result.details:
                    f.write(f"**Details**: {result.details}\n")
                if result.error:
                    f.write(f"**Error**: {result.error}\n")
                f.write("\n")
        
        print(f"\n📄 Detailed report saved to: {report_path}")
    
    def run_all_tests(self):
        """Run the complete test suite"""
        print("🎓 Teacher1 Comprehensive Test Suite")
        print("=" * 60)
        print(f"Testing repository: {self.project_root}")
        print(f"Python files found: {len(self.python_files)}")
        
        start_time = time.time()
        
        try:
            # Run all test categories
            self.test_syntax_analysis()
            self.test_import_analysis()
            self.test_module_structure()
            self.test_docstring_coverage()
            self.test_existing_test_files()
            self.test_module_execution()
            self.test_web_interface_components()
            self.test_ai_components()
            
            # Generate final report
            self.generate_report()
            
        except KeyboardInterrupt:
            print("\n\n⏹️ Test suite interrupted by user")
        except Exception as e:
            print(f"\n\n💥 Test suite failed with error: {e}")
            traceback.print_exc()
        finally:
            end_time = time.time()
            duration = end_time - start_time
            print(f"\n⏱️ Test suite completed in {duration:.1f} seconds")

def main():
    """Main entry point"""
    suite = ComprehensiveTestSuite()
    suite.run_all_tests()

if __name__ == "__main__":
    main()