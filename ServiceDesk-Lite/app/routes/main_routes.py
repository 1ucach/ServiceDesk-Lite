from flask import Blueprint, render_template
from app.database import get_connection

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    conn = get_connection()
    clients_count = conn.execute("SELECT COUNT(*) FROM clients").fetchone()[0]
    tickets_count = conn.execute("SELECT COUNT(*) FROM tickets").fetchone()[0]
    active_count = conn.execute("SELECT COUNT(*) FROM tickets WHERE status='В работе'").fetchone()[0]
    solved_count = conn.execute("SELECT COUNT(*) FROM tickets WHERE status='Решена'").fetchone()[0]
    tickets = conn.execute("SELECT * FROM tickets ORDER BY id DESC LIMIT 5").fetchall()
    conn.close()

    return render_template(
        "index.html",
        clients_count=clients_count,
        tickets_count=tickets_count,
        active_count=active_count,
        solved_count=solved_count,
        tickets=tickets,
    )
