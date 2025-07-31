from flask import Flask, request, jsonify
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)

@app.route("/placa", methods=["GET"])
def get_datos_por_placa():
    placa = request.args.get("placa")
    if not placa:
        return jsonify({"error": "Falta el parámetro 'placa'"}), 400

    url = f"https://placas.pe/?placa={placa}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    try:
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, "html.parser")

        # Extraer los datos
        resultado = soup.find("div", class_="resultado")
        if not resultado:
            return jsonify({"error": "No se encontraron datos para esta placa"}), 404

        data = {}
        for p in resultado.find_all("p"):
            if ":" in p.text:
                clave, valor = p.text.split(":", 1)
                data[clave.strip()] = valor.strip()

        return jsonify(data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
