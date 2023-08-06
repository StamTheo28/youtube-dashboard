import os
import platform
import subprocess
import sys
import venv

def create_virtual_environment(venv_path):
    venv.create(venv_path, with_pip=True)

def is_virtual_environment_active():
    return hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)

def check_virtual_environment():
    if not is_virtual_environment_active():
        print("ERROR: Virtual environment is not activated.")
        print("Please activate the virtual environment before running the setup script.")
        sys.exit(1)

def install_requirements():
    subprocess.run("pip install -r requirements.txt", shell=True)

if __name__ == "__main__":
    current_path = os.path.dirname(os.path.abspath(__file__))
    venv_path = os.path.join(current_path, ".venv")

    if not os.path.exists(venv_path):
        print("Creating virtual environment...")
        create_virtual_environment(venv_path)
        print("Virtual environment created.")

    check_virtual_environment()

    install_requirements()

    print("Setup completed successfully!")



