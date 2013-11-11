import os
import sys
import subprocess
import atexit
import signal

from django.conf import settings
from django.core.management.commands.runserver import Command as RunserverCommand


MESSAGES = {
    "Init": ">>> Loading...",
    "MissingConfig": ">>> You need to provide an absolute path to the folder containing config.rb. i.e.: FIRSTMATE_COMPASS_PROJECT_PATH.",
    "NotFound": ">>> Could not find a config.rb at {path}. Perhaps run : compass config",
    "StartingFor": ">>> Starting the compass watch command for path: {path}",
    "StartingPid": ">>> Compass watch process on pid: {pid}",
    "Closing": ">>> Closing Compass watch process for pid: {pid}"
}


class Command(RunserverCommand):
    option_list = RunserverCommand.option_list

    def run(self, *args, **options):
        """Runs the server and the compass watch process"""
        use_reloader = options.get('use_reloader')

        if use_reloader and os.environ.get("RUN_MAIN") != "true":
            self.stdout.write(self.style.NOTICE(MESSAGES.get("Init")))

            project_path = getattr(
                settings, 'FIRSTMATE_COMPASS_PROJECT_PATH', None)

            if not project_path:
                self.stdout.write(
                    MESSAGES.get("NotFound").format(path=project_path))
                sys.exit(1)

            if project_path and not os.path.exists(os.path.join(project_path, 'config.rb')):
                self.stdout.write(
                    MESSAGES.get("NotFound").format(path=project_path))
                sys.exit(1)

            self.stdout.write(
                self.style.NOTICE(MESSAGES.get("StartingFor").format(path=project_path)) + "\n")
            self.start_compass_watch(project_path)

        super(Command, self).run(*args, **options)

    def start_compass_watch(self, path=None):
        self.compass_process = subprocess.Popen(
            ['compass watch %s' % path],
            shell=True,
            stdin=subprocess.PIPE,
            stdout=self.stdout,
            stderr=self.stderr,
        )
        self.stdout.write(
            self.style.NOTICE(MESSAGES.get("StartingPid").format(pid=self.compass_process.pid)) + "\n")

        def kill_compass_project(pid):
            self.stdout.write(
                self.style.NOTICE(MESSAGES.get("Closing").format(pid=self.compass_process.pid)) + "\n")
            os.kill(pid, signal.SIGTERM)

        atexit.register(kill_compass_project, self.compass_process.pid)
