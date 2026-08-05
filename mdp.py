from werkzeug.security import generate_password_hash

mot_de_passe = "admin123"

hash_mdp = generate_password_hash(mot_de_passe)

print(hash_mdp)