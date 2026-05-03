import subprocess

def run_command(cmd):
    print(f"Ejecutando comando de bash: {cmd}")
    subprocess.run(cmd, shell=True)

def main():
    print("=== Limpiando el entorno del ejercicio ===")
    
    # Usamos sed para eliminar especificamente la linea 'umask 277' de .bashrc
    cmd_sed = "sed -i '/umask 277/d' /home/adam/.bashrc"
    run_command(cmd_sed)
    
    # (Opcional) Si quieres eliminar completamente al usuario de prueba 'adam'
    # puedes descomentar la siguiente linea:
    # run_command("userdel -r adam 2>/dev/null")
    
    print("\n=== Limpieza completada ===")
    print("Verificando que la linea ha sido eliminada:")
    run_command("cat /home/adam/.bashrc | grep 'umask 277' || echo 'Linea eliminada con exito.'")

if __name__ == '__main__':
    main()
