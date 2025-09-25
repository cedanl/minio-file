"""Test package imports and basic functionality."""

import subprocess

import pytest


class TestImports:
    """Test all package imports work correctly."""

    def test_main_package_import(self):
        """Test main package imports successfully."""
        import minio_file

        assert minio_file is not None

    def test_version_available(self):
        """Test package version is available."""
        import minio_file

        assert hasattr(minio_file, '__version__')
        assert minio_file.__version__ == "2025.1.2"

    def test_main_module_import(self):
        """Test main minio_file module imports successfully."""
        from minio_file import minio_file

        assert minio_file is not None

    def test_main_function_import(self):
        """Test main function is importable."""
        from minio_file import main

        assert callable(main)

    def test_package_attributes(self):
        """Test package has expected attributes."""
        import minio_file

        # Check __all__ is defined
        assert hasattr(minio_file, '__all__')
        assert isinstance(minio_file.__all__, list)

        # Check main functions are in __all__
        assert 'main' in minio_file.__all__

    def test_module_functions_exist(self):
        """Test that modules have callable functions."""
        from minio_file import minio_file as mf

        # Get non-private attributes
        main_funcs = [x for x in dir(mf) if not x.startswith('_')]

        # Should have at least some functions
        assert len(main_funcs) > 0, "Main module should have functions"


class TestPackageStructure:
    """Test package structure and installation."""

    def test_package_location(self):
        """Test package is installed in correct location."""
        import minio_file

        package_path = minio_file.__file__
        assert package_path is not None
        assert 'minio_file' in package_path

    def test_package_files_exist(self):
        """Test all expected package files exist."""
        import os

        import minio_file

        package_dir = os.path.dirname(minio_file.__file__)

        # Check for expected files
        expected_files = ['__init__.py', 'minio_file.py']
        for file in expected_files:
            file_path = os.path.join(package_dir, file)
            assert os.path.exists(file_path), f"Expected file {file} not found"

    def test_installation_type(self):
        """Test package installation type."""
        import minio_file

        package_path = minio_file.__file__

        # In development mode, should contain 'src'
        # In normal install, should contain 'site-packages'
        assert '/src/' in package_path or 'site-packages' in package_path


class TestCLI:
    """Test CLI functionality."""

    def test_cli_command_exists(self):
        """Test CLI command is available in PATH."""
        result = subprocess.run(['which', 'minio-file'], capture_output=True, text=True)
        assert result.returncode == 0, "CLI command not found in PATH"

    def test_cli_help(self):
        """Test CLI help command works or fails gracefully."""
        try:
            # Try different help flags that might work
            help_commands = [
                ['minio-file', '--help'],
                ['minio-file', '-h'],
            ]

            success = False
            for cmd in help_commands:
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)

                # Check if we got useful output (either stdout or stderr)
                output = result.stdout + result.stderr
                if len(output) > 0:
                    # If it shows help OR gives a config error, that's acceptable
                    if any(
                        word in output.lower()
                        for word in ['help', 'usage', 'command', 'config', 'credential', 'endpoint']
                    ):
                        success = True
                        break

            assert success, "CLI should show help or indicate missing config"

        except subprocess.TimeoutExpired:
            pytest.fail("CLI help command timed out")

    def test_cli_import_works(self):
        """Test CLI can import without errors."""
        # Test that the main function can be imported (not called)
        try:
            result = subprocess.run(
                ['python', '-c', 'from minio_file.minio_file import main; print("CLI import successful")'],
                capture_output=True,
                text=True,
            )
            assert result.returncode == 0, f"CLI import failed: {result.stderr}"
            assert "CLI import successful" in result.stdout
        except Exception as e:
            pytest.fail(f"CLI import test failed: {e}")


class TestDependencies:
    """Test package dependencies are available."""

    def test_minio_dependency(self):
        """Test minio dependency is available."""
        try:
            import minio

            assert minio is not None
        except ImportError:
            pytest.fail("minio dependency not available")

    def test_required_modules_importable(self):
        """Test all required modules can be imported."""
        # Add any other dependencies your package uses
        required_modules = ['minio']  # Add others as needed

        for module_name in required_modules:
            try:
                __import__(module_name)
            except ImportError:
                pytest.fail(f"Required module {module_name} not available")
