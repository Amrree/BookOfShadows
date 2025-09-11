"""
Configuration management for Book of Shadows - The Crone
"""

import os
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field

class DatabaseConfig(BaseModel):
    """Database configuration."""
    type: str = "sqlite"
    url: str = "sqlite:///book_of_shadows.db"
    vector_db_type: str = "chromadb"
    vector_db_path: str = "./data/vector_db"

class SafetyConfig(BaseModel):
    """Safety and ethics configuration."""
    enable_harm_detection: bool = True
    enable_cultural_validation: bool = True
    max_excerpt_length: int = 200
    require_user_consent: bool = True
    prohibited_keywords: List[str] = Field(default_factory=lambda: [
        "poison", "explosive", "weapon", "self-harm", "illegal"
    ])

class IngestionConfig(BaseModel):
    """Document ingestion configuration."""
    chunk_size: int = 2000
    chunk_overlap: int = 200
    summary_length: int = 150
    supported_formats: List[str] = Field(default_factory=lambda: [
        "pdf", "epub", "txt", "md", "docx", "html"
    ])
    ocr_confidence_threshold: float = 0.8

class UIConfig(BaseModel):
    """User interface configuration."""
    theme: str = "dark"
    layout: str = "three-pane"
    enable_cursor_suggestions: bool = True
    enable_real_time_citations: bool = True

class PluginConfig(BaseModel):
    """Plugin system configuration."""
    enabled_plugins: List[str] = Field(default_factory=lambda: [
        "pdf_ingestor", "ocr_processor", "vector_db", "citation_manager",
        "ingredients_manager", "ritual_simulator", "ethnography_validator",
        "safety_checker", "ui_bridge", "memory_store", "auth"
    ])
    plugin_directory: str = "./plugins"
    auto_load: bool = True

class Config:
    """Main configuration class."""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize configuration."""
        self.config_path = config_path or "config.yaml"
        self.data_dir = Path("./data")
        self.books_dir = self.data_dir / "books"
        self.entries_dir = self.data_dir / "entries"
        self.memory_dir = self.data_dir / "memory"
        self.plugins_dir = Path("./plugins")
        
        # Default configuration
        self.database = DatabaseConfig()
        self.safety = SafetyConfig()
        self.ingestion = IngestionConfig()
        self.ui = UIConfig()
        self.plugins = PluginConfig()
        
        # Load configuration if file exists
        self.load_config()
        
        # Ensure directories exist
        self._ensure_directories()
    
    def load_config(self):
        """Load configuration from file."""
        if os.path.exists(self.config_path):
            try:
                with open(self.config_path, 'r') as f:
                    config_data = yaml.safe_load(f)
                
                # Update configurations
                if 'database' in config_data:
                    self.database = DatabaseConfig(**config_data['database'])
                if 'safety' in config_data:
                    self.safety = SafetyConfig(**config_data['safety'])
                if 'ingestion' in config_data:
                    self.ingestion = IngestionConfig(**config_data['ingestion'])
                if 'ui' in config_data:
                    self.ui = UIConfig(**config_data['ui'])
                if 'plugins' in config_data:
                    self.plugins = PluginConfig(**config_data['plugins'])
                    
            except Exception as e:
                print(f"Warning: Could not load config file: {e}")
    
    def save_config(self):
        """Save current configuration to file."""
        config_data = {
            'database': self.database.dict(),
            'safety': self.safety.dict(),
            'ingestion': self.ingestion.dict(),
            'ui': self.ui.dict(),
            'plugins': self.plugins.dict()
        }
        
        with open(self.config_path, 'w') as f:
            yaml.dump(config_data, f, default_flow_style=False)
    
    def _ensure_directories(self):
        """Ensure required directories exist."""
        directories = [
            self.data_dir,
            self.books_dir,
            self.entries_dir,
            self.memory_dir,
            self.plugins_dir
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
    
    def get_chunk_id(self, book_id: str, chunk_index: int) -> str:
        """Generate chunk ID in the format @BOOKID::CHUNK0000."""
        return f"@{book_id}::CHUNK{chunk_index:04d}"
    
    def get_book_id(self, title: str, author: str) -> str:
        """Generate short book ID from title and author."""
        # Create a short, unique identifier
        title_short = ''.join(c for c in title if c.isalnum())[:6].upper()
        author_short = ''.join(c for c in author if c.isalnum())[:3].upper()
        return f"{title_short}{author_short}"