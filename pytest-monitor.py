#!/usr/bin/python
import os
import sys
import subprocess
import time
from datetime import datetime

from watchdog.observers.polling import PollingObserver
from watchdog.events import RegexMatchingEventHandler


class RunTestsHandler(RegexMatchingEventHandler):
    def __init__(self, project_name, *args, **kwargs):
        super(RunTestsHandler, self).__init__(*args, **kwargs)
        self.project_name = project_name
        self._last_result_id = None

        self.on_any_event()  # initial run

    def on_any_event(self, event=None):
        out, success = self._run_tests()
        result_id = self._extract_result_mark(out)

        if self._last_result_id != result_id:
            self._notify(success, out, project_name)
            self._last_result_id = result_id

    def _run_tests(self):
        process = subprocess.Popen(['py.test', '-q'], stdout=subprocess.PIPE)
        return process.communicate()[0], not process.returncode

    def _extract_result_mark(self, result):
        # TODO: extract with regex
        last_line = result.strip().split('\n')[-1]  # something like 1 failed, 1 passed in 0.07 seconds
        return last_line[:last_line.index('in')]

    def _build_title(self, success, project_name):
        return '%s TESTS %s at %s' % (project_name,
                                      'SUCCESS' if success else 'FAIL',
                                      str(datetime.now().strftime("%H:%M")))

    def _notify(self, success, output, project_name):
        subprocess.call(['notify-send', self._build_title(success, project_name), output])


if __name__ == '__main__':
    path = os.getcwd()
    project_name = len(sys.argv) > 1 and sys.argv[1] or path
    handler = RunTestsHandler(project_name, regexes=['.*\.py$'])
    observer = PollingObserver(timeout=3)
    observer.schedule(handler, path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
