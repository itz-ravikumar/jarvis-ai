"""
Memory System - Long-term context and learning for Jarvis
Uses ChromaDB for efficient vector storage and retrieval
"""

import chromadb
import json
import os
from datetime import datetime
from config import DEBUG_MODE


class JarvisMemory:
    """Long-term memory system with vector embeddings"""
    
    def __init__(self, memory_dir="./jarvis_data/memory"):
        """Initialize memory system"""
        self.memory_dir = memory_dir
        self.client = None
        self.collection = None
        
        # Create memory directory
        os.makedirs(memory_dir, exist_ok=True)
        
        self._initialize()
    
    def _initialize(self):
        """Initialize ChromaDB"""
        try:
            # Initialize ChromaDB (persistent storage)
            self.client = chromadb.PersistentClient(path=self.memory_dir)
            
            # Get or create collection
            self.collection = self.client.get_or_create_collection(
                name="jarvis_memory",
                metadata={"hnsw:space": "cosine"}
            )
            
            if DEBUG_MODE:
                print("✅ Memory system initialized")
        except Exception as e:
            if DEBUG_MODE:
                print(f"❌ Memory initialization error: {e}")
    
    def _simple_embedding(self, text: str):
        """Create simple embedding without ML libraries"""
        # Simple hash-based embedding for text
        # This is a fallback when ML libraries aren't available
        hash_val = hash(text)
        # Create a simple vector from the hash
        return [float((hash_val >> (i*8)) & 0xFF) / 256.0 for i in range(128)]
    
    def save_memory(self, command, response, memory_type="command"):
        """
        Save command/response to memory with embedding
        
        Args:
            command: User command
            response: System response
            memory_type: Type of memory (command, pattern, preference, etc.)
        """
        try:
            # Create simple embedding
            embedding = self._simple_embedding(command)
            
            # Create metadata
            metadata = {
                "type": memory_type,
                "timestamp": datetime.now().isoformat(),
                "command": command[:200],  # Limit size
                "response": response[:200]
            }
            
            # Generate unique ID
            doc_id = f"{memory_type}_{int(datetime.now().timestamp() * 1000)}"
            
            # Store in ChromaDB
            self.collection.add(
                ids=[doc_id],
                embeddings=[embedding],
                documents=[command],
                metadatas=[metadata]
            )
            
            if DEBUG_MODE:
                print(f"💾 Memory saved: {doc_id}")
        
        except Exception as e:
            if DEBUG_MODE:
                print(f"❌ Save memory error: {e}")
    
    def recall_memory(self, query, top_k=3):
        """
        Retrieve relevant memories based on similarity
        
        Args:
            query: Search query
            top_k: Number of results to return
        
        Returns:
            List of relevant memories
        """
        try:
            # Create query embedding
            query_embedding = self._simple_embedding(query)
            
            # Search collection
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=top_k
            )
            
            # Format results
            memories = []
            if results and len(results['metadatas']) > 0:
                for metadata_list, document in zip(results['metadatas'], results['documents']):
                    if metadata_list:
                        for meta in metadata_list:
                            memories.append({
                                'type': meta.get('type'),
                                'command': meta.get('command'),
                                'response': meta.get('response'),
                                'timestamp': meta.get('timestamp')
                            })
            
            if DEBUG_MODE and memories:
                print(f"🧠 Retrieved {len(memories)} memories")
            
            return memories
        
        except Exception as e:
            if DEBUG_MODE:
                print(f"❌ Recall error: {e}")
            return []
    
    def learn_pattern(self, pattern_name, pattern_data):
        """
        Learn and save behavioral patterns
        
        Args:
            pattern_name: Name of pattern
            pattern_data: Pattern details (dict)
        """
        try:
            command = f"pattern: {pattern_name}"
            response = json.dumps(pattern_data, indent=2)
            
            self.save_memory(command, response, memory_type="pattern")
            
            if DEBUG_MODE:
                print(f"📚 Pattern learned: {pattern_name}")
        
        except Exception as e:
            if DEBUG_MODE:
                print(f"❌ Pattern learning error: {e}")
    
    def get_user_preferences(self):
        """Get learned user preferences"""
        try:
            results = self.collection.get()
            preferences = {}
            
            if results and len(results['metadatas']) > 0:
                for metadata in results['metadatas']:
                    if metadata.get('type') == 'preference':
                        pref_name = metadata.get('command', '').replace('preference: ', '')
                        preferences[pref_name] = metadata.get('response')
            
            return preferences
        except Exception as e:
            if DEBUG_MODE:
                print(f"❌ Get preferences error: {e}")
            return {}
    
    def clear_memory(self):
        """Clear all memory (use with caution)"""
        try:
            if self.collection:
                # Delete collection and recreate
                self.client.delete_collection(name="jarvis_memory")
                self.collection = self.client.get_or_create_collection(
                    name="jarvis_memory",
                    metadata={"hnsw:space": "cosine"}
                )
            
            if DEBUG_MODE:
                print("🗑️  Memory cleared")
        except Exception as e:
            if DEBUG_MODE:
                print(f"❌ Clear memory error: {e}")


# Global memory instance
_memory = None

def get_memory():
    """Get global memory instance"""
    global _memory
    if _memory is None:
        _memory = JarvisMemory()
    return _memory


def save_memory(command, response, memory_type="command"):
    """Save to memory"""
    memory = get_memory()
    memory.save_memory(command, response, memory_type)


def recall_memory(query, top_k=3):
    """Recall from memory"""
    memory = get_memory()
    return memory.recall_memory(query, top_k)


def learn_pattern(pattern_name, pattern_data):
    """Learn pattern"""
    memory = get_memory()
    memory.learn_pattern(pattern_name, pattern_data)


def get_user_preferences():
    """Get preferences"""
    memory = get_memory()
    return memory.get_user_preferences()
