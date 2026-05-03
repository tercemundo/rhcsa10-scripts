import os
import subprocess

def run_command(cmd):
    print(f"Ejecutando: {cmd}")
    subprocess.run(cmd, shell=True)

def main():
    print("=== Configurando entorno para el ejercicio ===")
    
    # 1. Crear usuario steve
    # Usamos -m para que se cree el directorio home
    run_command("useradd -m steve 2>/dev/null")
    
    # 2. Crear archivos en el home de steve
    run_command("touch /home/steve/archivo_home1.txt")
    run_command("touch /home/steve/archivo_home2.txt")
    run_command("chown steve:steve /home/steve/archivo_home1.txt /home/steve/archivo_home2.txt")
    
    # 3. Crear archivos en /tmp
    run_command("touch /tmp/archivo_tmp_steve1.txt")
    run_command("touch /tmp/archivo_tmp_steve2.txt")
    run_command("chown steve:steve /tmp/archivo_tmp_steve1.txt /tmp/archivo_tmp_steve2.txt")
    
    # 4. Crear directorio destino
    run_command("mkdir -p /root/found.steve")
    
    print("\n=== Ejecutando la busqueda y copia ===")
    # Buscamos todos los archivos del usuario steve y los copiamos a /root/found.steve
    # Usamos -type f para copiar solo archivos (evitar directorios que podrian causar warnings con cp)
    run_command("find / -user steve -type f -exec cp -p {} /root/found.steve \\; 2>/dev/null")
    
    print("\n=== Verificando el resultado en /root/found.steve ===")
    run_command("ls -la /root/found.steve")
    
if __name__ == '__main__':
    main()
