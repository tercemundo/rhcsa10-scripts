#!/usr/bin/env python3
from pathlib import Path
import os
import subprocess
import sys

SCRIPT_PATH = Path('/usr/local/bin/event_logger')
SERVICE_PATH = Path('/etc/systemd/system/event_logger.service')
TIMER_PATH = Path('/etc/systemd/system/event_logger.timer')
LOG_DIR = Path('/root/logs')
LOG_FILE = LOG_DIR / 'events.trc'

SCRIPT_CONTENT = "#!/bin/bash\nls -l /tmp > /root/logs/events.trc\n"
SERVICE_CONTENT = """[Unit]
Description=Event Logger

[Service]
Type=oneshot
ExecStart=/usr/local/bin/event_logger
"""
TIMER_CONTENT = """[Unit]
Description=Run every minute

[Timer]
OnCalendar=*-*-* *:*:00
Persistent=true
Unit=event_logger.service

[Install]
WantedBy=timers.target
"""


def run(cmd):
    print('$', ' '.join(cmd))
    subprocess.run(cmd, check=True)


def require_root():
    if os.geteuid() != 0:
        print('Este script debe ejecutarse como root.', file=sys.stderr)
        sys.exit(1)


def main():
    require_root()

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    SCRIPT_PATH.parent.mkdir(parents=True, exist_ok=True)
    SERVICE_PATH.parent.mkdir(parents=True, exist_ok=True)

    SCRIPT_PATH.write_text(SCRIPT_CONTENT)
    SCRIPT_PATH.chmod(0o755)
    SERVICE_PATH.write_text(SERVICE_CONTENT)
    TIMER_PATH.write_text(TIMER_CONTENT)

    run(['systemctl', 'daemon-reload'])
    run(['systemctl', 'enable', '--now', 'event_logger.timer'])
    run(['systemctl', 'status', 'event_logger.timer', '--no-pager'])

    print('\nInstalación completada.')
    print(f'Script: {SCRIPT_PATH}')
    print(f'Service: {SERVICE_PATH}')
    print(f'Timer: {TIMER_PATH}')
    print(f'Log esperado: {LOG_FILE}')


if __name__ == '__main__':
    main()
