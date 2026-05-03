#!/usr/bin/env python3
"""
install_flatpak_destroy.py
Script to uninstall Flatpak, remove Flathub remote, and uninstall applications.
This script reverses the operations performed by install_flatpak_create.py.
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
        return False


def uninstall_glxinfo():                                            # <-- nueva función
    """Uninstall Glxinfo installed via Flatpak."""
    app_id = "org.freedesktop.Platform.GlxInfo"
    print(f"\nChecking if {app_id} is installed...")

    check_cmd = f"flatpak list --user | grep {app_id}"
    if subprocess.run(check_cmd, shell=True, capture_output=True).returncode == 0:
        command = f"flatpak uninstall --user -y {app_id}"
        return run_command(command, f"Uninstall {app_id}")
    else:
        print(f"ℹ {app_id} not found. Skipping.")
        return True


def uninstall_all_flatpaks():
    """Uninstall all applications and runtimes installed via Flatpak."""
    print("\nChecking for installed Flatpak applications/runtimes...")

    command = "flatpak uninstall --user --all -y"
    return run_command(command, "Uninstall all Flatpak apps and runtimes")


def remove_flathub_remote():
    """Remove the Flathub remote repository."""
    remote_name = "flathrain"
    print(f"\nChecking if remote '{remote_name}' exists...")

    check_cmd = f"flatpak remote-list --user | grep {remote_name}"
    if subprocess.run(check_cmd, shell=True, capture_output=True).returncode == 0:
        command = f"flatpak remote-delete --user {remote_name}"
        return run_command(command, f"Remove remote {remote_name}")
    else:
        print(f"ℹ Remote '{remote_name}' not found. Skipping.")
        return True


def uninstall_flatpak():
    """Uninstall Flatpak package from the system."""
    print("\nDetecting package manager for uninstallation...")

    if os.path.exists("/etc/debian_version"):
        commands = ["apt-get remove -y flatpak", "apt-get autoremove -y"]
    elif os.path.exists("/etc/arch-release"):
        commands = ["pacman -Rs --noconfirm flatpak"]
    elif os.path.exists("/etc/fedora-release") or os.path.exists("/etc/redhat-release") or os.path.exists("/etc/rocky-release"):
        commands = ["dnf remove -y flatpak"]
    else:
        if subprocess.run(["which", "dnf"], capture_output=True).returncode == 0:
            commands = ["dnf remove -y flatpak"]
        elif subprocess.run(["which", "apt-get"], capture_output=True).returncode == 0:
            commands = ["apt-get remove -y flatpak"]
        else:
            print("⚠ Unable to detect package manager for uninstallation. Please remove flatpak manually.")
            return False

    for cmd in commands:
        if not run_command(cmd, f"Uninstall step: {cmd.split()[0]}"):
            return False
    return True


def main():
    """Main execution function."""
    print("\n" + "="*60)
    print("  FLATPAK DESTRUCTION SCRIPT")
    print("  Removing Flatpak, remotes, and applications")
    print("="*60)

    confirm = input(
        "\nThis will uninstall Glxinfo, remove Flathub remotes, and uninstall Flatpak.\n"  # <-- mensaje actualizado
        "Are you sure you want to proceed? (y/N): "
    ).strip().lower()
    if confirm not in ['y', 'yes']:
        print("\nOperation cancelled.")
        sys.exit(0)

    # Step 1: Uninstall Glxinfo specifically               # <-- nuevo paso
    if not uninstall_glxinfo():
        print("⚠ Failed to uninstall Glxinfo or it was not found.")

    # Step 2: Uninstall all remaining Flatpak apps and runtimes
    if not uninstall_all_flatpaks():
        print("⚠ Failed to uninstall Flatpak applications or none were found.")

    # Step 3: Remove Flathub remote
    if not remove_flathub_remote():
        print("⚠ Failed to remove Flathub remote.")

    # Step 4: Uninstall Flatpak package
    if uninstall_flatpak():
        print("\n" + "="*60)
        print("  ✓ ALL OPERATIONS COMPLETED SUCCESSFULLY!")
        print("  Flatpak and associated data have been removed")
        print("="*60)
    else:
        print("\n✗ Failed to complete Flatpak uninstallation.")
        sys.exit(1)


if __name__ == "__main__":
    main()
