#!/usr/bin/env python3
import subprocess

def main():
    # Disable the swap
    print("Disabling swap on /dev/sdb1...")
    subprocess.run(["swapoff", "/dev/sdb1"], check=False)
    
    # Remove from /etc/fstab
    print("Removing /dev/sdb1 from /etc/fstab...")
    with open("/etc/fstab", "r") as f:
        lines = f.readlines()
        
    with open("/etc/fstab", "w") as f:
        for line in lines:
            if not line.strip().startswith("/dev/sdb1 swap"):
                f.write(line)
                
    # Destroy partition table using fdisk (create an empty GPT)
    print("Destroying partition table on /dev/sdb...")
    fdisk_input = "g\nw\n"
    subprocess.run(["fdisk", "/dev/sdb"], input=fdisk_input, text=True, check=True)
    print("Swap destruction complete.")

if __name__ == "__main__":
    main()
