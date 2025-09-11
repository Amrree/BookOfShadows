#!/usr/bin/env python3
"""
Book of Shadows - The Crone Android App
Mobile-optimized version of the Grimoire IDE
"""

import asyncio
import logging
import sys
from pathlib import Path
from typing import Dict, Any, Optional

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.core.window import Window

# Import our existing modules
sys.path.append(str(Path(__file__).parent))
from core.config import Config
from core.safety import SafetyManager
from core.memory import MemoryManager
from plugins.manager import PluginManager
from ui.grimoire_editor import GrimoireEditor, SpellEntryType

# Configure logging for mobile
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('book_of_shadows_mobile.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class BookOfShadowsMobileApp(App):
    """Main Android application class."""
    
    def __init__(self):
        """Initialize the mobile app."""
        super().__init__()
        self.title = "Book of Shadows - The Crone"
        self.icon = "assets/icon.png"
        
        # Initialize core components
        self.config_mobile = None
        self.safety_manager = None
        self.memory_manager = None
        self.plugin_manager = None
        self.grimoire_editor = None
        
        # UI state
        self.current_screen = "home"
        self.current_entry = None
        
    def build(self):
        """Build the main UI."""
        # Set window size for mobile (will be overridden on actual device)
        Window.size = (360, 640)
        
        # Create main layout
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header = Label(
            text="Book of Shadows - The Crone",
            size_hint_y=0.1,
            font_size=20,
            bold=True
        )
        main_layout.add_widget(header)
        
        # Navigation buttons
        nav_layout = BoxLayout(orientation='horizontal', size_hint_y=0.1, spacing=5)
        
        home_btn = Button(text="Home", size_hint_x=0.25)
        home_btn.bind(on_press=self.show_home)
        nav_layout.add_widget(home_btn)
        
        grimoire_btn = Button(text="Grimoire", size_hint_x=0.25)
        grimoire_btn.bind(on_press=self.show_grimoire)
        nav_layout.add_widget(grimoire_btn)
        
        ingest_btn = Button(text="Ingest", size_hint_x=0.25)
        ingest_btn.bind(on_press=self.show_ingest)
        nav_layout.add_widget(ingest_btn)
        
        settings_btn = Button(text="Settings", size_hint_x=0.25)
        settings_btn.bind(on_press=self.show_settings)
        nav_layout.add_widget(settings_btn)
        
        main_layout.add_widget(nav_layout)
        
        # Main content area
        self.content_area = ScrollView()
        self.content_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.content_layout.bind(minimum_height=self.content_layout.setter('height'))
        
        self.content_area.add_widget(self.content_layout)
        main_layout.add_widget(self.content_area)
        
        # Initialize app components
        Clock.schedule_once(self.initialize_app, 0.1)
        
        return main_layout
    
    def initialize_app(self, dt):
        """Initialize app components asynchronously."""
        async def init_components():
            try:
                # Initialize configuration
                self.config_mobile = Config("config_mobile.yaml")
                
                # Initialize core components
                self.safety_manager = SafetyManager()
                await self.safety_manager.initialize()
                
                self.memory_manager = MemoryManager()
                await self.memory_manager.initialize()
                
                self.plugin_manager = PluginManager()
                await self.plugin_manager.initialize()
                await self.plugin_manager.load_plugins()
                
                self.grimoire_editor = GrimoireEditor()
                
                # Show home screen
                self.show_home()
                
                logger.info("Book of Shadows mobile app initialized successfully")
                
            except Exception as e:
                logger.error(f"Failed to initialize app: {e}")
                self.show_error(f"Initialization failed: {str(e)}")
        
        # Run async initialization
        asyncio.create_task(init_components())
    
    def show_home(self, instance=None):
        """Show home screen."""
        self.current_screen = "home"
        self.clear_content()
        
        # Welcome message
        welcome = Label(
            text="Welcome to Book of Shadows - The Crone",
            size_hint_y=None,
            height=50,
            font_size=16
        )
        self.content_layout.add_widget(welcome)
        
        # Quick actions
        actions_layout = GridLayout(cols=2, size_hint_y=None, height=200, spacing=10)
        
        # Create new entry button
        new_entry_btn = Button(text="New Spell/Ritual")
        new_entry_btn.bind(on_press=self.create_new_entry)
        actions_layout.add_widget(new_entry_btn)
        
        # Browse grimoire button
        browse_btn = Button(text="Browse Grimoire")
        browse_btn.bind(on_press=self.browse_grimoire)
        actions_layout.add_widget(browse_btn)
        
        # Ingest document button
        ingest_btn = Button(text="Ingest Document")
        ingest_btn.bind(on_press=self.show_ingest)
        actions_layout.add_widget(ingest_btn)
        
        # Search button
        search_btn = Button(text="Search")
        search_btn.bind(on_press=self.show_search)
        actions_layout.add_widget(search_btn)
        
        self.content_layout.add_widget(actions_layout)
        
        # Recent entries
        recent_label = Label(
            text="Recent Entries",
            size_hint_y=None,
            height=30,
            font_size=14,
            bold=True
        )
        self.content_layout.add_widget(recent_label)
        
        # Add recent entries list
        self.show_recent_entries()
    
    def show_grimoire(self, instance=None):
        """Show grimoire browser."""
        self.current_screen = "grimoire"
        self.clear_content()
        
        # Grimoire header
        header = Label(
            text="Your Grimoire",
            size_hint_y=None,
            height=40,
            font_size=18,
            bold=True
        )
        self.content_layout.add_widget(header)
        
        # Add grimoire entries
        self.show_grimoire_entries()
    
    def show_ingest(self, instance=None):
        """Show document ingestion screen."""
        self.current_screen = "ingest"
        self.clear_content()
        
        # Ingest header
        header = Label(
            text="Ingest Document",
            size_hint_y=None,
            height=40,
            font_size=18,
            bold=True
        )
        self.content_layout.add_widget(header)
        
        # File selection (placeholder for now)
        file_label = Label(
            text="Select a document to ingest:",
            size_hint_y=None,
            height=30
        )
        self.content_layout.add_widget(file_label)
        
        # File input
        file_input = TextInput(
            hint_text="Enter file path or select from storage",
            size_hint_y=None,
            height=40
        )
        self.content_layout.add_widget(file_input)
        
        # Tag input
        tag_label = Label(
            text="Tag (optional):",
            size_hint_y=None,
            height=30
        )
        self.content_layout.add_widget(tag_label)
        
        tag_input = TextInput(
            hint_text="e.g., folk-magic, protection, healing",
            size_hint_y=None,
            height=40
        )
        self.content_layout.add_widget(tag_input)
        
        # Ingest button
        ingest_btn = Button(
            text="Ingest Document",
            size_hint_y=None,
            height=50
        )
        ingest_btn.bind(on_press=lambda x: self.ingest_document(file_input.text, tag_input.text))
        self.content_layout.add_widget(ingest_btn)
    
    def show_settings(self, instance=None):
        """Show settings screen."""
        self.current_screen = "settings"
        self.clear_content()
        
        # Settings header
        header = Label(
            text="Settings",
            size_hint_y=None,
            height=40,
            font_size=18,
            bold=True
        )
        self.content_layout.add_widget(header)
        
        # Settings options
        settings_layout = BoxLayout(orientation='vertical', spacing=10)
        
        # Safety settings
        safety_btn = Button(text="Safety & Ethics Settings")
        safety_btn.bind(on_press=self.show_safety_settings)
        settings_layout.add_widget(safety_btn)
        
        # Memory settings
        memory_btn = Button(text="Memory & Storage")
        memory_btn.bind(on_press=self.show_memory_settings)
        settings_layout.add_widget(memory_btn)
        
        # About
        about_btn = Button(text="About")
        about_btn.bind(on_press=self.show_about)
        settings_layout.add_widget(about_btn)
        
        self.content_layout.add_widget(settings_layout)
    
    def create_new_entry(self, instance=None):
        """Create a new spell/ritual entry."""
        self.clear_content()
        
        # Entry creation form
        header = Label(
            text="Create New Entry",
            size_hint_y=None,
            height=40,
            font_size=18,
            bold=True
        )
        self.content_layout.add_widget(header)
        
        # Title input
        title_label = Label(text="Title:", size_hint_y=None, height=30)
        self.content_layout.add_widget(title_label)
        
        title_input = TextInput(
            hint_text="Enter spell/ritual title",
            size_hint_y=None,
            height=40
        )
        self.content_layout.add_widget(title_input)
        
        # Type selection
        type_label = Label(text="Type:", size_hint_y=None, height=30)
        self.content_layout.add_widget(type_label)
        
        type_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40)
        
        spell_btn = Button(text="Spell")
        spell_btn.bind(on_press=lambda x: self.set_entry_type("spell"))
        type_layout.add_widget(spell_btn)
        
        ritual_btn = Button(text="Ritual")
        ritual_btn.bind(on_press=lambda x: self.set_entry_type("ritual"))
        type_layout.add_widget(ritual_btn)
        
        blessing_btn = Button(text="Blessing")
        blessing_btn.bind(on_press=lambda x: self.set_entry_type("blessing"))
        type_layout.add_widget(blessing_btn)
        
        self.content_layout.add_widget(type_layout)
        
        # Lineage input
        lineage_label = Label(text="Lineage/Tradition:", size_hint_y=None, height=30)
        self.content_layout.add_widget(lineage_label)
        
        lineage_input = TextInput(
            hint_text="e.g., County Cork tradition, Celtic, etc.",
            size_hint_y=None,
            height=40
        )
        self.content_layout.add_widget(lineage_input)
        
        # Create button
        create_btn = Button(
            text="Create Entry",
            size_hint_y=None,
            height=50
        )
        create_btn.bind(on_press=lambda x: self.create_entry(title_input.text, lineage_input.text))
        self.content_layout.add_widget(create_btn)
    
    def set_entry_type(self, entry_type):
        """Set the entry type."""
        self.selected_entry_type = entry_type
    
    def create_entry(self, title, lineage):
        """Create a new entry."""
        if not title:
            self.show_error("Please enter a title")
            return
        
        if not hasattr(self, 'selected_entry_type'):
            self.show_error("Please select an entry type")
            return
        
        try:
            # Map string to enum
            type_mapping = {
                "spell": SpellEntryType.SPELL,
                "ritual": SpellEntryType.RITUAL,
                "blessing": SpellEntryType.BLESSING
            }
            
            entry_type = type_mapping.get(self.selected_entry_type, SpellEntryType.OTHER)
            
            # Create entry using existing grimoire editor
            if self.grimoire_editor:
                result = asyncio.create_task(
                    self.grimoire_editor.create_entry(title, entry_type, lineage)
                )
                
                if result.done() and result.result()['success']:
                    self.show_success(f"Created entry: {title}")
                    self.show_grimoire()
                else:
                    self.show_error("Failed to create entry")
            
        except Exception as e:
            logger.error(f"Error creating entry: {e}")
            self.show_error(f"Error: {str(e)}")
    
    def ingest_document(self, file_path, tag):
        """Ingest a document."""
        if not file_path:
            self.show_error("Please enter a file path")
            return
        
        try:
            # Use existing plugin system
            if self.plugin_manager:
                result = asyncio.create_task(
                    self.plugin_manager.execute_plugin_capability(
                        "pdf_ingestor", "ingest", file_path=file_path, tag=tag
                    )
                )
                
                if result.done() and result.result()['success']:
                    self.show_success("Document ingested successfully")
                else:
                    self.show_error("Failed to ingest document")
            
        except Exception as e:
            logger.error(f"Error ingesting document: {e}")
            self.show_error(f"Error: {str(e)}")
    
    def show_recent_entries(self):
        """Show recent entries."""
        # Placeholder for recent entries
        recent_layout = BoxLayout(orientation='vertical', spacing=5)
        
        for i in range(3):
            entry_btn = Button(
                text=f"Recent Entry {i+1}",
                size_hint_y=None,
                height=40
            )
            recent_layout.add_widget(entry_btn)
        
        self.content_layout.add_widget(recent_layout)
    
    def show_grimoire_entries(self):
        """Show grimoire entries."""
        # Placeholder for grimoire entries
        entries_layout = BoxLayout(orientation='vertical', spacing=5)
        
        for i in range(5):
            entry_btn = Button(
                text=f"Grimoire Entry {i+1}",
                size_hint_y=None,
                height=40
            )
            entries_layout.add_widget(entry_btn)
        
        self.content_layout.add_widget(entries_layout)
    
    def show_search(self, instance=None):
        """Show search screen."""
        self.clear_content()
        
        # Search header
        header = Label(
            text="Search Grimoire",
            size_hint_y=None,
            height=40,
            font_size=18,
            bold=True
        )
        self.content_layout.add_widget(header)
        
        # Search input
        search_input = TextInput(
            hint_text="Enter search terms",
            size_hint_y=None,
            height=40
        )
        self.content_layout.add_widget(search_input)
        
        # Search button
        search_btn = Button(
            text="Search",
            size_hint_y=None,
            height=50
        )
        search_btn.bind(on_press=lambda x: self.perform_search(search_input.text))
        self.content_layout.add_widget(search_btn)
    
    def perform_search(self, query):
        """Perform search."""
        if not query:
            self.show_error("Please enter search terms")
            return
        
        # Placeholder search results
        results_label = Label(
            text=f"Search results for: {query}",
            size_hint_y=None,
            height=30
        )
        self.content_layout.add_widget(results_label)
        
        # Add search results
        for i in range(3):
            result_btn = Button(
                text=f"Search Result {i+1}",
                size_hint_y=None,
                height=40
            )
            self.content_layout.add_widget(result_btn)
    
    def show_safety_settings(self, instance=None):
        """Show safety settings."""
        self.show_info("Safety settings will be implemented in future version")
    
    def show_memory_settings(self, instance=None):
        """Show memory settings."""
        self.show_info("Memory settings will be implemented in future version")
    
    def show_about(self, instance=None):
        """Show about dialog."""
        about_text = """
Book of Shadows - The Crone
Version 1.0.0 (Android)

A research-grade, ritual-aware Grimoire IDE
for scholars, practitioners, and writers.

Built with Kivy for Android.
        """
        
        popup = Popup(
            title="About",
            content=Label(text=about_text),
            size_hint=(0.8, 0.6)
        )
        popup.open()
    
    def clear_content(self):
        """Clear the content area."""
        self.content_layout.clear_widgets()
    
    def show_error(self, message):
        """Show error message."""
        popup = Popup(
            title="Error",
            content=Label(text=message),
            size_hint=(0.8, 0.4)
        )
        popup.open()
    
    def show_success(self, message):
        """Show success message."""
        popup = Popup(
            title="Success",
            content=Label(text=message),
            size_hint=(0.8, 0.4)
        )
        popup.open()
    
    def show_info(self, message):
        """Show info message."""
        popup = Popup(
            title="Info",
            content=Label(text=message),
            size_hint=(0.8, 0.4)
        )
        popup.open()

if __name__ == "__main__":
    BookOfShadowsMobileApp().run()