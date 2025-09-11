# Book of Shadows - The Crone (Android)

A mobile-optimized version of the research-grade, ritual-aware Grimoire IDE for Android devices.

## Overview

This Android version preserves all the functionality of the desktop application while providing a mobile-friendly interface optimized for touch interactions and smaller screens.

## Features

### 📱 Mobile-Optimized Interface
- **Touch-Friendly Design**: Large buttons and touch-optimized controls
- **Responsive Layout**: Adapts to different screen sizes and orientations
- **Material Design**: Follows Android design guidelines
- **Navigation**: Intuitive tab-based navigation

### 🏛️ Core Functionality Preserved
- **Document Ingestion**: PDF, TXT, MD support
- **Grimoire Authoring**: Create and edit spells/rituals
- **Citation Management**: Track sources and references
- **Safety Framework**: Comprehensive harm prevention
- **Memory System**: Persistent storage with user consent

### 🔧 Mobile-Specific Features
- **Floating Action Button**: Quick access to create new entries
- **Card-Based UI**: Clean, organized information display
- **Mobile Forms**: Optimized input fields and validation
- **Touch Gestures**: Swipe and tap interactions

## Installation

### Prerequisites
- Python 3.8+
- Android SDK
- Java Development Kit (JDK)
- Buildozer

### Setup

1. **Install Buildozer**:
   ```bash
   pip install buildozer
   ```

2. **Install Android Requirements**:
   ```bash
   pip install -r android_requirements.txt
   ```

3. **Initialize Buildozer**:
   ```bash
   buildozer init
   ```

4. **Configure Buildozer**:
   Edit `buildozer.spec` to customize your app settings.

5. **Build APK**:
   ```bash
   buildozer android debug
   ```

6. **Install on Device**:
   ```bash
   buildozer android deploy run
   ```

## Project Structure

```
android_app/
├── main.py                    # Original desktop main (preserved)
├── mobile_main.py             # Mobile-optimized main application
├── config_mobile.yaml         # Mobile-specific configuration
├── buildozer.spec             # Android build configuration
├── android_requirements.txt   # Android-specific dependencies
├── core/                      # Core modules (preserved from desktop)
├── plugins/                   # Plugin system (preserved from desktop)
├── ui/                        # UI components
│   ├── mobile_components.py   # Mobile-optimized UI components
│   ├── mobile_grimoire_editor.py # Mobile grimoire editor
│   └── grimoire_editor.py    # Original desktop editor (preserved)
├── data/                      # Data storage
└── assets/                    # App assets (icons, etc.)
```

## Mobile UI Components

### Core Components
- **MobileButton**: Touch-friendly buttons with proper sizing
- **MobileTextInput**: Optimized text input fields
- **MobileLabel**: Responsive text labels
- **MobileCard**: Card-based layout components
- **MobileList**: Scrollable list components
- **MobileForm**: Form layout components
- **MobileDialog**: Modal dialog components

### Navigation
- **MobileNavigation**: Tab-based navigation
- **MobileSearchBar**: Search input with button
- **MobileFloatingActionButton**: Quick action button

### Specialized Components
- **MobileSpinner**: Dropdown selection
- **MobileCheckBox**: Touch-friendly checkboxes
- **MobileSwitch**: Toggle switches
- **MobileSlider**: Value selection sliders

## Usage

### Creating Entries
1. Tap the floating action button (+)
2. Fill in the entry form:
   - Title (required)
   - Type (Spell, Ritual, Blessing, etc.)
   - Lineage/Tradition
   - Efficacy Claim
3. Tap "Create Entry"

### Managing Ingredients
1. Open an entry
2. Tap "Manage Ingredients"
3. Add ingredients with name, description, and quantity
4. Remove ingredients as needed

### Adding Citations
1. Open an entry
2. Tap "Manage Citations"
3. Add chunk IDs (e.g., @BOOK001::CHUNK0042)
4. Provide context for each citation

### Document Ingestion
1. Navigate to "Ingest" tab
2. Enter file path or select from storage
3. Add optional tag
4. Tap "Ingest Document"

## Configuration

### Mobile-Specific Settings
Edit `config_mobile.yaml` to customize:

```yaml
mobile:
  enable_file_picker: true
  enable_camera: false
  enable_location: false
  enable_notifications: true
  storage_location: "internal"
  backup_enabled: true

ui:
  theme: "dark"
  layout: "mobile"
  touch_friendly: true
  button_size: "large"
  font_size: "medium"
```

### Build Configuration
Edit `buildozer.spec` to customize:

- App name and package
- Permissions
- Dependencies
- Build settings

## Development

### Running in Development
```bash
# Run desktop version for testing
python main.py

# Run mobile version for testing
python mobile_main.py
```

### Building for Release
```bash
# Build release APK
buildozer android release

# Sign APK (if configured)
buildozer android release --sign
```

### Testing
```bash
# Test on connected device
buildozer android deploy run

# Test on emulator
buildozer android emulator
```

## Safety & Ethics

The Android version maintains the same safety and ethics framework as the desktop version:

- **Harm Prevention**: Refuses dangerous content
- **Cultural Sensitivity**: Validates ethnographic material
- **Medical Disclaimers**: No professional medical advice
- **Copyright Compliance**: Respects intellectual property

## Performance Optimization

### Mobile Optimizations
- **Reduced Chunk Size**: 1500 tokens (vs 2000 on desktop)
- **Optimized UI**: Touch-friendly components
- **Efficient Storage**: SQLite for local data
- **Minimal Dependencies**: Only essential packages

### Memory Management
- **Efficient Caching**: Smart memory usage
- **Background Processing**: Non-blocking operations
- **Resource Cleanup**: Proper disposal of resources

## Troubleshooting

### Common Issues

1. **Build Failures**:
   - Check Android SDK installation
   - Verify Java JDK version
   - Update Buildozer to latest version

2. **App Crashes**:
   - Check device compatibility
   - Verify permissions
   - Review log files

3. **Performance Issues**:
   - Reduce chunk sizes
   - Limit concurrent operations
   - Optimize UI updates

### Debug Mode
```bash
# Enable debug logging
buildozer android debug -v

# Check logs
adb logcat | grep python
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Test on Android device/emulator
4. Submit pull request

## License

Same license as the main Book of Shadows project.

## Support

For Android-specific issues:
- Check the troubleshooting section
- Review Buildozer documentation
- Submit issues with device information

---

**Book of Shadows - The Crone (Android)**: Bringing scholarly grimoire authoring to mobile devices.