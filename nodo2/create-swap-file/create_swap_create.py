#!/usr/bin/env python3
import subprocess

def main():
    # Create GPT label and 800M swap partition using fdisk
    fdisk_input = "g\nn\n\n\n+800M\nt\nswap\nw\n"
    print("Partitioning /dev/sdb...")
    subprocess.run(["fdisk", "/dev/sdb"], input=fdisk_input, text=True, check=True)
    
    # Format the partition as swap
    print("Formatting /dev/sdb1 as swap...")
    subprocess.run(["mkswap", "/dev/sdb1"], check=True)
    
    # Add to /etc/fstab if not present
    fstab_entry = "/dev/sdb1 swap swap defaults 0 0\n"
    with open("/etc/fstab", "r") as f:
        fstab_content = f.read()
    
    if "/dev/sdb1" not in fstab_content:
        print("Adding /dev/sdb1 to /etc/fstab...")
        with open("/etc/fstab", "a") as f:
            f.write(fstab_entry)
    else:
        print("/dev/sdb1 already in /etc/fstab.")
            
    # Enable the swap
    print("Enabling swap...")
    subprocess.run(["swapon", "-a"], check=True)
    print("Swap setup complete.")

if __name__ == "__main__":
    main()
