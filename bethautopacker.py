import configparser
import tkinter as tk
import os
import sys
import shutil
from tkinter import filedialog
from typing import Optional, List

# ------------------- File Management & Config -------------------- #

def select_ini_file() -> Optional[str]:
    root = tk.Tk()
    root.withdraw()
    
    initial_path = os.path.join(os.path.expanduser("~"), "Documents", "My Games", "Starfield")
    if not os.path.exists(initial_path):
        initial_path = None

    file_path = filedialog.askopenfilename(
        initialdir=initial_path,
        title="Select your StarfieldCustom.ini file",
        filetypes=(("INI files", "*.ini"), ("All files", "*.*"))
    )

    if 'StarfieldCustom.ini' not in file_path:
        print(f"Error: Selected file path '{file_path}' does not include StarfieldCustom.ini, exiting...")
        sys.exit(1)
    
    return file_path if file_path else None


def select_bsarch_exe() -> Optional[str]:
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Select your BSArch64.exe file",
        filetypes=(("EXE files", "*.exe"), ("All files", "*.*"))
    )

    # Rudimentary check to ensure the selected executable is what we want
    if 'BSArch64.exe' not in file_path:
        print(f"Error: The selected file path '{file_path}' does not include BSArch64.exe, exiting...")
        sys.exit(1)

    # Ensure it has executable permissions
    if not os.access(file_path, os.X_OK):
        print(f"Error: The selected file '{file_path}' does not have executable permissions, exiting...")
        sys.exit(1)

    return file_path if file_path else None


def select_loose_folder() -> Optional[str]:
    root = tk.Tk()
    root.withdraw()

    folder_path = filedialog.askdirectory(
        title="Select your loose file folder",
        mustexist=True,
    )

    return folder_path if folder_path else None


def backup_ini_file(custom_ini_path: str):
    try:
        shutil.copy(custom_ini_path, f"{custom_ini_path}.bak")
        print(f"{custom_ini_path} has been backed up to {custom_ini_path}.bak")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def remove_config_option(config: configparser.ConfigParser, sect: str, opt: str) -> configparser.ConfigParser:
    if not config.has_option(sect, opt):
        print(f"Option '{opt}' does not exist, nothing to remove")
        return

    config.remove_option(sect, opt)

    return config


def disable_loose_files(custom_ini_path: str) -> None:
    sect = 'Archive'
    config = configparser.ConfigParser()
    config.read(custom_ini_path)

    if not config.has_section(sect):
        print(f"Section '[{sect}]' does not exist, nothing to remove")
        return

    config = remove_config_option(config, sect, 'bInvalidateOlderFiles')
    config = remove_config_option(config, sect, 'sResourceDataDirsFinal')

    with open(custom_ini_path, 'w') as configfile:
        config.write(configfile)

    print(f"Loose file loading has been DISABLED in '{custom_ini_path}'")

    return


def enable_loose_files(custom_ini_path: str) -> None:
    sect = 'Archive'
    config = configparser.ConfigParser()
    config.read(custom_ini_path)

    print("Setting loose file options...")

    if not config.has_section(sect):
        print(f"Section '[{sect}]' does not exist, adding it...")
        config.add_section(sect)

    config.set(sect, 'bInvalidateOlderFiles', '1')
    config.set(sect, 'sResourceDataDirsFinal', '')

    print(f"Writing changes to '{custom_ini_path}'...")

    with open(custom_ini_path, 'w') as configfile:
        config.write(fp=configfile, space_around_delimiters=False)

    print(f"Loose file loading has been ENABLED in '{custom_ini_path}'")

    return


def get_paths() -> List[str]:
    custom_ini_path = select_ini_file()
    if not custom_ini_path:
        print("No ini file selected. Exiting...")
        sys.exit(1)

    print(f"StarfieldCustom.ini selected at '{custom_ini_path}'")

    bsarch_exe_path = select_bsarch_exe()
    if not bsarch_exe_path:
        print("No BSArch64.exe file selected. Exiting...")
        sys.exit(1)

    print(f"BSArch64.exe selected at '{bsarch_exe_path}'")

    loose_folder = select_loose_folder()
    if not loose_folder:
        print("No loose folder selected. Exiting...")
        sys.exit(1)

    print(f"Loose folder selected at '{loose_folder}'")

    return [custom_ini_path, bsarch_exe_path, loose_folder]


# ------------------- Packing Config -------------------- #


# ------------------- Main -------------------- #

def main() -> None:
    ini_path, bsarch_path, loose_path = get_paths()

    backup_ini_file(ini_path)

    enable_loose_files(ini_path)

    return


if __name__ == "__main__":
    main()
