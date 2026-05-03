#!/usr/bin/env python3

import subprocess
import os
import sys
import re

PORT = 8082

# Verificar que se ejecuta como root
if os.geteuid() != 0:
    print("Debes ejecutar como root: sudo python3 setup_httpd.py")
    sys.exit(1)

def run(command, error_msg=None):
    try:
        result = subprocess.run(command, shell=True, check=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        msg = error_msg or f"Error ejecutando: {command}"
        print(f"❌ {msg}")
        print(f"   {e.stderr.strip()}")
        sys.exit(1)

def is_installed(pkg):
    result = subprocess.run(["rpm", "-q", pkg],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return result.returncode == 0

# 1. Instalar httpd si no está instalado
if not is_installed("httpd"):
    print("📦 httpd no está instalado. Instalando...")
    run("dnf -y install httpd", "No se pudo instalar httpd")
    print("✅ httpd instalado correctamente")
else:
    print("✅ httpd ya está instalado")

# 2. Instalar policycoreutils-python-utils si no está instalado
if not is_installed("policycoreutils-python-utils"):
    print("\n📦 policycoreutils-python-utils no está instalado. Instalando...")
    run("dnf -y install policycoreutils-python-utils",
        "No se pudo instalar policycoreutils-python-utils")
    print("✅ policycoreutils-python-utils instalado correctamente")
else:
    print("✅ policycoreutils-python-utils ya está instalado")

# 3. Cambiar el puerto en httpd.conf
HTTPD_CONF = "/etc/httpd/conf/httpd.conf"
print(f"\n🔧 Configurando httpd para escuchar en el puerto {PORT}...")

with open(HTTPD_CONF, "r") as f:
    contenido = f.read()

contenido_modificado = re.sub(r"^Listen\s+\d+", f"Listen {PORT}", contenido, flags=re.MULTILINE)

if contenido_modificado == contenido:
    print(f"⚠️  No se encontró directiva 'Listen' para reemplazar en {HTTPD_CONF}")
else:
    with open(HTTPD_CONF, "w") as f:
        f.write(contenido_modificado)
    print(f"✅ Puerto configurado: Listen {PORT}")

# 4. Habilitar el puerto en SELinux
print(f"\n🔐 Habilitando puerto {PORT} en SELinux...")
result = subprocess.run(f"semanage port -l | grep http_port_t | grep {PORT}",
                        shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if result.returncode != 0:
    run(f"semanage port -a -t http_port_t -p tcp {PORT}",
        f"No se pudo agregar el puerto {PORT} a SELinux")
    print(f"✅ Puerto {PORT} habilitado en SELinux")
else:
    print(f"✅ Puerto {PORT} ya estaba habilitado en SELinux")

# 5. Abrir el puerto en firewalld
print(f"\n🔥 Abriendo puerto {PORT} en firewalld...")
result = subprocess.run("systemctl is-active firewalld",
                        shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if result.returncode == 0:
    run(f"firewall-cmd --permanent --add-port={PORT}/tcp",
        f"No se pudo abrir el puerto {PORT} en firewalld")
    run("firewall-cmd --reload", "No se pudo recargar firewalld")
    print(f"✅ Puerto {PORT}/tcp abierto en firewalld")
else:
    print("ℹ️  firewalld no está activo, omitiendo")

# 6. Habilitar y reiniciar httpd
print("\n🚀 Habilitando y reiniciando httpd...")
run("systemctl enable --now httpd", "No se pudo habilitar httpd")
run("systemctl restart httpd", "No se pudo reiniciar httpd")
print("✅ httpd habilitado y en ejecución")

print(f"\n✅ Configuración completada. httpd escuchando en el puerto {PORT}")
print(f"   Verificar: curl http://localhost:{PORT}")
