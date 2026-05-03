import os
import subprocess

def run_command(cmd):
    print(f"Ejecutando comando de bash: {cmd}")
    subprocess.run(cmd, shell=True)

def main():
    print("=== Limpiando el entorno ===")
    
    # 1. Eliminar el archivo de resultados
    run_command("rm -f /root/apache_listens")
    
    # 2. Opcional: Limpiar la configuracion de prueba que se creo en /etc/httpd/conf
    run_command("rm -rf /etc/httpd")
    
    print("\n=== Limpieza completada ===")

if __name__ == '__main__':
    main()
