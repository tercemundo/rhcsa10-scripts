import os
import subprocess

def run_command(cmd):
    print(f"Ejecutando: {cmd}")
    subprocess.run(cmd, shell=True)

def main():
    print("=== Limpiando el entorno del ejercicio ===")
    
    # 1. Eliminar archivos especificos creados en /tmp
    run_command("rm -f /tmp/archivo_tmp_steve1.txt /tmp/archivo_tmp_steve2.txt")
    
    # 2. Eliminar el directorio de resultados y todo su contenido
    run_command("rm -rf /root/found.steve")
    
    # 3. Asegurarse de que no hay procesos del usuario corriendo antes de borrarlo
    run_command("killall -u steve 2>/dev/null")
    
    # 4. Eliminar al usuario steve y su directorio home (-r)
    run_command("userdel -r steve 2>/dev/null")
    
    print("\n=== Limpieza completada ===")
    
if __name__ == '__main__':
    main()
