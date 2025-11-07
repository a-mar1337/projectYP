import argparse
from datetime import datetime
from typing import List
from models import Note, Status, Priority
from storage import Storage

class NoteManager:
    def __init__(self):
        self.storage = Storage()
        self.notes = self.storage.load_notes()
    
    def save(self):
        self.storage.save_notes(self.notes)
    
    def add_note(self, title, content, priority=Priority.MEDIUM, tags=None):
        note = Note(title, content, priority=priority, tags=tags)
        note.id = self.storage.get_next_id(self.notes)
        self.notes.append(note)
        self.save()
        print(f"Заметка добавлена с ID: {note.id}")
    
    def list_notes(self, status=None, priority=None, tag=None, show_all=False):
        filtered_notes = self.notes
        
        if not show_all:
            filtered_notes = [note for note in filtered_notes if note.status != Status.ARCHIVED]
        
        if status:
            filtered_notes = [note for note in filtered_notes if note.status == status]
        
        if priority:
            filtered_notes = [note for note in filtered_notes if note.priority == priority]
        
        if tag:
            filtered_notes = [note for note in filtered_notes if tag in note.tags]
        
        if not filtered_notes:
            print("Заметки не найдены")
            return
        
        for note in filtered_notes:
            print(f"ID: {note.id}")
            print(f"Заголовок: {note.title}")
            print(f"Статус: {note.status.value}")
            print(f"Приоритет: {note.priority.value}")
            print(f"Теги: {', '.join(note.tags)}")
            print(f"Создана: {note.created_at.strftime('%Y-%m-%d %H:%M')}")
            print(f"Обновлена: {note.updated_at.strftime('%Y-%m-%d %H:%M')}")
            print("-" * 40)
    
    def search_notes(self, query):
        results = []
        query = query.lower()
        
        for note in self.notes:
            if (query in note.title.lower() or 
                query in note.content.lower() or
                any(query in tag.lower() for tag in note.tags)):
                results.append(note)
        
        if results:
            print(f"Найдено заметок: {len(results)}")
            self.list_notes_from_list(results)
        else:
            print("Заметки не найдены")
    
    def list_notes_from_list(self, notes_list):
        for note in notes_list:
            print(f"ID: {note.id} | {note.title} | {note.status.value} | {note.priority.value}")
            print(f"Теги: {', '.join(note.tags)}")
            print(f"Создана: {note.created_at.strftime('%Y-%m-%d %H:%M')}")
            print("-" * 40)
    
    def delete_note(self, note_id):
        for i, note in enumerate(self.notes):
            if note.id == note_id:
                del self.notes[i]
                self.save()
                print(f"Заметка с ID {note_id} удалена")
                return
        print(f"Заметка с ID {note_id} не найдена")
    
    def update_note_status(self, note_id, status):
        for note in self.notes:
            if note.id == note_id:
                note.status = status
                note.updated_at = datetime.now()
                self.save()
                print(f"Статус заметки {note_id} обновлен на {status.value}")
                return
        print(f"Заметка с ID {note_id} не найдена")

def main():
    manager = NoteManager()
    parser = argparse.ArgumentParser(description="Менеджер заметок")
    
    subparsers = parser.add_subparsers(dest="command", help="Доступные команды")

    add_parser = subparsers.add_parser("add", help="Добавить новую заметку")
    add_parser.add_argument("--title", required=True, help="Заголовок заметки")
    add_parser.add_argument("--content", required=True, help="Содержание заметки")
    add_parser.add_argument("--priority", choices=["low", "medium", "high"], 
                          default="medium", help="Приоритет заметки")
    add_parser.add_argument("--tags", help="Теги через запятую")
    
    # Команда списка
    list_parser = subparsers.add_parser("list", help="Показать список заметок")
    list_parser.add_argument("--status", choices=["active", "completed", "archived"],
                           help="Фильтр по статусу")
    list_parser.add_argument("--priority", choices=["low", "medium", "high"],
                           help="Фильтр по приоритету")
    list_parser.add_argument("--tag", help="Фильтр по тегу")
    list_parser.add_argument("--all", action="store_true", 
                           help="Показать все заметки включая архивные")
    
    # Команда поиска
    search_parser = subparsers.add_parser("search", help="Поиск заметок")
    search_parser.add_argument("query", help="Поисковый запрос")
    
    # Команда удаления
    delete_parser = subparsers.add_parser("delete", help="Удалить заметку")
    delete_parser.add_argument("id", type=int, help="ID заметки для удаления")
    
    # Команда обновления статуса
    status_parser = subparsers.add_parser("status", help="Изменить статус заметки")
    status_parser.add_argument("id", type=int, help="ID заметки")
    status_parser.add_argument("status", choices=["active", "completed", "archived"],
                             help="Новый статус")
    
    args = parser.parse_args()
    
    if args.command == "add":
        tags = [tag.strip() for tag in args.tags.split(",")] if args.tags else []
        priority = Priority(args.priority)
        manager.add_note(args.title, args.content, priority, tags)
    
    elif args.command == "list":
        status = Status(args.status) if args.status else None
        priority = Priority(args.priority) if args.priority else None
        manager.list_notes(status, priority, args.tag, args.all)
    
    elif args.command == "search":
        manager.search_notes(args.query)
    
    elif args.command == "delete":
        manager.delete_note(args.id)
    
    elif args.command == "status":
        manager.update_note_status(args.id, Status(args.status))
    
    else:
        parser.print_help()

if __name__ == "__main__":
    main()