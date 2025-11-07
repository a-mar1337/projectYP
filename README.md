*Менеджер заметок*

**Добавление новой заметки:**
```bash
python main.py add --title "Моя заметка" --content "Текст заметки"
# --title и --content обязательны
```
```bash
python main.py add --title "Срочная задача" --content "Выполнить до завтра" --priority high --tags "работа,срочно"
##можно так
```

**Просмотр всех заметок:**
```bash
python main.py list
```

**Фильтрация по заметкам:**
```bash
python main.py list --status active
##Вместо --status можно указывать другой параметр, а вместо active по какому значению фильтруем
```

**Поиск по заголовкам, содержанию или тегам:**
```bash
python main.py search "..."
```

**Удаление заметки по ID:**
```bash
python main.py delete "номер ID"
##ID можно узнать из всего списка
```

**Изменение статуса заметки:** 
```bash
python main.py status "ID" "один из статусов":
##Достпуные статусы: active, completed, archived
##По умолчанию идет active
```


**Дальше в планах:**
- REST API на FastAPI
- Работа с PostgreSQL
