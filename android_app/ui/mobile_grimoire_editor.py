"""
Mobile-optimized Grimoire Editor for Book of Shadows - The Crone
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
from enum import Enum

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.metrics import dp

from .mobile_components import (
    MobileButton, MobileTextInput, MobileLabel, MobileHeader,
    MobileCard, MobileList, MobileForm, MobileDialog, MobileSpinner
)
from ..core.safety import SafetyManager
from ..plugins.manager import PluginManager

logger = logging.getLogger(__name__)

class SpellEntryType(Enum):
    """Types of spell entries."""
    SPELL = "spell"
    RITUAL = "ritual"
    BLESSING = "blessing"
    CURSE = "curse"
    PROTECTION = "protection"
    HEALING = "healing"
    DIVINATION = "divination"
    OTHER = "other"

class EfficacyClaim(Enum):
    """Types of efficacy claims."""
    HISTORICAL = "historical"
    RITUAL_TRADITIONAL = "ritual_traditional"
    PERSONAL_ANECDOTAL = "personal_anecdotal"
    UNVERIFIABLE_SUPERNATURAL = "unverifiable_supernatural"

class MobileSpellEntry:
    """Mobile-optimized spell entry."""
    
    def __init__(self):
        self.id = ""
        self.title = ""
        self.entry_type = SpellEntryType.OTHER
        self.lineage_tradition = ""
        self.ingredients = []
        self.tools = []
        self.incipit = ""
        self.instructions = ""
        self.notes = ""
        self.efficacy_claim = EfficacyClaim.UNVERIFIABLE_SUPERNATURAL
        self.provenance_citations = []
        self.practice_log = []
        self.created_at = datetime.now()
        self.updated_at = datetime.now()
        self.tags = []

class MobileGrimoireEditor:
    """Mobile-optimized grimoire editor."""
    
    def __init__(self, safety_manager: SafetyManager = None, plugin_manager: PluginManager = None):
        """Initialize mobile grimoire editor."""
        self.safety_manager = safety_manager
        self.plugin_manager = plugin_manager
        self.entries = {}
        self.current_entry = None
        
    def create_entry_form(self, callback=None):
        """Create entry creation form."""
        form = MobileForm()
        
        # Title input
        title_input = MobileTextInput(hint_text="Enter spell/ritual title")
        form.add_field("Title", title_input, required=True)
        
        # Type selection
        type_spinner = MobileSpinner(
            text="Select Type",
            values=["Spell", "Ritual", "Blessing", "Protection", "Healing", "Divination", "Other"]
        )
        form.add_field("Type", type_spinner, required=True)
        
        # Lineage input
        lineage_input = MobileTextInput(hint_text="e.g., County Cork tradition")
        form.add_field("Lineage/Tradition", lineage_input)
        
        # Efficacy claim
        efficacy_spinner = MobileSpinner(
            text="Select Efficacy Claim",
            values=["Historical", "Ritual Traditional", "Personal Anecdotal", "Unverifiable Supernatural"]
        )
        form.add_field("Efficacy Claim", efficacy_spinner, required=True)
        
        # Create button
        create_btn = MobileButton(text="Create Entry")
        create_btn.bind(on_press=lambda x: self._create_entry(
            title_input.text, type_spinner.text, lineage_input.text, efficacy_spinner.text, callback
        ))
        form.add_widget(create_btn)
        
        return form
    
    def edit_entry_form(self, entry: MobileSpellEntry, callback=None):
        """Create entry editing form."""
        form = MobileForm()
        
        # Title input
        title_input = MobileTextInput(text=entry.title, hint_text="Enter spell/ritual title")
        form.add_field("Title", title_input, required=True)
        
        # Type selection
        type_spinner = MobileSpinner(
            text=entry.entry_type.value.title(),
            values=["Spell", "Ritual", "Blessing", "Protection", "Healing", "Divination", "Other"]
        )
        form.add_field("Type", type_spinner, required=True)
        
        # Lineage input
        lineage_input = MobileTextInput(text=entry.lineage_tradition, hint_text="e.g., County Cork tradition")
        form.add_field("Lineage/Tradition", lineage_input)
        
        # Incipit input
        incipit_input = MobileTextInput(text=entry.incipit, hint_text="Opening words or invocation")
        incipit_input.multiline = True
        incipit_input.height = dp(100)
        form.add_field("Incipit", incipit_input)
        
        # Instructions input
        instructions_input = MobileTextInput(text=entry.instructions, hint_text="Step-by-step instructions")
        instructions_input.multiline = True
        instructions_input.height = dp(150)
        form.add_field("Instructions", instructions_input)
        
        # Notes input
        notes_input = MobileTextInput(text=entry.notes, hint_text="Additional notes")
        notes_input.multiline = True
        notes_input.height = dp(100)
        form.add_field("Notes", notes_input)
        
        # Efficacy claim
        efficacy_spinner = MobileSpinner(
            text=entry.efficacy_claim.value.replace('_', ' ').title(),
            values=["Historical", "Ritual Traditional", "Personal Anecdotal", "Unverifiable Supernatural"]
        )
        form.add_field("Efficacy Claim", efficacy_spinner, required=True)
        
        # Save button
        save_btn = MobileButton(text="Save Changes")
        save_btn.bind(on_press=lambda x: self._save_entry(
            entry, title_input.text, type_spinner.text, lineage_input.text,
            incipit_input.text, instructions_input.text, notes_input.text,
            efficacy_spinner.text, callback
        ))
        form.add_widget(save_btn)
        
        return form
    
    def ingredients_management_form(self, entry: MobileSpellEntry, callback=None):
        """Create ingredients management form."""
        form = MobileForm()
        
        # Add ingredient section
        add_section = MobileCard()
        add_section.add_widget(MobileHeader(text="Add Ingredient"))
        
        ingredient_name = MobileTextInput(hint_text="Ingredient name")
        add_section.add_widget(ingredient_name)
        
        ingredient_desc = MobileTextInput(hint_text="Description")
        add_section.add_widget(ingredient_desc)
        
        ingredient_qty = MobileTextInput(hint_text="Quantity")
        add_section.add_widget(ingredient_qty)
        
        add_btn = MobileButton(text="Add Ingredient")
        add_btn.bind(on_press=lambda x: self._add_ingredient(
            entry, ingredient_name.text, ingredient_desc.text, ingredient_qty.text
        ))
        add_section.add_widget(add_btn)
        
        form.add_widget(add_section)
        
        # Current ingredients list
        ingredients_section = MobileCard()
        ingredients_section.add_widget(MobileHeader(text="Current Ingredients"))
        
        ingredients_list = MobileList()
        for ingredient in entry.ingredients:
            ingredient_card = MobileCard()
            ingredient_card.add_widget(MobileLabel(text=f"{ingredient.get('name', 'Unknown')} - {ingredient.get('quantity', '')}"))
            ingredient_card.add_widget(MobileLabel(text=ingredient.get('description', '')))
            
            remove_btn = MobileButton(text="Remove", size_hint_x=None, width=dp(100))
            remove_btn.bind(on_press=lambda x, ing=ingredient: self._remove_ingredient(entry, ing))
            ingredient_card.add_widget(remove_btn)
            
            ingredients_list.add_item(ingredient_card)
        
        ingredients_section.add_widget(ingredients_list)
        form.add_widget(ingredients_section)
        
        return form
    
    def citations_management_form(self, entry: MobileSpellEntry, callback=None):
        """Create citations management form."""
        form = MobileForm()
        
        # Add citation section
        add_section = MobileCard()
        add_section.add_widget(MobileHeader(text="Add Citation"))
        
        chunk_id_input = MobileTextInput(hint_text="Chunk ID (e.g., @BOOK001::CHUNK0042)")
        add_section.add_widget(chunk_id_input)
        
        context_input = MobileTextInput(hint_text="Context or description")
        context_input.multiline = True
        context_input.height = dp(80)
        add_section.add_widget(context_input)
        
        add_btn = MobileButton(text="Add Citation")
        add_btn.bind(on_press=lambda x: self._add_citation(
            entry, chunk_id_input.text, context_input.text
        ))
        add_section.add_widget(add_btn)
        
        form.add_widget(add_section)
        
        # Current citations list
        citations_section = MobileCard()
        citations_section.add_widget(MobileHeader(text="Current Citations"))
        
        citations_list = MobileList()
        for citation in entry.provenance_citations:
            citation_card = MobileCard()
            citation_card.add_widget(MobileLabel(text=citation.get('chunk_id', 'Unknown')))
            citation_card.add_widget(MobileLabel(text=citation.get('context', '')))
            
            remove_btn = MobileButton(text="Remove", size_hint_x=None, width=dp(100))
            remove_btn.bind(on_press=lambda x, cit=citation: self._remove_citation(entry, cit))
            citation_card.add_widget(remove_btn)
            
            citations_list.add_item(citation_card)
        
        citations_section.add_widget(citations_list)
        form.add_widget(citations_section)
        
        return form
    
    def entry_list_view(self, entries: List[MobileSpellEntry], callback=None):
        """Create entry list view."""
        scroll = ScrollView()
        list_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(8))
        list_layout.bind(minimum_height=list_layout.setter('height'))
        
        for entry in entries:
            entry_card = MobileCard()
            entry_card.height = dp(100)
            
            # Entry info
            info_layout = BoxLayout(orientation='vertical')
            info_layout.add_widget(MobileLabel(text=entry.title, font_size=dp(18), bold=True))
            info_layout.add_widget(MobileLabel(text=f"Type: {entry.entry_type.value.title()}"))
            info_layout.add_widget(MobileLabel(text=f"Lineage: {entry.lineage_tradition}"))
            info_layout.add_widget(MobileLabel(text=f"Created: {entry.created_at.strftime('%Y-%m-%d')}"))
            
            entry_card.add_widget(info_layout)
            
            # Action buttons
            actions_layout = BoxLayout(orientation='horizontal', size_hint_x=None, width=dp(200))
            
            view_btn = MobileButton(text="View", size_hint_x=None, width=dp(60))
            view_btn.bind(on_press=lambda x, e=entry: self._view_entry(e, callback))
            actions_layout.add_widget(view_btn)
            
            edit_btn = MobileButton(text="Edit", size_hint_x=None, width=dp(60))
            edit_btn.bind(on_press=lambda x, e=entry: self._edit_entry(e, callback))
            actions_layout.add_widget(edit_btn)
            
            delete_btn = MobileButton(text="Delete", size_hint_x=None, width=dp(60))
            delete_btn.bind(on_press=lambda x, e=entry: self._delete_entry(e, callback))
            actions_layout.add_widget(delete_btn)
            
            entry_card.add_widget(actions_layout)
            list_layout.add_widget(entry_card)
        
        scroll.add_widget(list_layout)
        return scroll
    
    def _create_entry(self, title, entry_type, lineage, efficacy_claim, callback=None):
        """Create a new entry."""
        if not title:
            if callback:
                callback({"success": False, "error": "Title is required"})
            return
        
        try:
            # Map string to enum
            type_mapping = {
                "Spell": SpellEntryType.SPELL,
                "Ritual": SpellEntryType.RITUAL,
                "Blessing": SpellEntryType.BLESSING,
                "Protection": SpellEntryType.PROTECTION,
                "Healing": SpellEntryType.HEALING,
                "Divination": SpellEntryType.DIVINATION,
                "Other": SpellEntryType.OTHER
            }
            
            efficacy_mapping = {
                "Historical": EfficacyClaim.HISTORICAL,
                "Ritual Traditional": EfficacyClaim.RITUAL_TRADITIONAL,
                "Personal Anecdotal": EfficacyClaim.PERSONAL_ANECDOTAL,
                "Unverifiable Supernatural": EfficacyClaim.UNVERIFIABLE_SUPERNATURAL
            }
            
            entry = MobileSpellEntry()
            entry.id = f"entry_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            entry.title = title
            entry.entry_type = type_mapping.get(entry_type, SpellEntryType.OTHER)
            entry.lineage_tradition = lineage
            entry.efficacy_claim = efficacy_mapping.get(efficacy_claim, EfficacyClaim.UNVERIFIABLE_SUPERNATURAL)
            
            self.entries[entry.id] = entry
            self.current_entry = entry
            
            if callback:
                callback({"success": True, "entry": entry})
                
        except Exception as e:
            logger.error(f"Error creating entry: {e}")
            if callback:
                callback({"success": False, "error": str(e)})
    
    def _save_entry(self, entry, title, entry_type, lineage, incipit, instructions, notes, efficacy_claim, callback=None):
        """Save entry changes."""
        try:
            entry.title = title
            entry.lineage_tradition = lineage
            entry.incipit = incipit
            entry.instructions = instructions
            entry.notes = notes
            entry.updated_at = datetime.now()
            
            if callback:
                callback({"success": True, "entry": entry})
                
        except Exception as e:
            logger.error(f"Error saving entry: {e}")
            if callback:
                callback({"success": False, "error": str(e)})
    
    def _add_ingredient(self, entry, name, description, quantity):
        """Add ingredient to entry."""
        if not name:
            return
        
        ingredient = {
            "name": name,
            "description": description,
            "quantity": quantity,
            "added_at": datetime.now().isoformat()
        }
        
        entry.ingredients.append(ingredient)
        entry.updated_at = datetime.now()
    
    def _remove_ingredient(self, entry, ingredient):
        """Remove ingredient from entry."""
        if ingredient in entry.ingredients:
            entry.ingredients.remove(ingredient)
            entry.updated_at = datetime.now()
    
    def _add_citation(self, entry, chunk_id, context):
        """Add citation to entry."""
        if not chunk_id:
            return
        
        citation = {
            "chunk_id": chunk_id,
            "context": context,
            "added_at": datetime.now().isoformat()
        }
        
        entry.provenance_citations.append(citation)
        entry.updated_at = datetime.now()
    
    def _remove_citation(self, entry, citation):
        """Remove citation from entry."""
        if citation in entry.provenance_citations:
            entry.provenance_citations.remove(citation)
            entry.updated_at = datetime.now()
    
    def _view_entry(self, entry, callback=None):
        """View entry details."""
        # Create view dialog
        content = ScrollView()
        view_layout = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(8))
        view_layout.bind(minimum_height=view_layout.setter('height'))
        
        # Entry details
        view_layout.add_widget(MobileHeader(text=entry.title))
        view_layout.add_widget(MobileLabel(text=f"Type: {entry.entry_type.value.title()}"))
        view_layout.add_widget(MobileLabel(text=f"Lineage: {entry.lineage_tradition}"))
        view_layout.add_widget(MobileLabel(text=f"Efficacy: {entry.efficacy_claim.value.replace('_', ' ').title()}"))
        
        if entry.incipit:
            view_layout.add_widget(MobileLabel(text="Incipit:"))
            view_layout.add_widget(MobileLabel(text=entry.incipit))
        
        if entry.instructions:
            view_layout.add_widget(MobileLabel(text="Instructions:"))
            view_layout.add_widget(MobileLabel(text=entry.instructions))
        
        if entry.notes:
            view_layout.add_widget(MobileLabel(text="Notes:"))
            view_layout.add_widget(MobileLabel(text=entry.notes))
        
        if entry.ingredients:
            view_layout.add_widget(MobileLabel(text="Ingredients:"))
            for ingredient in entry.ingredients:
                view_layout.add_widget(MobileLabel(text=f"• {ingredient.get('name', 'Unknown')} - {ingredient.get('quantity', '')}"))
        
        if entry.provenance_citations:
            view_layout.add_widget(MobileLabel(text="Citations:"))
            for citation in entry.provenance_citations:
                view_layout.add_widget(MobileLabel(text=f"• {citation.get('chunk_id', 'Unknown')}"))
        
        content.add_widget(view_layout)
        
        dialog = MobileDialog(title="Entry Details", content=content)
        dialog.open()
    
    def _edit_entry(self, entry, callback=None):
        """Edit entry."""
        form = self.edit_entry_form(entry, callback)
        dialog = MobileDialog(title="Edit Entry", content=form)
        dialog.open()
    
    def _delete_entry(self, entry, callback=None):
        """Delete entry."""
        if entry.id in self.entries:
            del self.entries[entry.id]
            if callback:
                callback({"success": True, "message": "Entry deleted"})
    
    def get_all_entries(self):
        """Get all entries."""
        return list(self.entries.values())
    
    def get_entry_by_id(self, entry_id):
        """Get entry by ID."""
        return self.entries.get(entry_id)