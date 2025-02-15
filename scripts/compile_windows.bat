@echo off
REM Install dependencies
if exist requirements.txt (
    echo Installing dependencies...
    pip install -r requirements.txt
)

REM Clean previous build artifacts
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist RepoRocket.spec del RepoRocket.spec
if exist RRCreator.spec del RRCreator.spec

REM Build RepoRocket (hide console window with --noconsole)
if exist RepoRocket.py (
    pyinstaller --onefile --noconsole --name RepoRocket --icon=img/Icons/logo.ico RepoRocket.py
) else (
    echo RepoRocket.py not found
    exit /b 1
)

REM Create RRCreator directory inside dist
mkdir dist\RRCreator

REM Build RRCreator (hide console window with --noconsole)
if exist RRCreator\RRCreator.py (
    pyinstaller --onefile --noconsole --name RRCreator --icon=img/Icons/logo.ico RRCreator/RRCreator.py --distpath dist\RRCreator
) else (
    echo RRCreator/RRCreator.py not found
    exit /b 1
)

REM Copy fonts to RRCreator directory
if exist RRCreator\fonts (
    xcopy RRCreator\fonts dist\RRCreator\fonts /E /I /Y
) else (
    echo RRCreator/fonts not found
)

REM Copy img folder to dist directory
if exist img (
    xcopy img dist\img /E /I /Y
) else (
    echo img folder not found
)

REM Copy steam_api64.dll, steam_api64.lib, and SteamworksPy64.dll to dist directory
if exist steam_api64.dll (
    xcopy steam_api64.dll dist /Y
) else (
    echo steam_api64.dll not found
)

if exist steam_api64.lib (
    xcopy steam_api64.lib dist /Y
) else (
    echo steam_api64.lib not found
)

if exist SteamworksPy64.dll (
    xcopy SteamworksPy64.dll dist /Y
) else (
    echo SteamworksPy64.dll not found
)

REM Move back to the scripts directory
cd scripts

echo Build completed successfully.
pause
