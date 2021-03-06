#!/usr/bin/python
import os
import sys
import subprocess
import time
from datetime import datetime

from watchdog.observers.polling import PollingObserver
from watchdog.events import RegexMatchingEventHandler

import notify2


class RunTestsHandler(RegexMatchingEventHandler):
    def __init__(self, project_name, *args, **kwargs):
        super(RunTestsHandler, self).__init__(*args, **kwargs)
        self.project_name = project_name
        self._last_result_id = None

        self.on_any_event()  # initial run

    def on_any_event(self, event=None):
        out, success = self._run_tests()
        last_line = out.strip().split('\n')[-1]

        result_id = self._extract_result_mark(last_line)

        if self._last_result_id != result_id:
            self._notify(success, last_line)
            self._last_result_id = result_id

    def _run_tests(self):
        process = subprocess.Popen(['py.test', '-q'], stdout=subprocess.PIPE)
        return process.communicate()[0], not process.returncode

    def _extract_result_mark(self, last_line):
        # TODO: extract with regex
        return last_line[:last_line.index('in')]

    def _notify(self, success, last_line):
        icon = "notification-power-disconnected" if not success else "notification-network-wireless-full"
        title = '%s TESTS %s at %s' % (self.project_name,
                                       'SUCCESS' if success else 'FAIL',
                                       str(datetime.now().strftime("%H:%M")))

        notification = notify2.Notification(title, last_line, icon)
        notification.set_urgency(notify2.URGENCY_CRITICAL)
        notification.show()


def main():
    path = os.getcwd()
    project_name = len(sys.argv) > 1 and sys.argv[1] or path
    notify2.init(project_name)

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


if __name__ == '__main__':
    main()
