import subprocess

def run_command(cmd):
    print(f"Ejecutando comando de bash: {cmd}")
    subprocess.run(cmd, shell=True)

def main():
    print("=== Creando usuario con UID especifico ===")
    
    # Comando para crear el usuario con UID 3456
    cmd_useradd = "useradd -u 3456 roger"
    run_command(cmd_useradd)
    
    # Comando para establecer la contraseña usando --stdin
    cmd_passwd = 'echo "Train@456" | passwd --stdin roger'
    run_command(cmd_passwd)
    
    print("\n=== Verificando usuario creado ===")
    run_command("id roger")

if __name__ == '__main__':
    main()
