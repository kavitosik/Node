import sqlite3
from typing import List, Optional


class Note:
    def __init__(self, id: int = None, title: str = "", content: str = ""):
        self.id = id
        self.title = title
        self.content = content


class Database:
    def __init__(self, db_name: str = "notes.db"):
        self.conn = sqlite3.connect(db_name)
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL
        )
        """
        self.conn.execute(query)
        self.conn.commit()

    def add_note(self, note: Note) -> int:
        query = "INSERT INTO notes (title, content) VALUES (?, ?)"
        cursor = self.conn.cursor()
        cursor.execute(query, (note.title, note.content))
        self.conn.commit()
        return cursor.lastrowid

    def get_note(self, note_id: int) -> Optional[Note]:
        query = "SELECT id, title, content FROM notes WHERE id = ?"
        cursor = self.conn.execute(query, (note_id,))
        row = cursor.fetchone()
        if row:
            return Note(id=row[0], title=row[1], content=row[2])
        return None

    def get_all_notes(self) -> List[Note]:
        query = "SELECT id, title, content FROM notes"
        cursor = self.conn.execute(query)
        return [Note(id=row[0],
                     title=row[1],
                     content=row[2]) for row in cursor]

    def update_note(self, note: Note) -> bool:
        query = "UPDATE notes SET title = ?, content = ? WHERE id = ?"
        cursor = self.conn.cursor()
        cursor.execute(query, (note.title, note.content, note.id))
        self.conn.commit()
        return cursor.rowcount > 0

    def delete_note(self, note_id: int) -> bool:
        query = "DELETE FROM notes WHERE id = ?"
        cursor = self.conn.cursor()
        cursor.execute(query, (note_id,))
        self.conn.commit()
        return cursor.rowcount > 0

    def __del__(self):
        self.conn.close()
