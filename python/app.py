from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from analysis import run_fourier_analysis

app = Flask(__name__, static_folder=".", static_url_path="")
CORS(app)


@app.route("/")
def home():
    return send_from_directory(".", "index.html")


@app.route("/api/analyze")
def analyze():
    low_cut = float(request.args.get("low", 25))
    high_cut = float(request.args.get("high", 220))

    result = run_fourier_analysis(
        low_cut=low_cut,
        high_cut=high_cut,
    )

    return jsonify(result)


if __name__ == "__main__":
    app.run(debug=True, port=4092)