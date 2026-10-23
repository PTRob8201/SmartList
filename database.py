import sqlite3
from datetime import datetime
import os

DB_NAME = "smartlist.db"

def get_connection():
    """Create a connection to the SQLite database"""
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initialize the database with the items table"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            parent_id INTEGER,
            title TEXT NOT NULL,
            completed BOOLEAN DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (parent_id) REFERENCES items(id) ON DELETE CASCADE
        )
    """)
    
    conn.commit()
    conn.close()

def add_item(title, parent_id=None):
    """Add a new item to the database"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO items (title, parent_id, completed)
        VALUES (?, ?, 0)
    """, (title, parent_id))
    
    conn.commit()
    conn.close()

def get_items():
    """Get all items from the database"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT id, parent_id, title, completed, created_at, updated_at
        FROM items
        ORDER BY created_at ASC
    """)
    
    rows = cursor.fetchall()
    conn.close()
    
    # Convert rows to dictionaries
    items = [dict(row) for row in rows]
    return items

def delete_item(item_id):
    """Delete an item and all its children"""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Delete the item (children will cascade due to ON DELETE CASCADE)
    cursor.execute("DELETE FROM items WHERE id = ?", (item_id,))
    
    conn.commit()
    conn.close()

def toggle_item(item_id, completed):
    """Toggle the completion status of an item"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE items
        SET completed = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (completed, item_id))
    
    conn.commit()
    conn.close()

def update_item(item_id, title):
    """Update an item's title"""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE items
        SET title = ?, updated_at = CURRENT_TIMESTAMP
        WHERE id = ?
    """, (title, item_id))
    
    conn.commit()
    conn.close()
