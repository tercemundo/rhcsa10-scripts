import subprocess
import os

def run_command(cmd):
    print(f"Ejecutando comando de bash: {cmd}")
    subprocess.run(cmd, shell=True)

def main():
    print("=== Preparando el entorno ===")
    # Nos aseguramos de que el directorio a respaldar exista y tenga algo de contenido
    # para que el comando tar funcione correctamente sin dar errores.
    run_command("mkdir -p /opt/localdata")
    run_command("touch /opt/localdata/archivo1.txt")
    run_command("touch /opt/localdata/archivo2.txt")
    
    print("\n=== Instalando dependencias (bzip2) ===")
    # Instalamos bzip2 usando yum por si no está en el sistema
    run_command("yum install -y bzip2")

    print("\n=== Creando el backup en formato bz2 ===")
    # El parametro -j se utiliza en tar para usar bzip2
    cmd_tar = "tar -cjvf /root/localbackup.tar.bz2 /opt/localdata"
    run_command(cmd_tar)
    
    print("\n=== Verificando el backup creado ===")
    run_command("ls -lh /root/localbackup.tar.bz2")

if __name__ == '__main__':
    main()
