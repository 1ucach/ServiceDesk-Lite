from flask import Blueprint, render_template, request, redirect, url_for
from app.database import get_connection

client_bp = Blueprint("clients", __name__, url_prefix="/clients")


@client_bp.route("/")
def list_clients():
    conn = get_connection()
    clients = conn.execute("SELECT * FROM clients ORDER BY id DESC").fetchall()
    conn.close()
    return render_template("clients.html", clients=clients)


@client_bp.route("/add", methods=["POST"])
def add_client():
    name = request.form.get("name", "").strip()
    contact_person = request.form.get("contact_person", "").strip()
    phone = request.form.get("phone", "").strip()
    email = request.form.get("email", "").strip()

    if name and phone:
        conn = get_connection()
        conn.execute(
            "INSERT INTO clients (name, contact_person, phone, email) VALUES (?, ?, ?, ?)",
            (name, contact_person, phone, email),
        )
        conn.commit()
        conn.close()

    return redirect(url_for("clients.list_clients"))
