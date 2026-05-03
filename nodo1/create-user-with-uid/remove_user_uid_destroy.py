import subprocess

def run_command(cmd):
    print(f"Ejecutando comando de bash: {cmd}")
    subprocess.run(cmd, shell=True)

def main():
    print("=== Limpiando el entorno (Eliminando usuario) ===")
    
    # Nos aseguramos de que no haya procesos de 'roger' antes de borrarlo
    cmd_kill = "killall -u roger 2>/dev/null"
    run_command(cmd_kill)
    
    # Comando para eliminar al usuario 'roger' y su directorio home
    cmd_userdel = "userdel -r roger"
    run_command(cmd_userdel)
    
    print("\n=== Limpieza completada ===")

if __name__ == '__main__':
    main()
