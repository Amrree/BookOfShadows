"""
Ingredients Manager Plugin for Book of Shadows - The Crone
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
from pathlib import Path

from .manager import BasePlugin, PluginManifest

logger = logging.getLogger(__name__)

class IngredientsManagerPlugin(BasePlugin):
    """Plugin for managing ritual ingredients and materials."""
    
    def __init__(self, manifest: PluginManifest):
        """Initialize ingredients manager plugin."""
        super().__init__(manifest)
        self.ingredients = {}
        self.substitutions = {}
        self.safety_flags = {}
        self.ingredients_file = Path("./data/ingredients.json")
    
    async def initialize(self) -> bool:
        """Initialize the plugin."""
        try:
            # Load existing ingredients data
            await self._load_ingredients()
            
            # Initialize default ingredients if none exist
            if not self.ingredients:
                await self._initialize_default_ingredients()
            
            self.initialized = True
            logger.info("Ingredients Manager plugin initialized")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize Ingredients Manager: {e}")
            return False
    
    async def cleanup(self):
        """Clean up plugin resources."""
        logger.info("Cleaning up Ingredients Manager plugin")
        await self._save_ingredients()
    
    async def execute(self, capability: str, **kwargs) -> Dict[str, Any]:
        """Execute plugin capability."""
        if capability == "add_ingredient":
            return await self.add_ingredient(**kwargs)
        elif capability == "get_ingredient":
            return await self.get_ingredient(**kwargs)
        elif capability == "search_ingredients":
            return await self.search_ingredients(**kwargs)
        elif capability == "add_substitution":
            return await self.add_substitution(**kwargs)
        elif capability == "check_safety":
            return await self.check_safety(**kwargs)
        elif capability == "export_ingredients":
            return await self.export_ingredients(**kwargs)
        else:
            return {
                'success': False,
                'error': f"Unknown capability: {capability}"
            }
    
    async def add_ingredient(
        self,
        name: str,
        category: str = "general",
        description: str = "",
        safety_level: str = "safe",
        legal_status: str = "legal",
        cultural_notes: str = "",
        **kwargs
    ) -> Dict[str, Any]:
        """Add a new ingredient to the registry."""
        try:
            ingredient_id = self._generate_ingredient_id(name)
            
            ingredient = {
                'id': ingredient_id,
                'name': name,
                'category': category,
                'description': description,
                'safety_level': safety_level,
                'legal_status': legal_status,
                'cultural_notes': cultural_notes,
                'substitutions': [],
                'created_at': datetime.now().isoformat(),
                'updated_at': datetime.now().isoformat()
            }
            
            self.ingredients[ingredient_id] = ingredient
            
            logger.info(f"Added ingredient: {name}")
            return {
                'success': True,
                'result': ingredient
            }
            
        except Exception as e:
            logger.error(f"Error adding ingredient: {e}")
            return {
                'success': False,
                'error': f"Failed to add ingredient: {str(e)}"
            }
    
    async def get_ingredient(self, ingredient_id: str, **kwargs) -> Dict[str, Any]:
        """Get ingredient information by ID."""
        try:
            if ingredient_id not in self.ingredients:
                return {
                    'success': False,
                    'error': f"Ingredient {ingredient_id} not found"
                }
            
            ingredient = self.ingredients[ingredient_id]
            
            return {
                'success': True,
                'result': ingredient
            }
            
        except Exception as e:
            logger.error(f"Error getting ingredient: {e}")
            return {
                'success': False,
                'error': f"Failed to get ingredient: {str(e)}"
            }
    
    async def search_ingredients(
        self,
        query: str,
        category: Optional[str] = None,
        safety_level: Optional[str] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Search for ingredients."""
        try:
            results = []
            query_lower = query.lower()
            
            for ingredient_id, ingredient in self.ingredients.items():
                # Check if ingredient matches search criteria
                if query_lower in ingredient['name'].lower() or query_lower in ingredient['description'].lower():
                    # Apply filters
                    if category and ingredient['category'] != category:
                        continue
                    if safety_level and ingredient['safety_level'] != safety_level:
                        continue
                    
                    results.append(ingredient)
            
            return {
                'success': True,
                'result': {
                    'query': query,
                    'results': results,
                    'total_results': len(results)
                }
            }
            
        except Exception as e:
            logger.error(f"Error searching ingredients: {e}")
            return {
                'success': False,
                'error': f"Failed to search ingredients: {str(e)}"
            }
    
    async def add_substitution(
        self,
        original_id: str,
        substitute_id: str,
        notes: str = "",
        **kwargs
    ) -> Dict[str, Any]:
        """Add a substitution for an ingredient."""
        try:
            if original_id not in self.ingredients:
                return {
                    'success': False,
                    'error': f"Original ingredient {original_id} not found"
                }
            
            if substitute_id not in self.ingredients:
                return {
                    'success': False,
                    'error': f"Substitute ingredient {substitute_id} not found"
                }
            
            substitution = {
                'substitute_id': substitute_id,
                'notes': notes,
                'created_at': datetime.now().isoformat()
            }
            
            self.ingredients[original_id]['substitutions'].append(substitution)
            
            logger.info(f"Added substitution: {original_id} -> {substitute_id}")
            return {
                'success': True,
                'result': substitution
            }
            
        except Exception as e:
            logger.error(f"Error adding substitution: {e}")
            return {
                'success': False,
                'error': f"Failed to add substitution: {str(e)}"
            }
    
    async def check_safety(self, ingredient_id: str, **kwargs) -> Dict[str, Any]:
        """Check safety status of an ingredient."""
        try:
            if ingredient_id not in self.ingredients:
                return {
                    'success': False,
                    'error': f"Ingredient {ingredient_id} not found"
                }
            
            ingredient = self.ingredients[ingredient_id]
            
            safety_info = {
                'ingredient_id': ingredient_id,
                'name': ingredient['name'],
                'safety_level': ingredient['safety_level'],
                'legal_status': ingredient['legal_status'],
                'cultural_notes': ingredient['cultural_notes'],
                'warnings': []
            }
            
            # Add safety warnings based on level
            if ingredient['safety_level'] == 'dangerous':
                safety_info['warnings'].append("This ingredient may be hazardous")
            elif ingredient['safety_level'] == 'restricted':
                safety_info['warnings'].append("This ingredient has legal restrictions")
            
            if ingredient['legal_status'] == 'illegal':
                safety_info['warnings'].append("This ingredient is illegal in many jurisdictions")
            
            return {
                'success': True,
                'result': safety_info
            }
            
        except Exception as e:
            logger.error(f"Error checking safety: {e}")
            return {
                'success': False,
                'error': f"Failed to check safety: {str(e)}"
            }
    
    async def export_ingredients(self, format: str = "json", **kwargs) -> Dict[str, Any]:
        """Export ingredients registry."""
        try:
            if format == "json":
                content = json.dumps(self.ingredients, indent=2)
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
                    'ingredient_count': len(self.ingredients)
                }
            }
            
        except Exception as e:
            logger.error(f"Error exporting ingredients: {e}")
            return {
                'success': False,
                'error': f"Failed to export ingredients: {str(e)}"
            }
    
    def _generate_ingredient_id(self, name: str) -> str:
        """Generate a unique ingredient ID."""
        # Simple ID generation - in production, you'd want more sophisticated logic
        clean_name = ''.join(c for c in name if c.isalnum()).lower()
        return f"ing_{clean_name[:20]}"
    
    async def _load_ingredients(self):
        """Load ingredients from file."""
        try:
            if self.ingredients_file.exists():
                with open(self.ingredients_file, 'r') as f:
                    self.ingredients = json.load(f)
                logger.info(f"Loaded {len(self.ingredients)} ingredients")
        except Exception as e:
            logger.error(f"Failed to load ingredients: {e}")
            self.ingredients = {}
    
    async def _save_ingredients(self):
        """Save ingredients to file."""
        try:
            self.ingredients_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.ingredients_file, 'w') as f:
                json.dump(self.ingredients, f, indent=2)
            logger.debug("Saved ingredients")
        except Exception as e:
            logger.error(f"Failed to save ingredients: {e}")
    
    async def _initialize_default_ingredients(self):
        """Initialize with some common ritual ingredients."""
        default_ingredients = [
            {
                'name': 'Salt',
                'category': 'mineral',
                'description': 'Common purification and protection ingredient',
                'safety_level': 'safe',
                'legal_status': 'legal',
                'cultural_notes': 'Used across many traditions for cleansing'
            },
            {
                'name': 'Candles',
                'category': 'tool',
                'description': 'Light source for rituals and ceremonies',
                'safety_level': 'safe',
                'legal_status': 'legal',
                'cultural_notes': 'Universal symbol of light and energy'
            },
            {
                'name': 'Herbs',
                'category': 'botanical',
                'description': 'Various botanical materials for ritual use',
                'safety_level': 'safe',
                'legal_status': 'legal',
                'cultural_notes': 'Check specific herb properties and cultural significance'
            }
        ]
        
        for ingredient_data in default_ingredients:
            await self.add_ingredient(**ingredient_data)