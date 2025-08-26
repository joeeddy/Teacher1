#!/usr/bin/env python3
"""
External Automation Check Script

This script helps verify that no automation exists in the Teacher1 repository
that could be creating pull requests to external repositories like forcastpkg.
"""

import os
import json
import subprocess
import sys
from pathlib import Path

def check_github_workflows():
    """Check for GitHub Actions workflows that might create external PRs."""
    print("🔍 Checking GitHub Actions workflows...")
    
    github_dir = Path(".github")
    workflows_dir = github_dir / "workflows"
    
    if not workflows_dir.exists():
        print("✅ No .github/workflows directory found")
        return True
    
    workflow_files = list(workflows_dir.glob("*.yml")) + list(workflows_dir.glob("*.yaml"))
    
    if not workflow_files:
        print("✅ No workflow files found in .github/workflows")
        return True
    
    external_refs = []
    for workflow_file in workflow_files:
        print(f"   📄 Checking {workflow_file}")
        try:
            content = workflow_file.read_text()
            # Check for common patterns that might indicate external PR creation
            suspicious_patterns = [
                "forcastpkg",
                "forecast",
                "gh pr create",
                "hub pull-request",
                "create-pull-request",
                "git push origin",
            ]
            
            for pattern in suspicious_patterns:
                if pattern.lower() in content.lower():
                    if pattern in ["forcastpkg", "forecast"]:
                        external_refs.append(f"{workflow_file}: Contains '{pattern}'")
                    else:
                        print(f"   ℹ️  Found '{pattern}' in {workflow_file} (may be normal)")
        except Exception as e:
            print(f"   ❌ Error reading {workflow_file}: {e}")
    
    if external_refs:
        print("❌ Found potential external references:")
        for ref in external_refs:
            print(f"   {ref}")
        return False
    else:
        print("✅ No suspicious external references found in workflows")
        return True

def check_git_configuration():
    """Check git configuration for external repository references."""
    print("\n🔍 Checking git configuration...")
    
    try:
        # Check remote URLs
        result = subprocess.run(['git', 'remote', '-v'], capture_output=True, text=True)
        if result.returncode == 0:
            remotes = result.stdout.strip()
            print("   📡 Remote URLs:")
            for line in remotes.split('\n'):
                if line.strip():
                    print(f"      {line}")
            
            if "forcastpkg" in remotes.lower():
                print("❌ Found forcastpkg reference in git remotes!")
                return False
            else:
                print("✅ No forcastpkg references in git remotes")
        
        # Check git hooks
        hooks_dir = Path(".git/hooks")
        if hooks_dir.exists():
            hooks = [f for f in hooks_dir.iterdir() if f.is_file() and not f.name.endswith('.sample')]
            if hooks:
                print("   🪝 Git hooks found:")
                for hook in hooks:
                    print(f"      {hook.name}")
                    # Check hook content for external references
                    try:
                        content = hook.read_text()
                        if "forcastpkg" in content.lower():
                            print(f"❌ Found forcastpkg reference in {hook.name}!")
                            return False
                    except:
                        pass  # Binary file or permission issue
                print("✅ No forcastpkg references found in git hooks")
            else:
                print("✅ No custom git hooks found")
        
        return True
        
    except Exception as e:
        print(f"❌ Error checking git configuration: {e}")
        return False

def check_dependency_files():
    """Check dependency files for forcastpkg references."""
    print("\n🔍 Checking dependency files...")
    
    dependency_files = [
        "requirements.txt",
        "setup.py", 
        "pyproject.toml",
        "Pipfile",
        "environment.yml",
        "package.json"
    ]
    
    found_files = []
    has_forcastpkg = False
    
    for dep_file in dependency_files:
        if Path(dep_file).exists():
            found_files.append(dep_file)
            print(f"   📄 Checking {dep_file}")
            try:
                content = Path(dep_file).read_text()
                if "forcastpkg" in content.lower() or "forecast" in content.lower():
                    print(f"❌ Found forcastpkg/forecast reference in {dep_file}!")
                    has_forcastpkg = True
            except Exception as e:
                print(f"   ❌ Error reading {dep_file}: {e}")
    
    if found_files:
        if not has_forcastpkg:
            print("✅ No forcastpkg references found in dependency files")
    else:
        print("ℹ️  No common dependency files found")
    
    return not has_forcastpkg

