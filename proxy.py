from flask import Flask, request, Response, jsonify
from flask_cors import CORS
import requests
from base64 import b64encode

app = Flask(__name__)
CORS(app)

@app.route("/api/fetch", methods=["GET"])
def fetch_data():
    school_code = request.args.get("school_code")
    username = request.args.get("username")
    password = request.args.get("password")
    date = request.args.get("date")

    if not (school_code and username and password and date):
        return jsonify({"error": "Missing parameters"}), 400

    url = f"https://www.stundenplan24.de/{school_code}/mobil/mobdaten/PlanKl{date}.xml"
    credentials = f"{username}:{password}"
    auth_header = f"Basic {b64encode(credentials.encode()).decode()}"

    try:
        r = requests.get(url, headers={"Authorization": auth_header}, timeout=10)
        r.raise_for_status()
        return Response(r.text, mimetype="application/xml")
    except requests.exceptions.HTTPError as he:
        # For 404 or auth problems, give the status code and text
        status = getattr(he.response, "status_code", 500)
        return jsonify({"error": f"HTTP {status}: {str(he)}"}), status
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Failed to fetch: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
