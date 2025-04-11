from model import Database, Note
from view import UserMenu
from loguru import logger


logger.add("file.log",
           format="{time:YYYY-MM-DD at HH-MM-SS} | {level} | {message}",
           rotation="3 days",
           backtrace=True,
           diagnose=True)


class Controller:
    def __init__(self):
        self.db = Database()
        self.menu = UserMenu()

    def run(self):
        while True:
            self.menu.show_menu()
            choice = self.menu.get_user_choice()

            if choice == 1:
                self.show_all_notes()
            elif choice == 2:
                self.add_note()
            elif choice == 3:
                self.edit_note()
            elif choice == 4:
                self.delete_note()
            elif choice == 5:
                print("Goodbye!")
                break
            else:
                self.menu.show_message("Invalid choice. Please try again.")

    def show_all_notes(self):
        notes = self.db.get_all_notes()
        self.menu.show_notes(notes)
        logger.info("Заметки отображены")

    def add_note(self):
        title, content = self.menu.get_note_data()
        note = Note(title=title, content=content)
        note_id = self.db.add_note(note)
        self.menu.show_message(f"Note added successfully with ID: {note_id}")
        logger.info("Добавлена новая заметка")

    def edit_note(self):
        note_id = self.menu.get_note_id()
        if note_id == -1:
            self.menu.show_message("Invalid note ID")
            return

        note = self.db.get_note(note_id)
        if not note:
            self.menu.show_message("Note not found")
            return

        print("\nCurrent note:")
        self.menu.show_notes([note])

        title, content = self.menu.get_note_data()
        updated_note = Note(id=note_id, title=title, content=content)
        if self.db.update_note(updated_note):
            self.menu.show_message("Note updated successfully")
        else:
            self.menu.show_message("Failed to update note")

    def delete_note(self):
        note_id = self.menu.get_note_id()
        if note_id == -1:
            self.menu.show_message("Invalid note ID")
            return

        if self.db.delete_note(note_id):
            self.menu.show_message("Note deleted successfully")
        else:
            self.menu.show_message("Note not found or could not be deleted")
