#!/usr/bin/env python3
"""Wrapper script for PyThermalCamera."""

import argparse
import subprocess
import sys
import os

def list_devices():
    """List available video devices using v4l2-ctl."""
    try:
        result = subprocess.run(
            ["v4l2-ctl", "--list-devices"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print(result.stdout)
        else:
            print("Error listing devices:", result.stderr, file=sys.stderr)
            sys.exit(1)
    except FileNotFoundError:
        print("v4l2-ctl not found. Install with: sudo apt install v4l-utils", file=sys.stderr)
        sys.exit(1)

def run_camera(device):
    """Run the thermal camera application."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    tc001_script = os.path.join(script_dir, "src", "tc001v4.2.py")
    subprocess.run(["python3", tc001_script, "--device", str(device)])

def install_dependencies():
    """Install required dependencies."""
    print("Installing dependencies...")
    packages = ["python3-opencv", "v4l-utils"]
    result = subprocess.run(
        ["sudo", "apt", "install", "-y"] + packages
    )
    if result.returncode == 0:
        print("Dependencies installed successfully.")
    else:
        print("Error installing dependencies.", file=sys.stderr)
        sys.exit(1)

def print_usage():
    """Print usage information."""
    print("""PyThermalCamera - Thermal Camera Software for Topdon TC001

Usage:
  ./run.py --devices              List available video devices
  ./run.py --dev <number>         Run thermal camera with specified device number
  ./run.py --install-dependencies Install required dependencies (python3-opencv, v4l-utils)
  ./run.py -h, --help             Show this help message

Examples:
  ./run.py --install-dependencies # Install dependencies
  ./run.py --devices              # List all video devices
  ./run.py --dev 4                # Run with device /dev/video4
""")

def main():
    if len(sys.argv) == 1:
        print_usage()
        sys.exit(0)

    parser = argparse.ArgumentParser(
        description="PyThermalCamera - Thermal Camera Software for Topdon TC001",
        add_help=False
    )
    parser.add_argument("--devices", action="store_true", help="List available video devices")
    parser.add_argument("--dev", type=int, metavar="<number>", help="Device number to use")
    parser.add_argument("--install-dependencies", action="store_true", help="Install required dependencies")
    parser.add_argument("-h", "--help", action="store_true", help="Show this help message")

    args = parser.parse_args()

    if args.help:
        print_usage()
        sys.exit(0)

    if args.install_dependencies:
        install_dependencies()
    elif args.devices:
        list_devices()
    elif args.dev is not None:
        run_camera(args.dev)
    else:
        print_usage()
        sys.exit(1)

if __name__ == "__main__":
    main()
