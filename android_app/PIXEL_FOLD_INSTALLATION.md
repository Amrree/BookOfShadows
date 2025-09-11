# Pixel Fold Installation Guide

## 📱 Google Pixel Fold Optimized APK

This Android app has been specifically optimized for the **Google Pixel Fold** with the following enhancements:

### 🎯 Pixel Fold Optimizations

- **Adaptive Layout**: Automatically adjusts between folded (6.2") and unfolded (7.6") states
- **Touch-Friendly UI**: Optimized button sizes and spacing for foldable interaction
- **Orientation Support**: Supports both portrait and landscape orientations
- **High-Density Display**: Optimized for Pixel Fold's high-resolution screens
- **Foldable Navigation**: Adaptive navigation that works in both states

### 📋 System Requirements

- **Device**: Google Pixel Fold
- **Android Version**: 8.0+ (API level 24+)
- **Architecture**: arm64-v8a
- **Storage**: 100MB minimum
- **Permissions**: Storage, Camera (optional), Internet

### 🚀 Installation Steps

#### Method 1: Direct APK Installation
1. Download the APK file: `bookofshadows-1.0.0-debug.apk`
2. Enable "Unknown Sources" in Android Settings
3. Tap the APK file to install
4. Follow the installation prompts

#### Method 2: ADB Installation
```bash
# Connect Pixel Fold via USB
adb devices

# Install the APK
adb install bookofshadows-1.0.0-debug.apk
```

#### Method 3: Buildozer Deploy
```bash
# From android_app directory
./build_android.sh

# Deploy directly to connected device
buildozer android deploy run
```

### 📱 Pixel Fold Specific Features

#### Folded State (6.2" Display)
- Standard mobile layout
- Single-column navigation
- Compact card design
- Touch-optimized buttons (48dp height)

#### Unfolded State (7.6" Display)
- Expanded layout with more horizontal space
- Multi-column content when appropriate
- Larger touch targets
- Enhanced readability

#### Adaptive Behavior
- **Automatic Detection**: App detects fold state automatically
- **Smooth Transitions**: Seamless layout changes when folding/unfolding
- **Context Preservation**: Maintains app state during transitions
- **Performance Optimized**: Efficient memory usage for foldable hardware

### 🎨 UI Adaptations

#### Navigation
- **Folded**: Standard bottom navigation (56dp height)
- **Unfolded**: Compact navigation (48dp height) with more content space

#### Typography
- **Folded**: Standard mobile font sizes (14-18dp)
- **Unfolded**: Larger fonts for better readability (16-20dp)

#### Cards & Components
- **Folded**: Standard card height (120dp)
- **Unfolded**: Optimized card height (100dp) with better spacing

#### Dialogs
- **Folded**: Full-screen dialogs (90% width/height)
- **Unfolded**: Centered dialogs (70% width/60% height)

### 🔧 Troubleshooting

#### Installation Issues
- Ensure "Unknown Sources" is enabled
- Check available storage space
- Verify Android version compatibility

#### Performance Issues
- Close other apps before installation
- Restart device after installation
- Clear app cache if needed

#### Fold Detection Issues
- Rotate device to trigger layout refresh
- Restart app if fold detection fails
- Check device orientation settings

### 📞 Support

For Pixel Fold specific issues:
- Check device compatibility
- Verify Android version
- Test in both folded and unfolded states
- Report any fold-specific bugs

### 🎉 Ready to Use!

Once installed, the Book of Shadows - The Crone app will:
- Automatically detect your Pixel Fold's state
- Adapt the interface for optimal use
- Provide a seamless experience across both screen configurations
- Maintain all core functionality from the desktop version

Enjoy your mobile grimoire authoring experience! 🏛️📱