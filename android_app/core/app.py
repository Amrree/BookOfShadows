"""
Main application class for Book of Shadows - The Crone
"""

import asyncio
import logging
from typing import Dict, Any, Optional, List
from pathlib import Path

from .config import Config
from .safety import SafetyManager
from .memory import MemoryManager
from plugins.manager import PluginManager

logger = logging.getLogger(__name__)

class BookOfShadowsApp:
    """Main application class."""
    
    def __init__(
        self,
        config: Config,
        safety_manager: SafetyManager,
        memory_manager: MemoryManager,
        plugin_manager: PluginManager
    ):
        """Initialize the application."""
        self.config = config
        self.safety_manager = safety_manager
        self.memory_manager = memory_manager
        self.plugin_manager = plugin_manager
        
        self.running = False
        self.session_id = None
        
    async def initialize(self):
        """Initialize the application."""
        logger.info("Initializing Book of Shadows application")
        
        # Initialize session
        self.session_id = await self.memory_manager.create_session()
        
        # Load plugins
        await self.plugin_manager.load_plugins()
        
        logger.info("Application initialized successfully")
    
    async def run(self):
        """Run the main application loop."""
        self.running = True
        logger.info("Starting main application loop")
        
        try:
            while self.running:
                # Main application loop
                await asyncio.sleep(0.1)
        except Exception as e:
            logger.error(f"Error in main loop: {e}")
            raise
    
    async def process_command(self, command: str, **kwargs) -> Dict[str, Any]:
        """Process a user command."""
        logger.info(f"Processing command: {command}")
        
        # Safety check first
        safety_result = await self.safety_manager.check_command(command, **kwargs)
        if not safety_result['safe']:
            return {
                'success': False,
                'error': safety_result['reason'],
                'suggestion': safety_result.get('suggestion')
            }
        
        # Route command to appropriate handler
        if command.startswith('INGEST'):
            return await self._handle_ingest(command, **kwargs)
        elif command.startswith('SYNTHESIZE'):
            return await self._handle_synthesize(command, **kwargs)
        elif command.startswith('EXCERPT'):
            return await self._handle_excerpt(command, **kwargs)
        elif command.startswith('CREATE_ENTRY'):
            return await self._handle_create_entry(command, **kwargs)
        elif command.startswith('EXPORT_CITATIONS'):
            return await self._handle_export_citations(command, **kwargs)
        elif command.startswith('HELP'):
            return await self._handle_help(command, **kwargs)
        else:
            return {
                'success': False,
                'error': f"Unknown command: {command}",
                'suggestion': "Type HELP for available commands"
            }
    
    async def _handle_ingest(self, command: str, **kwargs) -> Dict[str, Any]:
        """Handle document ingestion."""
        try:
            # Parse command arguments
            parts = command.split()
            file_path = None
            tag = None
            
            for i, part in enumerate(parts):
                if part == 'file=' and i + 1 < len(parts):
                    file_path = parts[i + 1].strip('"')
                elif part == 'TAG' and i + 1 < len(parts):
                    tag = parts[i + 1]
            
            if not file_path:
                return {
                    'success': False,
                    'error': 'File path required for INGEST command',
                    'suggestion': 'Usage: INGEST file="path/to/file.pdf" TAG tag_name'
                }
            
            # Use ingestor plugin
            ingestor = self.plugin_manager.get_plugin('pdf_ingestor')
            if not ingestor:
                return {
                    'success': False,
                    'error': 'PDF ingestor plugin not available'
                }
            
            result = await ingestor.ingest(file_path, tag=tag)
            return result
            
        except Exception as e:
            logger.error(f"Error in ingest handler: {e}")
            return {
                'success': False,
                'error': f"Ingestion failed: {str(e)}"
            }
    
    async def _handle_synthesize(self, command: str, **kwargs) -> Dict[str, Any]:
        """Handle content synthesis."""
        # TODO: Implement synthesis logic
        return {
            'success': False,
            'error': 'Synthesis not yet implemented',
            'suggestion': 'This feature is under development'
        }
    
    async def _handle_excerpt(self, command: str, **kwargs) -> Dict[str, Any]:
        """Handle excerpt retrieval."""
        # TODO: Implement excerpt logic
        return {
            'success': False,
            'error': 'Excerpt retrieval not yet implemented',
            'suggestion': 'This feature is under development'
        }
    
    async def _handle_create_entry(self, command: str, **kwargs) -> Dict[str, Any]:
        """Handle spell/ritual entry creation."""
        # TODO: Implement entry creation logic
        return {
            'success': False,
            'error': 'Entry creation not yet implemented',
            'suggestion': 'This feature is under development'
        }
    
    async def _handle_export_citations(self, command: str, **kwargs) -> Dict[str, Any]:
        """Handle citation export."""
        # TODO: Implement citation export logic
        return {
            'success': False,
            'error': 'Citation export not yet implemented',
            'suggestion': 'This feature is under development'
        }
    
    async def _handle_help(self, command: str, **kwargs) -> Dict[str, Any]:
        """Handle help requests."""
        help_text = """
Book of Shadows - The Crone - Available Commands:

INGEST file="path/to/file.pdf" TAG tag_name
  - Ingest a document into the grimoire

SYNTHESIZE "query" FROM tag:tag_name FORMAT=format
  - Synthesize content from ingested sources

EXCERPT @BOOKID::CHUNK0000 length=150
  - Retrieve an excerpt from a specific chunk

CREATE_ENTRY title="Title" lineage="tradition" source=@BOOKID
  - Create a new spell/ritual entry

EXPORT_CITATIONS format=bibtex include_chunks=true
  - Export citations in various formats

HELP [command]
  - Show this help or help for specific command
        """
        
        return {
            'success': True,
            'result': help_text.strip()
        }
    
    async def cleanup(self):
        """Clean up application resources."""
        logger.info("Cleaning up application resources")
        self.running = False
        
        if self.session_id:
            await self.memory_manager.close_session(self.session_id)