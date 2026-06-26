@echo off
echo ============================================================
echo  Compilation : Optimisation du Reseau Electrique au Maroc
echo ============================================================
echo.

cd /d "%~dp0app"

pyinstaller ^
  --onefile ^
  --windowed ^
  --name "Optimisation_Reseau_Electrique" ^
  --add-data "assets;assets" ^
  --hidden-import "networkx" ^
  --hidden-import "matplotlib" ^
  --hidden-import "matplotlib.backends.backend_tkagg" ^
  --hidden-import "matplotlib.backends._backend_tk" ^
  --hidden-import "PIL._tkinter_finder" ^
  main.py

echo.
echo ============================================================
echo  Executable genere dans : app\dist\
echo ============================================================
pause
