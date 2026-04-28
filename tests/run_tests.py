#!/usr/bin/env python3
import sys
import unittest


def main():
    loader = unittest.TestLoader()
    suite = loader.discover(start_dir="tests")

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    print("\n=== Test Summary ===")
    print(f"Ran: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Skipped: {len(result.skipped)}")
    print("Status: PASS" if result.wasSuccessful() else "Status: FAIL")

    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
