#!/usr/bin/env python3
"""
AI Framework Detection Test Suite
=================================
Comprehensive test suite to detect the presence and usage of any AI frameworks, 
libraries, or custom AI implementations in the Teacher1 repository.

This test suite checks for:
- Common AI/ML library imports (TensorFlow, PyTorch, scikit-learn, OpenAI, HuggingFace, etc.)
- Custom AI implementations and classes
- Dependency declarations in requirements files
- AI-related function calls and instantiations

Author: AI Assistant
Purpose: Detect non-Rasa AI code in Teacher1 repository
"""

import ast
import os
import re
import sys
from pathlib import Path
from typing import Dict, List, Set, Tuple, Any
import json
from collections import defaultdict

class AIFrameworkDetector:
    """
    Main class for detecting AI frameworks and implementations across the repository.
    """
    
    def __init__(self, repo_path: str):
        self.repo_path = Path(repo_path)
        self.findings = defaultdict(list)
        self.ai_libraries = {
            # Deep Learning Frameworks
            'tensorflow', 'tf', 'keras', 
            'torch', 'pytorch', 'torchvision', 'torchaudio',
            'jax', 'flax', 'haiku',
            'mxnet', 'gluon',
            'paddle', 'paddlepaddle',
            'oneflow',
            
            # Traditional ML Libraries
            'sklearn', 'scikit-learn', 'scikit_learn',
            'xgboost', 'lightgbm', 'catboost',
            'statsmodels',
            
            # NLP Libraries (beyond spaCy which is Rasa dependency)
            'nltk', 'gensim', 'textblob',
            'transformers', 'huggingface', 'huggingface_hub',
            'sentence_transformers',
            'openai', 'anthropic',
            
            # Computer Vision
            'cv2', 'opencv', 'PIL', 'pillow', 'skimage', 'imageio',
            
            # Reinforcement Learning
            'gym', 'gymnasium', 'stable_baselines3', 'ray', 'rllib',
            
            # Audio Processing
            'librosa', 'torchaudio', 'speechrecognition',
            
            # Numerical/Scientific (AI-adjacent)
            'numpy', 'scipy', 'pandas', 'matplotlib', 'seaborn', 'plotly',
            
            # Other AI/ML Tools
            'mlflow', 'wandb', 'tensorboard',
            'optuna', 'hyperopt',
            'dask',
        }
        
        # Custom AI class patterns (case-insensitive)
        self.ai_class_patterns = [
            r'.*ai.*', r'.*neural.*', r'.*network.*', r'.*model.*',
            r'.*learn.*', r'.*train.*', r'.*predict.*', r'.*classify.*',
            r'.*agent.*', r'.*bot.*', r'.*chat.*', r'.*fractal.*',
            r'.*emergent.*', r'.*cognitive.*', r'.*intelligence.*'
        ]
        
        # AI-related function patterns
        self.ai_function_patterns = [
            r'.*train.*', r'.*predict.*', r'.*classify.*', r'.*learn.*',
            r'.*neural.*', r'.*network.*', r'.*model.*', r'.*ai.*',
            r'.*attention.*', r'.*embedding.*', r'.*feature.*',
            r'.*optimize.*', r'.*gradient.*', r'.*backprop.*'
        ]

    def scan_repository(self) -> Dict[str, Any]:
        """
        Perform comprehensive scan of the repository for AI frameworks and implementations.
        """
        print(f"🔍 Scanning repository: {self.repo_path}")
        
        # Scan Python files
        python_files = list(self.repo_path.rglob("*.py"))
        print(f"Found {len(python_files)} Python files to analyze")
        
        for py_file in python_files:
            try:
                self._analyze_python_file(py_file)
            except Exception as e:
                self.findings['errors'].append({
                    'file': str(py_file),
                    'error': str(e),
                    'type': 'file_analysis_error'
                })
        
        # Scan dependency files
        self._scan_dependency_files()
        
        # Scan configuration files
        self._scan_config_files()
        
        return dict(self.findings)

    def _analyze_python_file(self, file_path: Path):
        """
        Analyze a single Python file for AI-related imports, classes, and functions.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Parse AST for detailed analysis
            try:
                tree = ast.parse(content)
                self._analyze_ast(tree, file_path)
            except SyntaxError:
                # If AST parsing fails, fall back to regex analysis
                self._analyze_with_regex(content, file_path)
                
        except Exception as e:
            self.findings['errors'].append({
                'file': str(file_path),
                'error': str(e),
                'type': 'file_read_error'
            })

    def _analyze_ast(self, tree: ast.AST, file_path: Path):
        """
        Analyze Python AST for imports, class definitions, and function calls.
        """
        class AIAnalysisVisitor(ast.NodeVisitor):
            def __init__(self, detector, file_path):
                self.detector = detector
                self.file_path = file_path
                
            def visit_Import(self, node):
                for alias in node.names:
                    self._check_import(alias.name, alias.asname)
                self.generic_visit(node)
                
            def visit_ImportFrom(self, node):
                module = node.module or ''
                for alias in node.names:
                    full_import = f"{module}.{alias.name}" if module else alias.name
                    self._check_import(full_import, alias.asname, module)
                self.generic_visit(node)
                
            def visit_ClassDef(self, node):
                self._check_class_definition(node)
                self.generic_visit(node)
                
            def visit_FunctionDef(self, node):
                self._check_function_definition(node)
                self.generic_visit(node)
                
            def visit_Call(self, node):
                self._check_function_call(node)
                self.generic_visit(node)
                
            def _check_import(self, import_name: str, alias: str = None, module: str = None):
                import_lower = import_name.lower()
                
                # Check for AI library imports
                for ai_lib in self.detector.ai_libraries:
                    if ai_lib in import_lower or (module and ai_lib in module.lower()):
                        self.detector.findings['ai_imports'].append({
                            'file': str(self.file_path),
                            'import': import_name,
                            'alias': alias,
                            'module': module,
                            'detected_library': ai_lib,
                            'line': getattr(node, 'lineno', 'unknown') if hasattr(self, 'node') else 'unknown'
                        })
                        
            def _check_class_definition(self, node):
                class_name = node.name.lower()
                
                # Check for AI-related class names
                for pattern in self.detector.ai_class_patterns:
                    if re.match(pattern, class_name):
                        self.detector.findings['custom_ai_classes'].append({
                            'file': str(self.file_path),
                            'class_name': node.name,
                            'line': node.lineno,
                            'pattern_matched': pattern,
                            'base_classes': [self._get_name(base) for base in node.bases]
                        })
                        break
                        
            def _check_function_definition(self, node):
                func_name = node.name.lower()
                
                # Check for AI-related function names
                for pattern in self.detector.ai_function_patterns:
                    if re.match(pattern, func_name):
                        self.detector.findings['ai_functions'].append({
                            'file': str(self.file_path),
                            'function_name': node.name,
                            'line': node.lineno,
                            'pattern_matched': pattern,
                            'args': [arg.arg for arg in node.args.args]
                        })
                        break
                        
            def _check_function_call(self, node):
                func_name = self._get_name(node.func)
                if func_name:
                    func_name_lower = func_name.lower()
                    
                    # Check for AI-related function calls
                    for pattern in self.detector.ai_function_patterns:
                        if re.match(pattern, func_name_lower):
                            self.detector.findings['ai_function_calls'].append({
                                'file': str(self.file_path),
                                'function_call': func_name,
                                'line': node.lineno,
                                'pattern_matched': pattern
                            })
                            break
                            
            def _get_name(self, node):
                """Extract name from AST node."""
                if isinstance(node, ast.Name):
                    return node.id
                elif isinstance(node, ast.Attribute):
                    value = self._get_name(node.value)
                    return f"{value}.{node.attr}" if value else node.attr
                return None
        
        visitor = AIAnalysisVisitor(self, file_path)
        visitor.visit(tree)

    def _analyze_with_regex(self, content: str, file_path: Path):
        """
        Fallback regex-based analysis when AST parsing fails.
        """
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            # Check imports
            import_match = re.match(r'^\s*(?:from\s+(\S+)\s+)?import\s+(.+)', line)
            if import_match:
                module, imports = import_match.groups()
                import_text = f"{module}.{imports}" if module else imports
                
                for ai_lib in self.ai_libraries:
                    if ai_lib in import_text.lower():
                        self.findings['ai_imports'].append({
                            'file': str(file_path),
                            'import': import_text,
                            'line': line_num,
                            'detected_library': ai_lib,
                            'analysis_method': 'regex'
                        })
            
            # Check class definitions
            class_match = re.match(r'^\s*class\s+(\w+)', line)
            if class_match:
                class_name = class_match.group(1)
                class_name_lower = class_name.lower()
                
                for pattern in self.ai_class_patterns:
                    if re.match(pattern, class_name_lower):
                        self.findings['custom_ai_classes'].append({
                            'file': str(file_path),
                            'class_name': class_name,
                            'line': line_num,
                            'pattern_matched': pattern,
                            'analysis_method': 'regex'
                        })
                        break

    def _scan_dependency_files(self):
        """
        Scan dependency files like requirements.txt, setup.py, pyproject.toml, etc.
        """
        dependency_files = [
            'requirements.txt', 'requirements-dev.txt', 'requirements-test.txt',
            'setup.py', 'setup.cfg', 'pyproject.toml', 'Pipfile', 'environment.yml'
        ]
        
        for dep_file in dependency_files:
            file_path = self.repo_path / dep_file
            if file_path.exists():
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    self._analyze_dependency_content(content, file_path)
                except Exception as e:
                    self.findings['errors'].append({
                        'file': str(file_path),
                        'error': str(e),
                        'type': 'dependency_file_error'
                    })

    def _analyze_dependency_content(self, content: str, file_path: Path):
        """
        Analyze dependency file content for AI libraries.
        """
        lines = content.split('\n')
        
        for line_num, line in enumerate(lines, 1):
            line = line.strip()
            if not line or line.startswith('#'):
                continue
                
            # Extract package name (handle various formats)
            package_match = re.match(r'([a-zA-Z0-9_-]+)', line)
            if package_match:
                package_name = package_match.group(1).lower()
                
                for ai_lib in self.ai_libraries:
                    if ai_lib == package_name or package_name.replace('-', '_') == ai_lib:
                        self.findings['ai_dependencies'].append({
                            'file': str(file_path),
                            'dependency': line,
                            'detected_library': ai_lib,
                            'line': line_num
                        })

    def _scan_config_files(self):
        """
        Scan configuration files for AI-related settings.
        """
        config_patterns = ['*.yml', '*.yaml', '*.json', '*.toml', '*.cfg', '*.ini']
        
        for pattern in config_patterns:
            for config_file in self.repo_path.rglob(pattern):
                if config_file.is_file():
                    try:
                        with open(config_file, 'r', encoding='utf-8') as f:
                            content = f.read().lower()
                        
                        # Check for AI-related keywords in config files
                        ai_keywords = ['tensorflow', 'pytorch', 'neural', 'model', 'train', 'predict']
                        for keyword in ai_keywords:
                            if keyword in content:
                                self.findings['ai_configs'].append({
                                    'file': str(config_file),
                                    'keyword': keyword,
                                    'type': 'config_file'
                                })
                    except:
                        # Skip files that can't be read as text
                        pass

    def generate_report(self) -> str:
        """
        Generate a comprehensive report of all AI framework findings.
        """
        report = []
        report.append("=" * 80)
        report.append("AI FRAMEWORK DETECTION REPORT")
        report.append("=" * 80)
        report.append(f"Repository: {self.repo_path}")
        report.append(f"Scan Date: {__import__('datetime').datetime.now()}")
        report.append("")
        
        # Summary
        total_findings = sum(len(findings) for key, findings in self.findings.items() if key != 'errors')
        report.append(f"SUMMARY: {total_findings} AI-related findings detected")
        report.append("")
        
        # AI Library Imports
        if self.findings['ai_imports']:
            report.append("🔍 AI LIBRARY IMPORTS:")
            report.append("-" * 40)
            for finding in self.findings['ai_imports']:
                report.append(f"  File: {finding['file']}")
                report.append(f"  Import: {finding['import']}")
                report.append(f"  Detected Library: {finding['detected_library']}")
                report.append(f"  Line: {finding.get('line', 'unknown')}")
                report.append("")
        
        # Custom AI Classes
        if self.findings['custom_ai_classes']:
            report.append("🧠 CUSTOM AI CLASSES:")
            report.append("-" * 40)
            for finding in self.findings['custom_ai_classes']:
                report.append(f"  File: {finding['file']}")
                report.append(f"  Class: {finding['class_name']}")
                report.append(f"  Line: {finding['line']}")
                report.append(f"  Pattern: {finding['pattern_matched']}")
                if finding.get('base_classes'):
                    report.append(f"  Base Classes: {', '.join(finding['base_classes'])}")
                report.append("")
        
        # AI Functions
        if self.findings['ai_functions']:
            report.append("⚙️ AI FUNCTIONS:")
            report.append("-" * 40)
            for finding in self.findings['ai_functions']:
                report.append(f"  File: {finding['file']}")
                report.append(f"  Function: {finding['function_name']}")
                report.append(f"  Line: {finding['line']}")
                report.append(f"  Pattern: {finding['pattern_matched']}")
                report.append("")
        
        # AI Dependencies
        if self.findings['ai_dependencies']:
            report.append("📦 AI DEPENDENCIES:")
            report.append("-" * 40)
            for finding in self.findings['ai_dependencies']:
                report.append(f"  File: {finding['file']}")
                report.append(f"  Dependency: {finding['dependency']}")
                report.append(f"  Detected Library: {finding['detected_library']}")
                report.append("")
        
        # Function Calls
        if self.findings['ai_function_calls']:
            report.append("📞 AI FUNCTION CALLS:")
            report.append("-" * 40)
            for finding in self.findings['ai_function_calls']:
                report.append(f"  File: {finding['file']}")
                report.append(f"  Function Call: {finding['function_call']}")
                report.append(f"  Line: {finding['line']}")
                report.append("")
        
        # Configuration Files
        if self.findings['ai_configs']:
            report.append("⚙️ AI CONFIGURATION FILES:")
            report.append("-" * 40)
            for finding in self.findings['ai_configs']:
                report.append(f"  File: {finding['file']}")
                report.append(f"  Keyword: {finding['keyword']}")
                report.append("")
        
        # Errors
        if self.findings['errors']:
            report.append("❌ ANALYSIS ERRORS:")
            report.append("-" * 40)
            for error in self.findings['errors']:
                report.append(f"  File: {error['file']}")
                report.append(f"  Error: {error['error']}")
                report.append(f"  Type: {error['type']}")
                report.append("")
        
        return "\n".join(report)

def run_ai_detection_tests(repo_path: str = None):
    """
    Main function to run the AI framework detection tests.
    """
    if repo_path is None:
        repo_path = os.getcwd()
    
    print("🎯 Starting AI Framework Detection Test Suite")
    print("=" * 60)
    
    detector = AIFrameworkDetector(repo_path)
    findings = detector.scan_repository()
    
    # Generate and print report
    report = detector.generate_report()
    print(report)
    
    # Save report to file
    report_file = Path(repo_path) / 'ai_framework_detection_report.txt'
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write(report)
    
    print(f"\n📄 Report saved to: {report_file}")
    
    # Save detailed findings as JSON
    json_file = Path(repo_path) / 'ai_framework_findings.json'
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(findings, f, indent=2, default=str)
    
    print(f"📄 Detailed findings saved to: {json_file}")
    
    return findings

if __name__ == "__main__":
    # Run the tests
    repo_path = sys.argv[1] if len(sys.argv) > 1 else None
    run_ai_detection_tests(repo_path)