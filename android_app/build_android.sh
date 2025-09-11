#!/bin/bash
# Build script for Book of Shadows - The Crone Android App

set -e

echo "🏛️ Building Book of Shadows - The Crone for Android"
echo "=================================================="

# Check if we're in the right directory
if [ ! -f "buildozer.spec" ]; then
    echo "❌ Error: buildozer.spec not found. Please run this script from the android_app directory."
    exit 1
fi

# Check if buildozer is installed
if ! command -v buildozer &> /dev/null; then
    echo "❌ Error: buildozer not found. Please install it with: pip install buildozer"
    exit 1
fi

# Check if Android SDK is available
if [ -z "$ANDROID_HOME" ] && [ -z "$ANDROID_SDK_ROOT" ]; then
    echo "⚠️  Warning: ANDROID_HOME or ANDROID_SDK_ROOT not set"
    echo "   Android SDK may not be found automatically"
fi

echo "📱 Starting Android build process..."

# Clean previous builds
echo "🧹 Cleaning previous builds..."
buildozer android clean

# Initialize buildozer if needed
if [ ! -f ".buildozer" ]; then
    echo "🔧 Initializing buildozer..."
    buildozer init
fi

# Build debug APK
echo "🔨 Building debug APK..."
buildozer android debug

# Check if build was successful
if [ $? -eq 0 ]; then
    echo "✅ Build successful!"
    echo ""
    echo "📦 APK location: bin/bookofshadows-1.0.0-debug.apk"
    echo ""
    echo "📱 To install on device:"
    echo "   buildozer android deploy run"
    echo ""
    echo "📱 To install manually:"
    echo "   adb install bin/bookofshadows-1.0.0-debug.apk"
    echo ""
    echo "🎉 Book of Shadows - The Crone is ready for Android!"
else
    echo "❌ Build failed!"
    echo "   Check the error messages above for details"
    exit 1
fi