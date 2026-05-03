#!/usr/bin/env python3
import os
import pwd
import grp
import subprocess
import sys

GROUP_NAME = 'opsmgrs'
USERS = {
    'adam': {'groups': [GROUP_NAME], 'shell': '/bin/bash', 'password': 'Train@123'},
    'linda': {'groups': [GROUP_NAME], 'shell': '/bin/bash', 'password': 'Train@123'},
    'steve': {'groups': [], 'shell': '/sbin/nologin', 'password': 'Train@123'},
}


def require_root():
    if os.geteuid() != 0:
        print('Este script debe ejecutarse como root.', file=sys.stderr)
        sys.exit(1)


def run(cmd, input_text=None):
    print('$', ' '.join(cmd))
    subprocess.run(cmd, input=input_text, text=True, check=True)


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

    if not group_exists(GROUP_NAME):
        run(['groupadd', GROUP_NAME])
    else:
        print(f'El grupo {GROUP_NAME} ya existe, se conserva.')

    for username, cfg in USERS.items():
        if not user_exists(username):
            cmd = ['useradd']
            if cfg['groups']:
                cmd += ['-G', ','.join(cfg['groups'])]
            if cfg['shell']:
                cmd += ['-s', cfg['shell']]
            cmd.append(username)
            run(cmd)
        else:
            print(f'El usuario {username} ya existe, se conserva.')
            if cfg['groups']:
                run(['usermod', '-aG', ','.join(cfg['groups']), username])
            if cfg['shell']:
                run(['usermod', '-s', cfg['shell'], username])

        run(['chpasswd'], input_text=f"{username}:{cfg['password']}\n")

    print('\nInstalación completada.')
    print('Grupo creado/configurado: opsmgrs')
    print('Usuarios configurados: adam, linda, steve')


if __name__ == '__main__':
    main()
