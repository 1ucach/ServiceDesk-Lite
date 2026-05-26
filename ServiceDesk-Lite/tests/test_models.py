import pytest
from app.models import Client, Ticket


def test_client_validation_success():
    client = Client(None, 'ООО "Альфа"', "Иванов И.И.", "+7 900 111-11-11", "test@mail.ru")
    assert client.validate() is True


def test_client_validation_error():
    client = Client(None, "", "", "", "")
    assert client.validate() is False


def test_ticket_validation_success():
    ticket = Ticket(None, 1, "Не работает интернет", "Нет доступа к сети")
    assert ticket.validate() is True


def test_ticket_update_status():
    ticket = Ticket(None, 1, "Ошибка", "Описание")
    ticket.update_status("В работе")
    assert ticket.status == "В работе"


def test_ticket_invalid_status():
    ticket = Ticket(None, 1, "Ошибка", "Описание")
    with pytest.raises(ValueError):
        ticket.update_status("Неверный статус")
