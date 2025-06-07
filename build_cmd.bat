@echo off
pyinstaller --onefile --noconsole --icon ../Assets/IconSmall.ico --name LegacyPlay_Launcher --distpath ./../ launcher.py
pause