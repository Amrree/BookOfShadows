"""
Grimoire Editor UI component for Book of Shadows - The Crone
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
from enum import Enum

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

@dataclass
class SpellEntry:
    """A spell/ritual entry in the grimoire."""
    id: str
    title: str
    entry_type: SpellEntryType
    lineage_tradition: str
    ingredients: List[Dict[str, Any]]
    tools: List[Dict[str, Any]]
    incipit: str
    instructions: str
    notes: str
    efficacy_claim: EfficacyClaim
    provenance_citations: List[str]
    practice_log: List[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime
    tags: List[str]

class GrimoireEditor:
    """Main grimoire editor interface."""
    
    def __init__(self):
        """Initialize the grimoire editor."""
        self.current_entry: Optional[SpellEntry] = None
        self.entries: Dict[str, SpellEntry] = {}
        self.citation_cache: Dict[str, Any] = {}
        
    async def create_entry(
        self,
        title: str,
        entry_type: SpellEntryType,
        lineage_tradition: str = "",
        **kwargs
    ) -> Dict[str, Any]:
        """Create a new spell/ritual entry."""
        try:
            entry_id = f"entry_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
            
            entry = SpellEntry(
                id=entry_id,
                title=title,
                entry_type=entry_type,
                lineage_tradition=lineage_tradition,
                ingredients=[],
                tools=[],
                incipit="",
                instructions="",
                notes="",
                efficacy_claim=EfficacyClaim.UNVERIFIABLE_SUPERNATURAL,
                provenance_citations=[],
                practice_log=[],
                created_at=datetime.now(),
                updated_at=datetime.now(),
                tags=[]
            )
            
            self.entries[entry_id] = entry
            self.current_entry = entry
            
            logger.info(f"Created spell entry: {title}")
            return {
                'success': True,
                'result': {
                    'entry_id': entry_id,
                    'entry': entry
                }
            }
            
        except Exception as e:
            logger.error(f"Error creating spell entry: {e}")
            return {
                'success': False,
                'error': f"Failed to create entry: {str(e)}"
            }
    
    async def update_entry(
        self,
        entry_id: str,
        updates: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Update an existing spell entry."""
        try:
            if entry_id not in self.entries:
                return {
                    'success': False,
                    'error': f"Entry {entry_id} not found"
                }
            
            entry = self.entries[entry_id]
            
            # Update fields
            for field, value in updates.items():
                if hasattr(entry, field):
                    setattr(entry, field, value)
            
            entry.updated_at = datetime.now()
            
            logger.info(f"Updated spell entry: {entry_id}")
            return {
                'success': True,
                'result': {
                    'entry_id': entry_id,
                    'entry': entry
                }
            }
            
        except Exception as e:
            logger.error(f"Error updating spell entry: {e}")
            return {
                'success': False,
                'error': f"Failed to update entry: {str(e)}"
            }
    
    async def add_ingredient(
        self,
        entry_id: str,
        ingredient: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Add an ingredient to a spell entry."""
        try:
            if entry_id not in self.entries:
                return {
                    'success': False,
                    'error': f"Entry {entry_id} not found"
                }
            
            entry = self.entries[entry_id]
            entry.ingredients.append(ingredient)
            entry.updated_at = datetime.now()
            
            logger.info(f"Added ingredient to entry {entry_id}")
            return {
                'success': True,
                'result': {
                    'entry_id': entry_id,
                    'ingredients': entry.ingredients
                }
            }
            
        except Exception as e:
            logger.error(f"Error adding ingredient: {e}")
            return {
                'success': False,
                'error': f"Failed to add ingredient: {str(e)}"
            }
    
    async def add_citation(
        self,
        entry_id: str,
        chunk_id: str,
        context: str = ""
    ) -> Dict[str, Any]:
        """Add a citation to a spell entry."""
        try:
            if entry_id not in self.entries:
                return {
                    'success': False,
                    'error': f"Entry {entry_id} not found"
                }
            
            entry = self.entries[entry_id]
            
            citation = {
                'chunk_id': chunk_id,
                'context': context,
                'added_at': datetime.now().isoformat()
            }
            
            entry.provenance_citations.append(citation)
            entry.updated_at = datetime.now()
            
            logger.info(f"Added citation to entry {entry_id}")
            return {
                'success': True,
                'result': {
                    'entry_id': entry_id,
                    'citations': entry.provenance_citations
                }
            }
            
        except Exception as e:
            logger.error(f"Error adding citation: {e}")
            return {
                'success': False,
                'error': f"Failed to add citation: {str(e)}"
            }
    
    async def get_entry(self, entry_id: str) -> Dict[str, Any]:
        """Get a spell entry by ID."""
        try:
            if entry_id not in self.entries:
                return {
                    'success': False,
                    'error': f"Entry {entry_id} not found"
                }
            
            entry = self.entries[entry_id]
            
            return {
                'success': True,
                'result': entry
            }
            
        except Exception as e:
            logger.error(f"Error getting entry: {e}")
            return {
                'success': False,
                'error': f"Failed to get entry: {str(e)}"
            }
    
    async def list_entries(
        self,
        entry_type: Optional[SpellEntryType] = None,
        tags: Optional[List[str]] = None
    ) -> Dict[str, Any]:
        """List spell entries with optional filtering."""
        try:
            filtered_entries = []
            
            for entry in self.entries.values():
                # Apply filters
                if entry_type and entry.entry_type != entry_type:
                    continue
                
                if tags:
                    entry_tags = set(entry.tags)
                    search_tags = set(tags)
                    if not entry_tags.intersection(search_tags):
                        continue
                
                filtered_entries.append(entry)
            
            return {
                'success': True,
                'result': {
                    'entries': filtered_entries,
                    'total_count': len(filtered_entries)
                }
            }
            
        except Exception as e:
            logger.error(f"Error listing entries: {e}")
            return {
                'success': False,
                'error': f"Failed to list entries: {str(e)}"
            }
    
    async def export_entry(self, entry_id: str, format: str = "markdown") -> Dict[str, Any]:
        """Export a spell entry in various formats."""
        try:
            if entry_id not in self.entries:
                return {
                    'success': False,
                    'error': f"Entry {entry_id} not found"
                }
            
            entry = self.entries[entry_id]
            
            if format == "markdown":
                content = self._export_markdown(entry)
            elif format == "json":
                content = self._export_json(entry)
            else:
                return {
                    'success': False,
                    'error': f"Unsupported export format: {format}"
                }
            
            return {
                'success': True,
                'result': {
                    'format': format,
                    'content': content,
                    'entry_id': entry_id
                }
            }
            
        except Exception as e:
            logger.error(f"Error exporting entry: {e}")
            return {
                'success': False,
                'error': f"Failed to export entry: {str(e)}"
            }
    
    def _export_markdown(self, entry: SpellEntry) -> str:
        """Export entry as markdown."""
        md = f"""# {entry.title}

**Type:** {entry.entry_type.value}  
**Lineage/Tradition:** {entry.lineage_tradition}  
**Efficacy Claim:** {entry.efficacy_claim.value}  
**Created:** {entry.created_at.strftime('%Y-%m-%d %H:%M')}  
**Updated:** {entry.updated_at.strftime('%Y-%m-%d %H:%M')}

## Ingredients
"""
        
        for ingredient in entry.ingredients:
            md += f"- {ingredient.get('name', 'Unknown')}: {ingredient.get('description', '')}\n"
        
        md += "\n## Tools\n"
        for tool in entry.tools:
            md += f"- {tool.get('name', 'Unknown')}: {tool.get('description', '')}\n"
        
        if entry.incipit:
            md += f"\n## Incipit\n{entry.incipit}\n"
        
        if entry.instructions:
            md += f"\n## Instructions\n{entry.instructions}\n"
        
        if entry.notes:
            md += f"\n## Notes\n{entry.notes}\n"
        
        if entry.provenance_citations:
            md += "\n## Citations\n"
            for citation in entry.provenance_citations:
                md += f"- {citation.get('chunk_id', '')}: {citation.get('context', '')}\n"
        
        if entry.tags:
            md += f"\n## Tags\n{', '.join(entry.tags)}\n"
        
        return md
    
    def _export_json(self, entry: SpellEntry) -> str:
        """Export entry as JSON."""
        import json
        return json.dumps(entry.__dict__, indent=2, default=str)