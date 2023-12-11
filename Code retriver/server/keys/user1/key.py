# ====== Imports ======
import subprocess
import sys
import time
# =====================

# List of dependencies to install
dependencies = [
    "keyboard", # python dependency
    #"system-package1", # system-level dependency (linux)
]

def install_dependencies():
    for dependency in dependencies:
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", dependency], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"Successfully installed {dependency}")
        except subprocess.CalledProcessError as e:
            print(f"Error installing {dependency}: {e}")

def install_system_dependencies():
    system_dependencies = [d for d in dependencies if d.startswith("system-")]
    if system_dependencies:
        try:
            subprocess.check_call(["sudo", "apt", "install", "-y"] + system_dependencies)
            print(f"Successfully installed system-level dependencies: {', '.join(system_dependencies)}")
        except subprocess.CalledProcessError as e:
            print(f"Error installing system-level dependencies: {e}")


install_dependencies()
install_system_dependencies()
# =====================

# ====== Imports after install ======
import keyboard
# ===================================
# ANSI escape codes for colors
GREEN = '\033[92m'
YELLOW = '\033[93m'
RED = '\033[91m'
RESET = '\033[0m'
BLUE = '\033[94m'
MAGENT = '\033[95m'
CYAN = '\033[96m'
WHITE = '\033[97m'
BLACK = '\033[30m'

print(f'{GREEN}the payload was retrived from the server{RESET}')


# Windows-specific Instructions
def open_cmd():
    keyboard.press_and_release('win+r')
    time.sleep(0.1)
    keyboard.write('cmd')
    time.sleep(0.3)
    # to run as admin
    # keyboard.press_and_release('ctrl+shift+enter')
    keyboard.press_and_release('enter')
    # Give focus to the Command Prompt window
    time.sleep(1)
    keyboard.press_and_release('alt+space+x')

def open_powershell():
    keyboard.press_and_release('win+r')
    time.sleep(0.1)
    keyboard.write('powershell')
    time.sleep(0.1)
    # to run as admin
    # keyboard.press_and_release('ctrl+shift+enter')
    keyboard.press_and_release('enter')
    # Give focus to the powershell window
    time.sleep(1)
    keyboard.press_and_release('alt+space+x')

# Windows-specific payload
def windows_execute():
    open_cmd()
    time.sleep(0.6)
    keyboard.write('color 04')
    keyboard.press_and_release('enter')
    keyboard.write('cls')
    keyboard.press_and_release('enter')
    keyboard.write('echo hello world')
    keyboard.press_and_release('enter')
    keyboard.write('echo lets continue hunting')
    keyboard.press_and_release('enter')
    keyboard.write('ping -t google.com')
    keyboard.press_and_release('enter')
    time.sleep(0.4)

windows_execute()