import os

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from werkzeug.security import check_password_hash

import config

from database import (
    afficher_utilisateurs,
    ajouter_utilisateur,
    modifier_utilisateur,
    supprimer_utilisateur,
    chercher_utilisateur,
    chercher_admin,
    chercher_carte,
    enregistrer_acces,
    statistiques_dashboard
)

app = Flask(__name__)

app.secret_key = "chu_rfid_2026"

# =====================================================
# LOGIN
# =====================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        admin = chercher_admin(username)

        if admin:

            resultat = check_password_hash(admin["password"], password)

            if resultat:
                session["admin"] = admin["username"]
                return redirect(url_for("index"))

        return render_template(
            "login.html",
            erreur="Nom d'utilisateur ou mot de passe incorrect."
        )

    return render_template("login.html")


# =====================================================
# LOGOUT
# =====================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect(url_for("login"))


# =====================================================
# ACCUEIL
# =====================================================

@app.route("/")
def index():

    if "admin" not in session:
        return redirect(url_for("login"))

    return render_template("index.html")


# =====================================================
# DASHBOARD
# =====================================================

@app.route("/dashboard")
def dashboard():

    if "admin" not in session:
        return redirect(url_for("login"))

    stats = statistiques_dashboard()

    return render_template(
        "dashboard.html",
        stats=stats
    )


# =====================================================
# HISTORIQUE
# =====================================================

@app.route("/historique")
def historique():

    if "admin" not in session:
        return redirect(url_for("login"))

    return render_template("historique.html")


# =====================================================
# EXPORT
# =====================================================

@app.route("/export")
def export():

    if "admin" not in session:
        return redirect(url_for("login"))

    return "<h2>Export Excel (à développer)</h2>"


# =====================================================
# UTILISATEURS
# =====================================================

@app.route("/utilisateurs")
def utilisateurs():

    if "admin" not in session:
        return redirect(url_for("login"))

    liste = afficher_utilisateurs()

    return render_template(
        "utilisateurs.html",
        utilisateurs=liste
    )


# =====================================================
# AJOUTER
# =====================================================

@app.route("/ajouter", methods=["POST"])
def ajouter():

    if "admin" not in session:
        return redirect(url_for("login"))

    uid = request.form["uid"]
    nom = request.form["nom"]
    service = request.form["service"]
    fonction = request.form["fonction"]
    email = request.form["email"]
    telephone = request.form["telephone"]

    actif = 1 if request.form.get("actif") else 0

    ajouter_utilisateur(
        uid,
        nom,
        service,
        fonction,
        email,
        telephone,
        actif
    )

    return redirect(url_for("utilisateurs"))


# =====================================================
# MODIFIER
# =====================================================

@app.route("/modifier/<int:id>", methods=["GET", "POST"])
def modifier(id):

    if "admin" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":

        uid = request.form["uid"]
        nom = request.form["nom"]
        service = request.form["service"]
        fonction = request.form["fonction"]
        email = request.form["email"]
        telephone = request.form["telephone"]

        actif = 1 if request.form.get("actif") else 0

        modifier_utilisateur(
            id,
            uid,
            nom,
            service,
            fonction,
            email,
            telephone,
            actif
        )

        return redirect(url_for("utilisateurs"))

    utilisateur = chercher_utilisateur(id)

    return render_template(
        "modifier_utilisateur.html",
        utilisateur=utilisateur
    )


# =====================================================
# SUPPRIMER
# =====================================================

@app.route("/supprimer/<int:id>")
def supprimer(id):

    if "admin" not in session:
        return redirect(url_for("login"))

    supprimer_utilisateur(id)

    return redirect(url_for("utilisateurs"))


# =====================================================
# API RFID (ESP32)
# =====================================================

@app.route("/api/rfid", methods=["POST"])
def api_rfid():

    donnees = request.get_json()

    if not donnees:

        return jsonify({
            "resultat": "ERREUR",
            "message": "JSON vide"
        }), 400

    uid = donnees.get("uid")

    utilisateur = chercher_carte(uid)

    if utilisateur and utilisateur["actif"]:

        enregistrer_acces(
            uid,
            utilisateur["nom"],
            "AUTORISE"
        )

        return jsonify({
            "resultat": "AUTORISE",
            "nom": utilisateur["nom"]
        })

    enregistrer_acces(
        uid,
        "Inconnu",
        "REFUSE"
    )

    return jsonify({
        "resultat": "REFUSE"
    })


# =====================================================
# HEALTHCHECK
# =====================================================

@app.route("/health")
def health():
    return "OK"


# =====================================================
# LANCEMENT
# =====================================================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )