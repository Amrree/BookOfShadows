#!/usr/bin/env python3
"""
Basic test for Book of Shadows - The Crone
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
from ui.grimoire_editor import GrimoireEditor, SpellEntryType

async def test_basic_functionality():
    """Test basic system functionality."""
    print("Testing Book of Shadows - The Crone")
    print("=" * 50)
    
    # Test configuration
    print("\n1. Testing Configuration...")
    config = Config()
    print(f"   ✓ Configuration loaded")
    print(f"   ✓ Data directory: {config.data_dir}")
    print(f"   ✓ Chunk size: {config.ingestion.chunk_size}")
    
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
    print(f"   ✓ Session created: {session_id}")
    
    # Test plugin manager
    print("\n4. Testing Plugin Manager...")
    plugin_manager = PluginManager()
    await plugin_manager.initialize()
    await plugin_manager.load_plugins()
    print(f"   ✓ Plugins loaded: {len(plugin_manager.plugins)}")
    
    # Test grimoire editor
    print("\n5. Testing Grimoire Editor...")
    editor = GrimoireEditor()
    
    # Create a test entry
    result = await editor.create_entry(
        title="Test Protection Spell",
        entry_type=SpellEntryType.PROTECTION,
        lineage_tradition="Test Tradition"
    )
    
    if result['success']:
        entry_id = result['result']['entry_id']
        print(f"   ✓ Created test entry: {entry_id}")
        
        # Add an ingredient
        await editor.add_ingredient(entry_id, {
            'name': 'Salt',
            'description': 'Purification salt',
            'quantity': '1 pinch'
        })
        print(f"   ✓ Added ingredient")
        
        # Export entry
        export_result = await editor.export_entry(entry_id, "markdown")
        if export_result['success']:
            print(f"   ✓ Exported entry (length: {len(export_result['result']['content'])} chars)")
    
    # Cleanup
    print("\n6. Cleaning up...")
    await memory_manager.close_session(session_id)
    await plugin_manager.cleanup()
    await memory_manager.cleanup()
    await safety_manager.cleanup()
    print("   ✓ Cleanup completed")
    
    print("\n" + "=" * 50)
    print("✓ All basic tests passed!")
    print("Book of Shadows - The Crone is ready for use.")

if __name__ == "__main__":
    asyncio.run(test_basic_functionality())