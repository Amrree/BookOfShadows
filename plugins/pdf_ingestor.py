"""
PDF Ingestor Plugin for Book of Shadows - The Crone
"""

import asyncio
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
import PyPDF2
import re
from datetime import datetime

from .manager import BasePlugin, PluginManifest

logger = logging.getLogger(__name__)

class PDFIngestorPlugin(BasePlugin):
    """Plugin for ingesting PDF documents."""
    
    def __init__(self, manifest: PluginManifest):
        """Initialize PDF ingestor plugin."""
        super().__init__(manifest)
        self.chunk_size = 2000
        self.chunk_overlap = 200
    
    async def initialize(self) -> bool:
        """Initialize the plugin."""
        try:
            self.initialized = True
            logger.info("PDF Ingestor plugin initialized")
            return True
        except Exception as e:
            logger.error(f"Failed to initialize PDF Ingestor: {e}")
            return False
    
    async def cleanup(self):
        """Clean up plugin resources."""
        logger.info("Cleaning up PDF Ingestor plugin")
    
    async def execute(self, capability: str, **kwargs) -> Dict[str, Any]:
        """Execute plugin capability."""
        if capability == "ingest":
            return await self.ingest(**kwargs)
        elif capability == "extract_metadata":
            return await self.extract_metadata(**kwargs)
        elif capability == "chunk_text":
            return await self.chunk_text(**kwargs)
        else:
            return {
                'success': False,
                'error': f"Unknown capability: {capability}"
            }
    
    async def ingest(self, file_path: str, tag: str = None, **kwargs) -> Dict[str, Any]:
        """Ingest a PDF file."""
        try:
            file_path = Path(file_path)
            if not file_path.exists():
                return {
                    'success': False,
                    'error': f"File not found: {file_path}"
                }
            
            # Extract metadata
            metadata = await self.extract_metadata(str(file_path))
            if not metadata['success']:
                return metadata
            
            # Extract text
            text = await self._extract_text(str(file_path))
            if not text:
                return {
                    'success': False,
                    'error': "No text extracted from PDF"
                }
            
            # Chunk the text
            chunks = await self.chunk_text(text, metadata['result'])
            
            # Generate book ID
            book_id = self._generate_book_id(
                metadata['result']['title'],
                metadata['result']['author']
            )
            
            # Create chunk IDs
            chunked_data = []
            for i, chunk in enumerate(chunks['result']['chunks']):
                chunk_id = f"@{book_id}::CHUNK{i:04d}"
                chunked_data.append({
                    'chunk_id': chunk_id,
                    'content': chunk,
                    'book_id': book_id,
                    'chunk_index': i,
                    'metadata': metadata['result']
                })
            
            result = {
                'success': True,
                'book_id': book_id,
                'metadata': metadata['result'],
                'chunks': chunked_data,
                'total_chunks': len(chunked_data),
                'tag': tag
            }
            
            logger.info(f"Ingested PDF: {book_id} with {len(chunked_data)} chunks")
            return result
            
        except Exception as e:
            logger.error(f"Error ingesting PDF {file_path}: {e}")
            return {
                'success': False,
                'error': f"Ingestion failed: {str(e)}"
            }
    
    async def extract_metadata(self, file_path: str) -> Dict[str, Any]:
        """Extract metadata from PDF."""
        try:
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                # Extract basic metadata
                metadata = {
                    'title': 'Unknown Title',
                    'author': 'Unknown Author',
                    'year': None,
                    'language': 'en',
                    'pages': len(pdf_reader.pages),
                    'file_path': file_path,
                    'file_size': Path(file_path).stat().st_size,
                    'ingested_at': datetime.now().isoformat()
                }
                
                # Try to get metadata from PDF info
                if pdf_reader.metadata:
                    pdf_metadata = pdf_reader.metadata
                    if pdf_metadata.title:
                        metadata['title'] = pdf_metadata.title
                    if pdf_metadata.author:
                        metadata['author'] = pdf_metadata.author
                    if pdf_metadata.creation_date:
                        metadata['year'] = pdf_metadata.creation_date.year
                
                return {
                    'success': True,
                    'result': metadata
                }
                
        except Exception as e:
            logger.error(f"Error extracting metadata from {file_path}: {e}")
            return {
                'success': False,
                'error': f"Metadata extraction failed: {str(e)}"
            }
    
    async def chunk_text(self, text: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Chunk text into manageable pieces."""
        try:
            # Clean and normalize text
            text = self._clean_text(text)
            
            # Split into sentences
            sentences = re.split(r'[.!?]+', text)
            sentences = [s.strip() for s in sentences if s.strip()]
            
            # Create chunks
            chunks = []
            current_chunk = ""
            current_length = 0
            
            for sentence in sentences:
                sentence_length = len(sentence)
                
                # If adding this sentence would exceed chunk size, save current chunk
                if current_length + sentence_length > self.chunk_size and current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = sentence
                    current_length = sentence_length
                else:
                    current_chunk += " " + sentence if current_chunk else sentence
                    current_length += sentence_length
            
            # Add the last chunk
            if current_chunk:
                chunks.append(current_chunk.strip())
            
            # Create summaries for each chunk
            summaries = []
            for chunk in chunks:
                summary = self._create_summary(chunk)
                summaries.append(summary)
            
            return {
                'success': True,
                'result': {
                    'chunks': chunks,
                    'summaries': summaries,
                    'total_chunks': len(chunks),
                    'chunk_size': self.chunk_size,
                    'chunk_overlap': self.chunk_overlap
                }
            }
            
        except Exception as e:
            logger.error(f"Error chunking text: {e}")
            return {
                'success': False,
                'error': f"Text chunking failed: {str(e)}"
            }
    
    async def _extract_text(self, file_path: str) -> str:
        """Extract text from PDF file."""
        try:
            text = ""
            with open(file_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                
                for page in pdf_reader.pages:
                    page_text = page.extract_text()
                    text += page_text + "\n"
            
            return text.strip()
            
        except Exception as e:
            logger.error(f"Error extracting text from {file_path}: {e}")
            return ""
    
    def _clean_text(self, text: str) -> str:
        """Clean and normalize text."""
        # Remove excessive whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove page numbers and headers/footers
        text = re.sub(r'^\d+\s*$', '', text, flags=re.MULTILINE)
        
        # Remove common PDF artifacts
        text = re.sub(r'[^\w\s.,!?;:()\-"\']', '', text)
        
        return text.strip()
    
    def _create_summary(self, chunk: str) -> str:
        """Create a summary of a text chunk."""
        # Simple summary: first sentence + key words
        sentences = chunk.split('.')
        if sentences:
            first_sentence = sentences[0].strip()
            if len(first_sentence) > 150:
                first_sentence = first_sentence[:147] + "..."
            return first_sentence
        return chunk[:150] + "..." if len(chunk) > 150 else chunk
    
    def _generate_book_id(self, title: str, author: str) -> str:
        """Generate a short book ID."""
        title_short = ''.join(c for c in title if c.isalnum())[:6].upper()
        author_short = ''.join(c for c in author if c.isalnum())[:3].upper()
        return f"{title_short}{author_short}"