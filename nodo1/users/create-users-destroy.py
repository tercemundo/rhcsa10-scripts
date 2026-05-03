#!/usr/bin/env python3
import os
import pwd
import grp
import subprocess
import sys

GROUP_NAME = 'opsmgrs'
USERS = ['adam', 'linda', 'steve']


def require_root():
    if os.geteuid() != 0:
        print('Este script debe ejecutarse como root.', file=sys.stderr)
        sys.exit(1)


def run(cmd, check=True):
    print('$', ' '.join(cmd))
    subprocess.run(cmd, check=check)


def group_exists(name):
    try:
        grp.getgrnam(name)
        return True
    except KeyError:
        return False


def user_exists(name):
    try:
        pwd.getpwnam(name)
        return True
    except KeyError:
        return False


def main():
    require_root()

    for username in USERS:
        if user_exists(username):
            run(['userdel', '-r', username], check=False)
            print(f'Usuario eliminado: {username}')
        else:
            print(f'No existe, se omite usuario: {username}')

    if group_exists(GROUP_NAME):
        run(['groupdel', GROUP_NAME], check=False)
        print(f'Grupo eliminado: {GROUP_NAME}')
    else:
        print(f'No existe, se omite grupo: {GROUP_NAME}')

    print('\nDesinstalación completada.')
    print('No deberían quedar usuarios ni grupo de esta práctica, salvo que alguno estuviera en uso o hubiera sido recreado manualmente.')


if __name__ == '__main__':
    main()
