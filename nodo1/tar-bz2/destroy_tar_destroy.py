import subprocess

def run_command(cmd):
    print(f"Ejecutando comando de bash: {cmd}")
    subprocess.run(cmd, shell=True)

def main():
    print("=== Limpiando el entorno del ejercicio ===")
    
    # Eliminar el archivo de respaldo generado
    cmd_rm = "rm -f /root/localbackup.tar.bz2"
    run_command(cmd_rm)
    
    # Opcional: eliminar el directorio de prueba que creamos
    cmd_rm_dir = "rm -rf /opt/localdata"
    run_command(cmd_rm_dir)
    
    print("\n=== Limpieza completada ===")

if __name__ == '__main__':
    main()
