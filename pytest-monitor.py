#!/usr/bin/python
import subprocess
from datetime import datetime


def run_tests():
    process = subprocess.Popen(['py.test', '-q'], stdout=subprocess.PIPE)
    return process.communicate()[0], not process.returncode


def extract_result_mark(result):
    # TODO: extract with regex
    last_line = result.strip().split('\n')[-1]  # something like 1 failed, 1 passed in 0.07 seconds
    return last_line[:last_line.index('in')]


def notify(success, output):
    title = 'TESTS %s at %s' % ('SUCCESS' if success else 'FAIL', datetime.now().time())
    subprocess.call(['notify-send', title, out])


last_result_id = None
while True:
    out, success = run_tests()
    result_id = extract_result_mark(out)

    if last_result_id != result_id:
        notify(success, out)
        last_result_id = result_id
