from loguru import logger


logger.add("file.log",
           format="{time:YYYY-MM-DD at HH-MM-SS} | {level} | {message}",
           rotation="3 days",
           backtrace=True,
           diagnose=True)


class UserMenu:
    @staticmethod
    def show_menu():
        print("\n=== Notes App ===")
        print("1. Show all notes")
        print("2. Add new note")
        print("3. Edit note")
        print("4. Delete note")
        print("5. Exit")
        logger.info("Заметки заработали и отобразили меню")

    @staticmethod
    def get_user_choice() -> int:
        try:
            return int(input("Enter your choice (1-5): "))
        except ValueError:
            logger.info("Получен неправильный ID")
            return -1

    @staticmethod
    def show_notes(notes: list):
        if not notes:
            print("No notes available.")
            return

        print("\n=== Your Notes ===")
        for note in notes:
            print(f"\nID: {note.id}")
            print(f"Title: {note.title}")
            print(f"Content: {note.content}")
            print("-" * 20)

    @staticmethod
    def get_note_data() -> tuple:
        title = input("Enter note title: ")
        content = input("Enter note content: ")
        return title, content

    @staticmethod
    def get_note_id() -> int:
        try:
            return int(input("Enter note ID: "))
        except ValueError:
            return -1

    @staticmethod
    def show_message(message: str):
        print(message)
