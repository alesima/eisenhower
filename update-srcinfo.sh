#!/bin/bash
# Script to update .SRCINFO file from PKGBUILD
# Usage: ./update-srcinfo.sh

if [ ! -f "PKGBUILD" ]; then
    echo "Error: PKGBUILD not found in current directory"
    exit 1
fi

echo "Updating .SRCINFO..."
makepkg --printsrcinfo > .SRCINFO

if [ $? -eq 0 ]; then
    echo ".SRCINFO updated successfully"
else
    echo "Error updating .SRCINFO"
    exit 1
fi