#!/usr/bin/env python
"""Django'ning ma'muriy buyruqlari uchun yordamchi skript."""
import os
import sys


def main():
    """Ma'muriy vazifalarni bajaradi."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'navbat_hub.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Django import qilib bo'lmadi. O'rnatilganmi va "
            "PYTHONPATH muhit o'zgaruvchisida ko'rsatilganmi? "
            "Virtual muhitni faollashtirishni unutdingizmi?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
