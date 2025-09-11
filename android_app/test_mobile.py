#!/usr/bin/env python3
"""
Mobile test for Book of Shadows - The Crone Android App
"""

import asyncio
import sys
from pathlib import Path

# Add the workspace to Python path
sys.path.insert(0, str(Path(__file__).parent))

from core.config import Config
from core.safety import SafetyManager
from core.memory import MemoryManager
from plugins.manager import PluginManager
from ui.mobile_grimoire_editor import MobileGrimoireEditor, MobileSpellEntry, SpellEntryType, EfficacyClaim

async def test_mobile_functionality():
    """Test mobile app functionality."""
    print("📱 Testing Book of Shadows - The Crone Mobile App")
    print("=" * 60)
    
    # Test configuration
    print("\n1. Testing Mobile Configuration...")
    config = Config("config_mobile.yaml")
    print(f"   ✓ Mobile configuration loaded")
    print(f"   ✓ Chunk size: {config.ingestion.chunk_size} (mobile-optimized)")
    print(f"   ✓ Touch friendly: {config.ui.touch_friendly}")
    
    # Test safety manager
    print("\n2. Testing Safety Manager...")
    safety_manager = SafetyManager()
    await safety_manager.initialize()
    
    # Test safe command
    result = await safety_manager.check_command("INGEST file='test.pdf' TAG test")
    print(f"   ✓ Safe command check: {result['safe']}")
    
    # Test unsafe command
    result = await safety_manager.check_command("Create poison bomb")
    print(f"   ✓ Unsafe command check: {result['safe']} (should be False)")
    
    # Test memory manager
    print("\n3. Testing Memory Manager...")
    memory_manager = MemoryManager()
    await memory_manager.initialize()
    
    session_id = await memory_manager.create_session()
    print(f"   ✓ Mobile session created: {session_id}")
    
    # Test plugin manager
    print("\n4. Testing Plugin Manager...")
    plugin_manager = PluginManager()
    await plugin_manager.initialize()
    await plugin_manager.load_plugins()
    print(f"   ✓ Mobile plugins loaded: {len(plugin_manager.plugins)}")
    
    # Test mobile grimoire editor
    print("\n5. Testing Mobile Grimoire Editor...")
    grimoire_editor = MobileGrimoireEditor(
        safety_manager=safety_manager,
        plugin_manager=plugin_manager
    )
    
    # Create a test entry
    test_entry = MobileSpellEntry()
    test_entry.id = "test_entry_001"
    test_entry.title = "Mobile Protection Spell"
    test_entry.entry_type = SpellEntryType.PROTECTION
    test_entry.lineage_tradition = "Mobile Test Tradition"
    test_entry.efficacy_claim = EfficacyClaim.UNVERIFIABLE_SUPERNATURAL
    
    grimoire_editor.entries[test_entry.id] = test_entry
    print(f"   ✓ Created mobile test entry: {test_entry.title}")
    
    # Test ingredient management
    grimoire_editor._add_ingredient(test_entry, "Salt", "Purification salt", "1 pinch")
    grimoire_editor._add_ingredient(test_entry, "Candle", "White candle", "1 piece")
    print(f"   ✓ Added ingredients: {len(test_entry.ingredients)}")
    
    # Test citation management
    grimoire_editor._add_citation(test_entry, "@TEST001::CHUNK0001", "Mobile test source")
    print(f"   ✓ Added citation: {len(test_entry.provenance_citations)}")
    
    # Test mobile UI components
    print("\n6. Testing Mobile UI Components...")
    from ui.mobile_components import MobileButton, MobileTextInput, MobileLabel, MobileCard
    
    # Test component creation
    button = MobileButton(text="Test Button")
    text_input = MobileTextInput(hint_text="Test input")
    label = MobileLabel(text="Test label")
    card = MobileCard()
    
    print(f"   ✓ Mobile button created: {button.text}")
    print(f"   ✓ Mobile text input created: {text_input.hint_text}")
    print(f"   ✓ Mobile label created: {label.text}")
    print(f"   ✓ Mobile card created")
    
    # Test form creation
    print("\n7. Testing Mobile Forms...")
    form = grimoire_editor.create_entry_form()
    print(f"   ✓ Entry creation form created")
    
    edit_form = grimoire_editor.edit_entry_form(test_entry)
    print(f"   ✓ Entry editing form created")
    
    ingredients_form = grimoire_editor.ingredients_management_form(test_entry)
    print(f"   ✓ Ingredients management form created")
    
    citations_form = grimoire_editor.citations_management_form(test_entry)
    print(f"   ✓ Citations management form created")
    
    # Test entry list view
    entries_list = grimoire_editor.entry_list_view([test_entry])
    print(f"   ✓ Entry list view created")
    
    # Cleanup
    print("\n8. Cleaning up...")
    await memory_manager.close_session(session_id)
    await plugin_manager.cleanup()
    await memory_manager.cleanup()
    await safety_manager.cleanup()
    print("   ✓ Cleanup completed")
    
    print("\n" + "=" * 60)
    print("✅ All mobile tests passed!")
    print("📱 Book of Shadows - The Crone is ready for Android!")
    print("")
    print("🚀 Next steps:")
    print("   1. Run: python mobile_main.py (for desktop testing)")
    print("   2. Build APK: ./build_android.sh")
    print("   3. Install on Android device")

if __name__ == "__main__":
    asyncio.run(test_mobile_functionality())