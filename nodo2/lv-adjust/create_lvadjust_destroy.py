#!/usr/bin/env python3
import subprocess

def run_bash(command):
    print(f"BASH> {command}")
    subprocess.run(command, shell=True, check=False)

def main():
    print("=== 1. Desmontando el LV ===")
    run_bash("umount /mountpoint")
    
    print("\n=== 2. Destruyendo el LV y el VG ===")
    run_bash("lvremove -y /dev/vgdata/lvstore")
    run_bash("vgremove -y vgdata")
    
    print("\n=== 3. Limpiando el PV y el archivo loop de pruebas ===")
    # Averiguamos qué loop device está usando nuestro archivo
    res = subprocess.run("losetup -j /tmp/vgdata.img", shell=True, capture_output=True, text=True)
    if res.stdout:
        loop_dev = res.stdout.split(":")[0].strip()
        if loop_dev:
            run_bash(f"pvremove -y {loop_dev}")
            run_bash(f"losetup -d {loop_dev}")
            
    run_bash("rm -f /tmp/vgdata.img")
    run_bash("rm -rf /mountpoint")
    
    print("\nDestrucción completada exitosamente.")

if __name__ == "__main__":
    main()