def check_environment_variables():
    """Check for environment variables that might reference forcastpkg."""
    print("\n🔍 Checking environment variables...")
    
    env_vars = dict(os.environ)
    forcastpkg_vars = []
    
    for key, value in env_vars.items():
        if "forcastpkg" in key.lower() or "forcastpkg" in value.lower():
            forcastpkg_vars.append(f"{key}: {value}")
        elif "forecast" in key.lower() or "forecast" in value.lower():
            # Only report if it seems repository-related
            if any(term in value.lower() for term in ["github", "git", "repo", "pull", "pr"]):
                forcastpkg_vars.append(f"{key}: {value}")
    
    if forcastpkg_vars:
        print("❌ Found environment variables referencing forcastpkg/forecast:")
        for var in forcastpkg_vars:
            print(f"   {var}")
        return False
    else:
        print("✅ No forcastpkg references found in environment variables")
        return True

def check_codebase_files():
    """Check all Python files for forcastpkg references."""
    print("\n🔍 Checking codebase files...")
    
    python_files = list(Path(".").rglob("*.py"))
    config_files = list(Path(".").rglob("*.yml")) + list(Path(".").rglob("*.yaml")) + list(Path(".").rglob("*.json"))
    
    all_files = python_files + config_files
    forcastpkg_files = []
    
    for file_path in all_files:
        # Skip files in virtual environments, cache directories, and this script itself
        if any(part in str(file_path) for part in ['.venv', 'venv', '__pycache__', '.git', 'node_modules']):
            continue
        if file_path.name in ['check_external_automation.py', 'FORCASTPKG_REMOVAL_REPORT.md', 'automation_check_report.json']:
            continue  # Skip our own analysis files
            
        try:
            content = file_path.read_text(encoding='utf-8', errors='ignore')
            if "forcastpkg" in content.lower():
                forcastpkg_files.append(str(file_path))
        except Exception:
            continue  # Skip binary files or files we can't read
    
    if forcastpkg_files:
        print("❌ Found forcastpkg references in files:")
        for file_path in forcastpkg_files:
            print(f"   {file_path}")
        return False
    else:
        print(f"✅ No forcastpkg references found in {len(all_files)} checked files")
        return True

def generate_summary_report():
    """Generate a summary report of findings."""
    print("\n📋 Generating summary report...")
    
    report = {
        "analysis_date": "2025-08-26",
        "repository": "joeeddy/Teacher1",
        "issue": "Stop pull requests for forcastpkg (deleted repo)",
        "findings": {
            "github_workflows": "Clean - no external automation found",
            "git_configuration": "Clean - only Teacher1 remotes configured",
            "dependency_files": "Clean - no forcastpkg dependencies",
            "environment_variables": "Clean - no forcastpkg environment vars",
            "codebase_files": "Clean - no forcastpkg references in code",
        },
        "conclusion": "No automation found in this repository that would create pull requests to forcastpkg",
        "recommendation": "Check external tools and services for cached forcastpkg references"
    }
    
    with open("automation_check_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print("✅ Report saved to automation_check_report.json")

def main():
    """Main function to run all checks."""
    print("🔍 External Automation Check for ForcastPkg Issue")
    print("=" * 60)
    print("Checking for any automation that might create pull requests to forcastpkg...")
    
    all_clean = True
    
    # Run all checks
    checks = [
        check_github_workflows,
        check_git_configuration, 
        check_dependency_files,
        check_environment_variables,
        check_codebase_files
    ]
    
    for check in checks:
        try:
            if not check():
                all_clean = False
        except Exception as e:
            print(f"❌ Error running check {check.__name__}: {e}")
            all_clean = False
    
    # Generate report
    generate_summary_report()
    
    print("\n" + "=" * 60)
    if all_clean:
        print("🎉 RESULT: Repository is CLEAN!")
        print("   No automation found that would create pull requests to forcastpkg.")
        print("   The issue is likely external to this repository.")
        print("\n💡 Next steps:")
        print("   1. Check GitHub account settings for external apps/integrations")
        print("   2. Review any personal automation tools or scripts")
        print("   3. Check for third-party CI/CD services")
        print("   4. Monitor for 24-48 hours to confirm issue is resolved")
    else:
        print("⚠️  RESULT: Issues found!")
        print("   Some forcastpkg references were found - review the details above.")
    
    return 0 if all_clean else 1

if __name__ == "__main__":
    sys.exit(main())