"""
Citation Manager Plugin for Book of Shadows - The Crone
"""

import asyncio
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime
import json

from .manager import BasePlugin, PluginManifest

logger = logging.getLogger(__name__)

class CitationManagerPlugin(BasePlugin):
    """Plugin for managing citations and references."""
    
    def __init__(self, manifest: PluginManifest):
        """Initialize citation manager plugin."""
        super().__init__(manifest)
        self.citations = {}
        self.reference_style = "chicago"
    
    async def initialize(self) -> bool:
        """Initialize the plugin."""
        try:
            self.initialized = True
            logger.info("Citation Manager plugin initialized")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize Citation Manager: {e}")
            return False
    
    async def cleanup(self):
        """Clean up plugin resources."""
        logger.info("Cleaning up Citation Manager plugin")
    
    async def execute(self, capability: str, **kwargs) -> Dict[str, Any]:
        """Execute plugin capability."""
        if capability == "create_citation":
            return await self.create_citation(**kwargs)
        elif capability == "format_citation":
            return await self.format_citation(**kwargs)
        elif capability == "export_citations":
            return await self.export_citations(**kwargs)
        elif capability == "resolve_citation":
            return await self.resolve_citation(**kwargs)
        else:
            return {
                'success': False,
                'error': f"Unknown capability: {capability}"
            }
    
    async def create_citation(
        self,
        chunk_id: str,
        metadata: Dict[str, Any],
        **kwargs
    ) -> Dict[str, Any]:
        """Create a citation entry."""
        try:
            citation_id = f"cite_{chunk_id}"
            
            citation = {
                'id': citation_id,
                'chunk_id': chunk_id,
                'title': metadata.get('title', 'Unknown Title'),
                'author': metadata.get('author', 'Unknown Author'),
                'year': metadata.get('year', 'Unknown Year'),
                'book_id': metadata.get('book_id', ''),
                'page_start': metadata.get('page_start', 0),
                'page_end': metadata.get('page_end', 0),
                'created_at': datetime.now().isoformat(),
                'style': self.reference_style
            }
            
            self.citations[citation_id] = citation
            
            logger.debug(f"Created citation: {citation_id}")
            return {
                'success': True,
                'result': citation
            }
            
        except Exception as e:
            logger.error(f"Error creating citation: {e}")
            return {
                'success': False,
                'error': f"Failed to create citation: {str(e)}"
            }
    
    async def format_citation(
        self,
        citation_id: str,
        style: str = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Format a citation in the specified style."""
        try:
            if citation_id not in self.citations:
                return {
                    'success': False,
                    'error': f"Citation {citation_id} not found"
                }
            
            citation = self.citations[citation_id]
            style = style or citation.get('style', 'chicago')
            
            if style == 'chicago':
                formatted = self._format_chicago(citation)
            elif style == 'mla':
                formatted = self._format_mla(citation)
            elif style == 'apa':
                formatted = self._format_apa(citation)
            else:
                formatted = self._format_inline(citation)
            
            return {
                'success': True,
                'result': {
                    'citation_id': citation_id,
                    'formatted': formatted,
                    'style': style
                }
            }
            
        except Exception as e:
            logger.error(f"Error formatting citation: {e}")
            return {
                'success': False,
                'error': f"Failed to format citation: {str(e)}"
            }
    
    async def export_citations(
        self,
        format: str = "bibtex",
        include_chunks: bool = False,
        **kwargs
    ) -> Dict[str, Any]:
        """Export citations in various formats."""
        try:
            if format == "bibtex":
                result = self._export_bibtex(include_chunks)
            elif format == "json":
                result = self._export_json(include_chunks)
            elif format == "csv":
                result = self._export_csv(include_chunks)
            else:
                return {
                    'success': False,
                    'error': f"Unsupported export format: {format}"
                }
            
            return {
                'success': True,
                'result': {
                    'format': format,
                    'content': result,
                    'citation_count': len(self.citations)
                }
            }
            
        except Exception as e:
            logger.error(f"Error exporting citations: {e}")
            return {
                'success': False,
                'error': f"Failed to export citations: {str(e)}"
            }
    
    async def resolve_citation(self, chunk_id: str, **kwargs) -> Dict[str, Any]:
        """Resolve a chunk ID to citation information."""
        try:
            citation_id = f"cite_{chunk_id}"
            
            if citation_id not in self.citations:
                return {
                    'success': False,
                    'error': f"Citation for chunk {chunk_id} not found"
                }
            
            citation = self.citations[citation_id]
            
            return {
                'success': True,
                'result': citation
            }
            
        except Exception as e:
            logger.error(f"Error resolving citation: {e}")
            return {
                'success': False,
                'error': f"Failed to resolve citation: {str(e)}"
            }
    
    def _format_chicago(self, citation: Dict[str, Any]) -> str:
        """Format citation in Chicago style."""
        author = citation.get('author', 'Unknown Author')
        title = citation.get('title', 'Unknown Title')
        year = citation.get('year', 'Unknown Year')
        
        return f"{author}. \"{title}.\" {year}."
    
    def _format_mla(self, citation: Dict[str, Any]) -> str:
        """Format citation in MLA style."""
        author = citation.get('author', 'Unknown Author')
        title = citation.get('title', 'Unknown Title')
        year = citation.get('year', 'Unknown Year')
        
        return f"{author}. {title}. {year}."
    
    def _format_apa(self, citation: Dict[str, Any]) -> str:
        """Format citation in APA style."""
        author = citation.get('author', 'Unknown Author')
        title = citation.get('title', 'Unknown Title')
        year = citation.get('year', 'Unknown Year')
        
        return f"{author} ({year}). {title}."
    
    def _format_inline(self, citation: Dict[str, Any]) -> str:
        """Format citation as inline reference."""
        chunk_id = citation.get('chunk_id', '')
        author = citation.get('author', 'Unknown Author')
        year = citation.get('year', 'Unknown Year')
        
        return f"({chunk_id}, {author} {year})"
    
    def _export_bibtex(self, include_chunks: bool) -> str:
        """Export citations in BibTeX format."""
        bibtex_entries = []
        
        for citation_id, citation in self.citations.items():
            entry = f"""@book{{{citation_id},
    title = {{{citation['title']}}},
    author = {{{citation['author']}}},
    year = {{{citation['year']}}},
}}"""
            bibtex_entries.append(entry)
        
        return "\n\n".join(bibtex_entries)
    
    def _export_json(self, include_chunks: bool) -> str:
        """Export citations in JSON format."""
        export_data = {
            'citations': list(self.citations.values()),
            'exported_at': datetime.now().isoformat(),
            'total_count': len(self.citations)
        }
        
        return json.dumps(export_data, indent=2)
    
    def _export_csv(self, include_chunks: bool) -> str:
        """Export citations in CSV format."""
        import csv
        import io
        
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write header
        writer.writerow(['Citation ID', 'Chunk ID', 'Title', 'Author', 'Year', 'Book ID'])
        
        # Write data
        for citation_id, citation in self.citations.items():
            writer.writerow([
                citation_id,
                citation.get('chunk_id', ''),
                citation.get('title', ''),
                citation.get('author', ''),
                citation.get('year', ''),
                citation.get('book_id', '')
            ])
        
        return output.getvalue()