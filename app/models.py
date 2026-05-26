from dataclasses import dataclass
from datetime import datetime


@dataclass
class Client:
    id: int | None
    name: str
    contact_person: str
    phone: str
    email: str

    def validate(self) -> bool:
        return bool(self.name and self.phone)


@dataclass
class Ticket:
    id: int | None
    client_id: int
    title: str
    description: str
    status: str = "Новая"
    priority: str = "Средний"
    responsible: str = "Иванов И.И."
    created_at: str = datetime.now().strftime("%d.%m.%Y %H:%M")

    def update_status(self, new_status: str) -> None:
        allowed = ["Новая", "В работе", "Ожидает ответа", "Решена", "Закрыта"]
        if new_status not in allowed:
            raise ValueError("Недопустимый статус заявки")
        self.status = new_status

    def validate(self) -> bool:
        return bool(self.client_id and self.title and self.description)
