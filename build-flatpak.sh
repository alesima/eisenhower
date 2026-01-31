#!/bin/bash
# Quick build and test script for development

set -e

echo "🏗️  Building Eisenhower Matrix..."

# Check if running in Flatpak environment
if [ -f "com.github.alesima.eisenhower.yml" ]; then
    echo "📦 Building Flatpak..."
    flatpak-builder --user --install --force-clean build-dir com.github.alesima.eisenhower.yml
    echo "✅ Flatpak built successfully!"
    echo ""
    echo "Run with: flatpak run com.github.alesima.eisenhower"
else
    echo "❌ Flatpak manifest not found"
    exit 1
fi
