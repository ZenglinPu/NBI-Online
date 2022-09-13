#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import argparse

from .NBIOnline.imageProcess.imageGCSchedule import GCTask

parser = argparse.ArgumentParser()
parser.add_argument('--django_settings', required=False, help='Django settings module', default='NBIOnline.settings')
parser.add_argument('--gc_mode', required=False, help='', default=False)
parameters = parser.parse_args()


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', parameters.django_settings)
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
    gc_task = GCTask(gc=parameters.gc_mode)
    gc_task.start()
    main()
    gc_task.shutdown()
