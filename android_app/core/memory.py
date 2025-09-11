"""
Memory and persistence management for Book of Shadows - The Crone
"""

import json
import uuid
import asyncio
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional, Union
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)

class MemoryType(Enum):
    """Types of memory storage."""
    SESSION = "session"
    PERSISTENT = "persistent"
    TEMPORARY = "temporary"
    CACHE = "cache"

class MemoryCategory(Enum):
    """Categories of memory content."""
    GRIMOIRE_METADATA = "grimoire_metadata"
    FREQUENT_REFERENCES = "frequent_references"
    PROJECT_CONFIG = "project_config"
    USER_PREFERENCES = "user_preferences"
    SAFETY_RULES = "safety_rules"
    CULTURAL_NOTES = "cultural_notes"

@dataclass
class MemoryEntry:
    """A single memory entry."""
    id: str
    category: MemoryCategory
    content: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    tags: List[str]
    user_approved: bool
    exportable: bool
    revocable: bool

class MemoryManager:
    """Manages memory and persistence."""
    
    def __init__(self):
        """Initialize memory manager."""
        self.memory_dir = Path("./data/memory")
        self.session_memory = {}
        self.persistent_memory = {}
        self.current_session_id = None
        
    async def initialize(self):
        """Initialize memory manager."""
        logger.info("Initializing memory manager")
        
        # Ensure memory directory exists
        self.memory_dir.mkdir(parents=True, exist_ok=True)
        
        # Load persistent memory
        await self._load_persistent_memory()
        
        logger.info("Memory manager initialized")
    
    async def create_session(self) -> str:
        """Create a new session."""
        session_id = str(uuid.uuid4())
        self.current_session_id = session_id
        self.session_memory[session_id] = {
            'created_at': datetime.now(),
            'entries': [],
            'context': {}
        }
        
        logger.info(f"Created session: {session_id}")
        return session_id
    
    async def close_session(self, session_id: str):
        """Close a session and clean up temporary memory."""
        if session_id in self.session_memory:
            # Save any user-approved persistent data
            session_data = self.session_memory[session_id]
            for entry in session_data['entries']:
                if entry.get('user_approved', False):
                    await self._save_persistent_entry(entry)
            
            # Remove session data
            del self.session_memory[session_id]
            logger.info(f"Closed session: {session_id}")
    
    async def store_memory(
        self,
        content: Dict[str, Any],
        category: MemoryCategory,
        memory_type: MemoryType = MemoryType.TEMPORARY,
        tags: List[str] = None,
        user_approved: bool = False
    ) -> str:
        """Store a memory entry."""
        memory_id = str(uuid.uuid4())
        now = datetime.now()
        
        entry = MemoryEntry(
            id=memory_id,
            category=category,
            content=content,
            created_at=now,
            updated_at=now,
            tags=tags or [],
            user_approved=user_approved,
            exportable=True,
            revocable=True
        )
        
        if memory_type == MemoryType.SESSION:
            if self.current_session_id:
                self.session_memory[self.current_session_id]['entries'].append(asdict(entry))
        elif memory_type == MemoryType.PERSISTENT:
            await self._save_persistent_entry(asdict(entry))
        else:
            # Temporary memory (not persisted)
            pass
        
        logger.debug(f"Stored memory: {memory_id} ({category.value})")
        return memory_id
    
    async def retrieve_memory(
        self,
        category: Optional[MemoryCategory] = None,
        tags: Optional[List[str]] = None,
        memory_type: MemoryType = MemoryType.TEMPORARY
    ) -> List[MemoryEntry]:
        """Retrieve memory entries."""
        results = []
        
        if memory_type == MemoryType.SESSION and self.current_session_id:
            session_data = self.session_memory.get(self.current_session_id, {})
            entries = session_data.get('entries', [])
            
            for entry_data in entries:
                entry = MemoryEntry(**entry_data)
                if self._matches_criteria(entry, category, tags):
                    results.append(entry)
        
        elif memory_type == MemoryType.PERSISTENT:
            for entry_data in self.persistent_memory.values():
                entry = MemoryEntry(**entry_data)
                if self._matches_criteria(entry, category, tags):
                    results.append(entry)
        
        return results
    
    async def update_memory(self, memory_id: str, updates: Dict[str, Any]) -> bool:
        """Update a memory entry."""
        # Update in session memory
        if self.current_session_id:
            session_data = self.session_memory.get(self.current_session_id, {})
            entries = session_data.get('entries', [])
            
            for i, entry_data in enumerate(entries):
                if entry_data['id'] == memory_id:
                    entry_data.update(updates)
                    entry_data['updated_at'] = datetime.now().isoformat()
                    return True
        
        # Update in persistent memory
        if memory_id in self.persistent_memory:
            self.persistent_memory[memory_id].update(updates)
            self.persistent_memory[memory_id]['updated_at'] = datetime.now().isoformat()
            await self._save_persistent_memory()
            return True
        
        return False
    
    async def delete_memory(self, memory_id: str) -> bool:
        """Delete a memory entry."""
        # Delete from session memory
        if self.current_session_id:
            session_data = self.session_memory.get(self.current_session_id, {})
            entries = session_data.get('entries', [])
            
            for i, entry_data in enumerate(entries):
                if entry_data['id'] == memory_id:
                    del entries[i]
                    return True
        
        # Delete from persistent memory
        if memory_id in self.persistent_memory:
            del self.persistent_memory[memory_id]
            await self._save_persistent_memory()
            return True
        
        return False
    
    async def export_memory(self, format: str = "json") -> str:
        """Export memory data."""
        exportable_entries = []
        
        # Collect exportable entries from persistent memory
        for entry_data in self.persistent_memory.values():
            entry = MemoryEntry(**entry_data)
            if entry.exportable:
                exportable_entries.append(asdict(entry))
        
        # Collect exportable entries from current session
        if self.current_session_id:
            session_data = self.session_memory.get(self.current_session_id, {})
            entries = session_data.get('entries', [])
            
            for entry_data in entries:
                entry = MemoryEntry(**entry_data)
                if entry.exportable:
                    exportable_entries.append(asdict(entry))
        
        if format == "json":
            return json.dumps(exportable_entries, indent=2, default=str)
        else:
            raise ValueError(f"Unsupported export format: {format}")
    
    def _matches_criteria(
        self,
        entry: MemoryEntry,
        category: Optional[MemoryCategory],
        tags: Optional[List[str]]
    ) -> bool:
        """Check if entry matches retrieval criteria."""
        if category and entry.category != category:
            return False
        
        if tags:
            entry_tags = set(entry.tags)
            search_tags = set(tags)
            if not entry_tags.intersection(search_tags):
                return False
        
        return True
    
    async def _load_persistent_memory(self):
        """Load persistent memory from disk."""
        memory_file = self.memory_dir / "persistent_memory.json"
        
        if memory_file.exists():
            try:
                with open(memory_file, 'r') as f:
                    data = json.load(f)
                    self.persistent_memory = data
                logger.info(f"Loaded {len(self.persistent_memory)} persistent memory entries")
            except Exception as e:
                logger.error(f"Failed to load persistent memory: {e}")
                self.persistent_memory = {}
        else:
            self.persistent_memory = {}
    
    async def _save_persistent_memory(self):
        """Save persistent memory to disk."""
        memory_file = self.memory_dir / "persistent_memory.json"
        
        try:
            with open(memory_file, 'w') as f:
                json.dump(self.persistent_memory, f, indent=2, default=str)
            logger.debug("Saved persistent memory")
        except Exception as e:
            logger.error(f"Failed to save persistent memory: {e}")
    
    async def _save_persistent_entry(self, entry_data: Dict[str, Any]):
        """Save a single entry to persistent memory."""
        memory_id = entry_data['id']
        self.persistent_memory[memory_id] = entry_data
        await self._save_persistent_memory()
    
    async def cleanup(self):
        """Clean up memory manager resources."""
        logger.info("Cleaning up memory manager")
        
        # Save any pending persistent memory
        await self._save_persistent_memory()