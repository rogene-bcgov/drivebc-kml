#!/usr/bin/env python3
"""
Test runner script for DriveBC KML Converter

This script runs all unit tests and provides a summary report.
"""

import sys
import unittest
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def run_tests():
    """Run all unit tests and return results."""
    # Discover and load tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2, stream=sys.stdout, buffer=True)
    result = runner.run(suite)
    
    # Print summary
    print(f"\n{'='*60}")
    print(f"TEST SUMMARY")
    print(f"{'='*60}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    
    success_rate = ((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100) if result.testsRun > 0 else 0
    print(f"Success rate: {success_rate:.1f}%")
    
    if result.failures:
        print(f"\nFAILURES ({len(result.failures)}):")
        for test, traceback in result.failures:
            print(f"  ❌ {test}")
            # Print first line of error for quick reference
            error_lines = traceback.strip().split('\n')
            for line in error_lines:
                if 'AssertionError:' in line:
                    print(f"     {line.split('AssertionError:')[-1].strip()}")
                    break
    
    if result.errors:
        print(f"\nERRORS ({len(result.errors)}):")
        for test, traceback in result.errors:
            print(f"  💥 {test}")
            # Print first line of error for quick reference
            error_lines = traceback.strip().split('\n')
            for line in error_lines:
                if 'Error:' in line or 'Exception:' in line:
                    print(f"     {line.split(':')[-1].strip()}")
                    break
    
    # Return exit code
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    print("🧪 Running DriveBC KML Converter Test Suite")
    print("=" * 60)
    exit_code = run_tests()
    
    if exit_code == 0:
        print("\n✅ All tests passed!")
        print("\n💡 To see a detailed demonstration of improvements:")
        print("   python -m unittest test_drivebc_to_kml.TestImprovementsDemo.test_improvement_summary_report -v")
    else:
        print(f"\n❌ Some tests failed. Exit code: {exit_code}")
    
    sys.exit(exit_code)
