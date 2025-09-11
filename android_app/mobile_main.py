#!/usr/bin/env python3
"""
Book of Shadows - The Crone Android App
Mobile-optimized main application
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
from kivy.metrics import dp

# Import our existing modules
sys.path.append(str(Path(__file__).parent))
from core.config import Config
from core.safety import SafetyManager
from core.memory import MemoryManager
from plugins.manager import PluginManager
from ui.mobile_components import (
    MobileButton, MobileTextInput, MobileLabel, MobileHeader,
    MobileCard, MobileList, MobileForm, MobileDialog, MobileNavigation,
    MobileSearchBar, MobileFloatingActionButton
)
from ui.mobile_grimoire_editor import MobileGrimoireEditor, MobileSpellEntry

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
        # Pixel Fold: 7.6" unfolded, 6.2" folded
        Window.size = (360, 640)
        
        # Enable adaptive layout for foldable devices
        if hasattr(Window, 'request_keyboard'):
            Window.request_keyboard()
        
        # Create main layout
        main_layout = BoxLayout(orientation='vertical', padding=dp(8), spacing=dp(8))
        
        # Header
        header = MobileHeader(text="Book of Shadows - The Crone")
        main_layout.add_widget(header)
        
        # Navigation
        self.navigation = MobileNavigation()
        self.navigation.add_tab("Home", self.show_home)
        self.navigation.add_tab("Grimoire", self.show_grimoire)
        self.navigation.add_tab("Ingest", self.show_ingest)
        self.navigation.add_tab("Settings", self.show_settings)
        main_layout.add_widget(self.navigation)
        
        # Main content area
        self.content_area = ScrollView()
        self.content_layout = BoxLayout(orientation='vertical', size_hint_y=None)
        self.content_layout.bind(minimum_height=self.content_layout.setter('height'))
        
        self.content_area.add_widget(self.content_layout)
        main_layout.add_widget(self.content_area)
        
        # Floating Action Button
        self.fab = MobileFloatingActionButton(text="+")
        self.fab.bind(on_press=self.show_create_entry)
        main_layout.add_widget(self.fab)
        
        # Initialize app components
        Clock.schedule_once(self.initialize_app, 0.1)
        
        # Bind to window size changes for Pixel Fold adaptation
        Window.bind(size=self.on_window_size_change)
        
        return main_layout
    
    def on_window_size_change(self, instance, size):
        """Handle window size changes for Pixel Fold adaptation."""
        width, height = size
        
        # Detect if device is folded/unfolded based on aspect ratio
        if width > height * 1.3:  # Landscape/unfolded
            self.adapt_layout_for_unfolded(width, height)
        else:  # Portrait/folded
            self.adapt_layout_for_folded(width, height)
    
    def adapt_layout_for_unfolded(self, width, height):
        """Adapt layout for unfolded Pixel Fold."""
        # Use more horizontal space
        if hasattr(self, 'navigation'):
            self.navigation.height = dp(48)  # Smaller nav for unfolded
        
        # Adjust content padding
        if hasattr(self, 'content_layout'):
            self.content_layout.padding = [dp(16), dp(8), dp(16), dp(8)]
    
    def adapt_layout_for_folded(self, width, height):
        """Adapt layout for folded Pixel Fold."""
        # Use standard mobile layout
        if hasattr(self, 'navigation'):
            self.navigation.height = dp(56)  # Standard nav height
        
        # Standard content padding
        if hasattr(self, 'content_layout'):
            self.content_layout.padding = [dp(8), dp(8), dp(8), dp(8)]
    
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
                
                self.grimoire_editor = MobileGrimoireEditor(
                    safety_manager=self.safety_manager,
                    plugin_manager=self.plugin_manager
                )
                
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
        
        # Welcome card
        welcome_card = MobileCard()
        welcome_card.add_widget(MobileLabel(
            text="Welcome to Book of Shadows - The Crone",
            font_size=dp(18),
            bold=True
        ))
        welcome_card.add_widget(MobileLabel(
            text="Your scholarly grimoire authoring companion"
        ))
        self.content_layout.add_widget(welcome_card)
        
        # Quick actions
        actions_card = MobileCard()
        actions_card.add_widget(MobileHeader(text="Quick Actions"))
        
        actions_grid = GridLayout(cols=2, size_hint_y=None, height=dp(200), spacing=dp(8))
        
        # Create new entry button
        new_entry_btn = MobileButton(text="New Spell/Ritual")
        new_entry_btn.bind(on_press=self.show_create_entry)
        actions_grid.add_widget(new_entry_btn)
        
        # Browse grimoire button
        browse_btn = MobileButton(text="Browse Grimoire")
        browse_btn.bind(on_press=self.show_grimoire)
        actions_grid.add_widget(browse_btn)
        
        # Ingest document button
        ingest_btn = MobileButton(text="Ingest Document")
        ingest_btn.bind(on_press=self.show_ingest)
        actions_grid.add_widget(ingest_btn)
        
        # Search button
        search_btn = MobileButton(text="Search")
        search_btn.bind(on_press=self.show_search)
        actions_grid.add_widget(search_btn)
        
        actions_card.add_widget(actions_grid)
        self.content_layout.add_widget(actions_card)
        
        # Recent entries
        recent_card = MobileCard()
        recent_card.add_widget(MobileHeader(text="Recent Entries"))
        
        recent_list = MobileList()
        entries = self.grimoire_editor.get_all_entries() if self.grimoire_editor else []
        
        if entries:
            for entry in entries[-3:]:  # Show last 3 entries
                entry_item = MobileCard()
                entry_item.height = dp(80)
                entry_item.add_widget(MobileLabel(text=entry.title, font_size=dp(16), bold=True))
                entry_item.add_widget(MobileLabel(text=f"{entry.entry_type.value.title()} • {entry.created_at.strftime('%Y-%m-%d')}"))
                
                view_btn = MobileButton(text="View", size_hint_x=None, width=dp(80))
                view_btn.bind(on_press=lambda x, e=entry: self.grimoire_editor._view_entry(e))
                entry_item.add_widget(view_btn)
                
                recent_list.add_item(entry_item)
        else:
            recent_list.add_item(MobileLabel(text="No entries yet. Create your first spell or ritual!"))
        
        recent_card.add_widget(recent_list)
        self.content_layout.add_widget(recent_card)
    
    def show_grimoire(self, instance=None):
        """Show grimoire browser."""
        self.current_screen = "grimoire"
        self.clear_content()
        
        # Grimoire header
        header_card = MobileCard()
        header_card.add_widget(MobileHeader(text="Your Grimoire"))
        self.content_layout.add_widget(header_card)
        
        # Search bar
        search_card = MobileCard()
        search_bar = MobileSearchBar()
        search_bar.bind_search(self.perform_search)
        search_card.add_widget(search_bar)
        self.content_layout.add_widget(search_card)
        
        # Entries list
        entries_card = MobileCard()
        entries = self.grimoire_editor.get_all_entries() if self.grimoire_editor else []
        
        if entries:
            entries_list = self.grimoire_editor.entry_list_view(entries)
            entries_card.add_widget(entries_list)
        else:
            entries_card.add_widget(MobileLabel(text="No entries in your grimoire yet."))
        
        self.content_layout.add_widget(entries_card)
    
    def show_ingest(self, instance=None):
        """Show document ingestion screen."""
        self.current_screen = "ingest"
        self.clear_content()
        
        # Ingest header
        header_card = MobileCard()
        header_card.add_widget(MobileHeader(text="Ingest Document"))
        self.content_layout.add_widget(header_card)
        
        # Ingest form
        ingest_form = MobileForm()
        
        # File selection
        file_input = MobileTextInput(hint_text="Enter file path or select from storage")
        ingest_form.add_field("Document", file_input, required=True)
        
        # Tag input
        tag_input = MobileTextInput(hint_text="e.g., folk-magic, protection, healing")
        ingest_form.add_field("Tag", tag_input)
        
        # Ingest button
        ingest_btn = MobileButton(text="Ingest Document")
        ingest_btn.bind(on_press=lambda x: self.ingest_document(file_input.text, tag_input.text))
        ingest_form.add_widget(ingest_btn)
        
        self.content_layout.add_widget(ingest_form)
    
    def show_settings(self, instance=None):
        """Show settings screen."""
        self.current_screen = "settings"
        self.clear_content()
        
        # Settings header
        header_card = MobileCard()
        header_card.add_widget(MobileHeader(text="Settings"))
        self.content_layout.add_widget(header_card)
        
        # Settings options
        settings_form = MobileForm()
        
        # Safety settings
        safety_btn = MobileButton(text="Safety & Ethics Settings")
        safety_btn.bind(on_press=self.show_safety_settings)
        settings_form.add_widget(safety_btn)
        
        # Memory settings
        memory_btn = MobileButton(text="Memory & Storage")
        memory_btn.bind(on_press=self.show_memory_settings)
        settings_form.add_widget(memory_btn)
        
        # About
        about_btn = MobileButton(text="About")
        about_btn.bind(on_press=self.show_about)
        settings_form.add_widget(about_btn)
        
        self.content_layout.add_widget(settings_form)
    
    def show_create_entry(self, instance=None):
        """Show create entry form."""
        if not self.grimoire_editor:
            self.show_error("Grimoire editor not initialized")
            return
        
        form = self.grimoire_editor.create_entry_form(self.on_entry_created)
        dialog = MobileDialog(title="Create New Entry", content=form)
        dialog.open()
    
    def show_search(self, instance=None):
        """Show search screen."""
        self.clear_content()
        
        # Search header
        header_card = MobileCard()
        header_card.add_widget(MobileHeader(text="Search Grimoire"))
        self.content_layout.add_widget(header_card)
        
        # Search form
        search_form = MobileForm()
        
        # Search input
        search_input = MobileTextInput(hint_text="Enter search terms")
        search_form.add_field("Search", search_input, required=True)
        
        # Search button
        search_btn = MobileButton(text="Search")
        search_btn.bind(on_press=lambda x: self.perform_search(search_input.text))
        search_form.add_widget(search_btn)
        
        self.content_layout.add_widget(search_form)
    
    def on_entry_created(self, result):
        """Handle entry creation result."""
        if result["success"]:
            self.show_success("Entry created successfully!")
            self.show_grimoire()
        else:
            self.show_error(result.get("error", "Failed to create entry"))
    
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
    
    def perform_search(self, query):
        """Perform search."""
        if not query:
            self.show_error("Please enter search terms")
            return
        
        # Clear content and show results
        self.clear_content()
        
        # Search results header
        header_card = MobileCard()
        header_card.add_widget(MobileHeader(text=f"Search Results: {query}"))
        self.content_layout.add_widget(header_card)
        
        # Placeholder search results
        results_card = MobileCard()
        results_card.add_widget(MobileLabel(text="Search functionality will be implemented in future version"))
        self.content_layout.add_widget(results_card)
    
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
        
        popup = MobileDialog(
            title="About",
            content=MobileLabel(text=about_text)
        )
        popup.open()
    
    def clear_content(self):
        """Clear the content area."""
        self.content_layout.clear_widgets()
    
    def show_error(self, message):
        """Show error message."""
        popup = MobileDialog(
            title="Error",
            content=MobileLabel(text=message)
        )
        popup.open()
    
    def show_success(self, message):
        """Show success message."""
        popup = MobileDialog(
            title="Success",
            content=MobileLabel(text=message)
        )
        popup.open()
    
    def show_info(self, message):
        """Show info message."""
        popup = MobileDialog(
            title="Info",
            content=MobileLabel(text=message)
        )
        popup.open()

if __name__ == "__main__":
    BookOfShadowsMobileApp().run()