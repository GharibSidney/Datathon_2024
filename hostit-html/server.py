from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Active CORS pour toutes les routes

@app.route('/run_script', methods=['POST'])
def run_script():
    result = {"message": "Votre script a été exécuté avec succès"}
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
