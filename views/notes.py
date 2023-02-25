#!/usr/bin/env python3

from flask import render_template, request, session, redirect, url_for
from views import app_notes
from auth.auth import AUTH


@app_notes.route("/home", methods=["GET", "POST"], strict_slashes=False)
def home() -> str:
    """home page"""
    if request.method == "GET":
        if session.get("email") is None:
            return redirect("/note")
        user = AUTH.get_user_from_email(session["email"])
        return render_template("home.html", user=user, notes=user.notes)
    if request.method == "POST":
        if "email" not in session:
            return redirect("/note")

        user = AUTH.get_user_from_email(session["email"])
        title = request.form.get("title")
        content = request.form.get("content")

        if not session.get("note_id"):
            AUTH.create_and_save_note(user, title, content)
        else:
            AUTH.update_and_save_note(user, session["note_id"], title, content)
            session["note_id"] = None

        return render_template("home.html", user=user, notes=user.notes)


@app_notes.route("/delete/<note_id>", methods=["GET"], strict_slashes=False)
def delete(note_id) -> str:
    """delete note"""
    if "email" not in session:
        return redirect("/note")

    user = AUTH.get_user_from_email(session["email"])

    AUTH.delete_note_by_id(user, note_id)

    return redirect(url_for("app_notes.home"))


@app_notes.route("/update/<note_id>", methods=["GET"], strict_slashes=False)
def update(note_id) -> str:
    """update note"""
    if "email" not in session:
        return redirect("/note")

    user = AUTH.get_user_from_email(session["email"])

    note = AUTH.get_note_by_id(user, note_id)
    session["note_id"] = note_id

    return render_template(
        "home.html",
        user=user,
        notes=user.notes,
        title=note.title,
        content=note.content,
        update=True,
    )
