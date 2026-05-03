#!/usr/bin/env python3

import subprocess
import os
import sys
import re

PORT = 8082
HTTPD_CONF = "/etc/httpd/conf/httpd.conf"

if os.geteuid() != 0:
    print("Debes ejecutar como root: sudo python3 remove_httpd.py")
    sys.exit(1)

def run(command, error_msg=None, exit_on_error=True):
    try:
        result = subprocess.run(command, shell=True, check=True,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        msg = error_msg or f"Error ejecutando: {command}"
        print(f"  ⚠️  {msg}: {e.stderr.strip()}")
        if exit_on_error:
            sys.exit(1)
        return None

def is_installed(pkg):
    result = subprocess.run(["rpm", "-q", pkg],
                            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    return result.returncode == 0

print("\n🧹 Iniciando limpieza de httpd...\n")

# 1. Detener y deshabilitar httpd
print("1. Deteniendo y deshabilitando httpd...")
result = subprocess.run("systemctl is-active httpd",
                        shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if result.returncode == 0:
    run("systemctl disable --now httpd", "No se pudo detener/deshabilitar httpd", exit_on_error=False)
    print("   ✅ httpd detenido y deshabilitado")
else:
    run("systemctl disable httpd", exit_on_error=False)
    print("   ℹ️  httpd ya estaba inactivo")

# 2. Restaurar puerto 80 en httpd.conf
print("\n2. Restaurando puerto en httpd.conf...")
if os.path.exists(HTTPD_CONF):
    with open(HTTPD_CONF, "r") as f:
        contenido = f.read()
    contenido_restaurado = re.sub(r"^Listen\s+\d+", "Listen 80", contenido, flags=re.MULTILINE)
    if contenido_restaurado != contenido:
        with open(HTTPD_CONF, "w") as f:
            f.write(contenido_restaurado)
        print(f"   ✅ Puerto restaurado a Listen 80 en {HTTPD_CONF}")
    else:
        print("   ℹ️  El puerto ya era 80 o no se encontró la directiva Listen")
else:
    print(f"   ℹ️  No existe {HTTPD_CONF}")

# 3. Eliminar el puerto de SELinux
print(f"\n3. Eliminando puerto {PORT} de SELinux...")
if is_installed("policycoreutils-python-utils"):
    result = subprocess.run(f"semanage port -l | grep -w http_port_t | grep -w {PORT}",
                            shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    if result.returncode == 0:
        run(f"semanage port -d -t http_port_t -p tcp {PORT}",
            f"No se pudo eliminar el puerto {PORT} de SELinux", exit_on_error=False)
        print(f"   ✅ Puerto {PORT} eliminado de SELinux")
    else:
        print(f"   ℹ️  El puerto {PORT} no estaba registrado en SELinux")
else:
    print("   ℹ️  policycoreutils-python-utils no está instalado, omitiendo SELinux")

# 4. Eliminar el puerto de firewalld
print(f"\n4. Cerrando puerto {PORT} en firewalld...")
result = subprocess.run("systemctl is-active firewalld",
                        shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
if result.returncode == 0:
    run(f"firewall-cmd --permanent --remove-port={PORT}/tcp",
        f"No se pudo cerrar el puerto {PORT} en firewalld", exit_on_error=False)
    run("firewall-cmd --reload", "No se pudo recargar firewalld", exit_on_error=False)
    print(f"   ✅ Puerto {PORT}/tcp removido de firewalld")
else:
    print("   ℹ️  firewalld no está activo, omitiendo")

# 5. Desinstalar paquetes
print("\n5. Desinstalando paquetes instalados por el lab...")
for pkg in ["httpd", "policycoreutils-python-utils"]:
    if is_installed(pkg):
        run(f"dnf -y remove {pkg}", f"No se pudo desinstalar {pkg}", exit_on_error=False)
        print(f"   ✅ {pkg} desinstalado")
    else:
        print(f"   ℹ️  {pkg} ya no está instalado")

print("\n✅ Limpieza completada. Podés volver a ejecutar setup_httpd.py desde cero.\n")

