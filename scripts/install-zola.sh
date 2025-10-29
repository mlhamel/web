#!/bin/bash
set -e

VERSION="0.19.2"
PLATFORM="x86_64-unknown-linux-gnu"
URL="https://github.com/getzola/zola/releases/download/v${VERSION}/zola-v${VERSION}-${PLATFORM}.tar.gz"

echo "Installing Zola ${VERSION}..."

# Download and extract
curl -sL "$URL" | tar xz

# Create local bin directory if it doesn't exist
mkdir -p ~/.local/bin

# Move binary
mv zola ~/.local/bin/

# Ensure ~/.local/bin is in PATH
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc
    echo "Added ~/.local/bin to PATH in ~/.bashrc"
    echo "Run: source ~/.bashrc"
fi

echo "Zola installed successfully!"
echo "Run 'zola --version' to verify (you may need to restart your shell)"
