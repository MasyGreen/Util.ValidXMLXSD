@ECHO OFF
rmdir /s /q build
rmdir /s /q dist
if exist *.log del *.log
if exist *.spec del *.spec