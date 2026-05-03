#!/usr/bin/env python3
"""
Configura el repositorio balinux en el cliente e instala el paquete hola.
"""

import os
import subprocess
import sys
from pathlib import Path

REPO_URL  = "http://192.168.56.121/repo"
REPO_FILE = Path("/etc/yum.repos.d/balinux.repo")
PACKAGE   = "hola"

if os.geteuid() != 0:
    print("Debes ejecutar como root: sudo python3 install_hola.py")
    sys.exit(1)

def run(cmd, error_msg=None, exit_on_error=True):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        msg = error_msg or f"Error ejecutando: {cmd}"
        print(f"  ❌ {msg}")
        print(f"     {result.stderr.strip()}")
        if exit_on_error:
            sys.exit(1)
    return result.stdout

# 1. Verificar conectividad con el repo
print(f"\n1. Verificando conectividad con {REPO_URL}...")
result = subprocess.run(f"curl -s --connect-timeout 5 -o /dev/null -w '%{{http_code}}' {REPO_URL}",
                        shell=True, capture_output=True, text=True)
http_code = result.stdout.strip()
if http_code not in ("200", "301", "302"):
    print(f"   ❌ No se puede acceder al repo (HTTP {http_code})")
    print(f"      Verificá que el servidor {REPO_URL} esté activo y accesible")
    sys.exit(1)
print(f"   ✅ Repositorio accesible (HTTP {http_code})")

# 2. Crear el archivo .repo
print(f"\n2. Configurando repositorio en {REPO_FILE}...")
REPO_FILE.write_text(f"""[balinux]
name=Repositorio Balinux Lab
baseurl={REPO_URL}
enabled=1
gpgcheck=0
""")
print(f"   ✅ Archivo de repo creado: {REPO_FILE}")

# 3. Limpiar caché de dnf
print("\n3. Limpiando caché de dnf...")
run("dnf clean all", "No se pudo limpiar el caché", exit_on_error=False)
run("dnf makecache", "No se pudo generar el caché", exit_on_error=False)
print("   ✅ Caché actualizado")

# 4. Verificar que el paquete está disponible en el repo
print(f"\n4. Verificando disponibilidad del paquete '{PACKAGE}' en el repo...")
result = subprocess.run(f"dnf repo-pkgs balinux list 2>/dev/null | grep {PACKAGE}",
                        shell=True, capture_output=True, text=True)
if result.returncode != 0 or not result.stdout.strip():
    print(f"   ⚠️  No se encontró '{PACKAGE}' en el repo balinux")
    print(f"      Verificá que el RPM esté indexado en {REPO_URL}")
else:
    print(f"   ✅ Paquete encontrado: {result.stdout.strip()}")

# 5. Instalar el paquete
print(f"\n5. Instalando paquete '{PACKAGE}'...")
run(f"dnf -y install {PACKAGE}", f"No se pudo instalar {PACKAGE}")
print(f"   ✅ Paquete '{PACKAGE}' instalado correctamente")

# 6. Verificar instalación
print(f"\n6. Verificando instalación...")
result = subprocess.run(f"rpm -q {PACKAGE}", shell=True, capture_output=True, text=True)
if result.returncode == 0:
    print(f"   ✅ {result.stdout.strip()}")
else:
    print(f"   ⚠️  No se pudo verificar la instalación con rpm -q")

# 7. Ejecutar hola
print(f"\n7. Ejecutando 'hola':")
print("   " + "-"*30)
run("hola", "No se pudo ejecutar hola")
print("   " + "-"*30)

print(f"""
✅ Todo listo.

   Repo configurado : {REPO_FILE}
   Paquete          : {PACKAGE}

   Comandos útiles:
     hola                          # Ejecutar el programa
     rpm -qi hola                  # Info del paquete instalado
     dnf repo-pkgs balinux list    # Ver paquetes del repo
""")
