#!/usr/bin/python
import os
import sys
import subprocess
from datetime import datetime


def run_tests():
    process = subprocess.Popen(['py.test', '-q'], stdout=subprocess.PIPE)
    return process.communicate()[0], not process.returncode


def extract_result_mark(result):
    # TODO: extract with regex
    last_line = result.strip().split('\n')[-1]  # something like 1 failed, 1 passed in 0.07 seconds
    return last_line[:last_line.index('in')]


def build_title(success, project_name):
    return '%s TESTS %s at %s' % (project_name,
                                  'SUCCESS' if success else 'FAIL',
                                  str(datetime.now().strftime("%H:%M")))


def notify(success, output, project_name):
    subprocess.call(['notify-send', build_title(success, project_name), output])


def run(project_name):
    last_result_id = None
    while True:
        out, success = run_tests()
        result_id = extract_result_mark(out)

        if last_result_id != result_id:
            notify(success, out, project_name)
            last_result_id = result_id


if __name__ == '__main__':
    project_name = len(sys.argv) > 1 and sys.argv[1] or os.getcwd()
    run(project_name)
