#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test runner for Gemini Auto Query.

Runs all tests and generates a comprehensive report.
"""

import sys
import unittest
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def run_all_tests():
    """Run all tests and return results"""
    # Windows encoding setup
    if sys.platform == "win32":
        import os
        if hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
        if hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8')
        os.environ['PYTHONIOENCODING'] = 'utf-8'
    
    # Discover and run tests
    loader = unittest.TestLoader()
    start_dir = str(Path(__file__).parent / "tests")
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(
        verbosity=2,
        stream=sys.stdout,
        buffer=True
    )
    
    print("=" * 70)
    print("Gemini Auto Query - Test Suite")
    print("=" * 70)
    print()
    
    result = runner.run(suite)
    
    print()
    print("=" * 70)
    print("Test Summary")
    print("=" * 70)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped) if hasattr(result, 'skipped') else 0}")
    
    if result.failures:
        print("\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback.split('AssertionError:')[-1].strip() if 'AssertionError:' in traceback else 'See details above'}")
    
    if result.errors:
        print("\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback.split('Exception:')[-1].strip() if 'Exception:' in traceback else 'See details above'}")
    
    success = len(result.failures) == 0 and len(result.errors) == 0
    
    if success:
        print("\n✅ All tests passed!")
    else:
        print(f"\n❌ {len(result.failures) + len(result.errors)} test(s) failed")
    
    print("=" * 70)
    
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(run_all_tests())