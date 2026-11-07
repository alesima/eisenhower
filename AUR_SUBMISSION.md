# AUR Package Submission Guide

This guide explains how to submit the Eisenhower Matrix package to the Arch User Repository (AUR).

## Prerequisites

1. Create an AUR account at https://aur.archlinux.org/
2. Set up SSH keys for AUR access

## Submission Steps

1. **Create the AUR package directory:**
   ```bash
   mkdir -p ~/aur/eisenhower-matrix
   cd ~/aur/eisenhower-matrix
   ```

2. **Copy the package files:**
   ```bash
   cp /path/to/eisenhower/PKGBUILD .
   cp /path/to/eisenhower/.SRCINFO .
   cp /path/to/eisenhower/README-AUR.md .
   ```

3. **Initialize git repository:**
   ```bash
   git init
   git add PKGBUILD .SRCINFO README-AUR.md
   git commit -m "Initial commit"
   ```

4. **Submit to AUR:**
   ```bash
   # Clone AUR repo (replace YOUR_USERNAME)
   git clone ssh://aur@aur.archlinux.org/eisenhower-matrix.git
   cd eisenhower-matrix

   # Copy files
   cp ~/aur/eisenhower-matrix/* .

   # Commit and push
   git add .
   git commit -m "Initial submission of eisenhower-matrix"
   git push origin master
   ```

## Updating the Package

When releasing a new version:

1. Update `pkgver` in PKGBUILD
2. Update `.SRCINFO` with `makepkg --printsrcinfo > .SRCINFO`
3. Update `sha256sums` if using a release tarball
4. Commit and push changes

## Testing

Before submitting, test the package locally:

```bash
# Build and install
makepkg -si

# Test the application
eisenhower-gui
```

## Notes

- The package uses `sha256sums=('SKIP')` for development. For production, calculate proper checksums.
- Ensure all dependencies are correctly specified.
- Test on a clean system to verify the package works.