#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path

# Variables
IP = "192.168.56.120"
NAME = "nodo1"
NFS4_MAP = "/etc/auto.nfs4"
AUTOMASTER_DIR = "/etc/auto.master.d"
MOUNT_ROOT = "/mnt/nfs4"

# Asegurarse de ejecutar como root
if os.geteuid() != 0:
    print("Debes ejecutar como root: sudo python3 add_nfs.py")
    sys.exit(1)

# Asegurar que el directorio de maps autofs existe
Path(AUTOMASTER_DIR).mkdir(parents=True, exist_ok=True)

# Verificar /etc/hosts y agregar si no existe
hosts = "/etc/hosts"
entry = f"{IP} {NAME}"

old = ""
found = False
if Path(hosts).exists():
    with open(hosts, "r") as f:
        old = f.read()
        if entry in old.splitlines():
            found = True

if not found:
    print(f"Agregando a {hosts}: {entry}")
    if old and not old.endswith("\n"):
        old += "\n"
    with open(hosts, "w") as f:
        f.write(old)
        f.write(entry + "\n")

print("Lista /etc/hosts actualizada")

# Instalar paquetes NFS y autofs
subprocess.run(["dnf", "install", "-y", "nfs-utils", "autofs"], check=True)

# Asegurar el punto de montaje en /mnt/nfs4
Path(MOUNT_ROOT).mkdir(parents=True, exist_ok=True)

# Crear el map indirecto en /etc/auto.nfs4
map_content = "* -rw,sync,fstype=nfs4 nodo1:/home/guests/&\n"
Path(NFS4_MAP).write_text(map_content)

# Crear el archivo de master en /etc/auto.master.d
master_file = Path(AUTOMASTER_DIR) / "exercise_nfs4.autofs"
master_content = f"{MOUNT_ROOT} {NFS4_MAP}\n"
master_file.write_text(master_content)

# Habilitar y arrancar autofs
subprocess.run(["systemctl", "enable", "--now", "autofs"], check=True)

# Mensaje final
print("\n✅ Autofs listo:")
print("- /mnt/nfs4 controlado por autofs con NFSv4")
print("- Accede: cd /mnt/nfs4/qq")
print("- Verifica: mount | grep /mnt/nfs4/qq")
