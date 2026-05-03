#!/usr/bin/env python3
from pathlib import Path
import os
import subprocess
import sys

SCRIPT_PATH = Path('/usr/local/bin/event_logger')
SERVICE_PATH = Path('/etc/systemd/system/event_logger.service')
TIMER_PATH = Path('/etc/systemd/system/event_logger.timer')
LOG_FILE = Path('/root/logs/events.trc')
LOG_DIR = Path('/root/logs')


def run(cmd, check=True):
    print('$', ' '.join(cmd))
    subprocess.run(cmd, check=check)


def require_root():
    if os.geteuid() != 0:
        print('Este script debe ejecutarse como root.', file=sys.stderr)
        sys.exit(1)


def remove_if_exists(path: Path):
    if path.exists() or path.is_symlink():
        path.unlink()
        print(f'Eliminado: {path}')
    else:
        print(f'No existe, se omite: {path}')


def main():
    require_root()

    run(['systemctl', 'disable', '--now', 'event_logger.timer'], check=False)
    run(['systemctl', 'stop', 'event_logger.service'], check=False)

    remove_if_exists(TIMER_PATH)
    remove_if_exists(SERVICE_PATH)
    remove_if_exists(SCRIPT_PATH)

    if LOG_FILE.exists():
        LOG_FILE.unlink()
        print(f'Eliminado: {LOG_FILE}')
    else:
        print(f'No existe, se omite: {LOG_FILE}')

    if LOG_DIR.exists() and not any(LOG_DIR.iterdir()):
        LOG_DIR.rmdir()
        print(f'Directorio vacío eliminado: {LOG_DIR}')
    elif LOG_DIR.exists():
        print(f'Se conserva {LOG_DIR} porque contiene otros archivos.')

    run(['systemctl', 'daemon-reload'])
    run(['systemctl', 'reset-failed'], check=False)

    print('\nDesinstalación completada.')


if __name__ == '__main__':
    main()
