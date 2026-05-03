#!/usr/bin/env python3
"""
install_flatpak_create.py
Script to install Flatpak, configure Flathub remote, and install applications.
This script automates the setup of Flatpak with a custom remote and installs Glxinfo.
"""

import subprocess
import sys
import os


def run_command(command, description):
    """Execute a shell command and handle errors."""
    print(f"\n{'='*60}")
    print(f"EXECUTING: {description}")
    print(f"Command: {command}")
    print(f"{'='*60}")

    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✓ SUCCESS: {description}")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ ERROR: {description}")
        print(f"Exit code: {e.returncode}")
        if e.stderr:
            print(f"Error output: {e.stderr}")
        if e.stdout:
            print(f"Standard output: {e.stdout}")
        return False


def check_flatpak_installed():
    """Check if flatpak is already installed."""
    try:
        subprocess.run(
            ["which", "flatpak"],
            check=True,
            capture_output=True
        )
        return True
    except subprocess.CalledProcessError:
        return False


def install_flatpak():
    """Install Flatpak on the system."""
    if check_flatpak_installed():
        print("\nℹ Flatpak is already installed. Skipping installation.")
        return True

    print("\nFlatpak not found. Installing...")

    if os.path.exists("/etc/debian_version"):
        commands = ["apt-get update", "apt-get install -y flatpak"]
    elif os.path.exists("/etc/arch-release"):
        commands = ["pacman -Sy --noconfirm flatpak"]
    elif os.path.exists("/etc/fedora-release") or os.path.exists("/etc/redhat-release") or os.path.exists("/etc/rocky-release"):
        commands = ["dnf install -y flatpak"]
    else:
        print("⚠ Unable to detect distribution specifically. Checking for common package managers...")
        if subprocess.run(["which", "dnf"], capture_output=True).returncode == 0:
            commands = ["dnf install -y flatpak"]
        elif subprocess.run(["which", "apt-get"], capture_output=True).returncode == 0:
            commands = ["apt-get update", "apt-get install -y flatpak"]
        elif subprocess.run(["which", "pacman"], capture_output=True).returncode == 0:
            commands = ["pacman -Sy --noconfirm flatpak"]
        else:
            print("⚠ Still unable to detect package manager. Attempting manual download install...")
            commands = [
                "curl -LO https://github.com/flatpak/flatpak/releases/latest/download/flatpak-x86_64.tar.xz && tar -xf flatpak-x86_64.tar.xz -C /usr/local/ --strip-components=1"
            ]

    for cmd in commands:
        if not run_command(cmd, f"Install step: {cmd.split()[0]}"):
            return False

    return True


def add_flathub_remote():
    """Add Flathub remote repository for the user."""
    remote_name = "flathrain"
    remote_url = "https://flathub.org/repo/flathub.flatpakrepo"

    subprocess.run(
        f"flatpak remote-delete --user {remote_name}",
        shell=True,
        capture_output=True
    )

    command = f"flatpak remote-add --user --if-not-exists {remote_name} {remote_url}"
    return run_command(command, "Add Flathub remote for user")


def install_glxinfo():
    """Install Glxinfo from the Flathub remote."""
    remote_name = "flathrain"
    app_id = "org.freedesktop.Platform.GlxInfo"
    branch = "24.08"

    command = f"flatpak install --user -y {remote_name} {app_id}//{branch}"
    return run_command(command, f"Install {app_id}//{branch}")


def main():
    """Main execution function."""
    print("\n" + "="*60)
    print("  FLATPAK AUTOMATED INSTALLATION SCRIPT")
    print("  Python-based Flatpak setup with Flathub remote")
    print("="*60)

    # Step 1: Install Flatpak
    if not install_flatpak():
        print("\n✗ Failed to install Flatpak. Exiting.")
        sys.exit(1)

    # Step 2: Add Flathub remote
    if not add_flathub_remote():
        print("\n✗ Failed to add Flathub remote. Continuing anyway...")

    # Step 3: Install Glxinfo
    confirm = input("\nProceed to install Glxinfo? (y/N): ").strip().lower()
    if confirm in ['y', 'yes']:
        if not install_glxinfo():
            print("\n✗ Failed to install Glxinfo.")
            sys.exit(1)
        print("\n" + "="*60)
        print("  ✓ ALL OPERATIONS COMPLETED SUCCESSFULLY!")
        print("  Glxinfo has been installed via Flatpak")
        print("="*60)
    else:
        print("\nSkipping Glxinfo installation.")

    print("\nTo list installed Flatpak apps, run:")
    print("  flatpak list --user")
    print("\nTo run Glxinfo, run:")
    print("  flatpak run org.freedesktop.Platform.GlxInfo//24.08")


if __name__ == "__main__":
    main()
