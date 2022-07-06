import os
from junit_xml import TestSuite, TestCase

RESULT_DIR = '/tmp/sonobuoy/results'


def handle_unexpected_error(err_msg):
    # Creating a junit report for setup failure
    test_case = TestCase('azure_arc_serviceconnector_setup', 'azure_arc_serviceconnector_setup')
    test_case.add_failure_info('Tests are not fully runned due to error: {}'.format(err_msg))
    test_cases = [test_case]
    test_suite = TestSuite("azure_arc_serviceconnector", test_cases)

    with open('{}/results.xml'.format(RESULT_DIR), 'w') as f:
        TestSuite.to_file(f, [test_suite], prettyprint=False)


def handle_test_results():
    test_cases = []
    res_files = [item for item in os.listdir(RESULT_DIR) if item != 'error']
    for name in res_files:
        test_case = TestCase(name)
        with open('{}/{}'.format(RESULT_DIR, name), 'r') as f:
            content = f.read()
            if content.startswith('Error'):
                test_case.add_error_info(content)
        test_cases.append(test_case)
    test_suite = TestSuite("azure_arc_serviceconnector", test_cases)
    with open('{}/results.xml'.format(RESULT_DIR), 'w') as f:
        TestSuite.to_file(f, [test_suite], prettyprint=False)


with open('{}/error'.format(RESULT_DIR), 'r') as f:
    error_message = f.read()
    if error_message:
        handle_unexpected_error(error_message)
    else:
        handle_test_results()
