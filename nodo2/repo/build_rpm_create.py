#!/usr/bin/env python3
"""
Genera hola-1.0-1.el10.noarch.rpm — Rocky Linux 10
El RPM instala /usr/bin/hola y al ejecutarlo imprime "Hola Mundo"
"""

import os
import subprocess
import sys
import shutil
from pathlib import Path

# Nomenclatura Rocky Linux 10
NAME    = "hola"
VERSION = "1.0"
RELEASE = "1.el10"
ARCH    = "noarch"
RPM_FILENAME = f"{NAME}-{VERSION}-{RELEASE}.{ARCH}.rpm"

def run(cmd, error_msg=None):
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ {error_msg or cmd}")
        print(f"   {result.stderr.strip()}")
        sys.exit(1)
    return result.stdout

# 1. Verificar e instalar rpm-build
print("1. Verificando dependencias...")
result = subprocess.run("rpm -q rpm-build", shell=True,
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if result.returncode != 0:
    print("   📦 Instalando rpm-build...")
    run("dnf -y install rpm-build", "No se pudo instalar rpm-build")
print("   ✅ rpm-build disponible")

# 2. Crear estructura rpmbuild
BUILD_DIR = Path.home() / "rpmbuild"
for d in ["BUILD", "BUILDROOT", "RPMS", "SOURCES", "SPECS", "SRPMS"]:
    (BUILD_DIR / d).mkdir(parents=True, exist_ok=True)
print("2. ✅ Estructura ~/rpmbuild creada")

# 3. Crear el script hola
SOURCES_DIR = BUILD_DIR / "SOURCES"
TAR_DIR     = SOURCES_DIR / f"{NAME}-{VERSION}"
TAR_DIR.mkdir(parents=True, exist_ok=True)

hola_script = TAR_DIR / "hola"
hola_script.write_text('''#!/bin/bash
echo "Hola Mundo"
''')
hola_script.chmod(0o755)

# Empaquetar en tar.gz
run(f"tar -czf {SOURCES_DIR}/{NAME}-{VERSION}.tar.gz -C {SOURCES_DIR} {NAME}-{VERSION}",
    "No se pudo crear el tarball")
shutil.rmtree(TAR_DIR)
print("3. ✅ Tarball fuente creado")

# 4. Crear el archivo SPEC
SPEC_FILE = BUILD_DIR / "SPECS" / f"{NAME}.spec"
SPEC_FILE.write_text(f'''Name:       {NAME}
Version:    {VERSION}
Release:    {RELEASE}
Summary:    Imprime Hola Mundo en pantalla
License:    GPL
BuildArch:  {ARCH}
Source0:    %{{name}}-%{{version}}.tar.gz

%description
Paquete de laboratorio: al ejecutar /usr/bin/hola imprime "Hola Mundo".

%prep
%setup -q

%install
mkdir -p %{{buildroot}}/%{{_bindir}}
install -m 755 hola %{{buildroot}}/%{{_bindir}}/hola

%files
%{{_bindir}}/hola

%changelog
* Sat Apr 18 2026 Lab <lab@nodo.local> - {VERSION}-1
- Primera version del paquete hola
''')
print("4. ✅ Archivo SPEC creado")

# 5. Construir el RPM
print("5. Construyendo el RPM...")
run(f"rpmbuild -bb {SPEC_FILE}", "No se pudo construir el RPM")

# 6. Mover el RPM al directorio actual
rpm_src = BUILD_DIR / "RPMS" / ARCH / RPM_FILENAME
rpm_dst = Path.cwd() / RPM_FILENAME
if rpm_src.exists():
    shutil.copy2(rpm_src, rpm_dst)
    print(f"   ✅ RPM generado: {rpm_dst}")
else:
    # Buscar el RPM generado con otro nombre
    rpms = list((BUILD_DIR / "RPMS" / ARCH).glob("*.rpm"))
    if rpms:
        shutil.copy2(rpms[0], Path.cwd() / rpms[0].name)
        print(f"   ✅ RPM generado: {rpms[0].name}")
    else:
        print("❌ No se encontró el RPM generado")
        sys.exit(1)

print(f"\n✅ Listo. Para instalar:")
print(f"   rpm -ivh {RPM_FILENAME}")
print(f"\n   Y luego ejecutar:")
print(f"   hola")

