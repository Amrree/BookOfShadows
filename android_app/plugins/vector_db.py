"""
Vector Database Plugin for Book of Shadows - The Crone
"""

import asyncio
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
import chromadb
from sentence_transformers import SentenceTransformer
import numpy as np

from .manager import BasePlugin, PluginManifest

logger = logging.getLogger(__name__)

class VectorDBPlugin(BasePlugin):
    """Plugin for vector database operations."""
    
    def __init__(self, manifest: PluginManifest):
        """Initialize vector DB plugin."""
        super().__init__(manifest)
        self.client = None
        self.collection = None
        self.embedding_model = None
        self.db_path = "./data/vector_db"
    
    async def initialize(self) -> bool:
        """Initialize the plugin."""
        try:
            # Initialize ChromaDB client
            self.client = chromadb.PersistentClient(path=self.db_path)
            
            # Initialize embedding model
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            
            # Create or get collection
            self.collection = self.client.get_or_create_collection(
                name="book_of_shadows",
                metadata={"description": "Book of Shadows vector database"}
            )
            
            self.initialized = True
            logger.info("Vector DB plugin initialized")
            return True
            
        except Exception as e:
            logger.error(f"Failed to initialize Vector DB: {e}")
            return False
    
    async def cleanup(self):
        """Clean up plugin resources."""
        logger.info("Cleaning up Vector DB plugin")
        # ChromaDB client doesn't need explicit cleanup
    
    async def execute(self, capability: str, **kwargs) -> Dict[str, Any]:
        """Execute plugin capability."""
        if capability == "store_chunks":
            return await self.store_chunks(**kwargs)
        elif capability == "search":
            return await self.search(**kwargs)
        elif capability == "get_chunk":
            return await self.get_chunk(**kwargs)
        elif capability == "delete_book":
            return await self.delete_book(**kwargs)
        elif capability == "get_stats":
            return await self.get_stats(**kwargs)
        else:
            return {
                'success': False,
                'error': f"Unknown capability: {capability}"
            }
    
    async def store_chunks(self, chunks: List[Dict[str, Any]], **kwargs) -> Dict[str, Any]:
        """Store text chunks in vector database."""
        try:
            if not chunks:
                return {
                    'success': False,
                    'error': "No chunks provided"
                }
            
            # Prepare data for ChromaDB
            ids = []
            documents = []
            metadatas = []
            embeddings = []
            
            for chunk in chunks:
                chunk_id = chunk['chunk_id']
                content = chunk['content']
                metadata = chunk['metadata']
                
                # Generate embedding
                embedding = self.embedding_model.encode(content).tolist()
                
                ids.append(chunk_id)
                documents.append(content)
                metadatas.append({
                    'book_id': metadata.get('book_id', ''),
                    'title': metadata.get('title', ''),
                    'author': metadata.get('author', ''),
                    'year': metadata.get('year', ''),
                    'chunk_index': chunk.get('chunk_index', 0),
                    'page_start': metadata.get('page_start', 0),
                    'page_end': metadata.get('page_end', 0),
                    'ingested_at': metadata.get('ingested_at', ''),
                    'tag': kwargs.get('tag', '')
                })
                embeddings.append(embedding)
            
            # Store in ChromaDB
            self.collection.add(
                ids=ids,
                documents=documents,
                metadatas=metadatas,
                embeddings=embeddings
            )
            
            logger.info(f"Stored {len(chunks)} chunks in vector database")
            return {
                'success': True,
                'result': {
                    'stored_count': len(chunks),
                    'chunk_ids': ids
                }
            }
            
        except Exception as e:
            logger.error(f"Error storing chunks: {e}")
            return {
                'success': False,
                'error': f"Failed to store chunks: {str(e)}"
            }
    
    async def search(
        self,
        query: str,
        n_results: int = 8,
        filter_metadata: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Search for similar chunks."""
        try:
            # Generate query embedding
            query_embedding = self.embedding_model.encode(query).tolist()
            
            # Search in ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=filter_metadata
            )
            
            # Format results
            formatted_results = []
            if results['ids'] and results['ids'][0]:
                for i, chunk_id in enumerate(results['ids'][0]):
                    formatted_results.append({
                        'chunk_id': chunk_id,
                        'content': results['documents'][0][i],
                        'metadata': results['metadatas'][0][i],
                        'distance': results['distances'][0][i] if 'distances' in results else None
                    })
            
            logger.debug(f"Search returned {len(formatted_results)} results")
            return {
                'success': True,
                'result': {
                    'query': query,
                    'results': formatted_results,
                    'total_results': len(formatted_results)
                }
            }
            
        except Exception as e:
            logger.error(f"Error searching vector database: {e}")
            return {
                'success': False,
                'error': f"Search failed: {str(e)}"
            }
    
    async def get_chunk(self, chunk_id: str, **kwargs) -> Dict[str, Any]:
        """Get a specific chunk by ID."""
        try:
            results = self.collection.get(
                ids=[chunk_id],
                include=['documents', 'metadatas', 'embeddings']
            )
            
            if not results['ids'] or not results['ids'][0]:
                return {
                    'success': False,
                    'error': f"Chunk {chunk_id} not found"
                }
            
            return {
                'success': True,
                'result': {
                    'chunk_id': chunk_id,
                    'content': results['documents'][0][0],
                    'metadata': results['metadatas'][0][0],
                    'embedding': results['embeddings'][0][0] if 'embeddings' in results else None
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting chunk {chunk_id}: {e}")
            return {
                'success': False,
                'error': f"Failed to get chunk: {str(e)}"
            }
    
    async def delete_book(self, book_id: str, **kwargs) -> Dict[str, Any]:
        """Delete all chunks for a specific book."""
        try:
            # Get all chunks for the book
            results = self.collection.get(
                where={"book_id": book_id},
                include=['ids']
            )
            
            if not results['ids']:
                return {
                    'success': True,
                    'result': {
                        'deleted_count': 0,
                        'message': f"No chunks found for book {book_id}"
                    }
                }
            
            # Delete chunks
            self.collection.delete(ids=results['ids'])
            
            logger.info(f"Deleted {len(results['ids'])} chunks for book {book_id}")
            return {
                'success': True,
                'result': {
                    'deleted_count': len(results['ids']),
                    'book_id': book_id
                }
            }
            
        except Exception as e:
            logger.error(f"Error deleting book {book_id}: {e}")
            return {
                'success': False,
                'error': f"Failed to delete book: {str(e)}"
            }
    
    async def get_stats(self, **kwargs) -> Dict[str, Any]:
        """Get database statistics."""
        try:
            count = self.collection.count()
            
            # Get sample of metadata to analyze
            sample_results = self.collection.get(
                limit=100,
                include=['metadatas']
            )
            
            # Analyze book distribution
            books = set()
            if sample_results['metadatas']:
                for metadata in sample_results['metadatas']:
                    if metadata and 'book_id' in metadata:
                        books.add(metadata['book_id'])
            
            return {
                'success': True,
                'result': {
                    'total_chunks': count,
                    'unique_books': len(books),
                    'sample_books': list(books)[:10]  # First 10 books
                }
            }
            
        except Exception as e:
            logger.error(f"Error getting database stats: {e}")
            return {
                'success': False,
                'error': f"Failed to get stats: {str(e)}"
            }