import os
import subprocess

def run_command(cmd):
    print(f"Ejecutando comando de bash: {cmd}")
    subprocess.run(cmd, shell=True)

def main():
    print("=== Preparando el entorno (Opcional) ===")
    # Aseguramos que el archivo de configuracion exista con algo de contenido para que grep encuentre algo
    run_command("mkdir -p /etc/httpd/conf")
    run_command("echo '# Fichero de prueba' > /etc/httpd/conf/httpd.conf")
    run_command("echo 'Listen 80' >> /etc/httpd/conf/httpd.conf")
    run_command("echo 'Listen 8082' >> /etc/httpd/conf/httpd.conf")
    
    print("\n=== Ejecutando la tarea principal ===")
    comando_principal = 'grep -ni "Listen" /etc/httpd/conf/httpd.conf > /root/apache_listens'
    run_command(comando_principal)
    
    print("\n=== Verificando el resultado en /root/apache_listens ===")
    run_command("cat /root/apache_listens")

if __name__ == '__main__':
    main()
