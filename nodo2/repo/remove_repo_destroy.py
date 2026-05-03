#!/usr/bin/env python3
"""
Limpia todo lo generado por setup_repo.py en el servidor.
Inverso de setup_repo.py — Rocky Linux 10
"""

import os
import subprocess
import sys
import shutil
from pathlib import Path

RPM_NAME    = "hola-1.0-1.el10.noarch.rpm"
BALINUX_DIR = Path("/usr/local/balinux")
REPO_DIR    = Path("/var/www/html/repo")
HTTPD_CONF  = Path("/etc/httpd/conf/httpd.conf")
REPO_FILE   = Path("/etc/yum.repos.d/balinux.repo")
RPMBUILD    = Path.home() / "rpmbuild"
PORT        = 80

if os.geteuid() != 0:
    print("Debes ejecutar como root: sudo python3 remove_repo_server.py")
    sys.exit(1)

def run(cmd, error_msg=None):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0 and error_msg:
        print(f"  ⚠️  {error_msg}: {result.stderr.strip()}")
    return result

def is_installed(pkg):
    return subprocess.run(["rpm", "-q", pkg],
                          stdout=subprocess.DEVNULL,
                          stderr=subprocess.DEVNULL).returncode == 0

print("\n🧹 Limpiando servidor (inverso de setup_repo.py)...\n")

# 1. Detener y deshabilitar httpd
print("1. Deteniendo y deshabilitando httpd...")
run("systemctl is-active httpd", )
result = subprocess.run("systemctl is-active httpd", shell=True,
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if result.returncode == 0:
    run("systemctl disable --now httpd", "No se pudo detener httpd")
    print("   ✅ httpd detenido y deshabilitado")
else:
    run("systemctl disable httpd")
    print("   ℹ️  httpd ya estaba inactivo")

# 2. Desinstalar httpd y createrepo_c
print("\n2. Desinstalando paquetes...")
for pkg in ["httpd", "createrepo_c"]:
    if is_installed(pkg):
        run(f"dnf -y remove {pkg}", f"No se pudo desinstalar {pkg}")
        print(f"   ✅ {pkg} desinstalado")
    else:
        print(f"   ℹ️  {pkg} no estaba instalado")

# 3. Eliminar configuración de httpd
print("\n3. Eliminando configuración de httpd...")
if HTTPD_CONF.parent.exists():
    shutil.rmtree(str(HTTPD_CONF.parent), ignore_errors=True)
    print(f"   ✅ Eliminado: /etc/httpd")
else:
    print("   ℹ️  /etc/httpd no existe")

# 4. Cerrar puerto 80 en firewalld
print(f"\n4. Cerrando puerto {PORT} en firewalld...")
result = subprocess.run("systemctl is-active firewalld", shell=True,
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if result.returncode == 0:
    run(f"firewall-cmd --permanent --remove-port={PORT}/tcp",
        f"No se pudo cerrar el puerto {PORT}")
    run("firewall-cmd --reload", "No se pudo recargar firewalld")
    print(f"   ✅ Puerto {PORT}/tcp cerrado en firewalld")
else:
    print("   ℹ️  firewalld no está activo, omitiendo")

# 5. Eliminar directorio del repositorio /var/www/html/repo
print(f"\n5. Eliminando directorio del repositorio {REPO_DIR}...")
if REPO_DIR.exists():
    shutil.rmtree(str(REPO_DIR), ignore_errors=True)
    print(f"   ✅ Eliminado: {REPO_DIR}")
else:
    print(f"   ℹ️  No existe: {REPO_DIR}")

# 6. Eliminar /usr/local/balinux
print(f"\n6. Eliminando directorio {BALINUX_DIR}...")
if BALINUX_DIR.exists():
    shutil.rmtree(str(BALINUX_DIR), ignore_errors=True)
    print(f"   ✅ Eliminado: {BALINUX_DIR}")
else:
    print(f"   ℹ️  No existe: {BALINUX_DIR}")

# 7. Eliminar archivo .repo local (si existe en el servidor)
print(f"\n7. Eliminando {REPO_FILE}...")
if REPO_FILE.exists():
    REPO_FILE.unlink()
    print(f"   ✅ Eliminado: {REPO_FILE}")
else:
    print(f"   ℹ️  No existe: {REPO_FILE}")

# 8. Eliminar árbol de rpmbuild (~/ rpmbuild)
print(f"\n8. Eliminando ~/rpmbuild...")
if RPMBUILD.exists():
    shutil.rmtree(str(RPMBUILD), ignore_errors=True)
    print(f"   ✅ Eliminado: {RPMBUILD}")
else:
    print(f"   ℹ️  No existe: {RPMBUILD}")

# 9. Limpiar caché de dnf
print("\n9. Limpiando caché de dnf...")
run("dnf clean all")
print("   ✅ Caché limpiado")

print("\n✅ Servidor limpio. Podés volver a ejecutar build_hola_rpm.py + setup_repo.py desde cero.\n")

