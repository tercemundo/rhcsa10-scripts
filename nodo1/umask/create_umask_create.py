import subprocess

def run_command(cmd):
    print(f"Ejecutando comando de bash: {cmd}")
    subprocess.run(cmd, shell=True)

def main():
    print("=== Preparando el entorno (Opcional) ===")
    # Nos aseguramos de que el usuario adam exista.
    # Si ya existe, useradd fallará de forma silenciosa gracias a 2>/dev/null.
    run_command("useradd -m adam 2>/dev/null || touch /home/adam/.bashrc")
    
    print("\n=== Configurando umask para el usuario adam ===")
    # Añadimos la linea al final del archivo .bashrc
    cmd_umask = 'echo "umask 277" >> /home/adam/.bashrc'
    run_command(cmd_umask)
    
    print("\n=== Verificando la configuracion ===")
    run_command("tail -n 3 /home/adam/.bashrc")

if __name__ == '__main__':
    main()
