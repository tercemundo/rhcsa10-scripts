#!/usr/bin/env python3
"""
Limpia la configuración del repo balinux y desinstala el paquete hola.
Inverso de install_hola.py
"""

import os
import subprocess
import sys
from pathlib import Path

REPO_FILE = Path("/etc/yum.repos.d/balinux.repo")
PACKAGE   = "hola"

if os.geteuid() != 0:
    print("Debes ejecutar como root: sudo python3 remove_repo.py")
    sys.exit(1)

def run(cmd, error_msg=None, exit_on_error=False):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        msg = error_msg or f"Error ejecutando: {cmd}"
        print(f"  ⚠️  {msg}")
        print(f"     {result.stderr.strip()}")
        if exit_on_error:
            sys.exit(1)
    return result.stdout

def is_installed(pkg):
    return subprocess.run(["rpm", "-q", pkg],
                          stdout=subprocess.DEVNULL,
                          stderr=subprocess.DEVNULL).returncode == 0

print("\n🧹 Iniciando limpieza del cliente...\n")

# 1. Desinstalar el paquete hola
print(f"1. Desinstalando paquete '{PACKAGE}'...")
if is_installed(PACKAGE):
    run(f"dnf -y remove {PACKAGE}", f"No se pudo desinstalar {PACKAGE}")
    if not is_installed(PACKAGE):
        print(f"   ✅ Paquete '{PACKAGE}' desinstalado correctamente")
    else:
        print(f"   ⚠️  El paquete sigue instalado, intentá manualmente: rpm -e {PACKAGE}")
else:
    print(f"   ℹ️  El paquete '{PACKAGE}' no estaba instalado")

# 2. Eliminar el archivo del repo
print(f"\n2. Eliminando archivo de repo {REPO_FILE}...")
if REPO_FILE.exists():
    REPO_FILE.unlink()
    print(f"   ✅ Eliminado: {REPO_FILE}")
else:
    print(f"   ℹ️  No existe: {REPO_FILE}")

# 3. Limpiar caché de dnf
print("\n3. Limpiando caché de dnf...")
run("dnf clean all", "No se pudo limpiar el caché")
print("   ✅ Caché limpiado")

print("\n✅ Limpieza completada. Podés volver a ejecutar install_hola.py desde cero.\n")
