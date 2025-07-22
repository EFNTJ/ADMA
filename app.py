from flask import Flask, jsonify
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route('/notams', methods=['GET'])
def get_notams():
    url = 'https://sofia-briefing.aviation-civile.gouv.fr/sofia/pages/prepavol.html'

    try:
        response = requests.get(url)
        response.raise_for_status()
    except Exception as e:
        return jsonify({"error": f"Erreur lors de la récupération : {str(e)}"}), 500

    soup = BeautifulSoup(response.text, 'html.parser')

    texte = soup.get_text()
    lignes = texte.splitlines()
    notams = [ligne.strip() for ligne in lignes if "LFRM" in ligne]

    return jsonify(notams)

if __name__ == '__main__':
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
