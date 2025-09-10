"""
Plugin manager for Book of Shadows - The Crone
"""

import json
import asyncio
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Type
from abc import ABC, abstractmethod
from dataclasses import dataclass

logger = logging.getLogger(__name__)

@dataclass
class PluginManifest:
    """Plugin manifest structure."""
    id: str
    name: str
    version: str
    capabilities: List[str]
    endpoints: Dict[str, str]
    security: Dict[str, Any]
    dependencies: List[str] = None
    description: str = ""

class BasePlugin(ABC):
    """Base class for all plugins."""
    
    def __init__(self, manifest: PluginManifest):
        """Initialize plugin."""
        self.manifest = manifest
        self.initialized = False
    
    @abstractmethod
    async def initialize(self) -> bool:
        """Initialize the plugin."""
        pass
    
    @abstractmethod
    async def cleanup(self):
        """Clean up plugin resources."""
        pass
    
    @abstractmethod
    async def execute(self, capability: str, **kwargs) -> Dict[str, Any]:
        """Execute a plugin capability."""
        pass

class PluginManager:
    """Manages plugin loading and execution."""
    
    def __init__(self):
        """Initialize plugin manager."""
        self.plugins: Dict[str, BasePlugin] = {}
        self.manifests: Dict[str, PluginManifest] = {}
        self.plugin_directory = Path("./plugins")
        
    async def initialize(self):
        """Initialize plugin manager."""
        logger.info("Initializing plugin manager")
        
        # Ensure plugin directory exists
        self.plugin_directory.mkdir(parents=True, exist_ok=True)
        
        # Load plugin manifests
        await self._load_manifests()
        
        logger.info("Plugin manager initialized")
    
    async def load_plugins(self):
        """Load all available plugins."""
        logger.info("Loading plugins")
        
        for plugin_id, manifest in self.manifests.items():
            try:
                plugin = await self._create_plugin(manifest)
                if plugin:
                    await plugin.initialize()
                    self.plugins[plugin_id] = plugin
                    logger.info(f"Loaded plugin: {plugin_id}")
            except Exception as e:
                logger.error(f"Failed to load plugin {plugin_id}: {e}")
    
    async def get_plugin(self, plugin_id: str) -> Optional[BasePlugin]:
        """Get a plugin by ID."""
        return self.plugins.get(plugin_id)
    
    async def execute_plugin_capability(
        self,
        plugin_id: str,
        capability: str,
        **kwargs
    ) -> Dict[str, Any]:
        """Execute a plugin capability."""
        plugin = self.plugins.get(plugin_id)
        if not plugin:
            return {
                'success': False,
                'error': f"Plugin {plugin_id} not found"
            }
        
        if capability not in plugin.manifest.capabilities:
            return {
                'success': False,
                'error': f"Capability {capability} not available in plugin {plugin_id}"
            }
        
        try:
            result = await plugin.execute(capability, **kwargs)
            return result
        except Exception as e:
            logger.error(f"Error executing {capability} in {plugin_id}: {e}")
            return {
                'success': False,
                'error': f"Plugin execution failed: {str(e)}"
            }
    
    async def _load_manifests(self):
        """Load plugin manifests from directory."""
        manifest_files = self.plugin_directory.glob("*.manifest.json")
        
        for manifest_file in manifest_files:
            try:
                with open(manifest_file, 'r') as f:
                    manifest_data = json.load(f)
                
                manifest = PluginManifest(**manifest_data)
                self.manifests[manifest.id] = manifest
                logger.debug(f"Loaded manifest: {manifest.id}")
                
            except Exception as e:
                logger.error(f"Failed to load manifest {manifest_file}: {e}")
    
    async def _create_plugin(self, manifest: PluginManifest) -> Optional[BasePlugin]:
        """Create a plugin instance from manifest."""
        # This is a simplified version - in a real implementation,
        # you would dynamically import and instantiate plugin classes
        
        if manifest.id == "pdf_ingestor":
            from .pdf_ingestor import PDFIngestorPlugin
            return PDFIngestorPlugin(manifest)
        elif manifest.id == "ocr_processor":
            from .ocr_processor import OCRProcessorPlugin
            return OCRProcessorPlugin(manifest)
        elif manifest.id == "vector_db":
            from .vector_db import VectorDBPlugin
            return VectorDBPlugin(manifest)
        elif manifest.id == "citation_manager":
            from .citation_manager import CitationManagerPlugin
            return CitationManagerPlugin(manifest)
        elif manifest.id == "ingredients_manager":
            from .ingredients_manager import IngredientsManagerPlugin
            return IngredientsManagerPlugin(manifest)
        elif manifest.id == "ritual_simulator":
            from .ritual_simulator import RitualSimulatorPlugin
            return RitualSimulatorPlugin(manifest)
        elif manifest.id == "ethnography_validator":
            from .ethnography_validator import EthnographyValidatorPlugin
            return EthnographyValidatorPlugin(manifest)
        elif manifest.id == "safety_checker":
            from .safety_checker import SafetyCheckerPlugin
            return SafetyCheckerPlugin(manifest)
        elif manifest.id == "ui_bridge":
            from .ui_bridge import UIBridgePlugin
            return UIBridgePlugin(manifest)
        elif manifest.id == "memory_store":
            from .memory_store import MemoryStorePlugin
            return MemoryStorePlugin(manifest)
        elif manifest.id == "auth":
            from .auth import AuthPlugin
            return AuthPlugin(manifest)
        else:
            logger.warning(f"Unknown plugin type: {manifest.id}")
            return None
    
    async def cleanup(self):
        """Clean up all plugins."""
        logger.info("Cleaning up plugins")
        
        for plugin_id, plugin in self.plugins.items():
            try:
                await plugin.cleanup()
                logger.debug(f"Cleaned up plugin: {plugin_id}")
            except Exception as e:
                logger.error(f"Error cleaning up plugin {plugin_id}: {e}")
        
        self.plugins.clear()