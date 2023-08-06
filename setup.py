import os
import platform
import subprocess
import sys
import venv

def create_virtual_environment(venv_path):
    venv.create(venv_path, with_pip=True)

def activate_virtual_environment(venv_path):
    if platform.system() == "Windows":
        activate_script = os.path.join(venv_path, "Scripts", "activate.bat")
    else:
        activate_script = os.path.join(venv_path, "bin", "activate")

    if not os.path.exists(activate_script):
        raise FileNotFoundError("Virtual environment activation script not found.")

    subprocess.run(activate_script, shell=True)

def set_environment_variables(env_variables):
    for key, value in env_variables.items():
        os.environ[key] = value

def install_requirements():
    subprocess.run("pip install -r requirements.txt", shell=True)

if __name__ == "__main__":
    venv_path = "venv"  # Replace "myenv" with the desired virtual environment directory name

    create_virtual_environment(venv_path)
    activate_virtual_environment(venv_path)

    # Dictionary of API Keys
    api_keys = {
        'YOUTUBE-API-KEY': "AIzaSyCj_o0-0ej8EOa6tPYPKfhJyI3c-zPJ9Yc" 
    }

    set_environment_variables(api_keys)
    install_requirements()

    print("Setup completed successfully!")
