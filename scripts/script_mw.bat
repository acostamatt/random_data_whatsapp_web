@echo off
echo Generaremos los archivos .qrc y .ui a .py
pause
if not exist ..\src\views\base mkdir ..\src\views\base

pyside6-uic ..\ui\sorteo_base.ui -o ..\src\views\base\sorteo_base.py