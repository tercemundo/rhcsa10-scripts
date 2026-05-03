#!/usr/bin/env python3
import os
import pwd
import subprocess
import sys
from tempfile import NamedTemporaryFile

USERNAME = 'adam'
CRON_LINE = '30 12 * * * /bin/echo "sample text"'


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


def install_crontab(lines):
    with NamedTemporaryFile('w', delete=False) as tmp:
        if lines:
            tmp.write('\n'.join(lines) + '\n')
        temp_name = tmp.name
    try:
        print('$', f'crontab -u {USERNAME} {temp_name}')
        subprocess.run(['crontab', '-u', USERNAME, temp_name], check=True)
    finally:
        os.unlink(temp_name)


def get_current_crontab_raw():
    result = subprocess.run(
        ['crontab', '-u', USERNAME, '-l'],
        capture_output=True,
        text=True
    )
    if result.returncode != 0:
        return None
    return result.stdout.splitlines()


def run(cmd, check=True):
    print('$', ' '.join(cmd))
    subprocess.run(cmd, check=check)


def main():
    require_root()

    if not user_exists(USERNAME):
        print(f'El usuario {USERNAME} no existe; no hay nada que desinstalar.')
        sys.exit(0)

    lines = get_current_crontab_raw()
    if lines is not None:
        new_lines = [line for line in lines if line.strip() != CRON_LINE]

        if len(new_lines) != len(lines):
            if new_lines:
                install_crontab(new_lines)
                print('Entrada eliminada del crontab.')
            else:
                print('$', f'crontab -u {USERNAME} -r')
                subprocess.run(['crontab', '-u', USERNAME, '-r'], check=True)
                print('Crontab eliminado por completo porque no quedaron entradas.')
        else:
            print('La entrada de cron no existía; se continúa con la eliminación del usuario.')
    else:
        print('El usuario no tenía crontab; se continúa con la eliminación del usuario.')

    run(['userdel', '-r', USERNAME], check=False)
    print(f'Usuario eliminado: {USERNAME}')
    print('\nDesinstalación completada.')


if __name__ == '__main__':
    main()
