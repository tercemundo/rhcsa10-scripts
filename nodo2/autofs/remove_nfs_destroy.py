#!/usr/bin/env python3
import os
import subprocess
import sys
from pathlib import Path

# Verifica ejecución como root
if os.geteuid() != 0:
    print("Debes ejecutar como root: sudo python3 remove_nfs_autofs.py")
    sys.exit(1)

# Paquetes a desinstalar
packages = ["nfs-utils", "autofs"]

# Intentar desinstalar (yum/dnf depende de la distribución)
for pkg in packages:
    try:
        print(f"Desinstalando paquete {pkg}...")
        subprocess.run(["dnf", "remove", "-y", pkg], check=True)
    except subprocess.CalledProcessError:
        print(f"Error desinstalando {pkg} (ignorado).")

# Archivos y directorios generados
master_dir = Path("/etc/auto.master.d")
maps = Path("/etc/auto.nfs4")

# Borrar maps si existe
if maps.exists():
    print(f"Borrando mapa {maps}...")
    maps.unlink()

# Borrar archivos en /etc/auto.master.d
if master_dir.exists():
    for f in master_dir.iterdir():
        if f.suffix == ".autofs":
            print(f"Borrando {f}...")
            f.unlink()

# Borrar /mnt/nfs4 o /mnt/autofs si existen (solo si es directorio vacío después de desmontar)
for mnt in ["/mnt/nfs4", "/mnt/autofs"]:
    mnt_path = Path(mnt)
    if mnt_path.exists() and mnt_path.is_dir():
        print(f"Desinstalando montajes de {mnt_path}...")
        subprocess.run(["umount", mnt], check=False)   # desmonta si está montado
        if not any(mnt_path.iterdir()):
            print(f"Borrando {mnt_path}...")
            mnt_path.rmdir()
        else:
            print(f"{mnt_path} no está vacío, no se borra.")

print("\n✅ Limpieza completa realizada.")
