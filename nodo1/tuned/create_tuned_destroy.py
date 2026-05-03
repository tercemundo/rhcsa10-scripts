import subprocess

def run_command(cmd):
    print(f"Ejecutando comando de bash: {cmd}")
    subprocess.run(cmd, shell=True)

def main():
    print("=== Limpiando el entorno del ejercicio (Tuned) ===")
    
    # Desactivar perfiles activos
    run_command("tuned-adm off 2>/dev/null")
    
    # Detener y deshabilitar el demonio
    run_command("systemctl disable --now tuned 2>/dev/null")
    
    # Remover el paquete del sistema
    cmd_remove = "dnf remove tuned -y"
    run_command(cmd_remove)
    
    print("\n=== Limpieza completada ===")

if __name__ == '__main__':
    main()
