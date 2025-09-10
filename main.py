#!/usr/bin/env python3
"""
Book of Shadows - The Crone
A research-grade, ritual-aware Grimoire IDE and conversational assistant.

Core model: gtposs 20gig (call-sign: The Crone)
"""

import asyncio
import logging
import sys
from pathlib import Path
from typing import Dict, Any, Optional

from core.app import BookOfShadowsApp
from core.config import Config
from core.safety import SafetyManager
from core.memory import MemoryManager
from plugins.manager import PluginManager

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('book_of_shadows.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class BookOfShadows:
    """Main application class for Book of Shadows IDE."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize the Book of Shadows application."""
        self.config = Config(config_path)
        self.safety_manager = SafetyManager()
        self.memory_manager = MemoryManager()
        self.plugin_manager = PluginManager()
        self.app = None
        
    async def initialize(self):
        """Initialize all components."""
        logger.info("Initializing Book of Shadows - The Crone")
        
        # Initialize core components
        await self.safety_manager.initialize()
        await self.memory_manager.initialize()
        await self.plugin_manager.initialize()
        
        # Create main application
        self.app = BookOfShadowsApp(
            config=self.config,
            safety_manager=self.safety_manager,
            memory_manager=self.memory_manager,
            plugin_manager=self.plugin_manager
        )
        
        await self.app.initialize()
        
        logger.info("Book of Shadows initialized successfully")
        
    async def run(self):
        """Run the main application loop."""
        if not self.app:
            raise RuntimeError("Application not initialized. Call initialize() first.")
            
        logger.info("Starting Book of Shadows - The Crone")
        print("Book of Shadows (gtposs 20gig — The Crone) online.")
        print("Available modules: ingestor, vector_db, ingredients_manager, citation_manager, ritual_simulator, ethnography_validator, safety_checker, ui_bridge.")
        print("Ready to ingest, remember, cite and synthesise grimoire content.")
        print("To ingest, issue: INGEST <file> TAG <tag>. For help, ask: HELP INGEST.")
        
        try:
            await self.app.run()
        except KeyboardInterrupt:
            logger.info("Shutting down Book of Shadows")
        except Exception as e:
            logger.error(f"Fatal error: {e}")
            raise
        finally:
            await self.cleanup()
            
    async def cleanup(self):
        """Clean up resources."""
        if self.app:
            await self.app.cleanup()
        await self.plugin_manager.cleanup()
        await self.memory_manager.cleanup()
        await self.safety_manager.cleanup()

async def main():
    """Main entry point."""
    app = BookOfShadows()
    await app.initialize()
    await app.run()

if __name__ == "__main__":
    asyncio.run(main())