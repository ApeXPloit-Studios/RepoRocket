#!/bin/bash

# Install dependencies
if [ -f requirements.txt ]; then
    echo "Installing dependencies..."
    pip install -r requirements.txt
fi

# Clean previous build artifacts
rm -rf dist build RepoRocket.spec RRCreator.spec

# Build RepoRocket
if [ -f RepoRocket.py ]; then
    pyinstaller --onefile --noconsole --name RepoRocket --icon=img/Icons/logo.ico RepoRocket.py
else
    echo "RepoRocket.py not found"
    exit 1
fi

# Create RRCreator directory inside dist
mkdir -p dist/RRCreator

# Build RRCreator
if [ -f RRCreator/RRCreator.py ]; then
    pyinstaller --onefile --noconsole --name RRCreator --icon=img/Icons/logo.ico RRCreator/RRCreator.py --distpath dist/RRCreator
else
    echo "RRCreator/RRCreator.py not found"
    exit 1
fi

# Copy fonts to RRCreator directory
if [ -d RRCreator/fonts ]; then
    cp -r RRCreator/fonts dist/RRCreator/fonts
else
    echo "RRCreator/fonts not found"
fi

# Copy img folder to dist directory
if [ -d img ]; then
    cp -r img dist/img
else
    echo "img folder not found"
fi

# Copy steam_api64.so, steam_api64.a, and SteamworksPy64.so to dist directory
if [ -f steam_api64.so ]; then
    cp steam_api64.so dist/
else
    echo "steam_api64.so not found"
fi

if [ -f steam_api64.a ]; then
    cp steam_api64.a dist/
else
    echo "steam_api64.a not found"
fi

if [ -f SteamworksPy64.so ]; then
    cp SteamworksPy64.so dist/
else
    echo "SteamworksPy64.so not found"
fi

echo "Build completed successfully."
