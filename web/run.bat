:: ___________________________________________________
:: 1. run "app.py" in one CMD terminal
:: 2. open tab in browser
:: ___________________________________________________
@echo off
::"C:\Program Files (x86)\BraveSoftware\Brave-Browser\Application\brave.exe"
::sleep1
:: 1.
python app.py

start cmd.exe
start brave.exe "http://127.0.0.1:3700/"

:: 2.
rem pause
