#!/usr/bin/env python3
import os
import pwd
import subprocess
import sys
from pathlib import Path

NETWORK = os.environ.get("NFS_NETWORK", "192.168.56.0/24")
USER = os.environ.get("NFS_USER", "qq")
UID = int(os.environ.get("NFS_UID", "1006"))
GID = int(os.environ.get("NFS_GID", str(UID)))
HOME_BASE = Path(os.environ.get("NFS_HOME_BASE", "/home/guests"))
EXTRA_EXPORT = Path(os.environ.get("NFS_EXTRA_EXPORT", "/externals"))
EXPORTS_FILE = Path("/etc/exports")
USER_HOME = HOME_BASE / USER

EXPORT_LINES = [
    f"{HOME_BASE} {NETWORK}(rw,no_root_squash,sync)",
    f"{EXTRA_EXPORT} {NETWORK}(rw,no_root_squash,sync)",
]


def run(cmd, check=True):
    print('+', ' '.join(cmd))
    return subprocess.run(cmd, check=check)


def ensure_root():
    if os.geteuid() != 0:
        print('Ejecutar como root: sudo python3 nodo1_nfs_qq_full.py')
        sys.exit(1)


def ensure_group():
    try:
        import grp
        grp.getgrgid(GID)
    except KeyError:
        run(['groupadd', '-g', str(GID), USER])


def ensure_user():
    try:
        pwd.getpwnam(USER)
        print(f'Usuario {USER} ya existe')
    except KeyError:
        run(['useradd', '-u', str(UID), '-g', str(GID), '-d', str(USER_HOME), '-M', '-s', '/bin/bash', USER])


def ensure_dirs():
    HOME_BASE.mkdir(parents=True, exist_ok=True)
    EXTRA_EXPORT.mkdir(parents=True, exist_ok=True)
    USER_HOME.mkdir(parents=True, exist_ok=True)
    run(['chown', '-R', f'{UID}:{GID}', str(USER_HOME)])
    run(['chmod', '755', str(HOME_BASE)])
    run(['chmod', '755', str(USER_HOME)])
    run(['chmod', '755', str(EXTRA_EXPORT)])


def ensure_exports():
    current = EXPORTS_FILE.read_text(encoding='utf-8') if EXPORTS_FILE.exists() else ''
    lines = [line.strip() for line in current.splitlines() if line.strip()]
    changed = False
    for exp in EXPORT_LINES:
        if exp not in lines:
            lines.append(exp)
            changed = True
    if changed:
        EXPORTS_FILE.write_text('\n'.join(lines) + '\n', encoding='utf-8')


def ensure_sample_files():
    f1 = USER_HOME / 'desde_nodo1.txt'
    if not f1.exists():
        f1.write_text('Archivo creado en nodo1 dentro del home exportado de qq\n', encoding='utf-8')
    run(['chown', f'{UID}:{GID}', str(f1)])
    run(['chmod', '644', str(f1)])


def main():
    ensure_root()
    run(['dnf', 'install', '-y', 'nfs-utils'])
    ensure_group()
    ensure_user()
    ensure_dirs()
    ensure_exports()
    ensure_sample_files()
    run(['systemctl', 'enable', '--now', 'nfs-server'])
    run(['exportfs', '-ra'])
    try:
        run(['firewall-cmd', '--permanent', '--add-service=nfs'])
        run(['firewall-cmd', '--reload'])
    except Exception:
        print('Aviso: firewalld no se pudo configurar automáticamente.')
    print('\nConfiguración final nodo1:')
    print(f'Usuario: {USER} uid={UID} gid={GID} home={USER_HOME}')
    print('Exports:')
    for x in EXPORT_LINES:
        print(' ', x)
    print('\nPruebas:')
    print('  showmount -e localhost')
    print(f'  ls -l {USER_HOME}')


if __name__ == '__main__':
    main()
