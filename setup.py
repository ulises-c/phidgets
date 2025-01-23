"""
Helper script for importing required python packages to use Phidgets.

Becomes redundant with a requirements.txt file.
"""

import subprocess
import sys
from typing import List


def install_packages(packages: List[str]) -> None:
    """
    Install a list of packages using pip.

    Args:
        packages (list): List of package names to install.
    """
    for package in packages:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])
            print(f"Successfully installed {package}")
        except subprocess.CalledProcessError as e:
            print(f"Failed to install {package}: {e}")


if __name__ == "__main__":
    # List of packages to install
    packages_to_install = [
        "Phidget22",
    ]

    install_packages(packages_to_install)
