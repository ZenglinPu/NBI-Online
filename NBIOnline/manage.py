#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

from NBIOnline.imageProcess.imageGCSchedule import GCTask
from NBIOnline.configLoader import nbi_conf


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NBIOnline.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    gc_task = GCTask(gc=nbi_conf.configs['gc_mode'])
    gc_task.start(hours=nbi_conf.configs['gc_interval'])
    main()
    gc_task.shutdown()
