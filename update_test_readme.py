#!/usr/bin/env python3
"""
Script to run unit tests and update the TEST_README.md document.
"""

import unittest
import sys
from datetime import datetime
import io
import os
from contextlib import redirect_stdout, redirect_stderr

# Import the test module
import test_variance

def run_tests():
    """Run the tests and return the result object and captured output."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(test_variance)
    runner = unittest.TextTestRunner(verbosity=2, stream=io.StringIO())
    result = runner.run(suite)
    output = runner.stream.getvalue()
    return result, output

def get_test_descriptions():
    """Return a dict of test names to descriptions."""
    return {
        'test_find_variance_normal_case': 'Tests variance calculation for a normal set of scores.',
        'test_find_variance_single_score': 'Tests variance for a single score (should be 0).',
        'test_find_variance_identical_scores': 'Tests variance for identical scores (should be 0).',
        'test_find_variance_empty_list': 'Tests that empty list raises ValueError.',
        'test_find_variance_not_a_list': 'Tests that non-list input raises TypeError.',
        'test_find_variance_non_int_elements': 'Tests that non-integer elements raise TypeError.',
        'test_find_variance_bool_elements': 'Tests that boolean elements raise TypeError.',
        'test_find_variance_negative_scores': 'Tests variance calculation with negative scores.',
        'test_find_variance_from_user_input_valid': 'Tests full user input flow with valid input.',
        'test_find_variance_from_user_input_too_many_scores': 'Tests user input with too many scores, then valid retry.',
        'test_get_scores_from_user_valid': 'Tests _get_scores_from_user with valid input.',
        'test_get_scores_from_user_invalid_int': 'Tests _get_scores_from_user with invalid integer input.',
        'test_get_scores_from_user_too_many': 'Tests _get_scores_from_user with too many scores.',
        'test_get_scores_from_user_out_of_range': 'Tests _get_scores_from_user with out-of-range scores.',
    }

def update_readme(result, output):
    """Update the TEST_README.md file with test results."""
    descriptions = get_test_descriptions()
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Collect failed tests with their error messages
    failed_tests = []
    for failure in result.failures + result.errors:
        test_name = failure[0]._testMethodName
        error_msg = failure[1]
        failed_tests.append((test_name, error_msg))

    # Get all test names from the suite
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromModule(test_variance)
    all_tests = []
    for test_group in suite:
        for test_case in test_group:
            all_tests.append(test_case._testMethodName)

    # Create test_results directory if it doesn't exist
    os.makedirs('test_results', exist_ok=True)

    # Generate filename with date and time
    timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    filename = f'test_results/test_results_{timestamp}.md'

    # Write the README
    with open(filename, 'w') as f:
        f.write('# Unit Tests for Variance Calculator\n\n')
        f.write(f'**Latest Test Run:** {current_date}\n\n')
        f.write(f'**Total Tests:** {result.testsRun}\n')
        f.write(f'**Passed:** {result.testsRun - len(result.failures) - len(result.errors)}\n')
        f.write(f'**Failed:** {len(result.failures)}\n')
        f.write(f'**Errors:** {len(result.errors)}\n\n')

        if failed_tests:
            f.write('## Failed Tests\n\n')
            for test_name, error_msg in sorted(failed_tests):
                f.write(f'- **{test_name}**\n')
                f.write('```\n')
                f.write(error_msg)
                f.write('\n```\n\n')

        f.write('## Test Results\n\n')

        for test_name in sorted(all_tests):
            status_emoji = '✅' if test_name not in [ft[0] for ft in failed_tests] else '❌'
            f.write(f'{status_emoji} - {test_name} - {current_date}\n')

if __name__ == '__main__':
    result, output = run_tests()
    update_readme(result, output)
    print("Test results saved to test_results/ directory.")