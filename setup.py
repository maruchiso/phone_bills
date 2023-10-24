
import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["numpy", "pandas", "tkinter", "os"], 
    "include_files": ["numery_tel.csv"], # Dodaj nazwy pakietów, które twoja aplikacja używa

}

base = None
if sys.platform == "win32":
    base = "Win32GUI"

executables = [Executable("main.py", base=base)]

setup(
    name="_adm_szymczam",
    version="21.37",
    description="Robi fikolka",
    options={"build_exe": build_exe_options},
    executables=executables,
    
)
