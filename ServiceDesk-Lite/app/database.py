import sqlite3
from pathlib import Path

DB_PATH = Path("servicedesk.db")


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS clients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            contact_person TEXT,
            phone TEXT NOT NULL,
            email TEXT
        )
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            client_id INTEGER NOT NULL,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Новая',
            priority TEXT NOT NULL DEFAULT 'Средний',
            responsible TEXT DEFAULT 'Иванов И.И.',
            created_at TEXT,
            FOREIGN KEY(client_id) REFERENCES clients(id)
        )
    ''')

    cursor.execute("SELECT COUNT(*) FROM clients")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            "INSERT INTO clients (name, contact_person, phone, email) VALUES (?, ?, ?, ?)",
            [
                ('ООО "Альфа"', "Иванов И.И.", "+7 (900) 111-11-11", "ivanov@alfa.ru"),
                ('ООО "Бета"', "Петров П.П.", "+7 (900) 222-22-22", "petrov@beta.ru"),
                ('ЗАО "Гамма"', "Сидоров С.С.", "+7 (900) 333-33-33", "sidorov@gamma.ru"),
            ],
        )

    cursor.execute("SELECT COUNT(*) FROM tickets")
    if cursor.fetchone()[0] == 0:
        cursor.executemany(
            '''
            INSERT INTO tickets (client_id, title, description, status, priority, responsible, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''',
            [
                (1, "Не работает интернет", "Сотрудники офиса не могут выйти в интернет.", "Новая", "Средний", "Иванов И.И.", "21.05.2024 14:10"),
                (2, "Ошибка при печати", "Принтер не печатает документы.", "В работе", "Высокий", "Петров П.П.", "21.05.2024 13:40"),
                (3, "Замена картриджа", "Необходимо заменить картридж.", "Ожидает ответа", "Низкий", "Сидоров С.С.", "21.05.2024 12:50"),
            ],
        )

    conn.commit()
    conn.close()
