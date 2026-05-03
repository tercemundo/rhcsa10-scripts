#!/usr/bin/env python3
import subprocess
import os

def run_bash(command):
    print(f"BASH> {command}")
    subprocess.run(command, shell=True, check=False)

def main():
    print("=== 1. Desmontando el LV ===")
    run_bash("umount /mnt/testqa")
    
    print("\n=== 2. Limpiando /etc/fstab ===")
    print('BASH> sed -i "/qavg\\/testqa/d" /etc/fstab')
    if os.path.exists("/etc/fstab"):
        with open("/etc/fstab", "r") as f:
            lines = f.readlines()
        with open("/etc/fstab", "w") as f:
            for line in lines:
                if "/dev/qavg/testqa" not in line:
                    f.write(line)
                    
    print("\n=== 3. Destruyendo LVM ===")
    run_bash("lvremove -y /dev/qavg/testqa")
    run_bash("vgremove -y qavg")
    
    print("\n=== 4. Limpiando el Physical Volume y simulador ===")
    # Averiguamos si usamos loop para simular sdc
    res = subprocess.run("losetup -j /tmp/sdc_sim.img", shell=True, capture_output=True, text=True)
    if res.stdout:
        loop_dev = res.stdout.split(":")[0].strip()
        run_bash(f"pvremove -y {loop_dev}")
        run_bash(f"losetup -d {loop_dev}")
        run_bash("rm -f /tmp/sdc_sim.img")
    else:
        # Si /dev/sdc físico realmente existió y fue usado
        if os.path.exists("/dev/sdc"):
            run_bash("pvremove -y /dev/sdc")
            
    run_bash("rm -rf /mnt/testqa")
    print("\n¡Destrucción completada exitosamente!")

if __name__ == "__main__":
    main()
