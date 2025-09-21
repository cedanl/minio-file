#!/usr/bin/env python3
"""
Test runner script for minio-file package.
Provides easy ways to run different test suites.
"""

import subprocess
import sys
import argparse
from pathlib import Path


def run_command(cmd, description=""):
    """Run a command and return success status."""
    if description:
        print(f"\n🔄 {description}")
        print("=" * 50)
    
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=False)
    
    if result.returncode == 0:
        print(f"✅ Success: {description}" if description else "✅ Command succeeded")
        return True
    else:
        print(f"❌ Failed: {description}" if description else "❌ Command failed")
        return False


def test_imports():
    """Test package imports."""
    return run_command([
        "pytest", "tests/test_imports.py", "-v"
    ], "Testing package imports")


def test_functionality():
    """Test core functionality."""
    return run_command([
        "pytest", "tests/test_functionality.py", "-v"
    ], "Testing core functionality")


def test_build():
    """Test building and distribution."""
    return run_command([
        "pytest", "tests/test_build_and_distribution.py", "-v", "-m", "not slow"
    ], "Testing package building")


def test_all():
    """Run all tests."""
    return run_command([
        "pytest", "tests/", "-v"
    ], "Running all tests")


def test_fast():
    """Run fast tests only."""
    return run_command([
        "pytest", "tests/", "-v", "-m", "not slow"
    ], "Running fast tests")


def test_with_coverage():
    """Run tests with coverage."""
    return run_command([
        "pytest", "tests/", "--cov=minio_file", "--cov-report=term-missing", "--cov-report=html"
    ], "Running tests with coverage")


def lint_code():
    """Run linting tools."""
    success = True
    
    # Black
    success &= run_command([
        "black", "--check", "src/", "tests/"
    ], "Checking code formatting with black")
    
    # isort
    success &= run_command([
        "isort", "--check-only", "src/", "tests/"
    ], "Checking import sorting with isort")
    
    # flake8
    success &= run_command([
        "flake8", "src/", "tests/"
    ], "Checking code style with flake8")
    
    # mypy (optional, might have issues)
    try:
        success &= run_command([
            "mypy", "src/"
        ], "Type checking with mypy")
    except FileNotFoundError:
        print("⚠️  mypy not found, skipping type checking")
    
    return success


def format_code():
    """Format code with black and isort."""
    success = True
    
    success &= run_command([
        "black", "src/", "tests/"
    ], "Formatting code with black")
    
    success &= run_command([
        "isort", "src/", "tests/"
    ], "Sorting imports with isort")
    
    return success


def build_package():
    """Build the package."""
    # Clean first
    run_command([
        "rm", "-rf", "dist/", "build/", "*.egg-info/"
    ], "Cleaning build artifacts")
    
    return run_command([
        "uv", "build"
    ], "Building package")


def quick_check():
    """Quick development check."""
    print("🚀 Quick Development Check")
    print("=" * 50)
    
    success = True
    
    # Test import
    print("\n1. Testing package import...")
    result = subprocess.run([
        "python", "-c", "import minio_file; print('✅ Package imports successfully')"
    ], capture_output=True, text=True)
    
    if result.returncode == 0:
        print(result.stdout.strip())
    else:
        print(f"❌ Import failed: {result.stderr}")
        success = False
    
    # Run basic tests
    print("\n2. Running basic tests...")
    success &= test_imports()
    
    return success


def full_ci_check():
    """Full CI-style check."""
    print("🏗️  Full CI Check")
    print("=" * 50)
    
    success = True
    
    # Linting
    success &= lint_code()
    
    # Testing
    success &= test_all()
    
    # Building
    success &= build_package()
    
    if success:
        print("\n🎉 All checks passed! Ready for CI/deployment.")
    else:
        print("\n💥 Some checks failed. Please fix issues before proceeding.")
    
    return success


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(description="Test runner for minio-file package")
    parser.add_argument("command", choices=[
        "imports", "functionality", "build", "all", "fast", "coverage",
        "lint", "format", "package", "quick", "ci"
    ], help="Test command to run")
    
    args = parser.parse_args()
    
    commands = {
        "imports": test_imports,
        "functionality": test_functionality,
        "build": test_build,
        "all": test_all,
        "fast": test_fast,
        "coverage": test_with_coverage,
        "lint": lint_code,
        "format": format_code,
        "package": build_package,
        "quick": quick_check,
        "ci": full_ci_check,
    }
    
    success = commands[args.command]()
    
    if not success:
        sys.exit(1)


if __name__ == "__main__":
    main()
