#!/usr/bin/env python3
"""
Configura un repositorio HTTP con Apache en Rocky Linux 10.
Incluye el paquete hola-1.0-1.el10.noarch.rpm generado con build_hola_rpm.py
"""

import os
import subprocess
import sys
from pathlib import Path

# ── Rutas y configuración ────────────────────────────────────────────────────
RPM_NAME     = "hola-1.0-1.el10.noarch.rpm"
RPM_ORIGEN   = Path.home() / f"rpmbuild/RPMS/noarch/{RPM_NAME}"
BALINUX_DIR  = Path("/usr/local/balinux")
REPO_DIR     = Path("/var/www/html/repo")
HTTPD_CONF   = Path("/etc/httpd/conf/httpd.conf")
PORT         = 80

# ── Root check ───────────────────────────────────────────────────────────────
if os.geteuid() != 0:
    print("Debes ejecutar como root: sudo python3 setup_repo.py")
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

def is_installed(pkg):
    return subprocess.run(["rpm", "-q", pkg],
                          stdout=subprocess.DEVNULL,
                          stderr=subprocess.DEVNULL).returncode == 0

# ── 1. Instalar Apache ───────────────────────────────────────────────────────
print("\n1. Instalando Apache (httpd)...")
if not is_installed("httpd"):
    run("dnf -y install httpd", "No se pudo instalar httpd")
    print("   ✅ httpd instalado")
else:
    print("   ✅ httpd ya estaba instalado")

# ── 2. Instalar createrepo_c ─────────────────────────────────────────────────
# En Rocky 10, 'createrepo' fue reemplazado por 'createrepo_c'
print("\n2. Instalando createrepo_c...")
if not is_installed("createrepo_c"):
    run("dnf -y install createrepo_c", "No se pudo instalar createrepo_c")
    print("   ✅ createrepo_c instalado")
else:
    print("   ✅ createrepo_c ya estaba instalado")

# ── 3. Verificar que el RPM existe ───────────────────────────────────────────
print(f"\n3. Verificando RPM fuente: {RPM_ORIGEN}...")
if not RPM_ORIGEN.exists():
    # Buscar en rutas alternativas comunes
    alternativas = [
        Path.cwd() / RPM_NAME,
        Path("/root") / RPM_NAME,
    ]
    encontrado = None
    for alt in alternativas:
        if alt.exists():
            encontrado = alt
            break
    if encontrado:
        RPM_ORIGEN = encontrado
        print(f"   ℹ️  RPM encontrado en: {RPM_ORIGEN}")
    else:
        print(f"   ❌ No se encontró {RPM_NAME}")
        print(f"      Generalo primero con: python3 build_hola_rpm.py")
        sys.exit(1)
else:
    print(f"   ✅ RPM encontrado: {RPM_ORIGEN}")

# ── 4. Crear directorio /usr/local/balinux y copiar RPM ─────────────────────
print(f"\n4. Copiando RPM a {BALINUX_DIR}...")
BALINUX_DIR.mkdir(parents=True, exist_ok=True)
run(f"cp {RPM_ORIGEN} {BALINUX_DIR}/{RPM_NAME}", "No se pudo copiar el RPM a balinux")
print(f"   ✅ RPM copiado: {BALINUX_DIR}/{RPM_NAME}")

# ── 5. Configurar puerto en httpd.conf ───────────────────────────────────────
print(f"\n5. Configurando Apache en puerto {PORT}...")
contenido = HTTPD_CONF.read_text()
import re
contenido_nuevo = re.sub(r"^Listen\s+\d+", f"Listen {PORT}", contenido, flags=re.MULTILINE)
HTTPD_CONF.write_text(contenido_nuevo)
print(f"   ✅ Puerto configurado: Listen {PORT}")

# ── 6. Configurar firewall ───────────────────────────────────────────────────
print(f"\n6. Abriendo puerto {PORT} en firewalld...")
result = subprocess.run("systemctl is-active firewalld",
                        shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if result.returncode == 0:
    run(f"firewall-cmd --permanent --add-port={PORT}/tcp",
        f"No se pudo abrir el puerto {PORT}", exit_on_error=False)
    run("firewall-cmd --reload", "No se pudo recargar firewalld", exit_on_error=False)
    print(f"   ✅ Puerto {PORT}/tcp abierto")
else:
    print("   ℹ️  firewalld no está activo, omitiendo")

# ── 7. Crear estructura del repositorio ──────────────────────────────────────
print(f"\n7. Creando repositorio en {REPO_DIR}...")
REPO_DIR.mkdir(parents=True, exist_ok=True)
run(f"cp {BALINUX_DIR}/{RPM_NAME} {REPO_DIR}/", "No se pudo copiar el RPM al repo")
run(f"createrepo_c {REPO_DIR}", "No se pudo crear el repositorio con createrepo_c")
print(f"   ✅ Repositorio creado e indexado en {REPO_DIR}")

# ── 8. Habilitar y reiniciar Apache ─────────────────────────────────────────
print("\n8. Habilitando y reiniciando Apache...")
run("systemctl enable --now httpd", "No se pudo habilitar httpd")
run("systemctl restart httpd", "No se pudo reiniciar httpd")
print("   ✅ Apache en ejecución")

# ── 9. Crear el archivo .repo para el cliente ────────────────────────────────
REPO_FILE = Path("/etc/yum.repos.d/balinux.repo")
hostname   = subprocess.run("hostname -I | awk '{print $1}'",
                             shell=True, capture_output=True, text=True).stdout.strip()
REPO_FILE.write_text(f"""[balinux]
name=Repositorio Balinux Lab
baseurl=http://{hostname}/repo
enabled=1
gpgcheck=0
""")
print(f"\n9. ✅ Archivo de repositorio creado: {REPO_FILE}")

print(f"""
✅ Repositorio listo.

   URL del repo : http://{hostname}/repo
   RPM incluido : {RPM_NAME}

   Para instalar desde el repo:
     dnf install hola

   Para verificar el repo:
     dnf repolist
     dnf repo-pkgs balinux list
""")

