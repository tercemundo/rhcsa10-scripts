import subprocess

def run_command(cmd):
    print(f"Ejecutando comando de bash: {cmd}")
    subprocess.run(cmd, shell=True)

def main():
    print("=== Instalando e iniciando Tuned ===")
    
    # Instalar el paquete
    cmd_install = "dnf install tuned -y"
    run_command(cmd_install)
    
    # Iniciar y habilitar el servicio (necesario para usar tuned-adm)
    run_command("systemctl enable --now tuned")
    
    print("\n=== Recomendacion de perfil ===")
    # Ver cual es el perfil recomendado para el sistema
    cmd_recommend = "tuned-adm recommend"
    run_command(cmd_recommend)
    
    print("\n=== Estableciendo el perfil powersave ===")
    # Aplicar el perfil especifico requerido
    cmd_profile = "tuned-adm profile powersave"
    run_command(cmd_profile)
    
    print("\n=== Verificando el perfil activo ===")
    run_command("tuned-adm active")

if __name__ == '__main__':
    main()
