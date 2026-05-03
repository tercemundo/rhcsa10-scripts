#!/usr/bin/env python3
import subprocess

def run_bash(command):
    """Ejecuta un comando bash y muestra por pantalla lo que está haciendo"""
    print(f"BASH> {command}")
    subprocess.run(command, shell=True, check=False)

def main():
    print("=== 1. Instalando herramientas necesarias ===")
    run_bash("dnf install -y lvm2 xfsprogs")
    # Se intenta instalar vgutils tal como pediste (si el paquete no existe en tu repo, omitirá el error)
    run_bash("dnf install -y vgutils || echo 'Aviso: vgutils no se encontró, continuando...'")

    print("\n=== 2. Creando VG (vgdata) y LV (lvstore) si no existen ===")
    # Comprobamos si el VG existe
    res_vg = subprocess.run("vgs vgdata", shell=True, capture_output=True)
    if res_vg.returncode != 0:
        print("El VG 'vgdata' no existe. Creando entorno con un archivo loop para pruebas...")
        run_bash("dd if=/dev/zero of=/tmp/vgdata.img bs=1M count=500")
        
        # Configuramos un dispositivo loop para usarlo como Physical Volume (PV)
        loop_res = subprocess.run("losetup -f --show /tmp/vgdata.img", shell=True, capture_output=True, text=True)
        loop_dev = loop_res.stdout.strip()
        
        if loop_dev:
            run_bash(f"pvcreate {loop_dev}")
            run_bash(f"vgcreate vgdata {loop_dev}")
        else:
            print("Error: No se pudo configurar el loop device.")
            return

    # Comprobamos si el LV existe
    res_lv = subprocess.run("lvs /dev/vgdata/lvstore", shell=True, capture_output=True)
    if res_lv.returncode != 0:
        print("El LV 'lvstore' no existe. Creándolo con un tamaño inicial de 300M (requerido por XFS)...")
        run_bash("lvcreate -L 300M -n lvstore vgdata")
        # Le damos formato XFS para poder usar xfs_growfs luego
        run_bash("mkfs.xfs -f /dev/vgdata/lvstore")

    print("\n=== 3. Montando el LV en /mountpoint ===")
    run_bash("mkdir -p /mountpoint")
    # Verificamos si ya está montado
    res_mount = subprocess.run("mountpoint -q /mountpoint", shell=True)
    if res_mount.returncode != 0:
        run_bash("mount /dev/vgdata/lvstore /mountpoint")

    print("\n=== 4. Ejecutando la redimensión solicitada ===")
    # Redimensionamos el LV
    run_bash("lvresize -L 300M /dev/vgdata/lvstore")
    # Redimensionamos el sistema de archivos
    run_bash("xfs_growfs /mountpoint")

if __name__ == "__main__":
    main()
