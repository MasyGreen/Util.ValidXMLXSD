rmdir /s /q build
rmdir /s /q dist
if exist *.log del *.log
if exist *.spec del *.spec
pyinstaller -F -i "Icon.ico" getsomeel.py