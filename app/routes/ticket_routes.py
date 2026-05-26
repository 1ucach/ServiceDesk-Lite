from flask import Blueprint, render_template, request, redirect, url_for
from app.database import get_connection
from datetime import datetime

ticket_bp = Blueprint("tickets", __name__, url_prefix="/tickets")


@ticket_bp.route("/")
def list_tickets():
    conn = get_connection()
    tickets = conn.execute('''
        SELECT tickets.*, clients.name AS client_name
        FROM tickets
        JOIN clients ON clients.id = tickets.client_id
        ORDER BY tickets.id DESC
    ''').fetchall()
    clients = conn.execute("SELECT * FROM clients ORDER BY name").fetchall()
    conn.close()
    return render_template("tickets.html", tickets=tickets, clients=clients)


@ticket_bp.route("/add", methods=["POST"])
def add_ticket():
    client_id = request.form.get("client_id")
    title = request.form.get("title", "").strip()
    description = request.form.get("description", "").strip()
    priority = request.form.get("priority", "Средний")
    responsible = request.form.get("responsible", "Иванов И.И.")

    if client_id and title and description:
        conn = get_connection()
        conn.execute(
            '''
            INSERT INTO tickets (client_id, title, description, status, priority, responsible, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            ''',
            (client_id, title, description, "Новая", priority, responsible, datetime.now().strftime("%d.%m.%Y %H:%M")),
        )
        conn.commit()
        conn.close()

    return redirect(url_for("tickets.list_tickets"))


@ticket_bp.route("/<int:ticket_id>")
def detail_ticket(ticket_id):
    conn = get_connection()
    ticket = conn.execute('''
        SELECT tickets.*, clients.name AS client_name, clients.contact_person, clients.phone, clients.email
        FROM tickets
        JOIN clients ON clients.id = tickets.client_id
        WHERE tickets.id = ?
    ''', (ticket_id,)).fetchone()
    conn.close()
    return render_template("ticket_detail.html", ticket=ticket)
