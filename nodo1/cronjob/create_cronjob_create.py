#!/usr/bin/env python3
import os
import pwd
import subprocess
import sys
from tempfile import NamedTemporaryFile

USERNAME = 'adam'
CRON_LINE = '30 12 * * * /bin/echo "sample text"'
DEFAULT_SHELL = '/bin/bash'


def require_root():
    if os.geteuid() != 0:
        print('Este script debe ejecutarse como root.', file=sys.stderr)
        sys.exit(1)


def user_exists(name):
    try:
        pwd.getpwnam(name)
        return True
    except KeyError:
        return False


def run(cmd):
    print('$', ' '.join(cmd))
    subprocess.run(cmd, check=True)


def ensure_user_exists():
    if user_exists(USERNAME):
        print(f'El usuario {USERNAME} ya existe, se reutiliza.')
        return
    run(['useradd', '-m', '-s', DEFAULT_SHELL, USERNAME])
    print(f'Usuario creado: {USERNAME}')


def get_current_crontab():
    result = subprocess.run(
        ['crontab', '-u', USERNAME, '-l'],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        return []
    return [line for line in result.stdout.splitlines() if line.strip()]


def install_crontab(lines):
    with NamedTemporaryFile('w', delete=False) as tmp:
        tmp.write('\n'.join(lines) + '\n')
        temp_name = tmp.name
    try:
        print('$', f'crontab -u {USERNAME} {temp_name}')
        subprocess.run(['crontab', '-u', USERNAME, temp_name], check=True)
    finally:
        os.unlink(temp_name)


def main():
    require_root()
    ensure_user_exists()

    lines = get_current_crontab()
    if CRON_LINE in lines:
        print('La entrada ya existe en el crontab, no se duplica.')
    else:
        lines.append(CRON_LINE)
        install_crontab(lines)
        print('Entrada agregada al crontab.')

    print('\nConfiguración completada.')
    print(f'Usuario: {USERNAME}')
    print(f'Tarea: {CRON_LINE}')


if __name__ == '__main__':
    main()
