import mysql.connector
from datetime import datetime
from config import HOST, USER, PASSWORD, DATABASE, DB_PORT


# ==========================================
# Connexion à MySQL
# ==========================================

def connecter():

    try:

        connexion = mysql.connector.connect(
            host=HOST,
            user=USER,
            password=PASSWORD,
            database=DATABASE,
            port=DB_PORT
        )

        print("\n===================================")
        print("✅ CONNEXION MYSQL REUSSIE")
        print("HOST :", HOST)
        print("PORT :", DB_PORT)
        print("DATABASE :", DATABASE)
        print("USER :", USER)
        print("===================================\n")

        return connexion

    except mysql.connector.Error as erreur:

        print("\n===================================")
        print("❌ ERREUR DE CONNEXION MYSQL")
        print(erreur)
        print("===================================\n")

        return None


# ==========================================
# Afficher tous les utilisateurs
# ==========================================

def afficher_utilisateurs():

    connexion = connecter()

    if connexion is None:
        return []

    curseur = connexion.cursor(dictionary=True)

    requete = "SELECT * FROM users ORDER BY nom"

    curseur.execute(requete)

    utilisateurs = curseur.fetchall()

    print("Nombre d'utilisateurs :", len(utilisateurs))

    curseur.close()
    connexion.close()

    return utilisateurs


# ==========================================
# Chercher une carte RFID
# ==========================================

def chercher_carte(uid):

    connexion = connecter()

    if connexion is None:
        return None

    curseur = connexion.cursor(dictionary=True)

    sql = "SELECT * FROM users WHERE uid=%s"

    curseur.execute(sql, (uid,))

    utilisateur = curseur.fetchone()

    curseur.close()
    connexion.close()

    return utilisateur


# ==========================================
# Ajouter un utilisateur
# ==========================================

def ajouter_utilisateur(uid,
                         nom,
                         service,
                         fonction,
                         email,
                         telephone,
                         actif):

    connexion = connecter()

    if connexion is None:
        return

    curseur = connexion.cursor()

    sql = """
    INSERT INTO users
    (uid, nom, service, fonction, email, telephone, actif)
    VALUES (%s,%s,%s,%s,%s,%s,%s)
    """

    valeurs = (
        uid,
        nom,
        service,
        fonction,
        email,
        telephone,
        actif
    )

    curseur.execute(sql, valeurs)

    connexion.commit()

    curseur.close()
    connexion.close()


# ==========================================
# Modifier un utilisateur
# ==========================================

def modifier_utilisateur(id,
                          uid,
                          nom,
                          service,
                          fonction,
                          email,
                          telephone,
                          actif):

    connexion = connecter()

    if connexion is None:
        return

    curseur = connexion.cursor()

    sql = """
    UPDATE users
    SET
        uid=%s,
        nom=%s,
        service=%s,
        fonction=%s,
        email=%s,
        telephone=%s,
        actif=%s
    WHERE id=%s
    """

    valeurs = (
        uid,
        nom,
        service,
        fonction,
        email,
        telephone,
        actif,
        id
    )

    curseur.execute(sql, valeurs)

    connexion.commit()

    curseur.close()
    connexion.close()


# ==========================================
# Supprimer un utilisateur
# ==========================================

def supprimer_utilisateur(id):

    connexion = connecter()

    if connexion is None:
        return

    curseur = connexion.cursor()

    sql = "DELETE FROM users WHERE id=%s"

    curseur.execute(sql, (id,))

    connexion.commit()

    curseur.close()
    connexion.close()


# ==========================================
# Chercher un utilisateur
# ==========================================

def chercher_utilisateur(id):

    connexion = connecter()

    if connexion is None:
        return None

    curseur = connexion.cursor(dictionary=True)

    sql = "SELECT * FROM users WHERE id=%s"

    curseur.execute(sql, (id,))

    utilisateur = curseur.fetchone()

    curseur.close()
    connexion.close()

    return utilisateur


# ==========================================
# Chercher admin
# ==========================================

def chercher_admin(username):

    connexion = connecter()

    if connexion is None:
        return None

    curseur = connexion.cursor(dictionary=True)

    sql = "SELECT * FROM admins WHERE username=%s"

    curseur.execute(sql, (username,))

    admin = curseur.fetchone()

    curseur.close()
    connexion.close()

    return admin


# ==========================================
# Enregistrer accès
# ==========================================

def enregistrer_acces(uid, nom, resultat):

    connexion = connecter()

    if connexion is None:
        return

    curseur = connexion.cursor()

    maintenant = datetime.now()

    sql = """
    INSERT INTO logs(uid, nom, date_acces, heure_acces, resultat)
    VALUES (%s,%s,%s,%s,%s)
    """

    curseur.execute(
        sql,
        (
            uid,
            nom,
            maintenant.date(),
            maintenant.strftime("%H:%M:%S"),
            resultat
        )
    )

    connexion.commit()

    curseur.close()
    connexion.close()

    # ==========================================
# Dashboard
# ==========================================

def statistiques_dashboard():

    connexion = connecter()

    if connexion is None:
        return None

    curseur = connexion.cursor(dictionary=True)

    stats = {}

    # Nombre total d'utilisateurs
    curseur.execute("SELECT COUNT(*) AS total FROM users")
    stats["total_utilisateurs"] = curseur.fetchone()["total"]

    # Nombre d'utilisateurs actifs
    curseur.execute("SELECT COUNT(*) AS total FROM users WHERE actif=1")
    stats["utilisateurs_actifs"] = curseur.fetchone()["total"]

    # Nombre total d'accès
    curseur.execute("SELECT COUNT(*) AS total FROM logs")
    stats["total_acces"] = curseur.fetchone()["total"]

    # Accès autorisés
    curseur.execute("SELECT COUNT(*) AS total FROM logs WHERE resultat='AUTORISE'")
    stats["acces_autorises"] = curseur.fetchone()["total"]

    # Accès refusés
    curseur.execute("SELECT COUNT(*) AS total FROM logs WHERE resultat='REFUSE'")
    stats["acces_refuses"] = curseur.fetchone()["total"]

    # Dernier accès
    curseur.execute("""
        SELECT nom, date_acces, heure_acces, resultat
        FROM logs
        ORDER BY id DESC
        LIMIT 1
    """)

    stats["dernier_acces"] = curseur.fetchone()

    curseur.close()
    connexion.close()

    return stats