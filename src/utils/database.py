# Database persistence module using JSON for data storage

import json
import os
from datetime import datetime
from typing import Dict, List, Any, Optional

class Database:
    """Simple JSON-based database for loan management"""
    
    def __init__(self, db_dir: str = "data"):
        self.db_dir = db_dir
        self._ensure_db_directory()
    
    def _ensure_db_directory(self):
        """Ensure database directory exists"""
        if not os.path.exists(self.db_dir):
            os.makedirs(self.db_dir)
    
    def _get_file_path(self, collection: str) -> str:
        """Get file path for a collection"""
        return os.path.join(self.db_dir, f"{collection}.json")
    
    def _read_collection(self, collection: str) -> Dict[str, Any]:
        """Read a collection from disk"""
        file_path = self._get_file_path(collection)
        if not os.path.exists(file_path):
            return {}
        
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    
    def _write_collection(self, collection: str, data: Dict[str, Any]):
        """Write a collection to disk"""
        file_path = self._get_file_path(collection)
        try:
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2, default=str)
        except IOError as e:
            raise Exception(f"Failed to write to database: {e}")
    
    def insert_one(self, collection: str, document: Dict[str, Any], doc_id: Optional[str] = None) -> str:
        """Insert a document into a collection"""
        data = self._read_collection(collection)
        
        if doc_id is None:
            doc_id = str(len(data) + 1)
        
        document['_id'] = doc_id
        document['_created_at'] = datetime.now().isoformat()
        document['_updated_at'] = datetime.now().isoformat()
        
        data[doc_id] = document
        self._write_collection(collection, data)
        
        return doc_id
    
    def find_one(self, collection: str, doc_id: str) -> Optional[Dict[str, Any]]:
        """Find a single document"""
        data = self._read_collection(collection)
        return data.get(doc_id)
    
    def find_all(self, collection: str) -> List[Dict[str, Any]]:
        """Find all documents in a collection"""
        data = self._read_collection(collection)
        return list(data.values())
    
    def update_one(self, collection: str, doc_id: str, updates: Dict[str, Any]) -> bool:
        """Update a document"""
        data = self._read_collection(collection)
        
        if doc_id not in data:
            return False
        
        data[doc_id].update(updates)
        data[doc_id]['_updated_at'] = datetime.now().isoformat()
        
        self._write_collection(collection, data)
        return True
    
    def delete_one(self, collection: str, doc_id: str) -> bool:
        """Delete a document"""
        data = self._read_collection(collection)
        
        if doc_id not in data:
            return False
        
        del data[doc_id]
        self._write_collection(collection, data)
        return True
    
    def find_by_field(self, collection: str, field: str, value: Any) -> List[Dict[str, Any]]:
        """Find documents by field value"""
        data = self._read_collection(collection)
        return [doc for doc in data.values() if doc.get(field) == value]
    
    def count(self, collection: str) -> int:
        """Count documents in a collection"""
        data = self._read_collection(collection)
        return len(data)
