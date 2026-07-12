import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Any, Optional
from .config import settings

def get_db_connection():
    conn = sqlite3.connect(settings.SQLITE_DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS frameworks (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        current_version TEXT NOT NULL,
        doc_format TEXT NOT NULL,
        language TEXT NOT NULL
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS docs (
        id TEXT PRIMARY KEY,
        framework_id TEXT NOT NULL,
        file_name TEXT NOT NULL,
        file_path TEXT NOT NULL,
        file_format TEXT NOT NULL,
        uploaded_at TEXT NOT NULL,
        FOREIGN KEY (framework_id) REFERENCES frameworks (id) ON DELETE CASCADE
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS code_examples (
        id TEXT PRIMARY KEY,
        framework TEXT NOT NULL,
        language TEXT NOT NULL,
        task_description TEXT NOT NULL,
        code_block TEXT NOT NULL,
        tags TEXT
    )
    """)
    
    # Insert default frameworks
    cursor.execute("SELECT COUNT(*) FROM frameworks")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO frameworks VALUES ('fastapi', 'FastAPI', '0.111.0', 'HTML', 'Python')")
        cursor.execute("INSERT INTO frameworks VALUES ('django', 'Django', '5.0.6', 'Markdown', 'Python')")
        cursor.execute("INSERT INTO frameworks VALUES ('react', 'React', '18.3.1', 'HTML', 'JavaScript')")
        cursor.execute("INSERT INTO frameworks VALUES ('pytorch', 'PyTorch', '2.3.0', 'PDF', 'Python')")
        
    conn.commit()
    conn.close()

# Framework operations
def list_frameworks() -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    rows = cursor.execute("SELECT * FROM frameworks").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_framework(fw_id: str) -> Optional[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    row = cursor.execute("SELECT * FROM frameworks WHERE id = ?", (fw_id,)).fetchone()
    conn.close()
    return dict(row) if row else None

# Docs operations
def save_doc_file(doc: Dict[str, Any]) -> None:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT OR REPLACE INTO docs (id, framework_id, file_name, file_path, file_format, uploaded_at)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        doc["id"], doc["framework_id"], doc["file_name"], doc["file_path"],
        doc["file_format"], doc.get("uploaded_at", datetime.now().isoformat())
    ))
    conn.commit()
    conn.close()

def list_framework_docs(fw_id: str) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    rows = cursor.execute("SELECT * FROM docs WHERE framework_id = ?", (fw_id,)).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def delete_doc_file(doc_id: str) -> None:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM docs WHERE id = ?", (doc_id,))
    conn.commit()
    conn.close()

# Code example operations
def save_code_example(example: Dict[str, Any]) -> None:
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT OR REPLACE INTO code_examples (id, framework, language, task_description, code_block, tags)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (
        example["id"], example["framework"], example["language"],
        example["task_description"], example["code_block"], json.dumps(example.get("tags", []))
    ))
    conn.commit()
    conn.close()

def list_code_examples(fw_name: str = None) -> List[Dict[str, Any]]:
    conn = get_db_connection()
    cursor = conn.cursor()
    if fw_name:
        rows = cursor.execute("SELECT * FROM code_examples WHERE LOWER(framework) = LOWER(?)", (fw_name,)).fetchall()
    else:
        rows = cursor.execute("SELECT * FROM code_examples").fetchall()
    conn.close()
    
    examples = []
    for r in rows:
        ex = dict(r)
        ex["tags"] = json.loads(ex["tags"]) if ex["tags"] else []
        examples.append(ex)
    return examples
